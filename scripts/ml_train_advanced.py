"""
Advanced ML Training Script - Improved version with better feature engineering
and cross-validation for more robust accuracy metrics
"""
import argparse
import logging
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score
)
from sklearn.preprocessing import StandardScaler
import pickle
import json
from datetime import datetime

# Agregar src/ al path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from trading_phantom.analytics.db import Trade, get_session

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


class AdvancedStrategyModel:
    """
    Advanced ML model with improved feature engineering and cross-validation.
    """
    
    def __init__(self, model_type='random_forest'):
        self.model_type = model_type
        if model_type == 'random_forest':
            self.model = RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
        elif model_type == 'gradient_boosting':
            self.model = GradientBoostingClassifier(
                n_estimators=150,
                learning_rate=0.1,
                max_depth=7,
                random_state=42
            )
        else:
            self.model = RandomForestClassifier(n_estimators=200, random_state=42)
        
        self.is_trained = False
        self.scaler = StandardScaler()
        self.feature_names = []
        self.metrics = {}
    
    def _load_trade_df(self):
        """Load trades from database and create enhanced dataframe."""
        session = get_session()
        rows = session.query(Trade).all()
        session.close()
        
        data = [
            {
                'symbol': r.symbol,
                'side': 1 if (r.side or '').upper() == 'BUY' else -1,
                'price': r.price or 0.0,
                'volume': r.volume or 0.0,
                'pnl': (r.pnl if r.pnl is not None else 0.0),
                'timestamp': r.timestamp or 0,
            }
            for r in rows
        ]
        df = pd.DataFrame(data)
        return df
    
    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create advanced features from trade data."""
        if df.empty:
            return df
        
        # Existing features
        df['abs_pnl'] = df['pnl'].abs()
        df['pnl_lag1'] = df['pnl'].shift(1).fillna(0)
        df['pnl_lag2'] = df['pnl'].shift(2).fillna(0)
        
        # Rolling statistics
        df['pnl_ma_5'] = df['pnl'].rolling(5).mean().fillna(0)
        df['pnl_ma_10'] = df['pnl'].rolling(10).mean().fillna(0)
        df['pnl_std_5'] = df['pnl'].rolling(5).std().fillna(0)
        df['pnl_std_10'] = df['pnl'].rolling(10).std().fillna(0)
        
        # Volatility measures
        df['pnl_volatility'] = df['pnl'].rolling(5).std().fillna(0)
        df['pnl_range'] = df['pnl'].rolling(5).max() - df['pnl'].rolling(5).min()
        df['pnl_range'] = df['pnl_range'].fillna(0)
        
        # Momentum
        df['pnl_momentum'] = df['pnl'] - df['pnl_ma_5']
        df['pnl_momentum'] = df['pnl_momentum'].fillna(0)
        
        # Side features
        df['side_encoded'] = df['side']
        df['is_buy'] = (df['side'] == 1).astype(int)
        df['is_sell'] = (df['side'] == -1).astype(int)
        
        # Volume features
        df['volume_ma_5'] = df['volume'].rolling(5).mean().fillna(0)
        df['volume_std_5'] = df['volume'].rolling(5).std().fillna(0)
        
        # Price features
        df['price_ma_5'] = df['price'].rolling(5).mean().fillna(0)
        df['price_change'] = df['price'].pct_change().fillna(0)
        
        # Win/Loss streak
        df['is_profitable'] = (df['pnl'] > 0).astype(int)
        df['profit_streak'] = (df['is_profitable'] != df['is_profitable'].shift()).cumsum()
        
        # Cumulative metrics
        df['cumulative_pnl'] = df['pnl'].cumsum()
        df['cumulative_wins'] = df['is_profitable'].cumsum()
        df['cumulative_win_rate'] = df['cumulative_wins'] / (np.arange(len(df)) + 1)
        
        return df.fillna(0)
    
    def _select_features(self, df: pd.DataFrame):
        """Select features for model training."""
        cols = [
            'side_encoded', 'price', 'volume',
            'abs_pnl', 'pnl_lag1', 'pnl_lag2',
            'pnl_ma_5', 'pnl_ma_10',
            'pnl_std_5', 'pnl_std_10',
            'pnl_volatility', 'pnl_range', 'pnl_momentum',
            'is_buy', 'is_sell',
            'volume_ma_5', 'volume_std_5',
            'price_ma_5', 'price_change',
            'cumulative_win_rate'
        ]
        existing = [c for c in cols if c in df.columns]
        self.feature_names = existing
        return df[existing]
    
    def train(self, cv_folds=5):
        """Train model with cross-validation."""
        df = self._load_trade_df()
        if df.empty or len(df) < 20:
            return {'status': 'no_data', 'message': 'Not enough trade data'}
        
        logger.info(f"📊 Analyzing {len(df)} trades from database...")
        
        # Engineer features
        df = self._engineer_features(df)
        
        # Create target
        df['target'] = (df['pnl'] > 0).astype(int)
        
        # Get features
        X = self._select_features(df)
        y = df['target']
        
        logger.info(f"🔧 Features engineered: {len(self.feature_names)} features")
        logger.info(f"📈 Class distribution: {y.value_counts().to_dict()}")
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Cross-validation
        logger.info(f"🔄 Running {cv_folds}-fold cross-validation...")
        cv_scores = cross_val_score(self.model, X_train, y_train, cv=cv_folds, scoring='accuracy')
        
        logger.info(f"✅ Cross-validation scores: {cv_scores}")
        logger.info(f"   Mean CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        # Train final model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        
        # Feature importance
        feature_importance = sorted(
            zip(self.feature_names, self.model.feature_importances_),
            key=lambda x: x[1],
            reverse=True
        )
        
        self.is_trained = True
        
        self.metrics = {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1': float(f1),
            'roc_auc': float(roc_auc),
            'cv_mean': float(cv_scores.mean()),
            'cv_std': float(cv_scores.std()),
            'n_samples': int(len(df)),
            'n_features': len(self.feature_names),
            'test_set_size': len(y_test),
            'train_set_size': len(y_train),
            'model_type': self.model_type
        }
        
        return {
            'status': 'trained',
            'metrics': self.metrics,
            'feature_importance': feature_importance[:10],
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
    
    def save_model(self, path='src/data/models/advanced_model.pkl'):
        """Save trained model."""
        if not self.is_trained:
            logger.error("❌ Model not trained yet")
            return False
        
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'metrics': self.metrics,
            'model_type': self.model_type,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(path, 'wb') as f:
            pickle.dump(model_data, f)
        
        logger.info(f"💾 Model saved to {path}")
        return True


def print_results(result):
    """Pretty print training results."""
    if result.get('status') == 'no_data':
        logger.warning("⚠️ No data available for training")
        return
    
    metrics = result.get('metrics', {})
    feature_importance = result.get('feature_importance', [])
    
    print("\n" + "="*70)
    print("🎯 ADVANCED ML TRAINING RESULTS")
    print("="*70)
    
    print("\n📊 ACCURACY METRICS:")
    print(f"   • Accuracy:        {metrics.get('accuracy', 0):.4f} ({metrics.get('accuracy', 0)*100:.2f}%)")
    print(f"   • Precision:       {metrics.get('precision', 0):.4f}")
    print(f"   • Recall:          {metrics.get('recall', 0):.4f}")
    print(f"   • F1-Score:        {metrics.get('f1', 0):.4f}")
    print(f"   • ROC-AUC:         {metrics.get('roc_auc', 0):.4f}")
    
    print("\n🔄 CROSS-VALIDATION:")
    print(f"   • CV Mean:         {metrics.get('cv_mean', 0):.4f}")
    print(f"   • CV Std Dev:      {metrics.get('cv_std', 0):.4f}")
    
    print("\n📈 TRAINING DATA:")
    print(f"   • Total Trades:    {metrics.get('n_samples', 0)}")
    print(f"   • Train Set:       {metrics.get('train_set_size', 0)}")
    print(f"   • Test Set:        {metrics.get('test_set_size', 0)}")
    print(f"   • Features:        {metrics.get('n_features', 0)}")
    print(f"   • Model Type:      {metrics.get('model_type', 'N/A')}")
    
    if feature_importance:
        print("\n🔝 TOP 10 FEATURES:")
        for i, (name, importance) in enumerate(feature_importance, 1):
            bar = '█' * int(importance * 50)
            print(f"   {i:2d}. {name:25s} {bar} {importance:.4f}")
    
    print("\n" + "="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Advanced ML Training with enhanced features")
    parser.add_argument("--model", choices=['random_forest', 'gradient_boosting'], 
                       default='random_forest', help="Model type to train")
    parser.add_argument("--save", action="store_true", help="Save trained model")
    parser.add_argument("--cv", type=int, default=5, help="Number of cross-validation folds")
    args = parser.parse_args()
    
    logger.info("🚀 Starting Advanced ML Training...")
    
    trainer = AdvancedStrategyModel(model_type=args.model)
    result = trainer.train(cv_folds=args.cv)
    
    print_results(result)
    
    if args.save and result.get('status') == 'trained':
        trainer.save_model()
        logger.info("✅ Model saved successfully!")


if __name__ == "__main__":
    main()

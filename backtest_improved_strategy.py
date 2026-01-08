"""
Estrategia de Trading Mejorada con Gestión de Riesgo Avanzada
Usa el modelo ML avanzado pero con stop-loss y take-profit optimizados
"""
import sys
from pathlib import Path
import json
import pickle
import sqlite3
from datetime import datetime
import logging
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


class ImprovedTradingStrategy:
    """
    Estrategia mejorada que usa el modelo ML pero con:
    - Stop-loss dinámico
    - Take-profit a 2x del riesgo (risk-reward ratio 1:2)
    - Filtro de señales débiles
    - Position sizing basado en riesgo
    """
    
    def __init__(self, model_path='src/data/models/advanced_model.pkl'):
        self.model_path = model_path
        self.model_data = None
        self.load_model()
        
        # Parámetros de estrategia
        self.stop_loss_pct = 0.02      # 2% stop loss
        self.take_profit_pct = 0.04    # 4% take profit (1:2 ratio)
        self.min_confidence = 0.55     # Solo operar si confianza > 55%
        self.position_size = 0.95      # Usar 95% del equity en cada trade
        
    def load_model(self):
        """Load trained model from disk"""
        try:
            with open(self.model_path, 'rb') as f:
                self.model_data = pickle.load(f)
            logger.info(f"✅ Advanced model loaded")
            return True
        except FileNotFoundError:
            logger.error(f"❌ Model file not found at {self.model_path}")
            return False
    
    def get_trade_features(self, trade_df: pd.DataFrame):
        """Extract features for model prediction"""
        df = trade_df.copy()
        
        df['abs_pnl'] = df['pnl'].abs()
        df['pnl_lag1'] = df['pnl'].shift(1).fillna(0)
        df['pnl_lag2'] = df['pnl'].shift(2).fillna(0)
        
        df['pnl_ma_5'] = df['pnl'].rolling(5).mean().fillna(0)
        df['pnl_ma_10'] = df['pnl'].rolling(10).mean().fillna(0)
        df['pnl_std_5'] = df['pnl'].rolling(5).std().fillna(0)
        df['pnl_std_10'] = df['pnl'].rolling(10).std().fillna(0)
        
        df['pnl_volatility'] = df['pnl'].rolling(5).std().fillna(0)
        df['pnl_range'] = df['pnl'].rolling(5).max() - df['pnl'].rolling(5).min()
        df['pnl_range'] = df['pnl_range'].fillna(0)
        
        df['pnl_momentum'] = df['pnl'] - df['pnl_ma_5']
        df['pnl_momentum'] = df['pnl_momentum'].fillna(0)
        
        df['side_encoded'] = df['side']
        df['is_buy'] = (df['side'] == 1).astype(int)
        df['is_sell'] = (df['side'] == -1).astype(int)
        
        df['volume_ma_5'] = df['volume'].rolling(5).mean().fillna(0)
        df['volume_std_5'] = df['volume'].rolling(5).std().fillna(0)
        
        df['price_ma_5'] = df['price'].rolling(5).mean().fillna(0)
        df['price_change'] = df['price'].pct_change().fillna(0)
        
        df['is_profitable'] = (df['pnl'] > 0).astype(int)
        df['cumulative_wins'] = df['is_profitable'].cumsum()
        df['cumulative_win_rate'] = df['cumulative_wins'] / (np.arange(len(df)) + 1)
        
        return df.fillna(0)
    
    def simulate_trade_with_risk_management(self, trade, equity):
        """
        Simula un trade con risk management
        Retorna: (new_equity, trade_result, reason)
        """
        # Calcular posición basada en riesgo
        risk_amount = equity * 0.02  # Arriesgar 2% máximo por trade
        position_value = equity * self.position_size
        
        # Entrada
        entry_price = trade['price']
        actual_pnl = trade['pnl']
        
        # Stop loss y take profit
        stop_loss_value = -risk_amount
        take_profit_value = risk_amount * 2  # Risk:Reward 1:2
        
        # Determinar resultado basado en P&L actual
        if actual_pnl <= stop_loss_value:
            # Ejecutó stop loss
            return equity + stop_loss_value, stop_loss_value, "SL"
        elif actual_pnl >= take_profit_value:
            # Ejecutó take profit
            return equity + take_profit_value, take_profit_value, "TP"
        else:
            # Trade a mitad de camino (usa P&L actual pero limitado)
            result = max(min(actual_pnl, take_profit_value), stop_loss_value)
            return equity + result, result, "MID"
    
    def run_backtest(self):
        """Run backtesting with improved strategy"""
        # Load trades from database
        conn = sqlite3.connect('src/data/trading_phantom.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT symbol, side, price, volume, pnl, timestamp FROM trades ORDER BY timestamp')
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            logger.warning("⚠️ No trades found in database")
            return None
        
        # Build dataframe
        data = [
            {
                'symbol': row['symbol'],
                'side': 1 if (row['side'] or '').upper() == 'BUY' else -1,
                'price': row['price'] or 0.0,
                'volume': row['volume'] or 0.0,
                'pnl': row['pnl'] if row['pnl'] is not None else 0.0,
                'timestamp': row['timestamp'] or 0,
            }
            for row in rows
        ]
        df = pd.DataFrame(data)
        
        # Engineer features
        df = self.get_trade_features(df)
        
        # Select features
        feature_cols = [
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
        
        X = df[feature_cols].values
        
        # Make predictions
        model = self.model_data['model']
        scaler = self.model_data['scaler']
        
        X_scaled = scaler.transform(X)
        predictions = model.predict(X_scaled)
        probabilities = model.predict_proba(X_scaled)[:, 1]
        
        # Simulate trading with risk management
        initial_equity = 10000.0
        equity = initial_equity
        
        trades_list = []
        winners = 0
        losers = 0
        signals_taken = 0
        signals_rejected = 0
        
        for i, row in df.iterrows():
            pred = predictions[i]
            prob = probabilities[i]
            
            # Signal filtering: solo operar si confianza > threshold
            if prob < self.min_confidence and pred == 1:
                # Señal débil - rechazar
                signals_rejected += 1
                trade_info = {
                    'index': i,
                    'timestamp': row['timestamp'],
                    'symbol': row['symbol'],
                    'side': 'BUY' if row['side'] == 1 else 'SELL',
                    'price': row['price'],
                    'signal_strength': float(prob),
                    'actual_pnl': row['pnl'],
                    'status': 'SIGNAL_REJECTED',
                    'equity': equity,
                }
                trades_list.append(trade_info)
                continue
            
            if pred == 1:  # Señal de rentabilidad
                signals_taken += 1
                new_equity, pnl, exit_reason = self.simulate_trade_with_risk_management(row, equity)
                
                trade_info = {
                    'index': i,
                    'timestamp': row['timestamp'],
                    'symbol': row['symbol'],
                    'side': 'BUY' if row['side'] == 1 else 'SELL',
                    'price': row['price'],
                    'signal_strength': float(prob),
                    'pnl': float(pnl),
                    'exit_reason': exit_reason,
                    'equity': float(new_equity),
                    'status': 'TRADE_TAKEN',
                }
                
                equity = new_equity
                if pnl > 0:
                    winners += 1
                else:
                    losers += 1
            else:
                # No hay señal - descartar
                trade_info = {
                    'index': i,
                    'timestamp': row['timestamp'],
                    'symbol': row['symbol'],
                    'side': 'BUY' if row['side'] == 1 else 'SELL',
                    'price': row['price'],
                    'signal_strength': float(prob),
                    'actual_pnl': row['pnl'],
                    'status': 'NO_SIGNAL',
                    'equity': equity,
                }
            
            trades_list.append(trade_info)
        
        # Calculate metrics
        taken_trades = [t for t in trades_list if t['status'] == 'TRADE_TAKEN']
        total_taken = len(taken_trades)
        total_pnl = sum(t['pnl'] for t in taken_trades) if taken_trades else 0
        win_rate = winners / total_taken if total_taken > 0 else 0
        
        # Equity metrics
        equity_curve = [t['equity'] for t in trades_list]
        max_equity = max(equity_curve) if equity_curve else initial_equity
        min_equity = min(equity_curve) if equity_curve else initial_equity
        
        return {
            'summary': {
                'total_signals': len(df),
                'signals_taken': signals_taken,
                'signals_rejected': signals_rejected,
                'trades_executed': total_taken,
                'winning_trades': winners,
                'losing_trades': losers,
                'win_rate': float(win_rate),
                'total_pnl': float(total_pnl),
                'roi': float((equity - initial_equity) / initial_equity),
                'initial_equity': float(initial_equity),
                'final_equity': float(equity),
            },
            'equity_metrics': {
                'max_equity': float(max_equity),
                'min_equity': float(min_equity),
                'max_drawdown': float((min_equity - initial_equity) / initial_equity),
            },
            'risk_params': {
                'stop_loss_pct': self.stop_loss_pct,
                'take_profit_pct': self.take_profit_pct,
                'min_confidence': self.min_confidence,
                'position_size': self.position_size,
            },
            'trades': taken_trades[:10],
            'full_equity_curve': equity_curve,
            'timestamp': datetime.now().isoformat()
        }


def print_results(results):
    """Pretty print backtesting results"""
    if not results:
        print("❌ No results to display")
        return
    
    summary = results['summary']
    equity = results['equity_metrics']
    risk = results['risk_params']
    
    print("\n" + "="*70)
    print("🎯 IMPROVED TRADING STRATEGY - BACKTESTING RESULTS")
    print("="*70)
    
    print("\n📊 SIGNAL FILTERING:")
    print(f"   • Total Signals:       {summary['total_signals']}")
    print(f"   • Signals Taken:       {summary['signals_taken']}")
    print(f"   • Signals Rejected:    {summary['signals_rejected']}")
    print(f"   • Rejection Rate:      {(summary['signals_rejected']/summary['total_signals']*100):.1f}%")
    
    print("\n💰 TRADE RESULTS:")
    print(f"   • Trades Executed:     {summary['trades_executed']}")
    print(f"   • Winning Trades:      {summary['winning_trades']}")
    print(f"   • Losing Trades:       {summary['losing_trades']}")
    print(f"   • Win Rate:            {summary['win_rate']*100:.2f}%")
    print(f"   • Total P&L:           ${summary['total_pnl']:.2f}")
    
    print("\n💵 FINANCIAL RESULTS:")
    print(f"   • Initial Equity:      ${summary['initial_equity']:.2f}")
    print(f"   • Final Equity:        ${summary['final_equity']:.2f}")
    print(f"   • ROI:                 {summary['roi']*100:.2f}%")
    
    print("\n📈 EQUITY METRICS:")
    print(f"   • Max Equity:          ${equity['max_equity']:.2f}")
    print(f"   • Min Equity:          ${equity['min_equity']:.2f}")
    print(f"   • Max Drawdown:        {equity['max_drawdown']*100:.2f}%")
    
    print("\n⚙️  RISK PARAMETERS:")
    print(f"   • Stop Loss:           {risk['stop_loss_pct']*100:.1f}%")
    print(f"   • Take Profit:         {risk['take_profit_pct']*100:.1f}%")
    print(f"   • Min Confidence:      {risk['min_confidence']*100:.0f}%")
    print(f"   • Position Size:       {risk['position_size']*100:.0f}%")
    
    print("\n" + "="*70 + "\n")


def main():
    logger.info("🚀 Starting Improved Trading Strategy Backtest...")
    
    strategy = ImprovedTradingStrategy()
    results = strategy.run_backtest()
    
    print_results(results)
    
    if results:
        # Save results
        output_file = 'backtest_results_improved_strategy.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"✅ Results saved to {output_file}")


if __name__ == "__main__":
    main()

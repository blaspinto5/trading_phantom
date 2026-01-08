# src/trading_phantom/api/knowledge.py

"""
API Endpoints para acceso a Knowledge Base.

Futuras IAs pueden consultar el conocimiento via HTTP:
  GET /api/knowledge/feature-importance
  GET /api/knowledge/performance
  GET /api/knowledge/embeddings
  etc
"""

from flask import Blueprint, jsonify
import logging

bp = Blueprint('knowledge', __name__)
logger = logging.getLogger(__name__)


@bp.route('/knowledge/summary', methods=['GET'])
def get_knowledge_summary():
    """
    Retorna resumen del Knowledge Base disponible.
    
    Response: {
        'metadata': {...},
        'feature_importance': {...},
        'performance_metrics': {...},
        ...
    }
    """
    try:
        from trading_phantom.analytics.knowledge_base import KnowledgeBase
        kb = KnowledgeBase()
        summary = kb.get_summary()
        return jsonify({'status': 'ok', 'knowledge': summary}), 200
    except Exception as e:
        logger.exception('Error fetching knowledge summary')
        return jsonify({'status': 'error', 'message': str(e)}), 500


@bp.route('/knowledge/feature-importance', methods=['GET'])
def get_feature_importance():
    """Retorna ranking de features importantes"""
    try:
        from trading_phantom.analytics.knowledge_base import KnowledgeBase
        kb = KnowledgeBase()
        importance = kb.get_feature_importance()
        if importance:
            return jsonify({'status': 'ok', 'data': importance}), 200
        return jsonify({'status': 'not_found'}), 404
    except Exception as e:
        logger.exception('Error fetching feature importance')
        return jsonify({'status': 'error', 'message': str(e)}), 500


@bp.route('/knowledge/performance', methods=['GET'])
def get_performance():
    """Retorna métricas de performance del modelo actual"""
    try:
        from trading_phantom.analytics.knowledge_base import KnowledgeBase
        kb = KnowledgeBase()
        metrics = kb.get_performance_metrics()
        if metrics:
            return jsonify({'status': 'ok', 'data': metrics}), 200
        return jsonify({'status': 'not_found'}), 404
    except Exception as e:
        logger.exception('Error fetching performance metrics')
        return jsonify({'status': 'error', 'message': str(e)}), 500


@bp.route('/knowledge/embeddings', methods=['GET'])
def get_embeddings():
    """Retorna feature embeddings (para inicializar NNs)"""
    try:
        from trading_phantom.analytics.knowledge_base import KnowledgeBase
        kb = KnowledgeBase()
        embeddings = kb.get_feature_embeddings()
        if embeddings:
            return jsonify({'status': 'ok', 'data': embeddings}), 200
        return jsonify({'status': 'not_found'}), 404
    except Exception as e:
        logger.exception('Error fetching embeddings')
        return jsonify({'status': 'error', 'message': str(e)}), 500


@bp.route('/knowledge/correlation', methods=['GET'])
def get_correlation():
    """Retorna matriz de correlación de features"""
    try:
        from trading_phantom.analytics.knowledge_base import KnowledgeBase
        kb = KnowledgeBase()
        corr = kb.get_correlation_matrix()
        if corr:
            return jsonify({'status': 'ok', 'data': corr}), 200
        return jsonify({'status': 'not_found'}), 404
    except Exception as e:
        logger.exception('Error fetching correlation matrix')
        return jsonify({'status': 'error', 'message': str(e)}), 500


@bp.route('/knowledge/patterns', methods=['GET'])
def get_patterns():
    """Retorna patrones de decisión extraídos del RF"""
    try:
        from trading_phantom.analytics.knowledge_base import KnowledgeBase
        kb = KnowledgeBase()
        patterns = kb.get_decision_patterns()
        if patterns:
            return jsonify({'status': 'ok', 'data': patterns}), 200
        return jsonify({'status': 'not_found'}), 404
    except Exception as e:
        logger.exception('Error fetching patterns')
        return jsonify({'status': 'error', 'message': str(e)}), 500


@bp.route('/knowledge/status', methods=['GET'])
def get_knowledge_status():
    """
    Status del Knowledge Base para diagnosticar.
    
    Útil para futuras IAs para validar que el KB está disponible.
    """
    try:
        from trading_phantom.analytics.knowledge_base import KnowledgeBase
        from pathlib import Path
        
        kb = KnowledgeBase()
        
        # Verificar qué archivos existen
        files = {
            'feature_importance': (kb.kb_dir / 'feature_importance.json').exists(),
            'embeddings': (kb.kb_dir / 'feature_embeddings.json').exists(),
            'correlation': (kb.kb_dir / 'correlation_matrix.json').exists(),
            'patterns': (kb.kb_dir / 'decision_patterns.json').exists(),
            'performance': (kb.kb_dir / 'performance_metrics.json').exists(),
            'model': (kb.kb_dir / 'models' / 'random_forest.pkl').exists(),
            'scaler': (kb.kb_dir / 'models' / 'feature_scaler.pkl').exists(),
        }
        
        all_available = all(files.values())
        
        return jsonify({
            'status': 'ok',
            'knowledge_available': all_available,
            'files': files,
            'kb_directory': str(kb.kb_dir)
        }), 200
    except Exception as e:
        logger.exception('Error checking knowledge status')
        return jsonify({'status': 'error', 'message': str(e)}), 500


@bp.route('/knowledge/guide', methods=['GET'])
def get_transfer_guide():
    """Retorna guía de transferencia para futuras IAs"""
    try:
        from trading_phantom.analytics.transfer_learning import TransferLearningPipeline
        
        pipeline = TransferLearningPipeline()
        guide = pipeline.create_knowledge_transfer_guide()
        
        return jsonify({
            'status': 'ok',
            'guide': guide,
            'location': 'data/knowledge_base/KNOWLEDGE_TRANSFER_GUIDE.md'
        }), 200
    except Exception as e:
        logger.exception('Error generating transfer guide')
        return jsonify({'status': 'error', 'message': str(e)}), 500

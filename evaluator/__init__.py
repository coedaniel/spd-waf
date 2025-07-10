"""
🛡️ AWS WAF Service Delivery Program Evaluator v2.0
Evaluador completo basado en requisitos oficiales de Febrero 2025
"""

from .waf_spd_evaluator_v2 import WAFSPDEvaluator, ComplianceLevel, EvaluationResult
from .waf_spd_evaluator_methods import WAFSPDEvaluatorMethods  
from .waf_spd_calculator import WAFSPDCalculator

class CompleteWAFSPDEvaluator(WAFSPDEvaluator, WAFSPDEvaluatorMethods, WAFSPDCalculator):
    """
    Evaluador completo que combina todas las funcionalidades
    """
    pass

__all__ = [
    'CompleteWAFSPDEvaluator',
    'WAFSPDEvaluator', 
    'ComplianceLevel',
    'EvaluationResult'
]

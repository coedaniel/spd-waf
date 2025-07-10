"""
🛡️ AWS WAF SPD Evaluator - Calculadora y Generador de Reportes
Métodos de cálculo de puntuaciones y generación de reportes
"""

from typing import Dict, List, Any
from .waf_spd_evaluator_v2 import EvaluationResult, ComplianceLevel
import json

class WAFSPDCalculator:
    """Calculadora de puntuaciones y generador de reportes para WAF SPD"""
    
    def _calculate_scores_and_summary(self, evaluations: List[EvaluationResult], 
                                    results: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula puntuaciones y genera resumen completo"""
        
        # Calcular puntuación general
        total_weighted_score = 0
        total_weight = 0
        
        # Agrupar por categorías
        category_results = {}
        
        for eval_result in evaluations:
            category = eval_result.category
            if category not in category_results:
                category_results[category] = []
            category_results[category].append(eval_result)
            
            # Obtener peso del requisito
            weight = self._get_requirement_weight(eval_result.requirement_id)
            total_weighted_score += eval_result.score * weight
            total_weight += weight
        
        # Puntuación general
        overall_score = round(total_weighted_score / total_weight if total_weight > 0 else 0, 1)
        results["overall_score"] = overall_score
        
        # Puntuaciones por categoría
        for category, cat_evaluations in category_results.items():
            cat_score = sum(eval.score for eval in cat_evaluations) / len(cat_evaluations)
            results["category_scores"][category] = round(cat_score, 1)
        
        # Resumen de compliance
        compliance_counts = {}
        for eval_result in evaluations:
            level = eval_result.compliance_level.value
            compliance_counts[level] = compliance_counts.get(level, 0) + 1
        
        results["compliance_summary"] = compliance_counts
        
        # Resultados detallados
        results["detailed_results"] = {
            eval.requirement_id: {
                "title": eval.title,
                "category": eval.category,
                "compliance_level": eval.compliance_level.value,
                "score": eval.score,
                "evidence_provided": eval.evidence_provided,
                "gaps": eval.gaps,
                "recommendations": eval.recommendations,
                "priority": eval.priority,
                "estimated_effort": eval.estimated_effort
            }
            for eval in evaluations
        }
        
        # Identificar gaps críticos
        results["critical_gaps"] = self._identify_critical_gaps(evaluations)
        
        # Generar recomendaciones generales
        results["recommendations"] = self._generate_general_recommendations(evaluations, overall_score)
        
        # Próximos pasos
        results["next_steps"] = self._generate_next_steps(evaluations, overall_score)
        
        return results
    
    def _get_requirement_weight(self, req_id: str) -> int:
        """Obtiene el peso de un requisito específico"""
        weight_mapping = {
            # Prerequisites
            "PROG-001": 5,
            "PROG-002": 10,
            
            # Case Studies
            "CASE-001": 15,
            "CASE-002": 10,
            "CASE-003": 5,
            
            # WAF Expertise (más peso por ser específicos del servicio)
            "WAF-001": 15,
            "WAF-002": 15,
            "WAF-003": 10,
            
            # Common Requirements
            "DOC-001": 10,
            "ACCT-001": 8,
            "ACCT-002": 7
        }
        
        return weight_mapping.get(req_id, 5)
    
    def _identify_critical_gaps(self, evaluations: List[EvaluationResult]) -> List[Dict[str, Any]]:
        """Identifica gaps críticos que bloquean la certificación"""
        critical_gaps = []
        
        # Requisitos críticos que deben estar compliant
        critical_requirements = ["PROG-002", "CASE-001", "WAF-001", "WAF-002"]
        
        for eval_result in evaluations:
            if (eval_result.requirement_id in critical_requirements and 
                eval_result.compliance_level == ComplianceLevel.NON_COMPLIANT):
                
                critical_gaps.append({
                    "requirement_id": eval_result.requirement_id,
                    "title": eval_result.title,
                    "category": eval_result.category,
                    "impact": "BLOCKS CERTIFICATION",
                    "gaps": eval_result.gaps,
                    "priority": "CRITICAL",
                    "estimated_effort": eval_result.estimated_effort
                })
        
        return critical_gaps
    
    def _generate_general_recommendations(self, evaluations: List[EvaluationResult], 
                                        overall_score: float) -> List[str]:
        """Genera recomendaciones generales basadas en la evaluación"""
        recommendations = []
        
        if overall_score >= 85:
            recommendations.extend([
                "🎉 Excellent readiness for WAF SPD certification!",
                "📋 Complete final documentation review",
                "✅ Submit application through AWS Partner Central",
                "🔍 Prepare for technical validation interview"
            ])
        elif overall_score >= 75:
            recommendations.extend([
                "👍 Good progress toward WAF SPD readiness",
                "🔧 Address remaining gaps before application",
                "📝 Strengthen documentation and evidence",
                "🎯 Focus on critical requirements first"
            ])
        elif overall_score >= 60:
            recommendations.extend([
                "⚠️ Moderate readiness - significant work needed",
                "🚨 Address critical gaps immediately",
                "📚 Review WAF SPD requirements thoroughly",
                "🤝 Consider engaging AWS Professional Services"
            ])
        else:
            recommendations.extend([
                "🚨 Low readiness - substantial preparation required",
                "📖 Start with program prerequisites and guidelines",
                "🏗️ Build foundational WAF expertise and case studies",
                "⏰ Plan 2-3 months preparation timeline"
            ])
        
        # Recomendaciones específicas por gaps
        non_compliant_count = sum(1 for eval in evaluations 
                                if eval.compliance_level == ComplianceLevel.NON_COMPLIANT)
        
        if non_compliant_count > 5:
            recommendations.append("🎯 Prioritize top 3 critical requirements first")
        
        # Verificar si hay case studies
        case_study_compliant = any(eval.requirement_id == "CASE-001" and 
                                 eval.compliance_level == ComplianceLevel.COMPLIANT 
                                 for eval in evaluations)
        
        if not case_study_compliant:
            recommendations.append("📝 Customer case studies are mandatory - prioritize immediately")
        
        return recommendations
    
    def _generate_next_steps(self, evaluations: List[EvaluationResult], 
                           overall_score: float) -> List[Dict[str, Any]]:
        """Genera próximos pasos específicos con timeline"""
        next_steps = []
        
        # Ordenar evaluaciones por prioridad
        high_priority = [eval for eval in evaluations if eval.priority == "HIGH"]
        medium_priority = [eval for eval in evaluations if eval.priority == "MEDIUM"]
        
        # Próximos pasos inmediatos (1-2 semanas)
        immediate_steps = []
        for eval in high_priority[:3]:  # Top 3 high priority
            if eval.compliance_level != ComplianceLevel.COMPLIANT:
                immediate_steps.append({
                    "action": f"Address {eval.requirement_id}: {eval.title}",
                    "timeline": "1-2 weeks",
                    "effort": eval.estimated_effort,
                    "priority": "HIGH"
                })
        
        # Pasos a corto plazo (2-4 semanas)
        short_term_steps = []
        for eval in medium_priority[:3]:  # Top 3 medium priority
            if eval.compliance_level != ComplianceLevel.COMPLIANT:
                short_term_steps.append({
                    "action": f"Complete {eval.requirement_id}: {eval.title}",
                    "timeline": "2-4 weeks", 
                    "effort": eval.estimated_effort,
                    "priority": "MEDIUM"
                })
        
        # Pasos a largo plazo (1-2 meses)
        long_term_steps = [
            {
                "action": "Conduct comprehensive documentation review",
                "timeline": "1-2 months",
                "effort": "1 week",
                "priority": "MEDIUM"
            },
            {
                "action": "Prepare technical validation materials",
                "timeline": "1-2 months", 
                "effort": "3-5 days",
                "priority": "MEDIUM"
            }
        ]
        
        if overall_score >= 75:
            long_term_steps.append({
                "action": "Submit WAF SPD application",
                "timeline": "1-2 months",
                "effort": "1-2 days", 
                "priority": "HIGH"
            })
        
        next_steps.extend([
            {
                "phase": "Immediate (1-2 weeks)",
                "steps": immediate_steps
            },
            {
                "phase": "Short-term (2-4 weeks)", 
                "steps": short_term_steps
            },
            {
                "phase": "Long-term (1-2 months)",
                "steps": long_term_steps
            }
        ])
        
        return next_steps
    
    def generate_detailed_report(self, evaluation_results: Dict[str, Any]) -> str:
        """Genera un reporte detallado en formato markdown"""
        
        report = f"""# 🛡️ AWS WAF Service Delivery Program - Evaluation Report

## 📊 Executive Summary

**Overall Readiness Score:** {evaluation_results['overall_score']}/100

**Evaluation Date:** {evaluation_results['evaluation_metadata']['evaluation_date'][:10]}
**Checklist Version:** {evaluation_results['evaluation_metadata']['checklist_version']}
**Validity Period:** {evaluation_results['evaluation_metadata']['validity_period']}

### 🎯 Readiness Assessment

"""
        
        overall_score = evaluation_results['overall_score']
        
        if overall_score >= 85:
            report += "✅ **READY FOR CERTIFICATION** - Excellent preparation level\n\n"
        elif overall_score >= 75:
            report += "⚠️ **NEARLY READY** - Minor gaps to address\n\n"
        elif overall_score >= 60:
            report += "🔧 **PREPARATION NEEDED** - Moderate work required\n\n"
        else:
            report += "🚨 **SIGNIFICANT PREPARATION REQUIRED** - Substantial work needed\n\n"
        
        # Compliance Summary
        report += "### 📈 Compliance Summary\n\n"
        for status, count in evaluation_results['compliance_summary'].items():
            report += f"- {status}: {count} requirements\n"
        report += "\n"
        
        # Category Scores
        report += "### 🏷️ Category Scores\n\n"
        for category, score in evaluation_results['category_scores'].items():
            report += f"- **{category}:** {score}/100\n"
        report += "\n"
        
        # Critical Gaps
        if evaluation_results['critical_gaps']:
            report += "## 🚨 Critical Gaps (Must Fix)\n\n"
            for gap in evaluation_results['critical_gaps']:
                report += f"### {gap['requirement_id']}: {gap['title']}\n"
                report += f"**Impact:** {gap['impact']}\n"
                report += f"**Effort:** {gap['estimated_effort']}\n\n"
                report += "**Gaps:**\n"
                for gap_item in gap['gaps']:
                    report += f"- {gap_item}\n"
                report += "\n"
        
        # Detailed Results
        report += "## 📋 Detailed Requirements Analysis\n\n"
        
        categories = {}
        for req_id, details in evaluation_results['detailed_results'].items():
            category = details['category']
            if category not in categories:
                categories[category] = []
            categories[category].append((req_id, details))
        
        for category, requirements in categories.items():
            report += f"### {category}\n\n"
            
            for req_id, details in requirements:
                status_icon = "✅" if "Compliant" in details['compliance_level'] else "❌"
                report += f"#### {status_icon} {req_id}: {details['title']}\n"
                report += f"**Status:** {details['compliance_level']}\n"
                report += f"**Score:** {details['score']}/100\n"
                report += f"**Priority:** {details['priority']}\n"
                report += f"**Effort:** {details['estimated_effort']}\n\n"
                
                if details['gaps']:
                    report += "**Gaps:**\n"
                    for gap in details['gaps']:
                        report += f"- {gap}\n"
                    report += "\n"
                
                if details['recommendations']:
                    report += "**Recommendations:**\n"
                    for rec in details['recommendations']:
                        report += f"- {rec}\n"
                    report += "\n"
        
        # General Recommendations
        report += "## 💡 General Recommendations\n\n"
        for rec in evaluation_results['recommendations']:
            report += f"- {rec}\n"
        report += "\n"
        
        # Next Steps
        report += "## 🚀 Next Steps\n\n"
        for phase in evaluation_results['next_steps']:
            report += f"### {phase['phase']}\n\n"
            for step in phase['steps']:
                report += f"- **{step['action']}**\n"
                report += f"  - Timeline: {step['timeline']}\n"
                report += f"  - Effort: {step['effort']}\n"
                report += f"  - Priority: {step['priority']}\n\n"
        
        # Footer
        report += """---

## 📞 Support Resources

- **AWS Partner Central:** Submit application when ready
- **Partner Development Representative (PDR):** Contact for guidance
- **AWS Professional Services:** Consider for complex implementations
- **AWS Well-Architected Reviews:** Alternative path for some requirements

**Generated by:** AWS WAF SPD Evaluator v2.0
**Based on:** Official AWS WAF Service Delivery Validation Checklist (February 2025)
"""
        
        return report
    
    def export_results_json(self, evaluation_results: Dict[str, Any], 
                          filename: str = "waf_spd_evaluation.json") -> str:
        """Exporta resultados a JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(evaluation_results, f, indent=2, ensure_ascii=False, default=str)
        
        return f"Results exported to {filename}"

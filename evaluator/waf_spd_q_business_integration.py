#!/usr/bin/env python3
"""
AWS WAF SPD Evaluator - Amazon Q Business Integration
Integración completa del evaluador WAF SPD con Amazon Q Business
"""

import boto3
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from example_usage import create_sample_partner_data as create_partner_data_example
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class WAFSPDQBusinessIntegration:
    """Integración del evaluador WAF SPD con Amazon Q Business"""
    
    def __init__(self, application_id: str, region: str = "us-east-1"):
        """
        Inicializar integración con Amazon Q Business
        
        Args:
            application_id: ID de la aplicación Amazon Q Business
            region: Región AWS
        """
        self.application_id = application_id
        self.region = region
        self.qbusiness_client = boto3.client('qbusiness', region_name=region)
        self.evaluator = WAFSPDEvaluator()
        
    def query_waf_spd_guidance(self, question: str, user_id: str = "waf-spd-user") -> Dict[str, Any]:
        """
        Consultar guidance específico de WAF SPD usando Amazon Q Business
        
        Args:
            question: Pregunta sobre WAF SPD
            user_id: ID del usuario
            
        Returns:
            Respuesta de Amazon Q Business
        """
        try:
            response = self.qbusiness_client.chat_sync(
                applicationId=self.application_id,
                userId=user_id,
                userMessage=question,
                conversationId=f"waf-spd-{int(time.time())}"
            )
            
            return {
                "success": True,
                "response": response.get('systemMessage', ''),
                "sources": response.get('sourceAttributions', []),
                "conversation_id": response.get('conversationId', '')
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": "Error al consultar Amazon Q Business"
            }
    
    def analyze_evaluation_with_q(self, evaluation_results: Dict[str, Any], user_id: str = "waf-spd-user") -> Dict[str, Any]:
        """
        Analizar resultados de evaluación usando Amazon Q Business
        
        Args:
            evaluation_results: Resultados de la evaluación WAF SPD
            user_id: ID del usuario
            
        Returns:
            Análisis inteligente de los resultados
        """
        # Crear prompt contextual para Amazon Q
        analysis_prompt = f"""
        Analiza estos resultados de evaluación AWS WAF Service Delivery Program:
        
        Puntuación General: {evaluation_results['overall_score']}/100
        
        Gaps Críticos: {len(evaluation_results.get('critical_gaps', []))}
        
        Puntuaciones por Categoría:
        {json.dumps(evaluation_results.get('category_scores', {}), indent=2)}
        
        Estado de Compliance:
        {json.dumps(evaluation_results.get('compliance_summary', {}), indent=2)}
        
        Proporciona:
        1. Análisis del estado actual de preparación
        2. Priorización de gaps críticos
        3. Plan de acción específico con timelines
        4. Recomendaciones de mejores prácticas
        5. Próximos pasos concretos
        """
        
        return self.query_waf_spd_guidance(analysis_prompt, user_id)
    
    def get_gap_remediation_plan(self, critical_gaps: List[Dict[str, Any]], user_id: str = "waf-spd-user") -> Dict[str, Any]:
        """
        Obtener plan de remediación para gaps críticos
        
        Args:
            critical_gaps: Lista de gaps críticos
            user_id: ID del usuario
            
        Returns:
            Plan de remediación detallado
        """
        gaps_summary = []
        for gap in critical_gaps:
            gaps_summary.append(f"- {gap['requirement_id']}: {gap['title']} (Impacto: {gap['impact']}, Esfuerzo: {gap['estimated_effort']})")
        
        remediation_prompt = f"""
        Necesito un plan de remediación detallado para estos gaps críticos de AWS WAF SPD:
        
        {chr(10).join(gaps_summary)}
        
        Para cada gap, proporciona:
        1. Pasos específicos de implementación
        2. Recursos AWS necesarios
        3. Documentación requerida
        4. Timeline realista
        5. Criterios de aceptación
        6. Riesgos y mitigaciones
        
        Prioriza por impacto en la certificación WAF SPD.
        """
        
        return self.query_waf_spd_guidance(remediation_prompt, user_id)
    
    def validate_case_study(self, case_study_data: Dict[str, Any], user_id: str = "waf-spd-user") -> Dict[str, Any]:
        """
        Validar case study usando Amazon Q Business
        
        Args:
            case_study_data: Datos del case study
            user_id: ID del usuario
            
        Returns:
            Validación y recomendaciones
        """
        validation_prompt = f"""
        Valida este case study para AWS WAF Service Delivery Program:
        
        Cliente: {case_study_data.get('client_name', 'No especificado')}
        Industria: {case_study_data.get('industry', 'No especificada')}
        Caso de Uso: {case_study_data.get('use_case', 'No especificado')}
        Servicios AWS: {', '.join(case_study_data.get('aws_services', []))}
        Arquitectura: {case_study_data.get('architecture_description', 'No especificada')}
        
        Evalúa:
        1. Completitud según requisitos WAF SPD
        2. Calidad técnica de la implementación
        3. Evidencia de best practices
        4. Métricas y resultados
        5. Áreas de mejora
        
        Proporciona recomendaciones específicas para cumplir con WAF SPD.
        """
        
        return self.query_waf_spd_guidance(validation_prompt, user_id)
    
    def get_certification_readiness_assessment(self, evaluation_results: Dict[str, Any], user_id: str = "waf-spd-user") -> Dict[str, Any]:
        """
        Evaluación de preparación para certificación
        
        Args:
            evaluation_results: Resultados completos de evaluación
            user_id: ID del usuario
            
        Returns:
            Evaluación de preparación para certificación
        """
        readiness_prompt = f"""
        Evalúa la preparación para certificación AWS WAF Service Delivery Program:
        
        Puntuación Actual: {evaluation_results['overall_score']}/100
        Gaps Críticos: {len(evaluation_results.get('critical_gaps', []))}
        
        Requisitos Pendientes:
        {json.dumps([gap['requirement_id'] + ': ' + gap['title'] for gap in evaluation_results.get('critical_gaps', [])], indent=2)}
        
        Determina:
        1. ¿Está listo para aplicar a la certificación?
        2. ¿Cuánto tiempo estimado para estar listo?
        3. ¿Cuáles son los blockers más críticos?
        4. ¿Qué documentación adicional se necesita?
        5. ¿Cuál es el plan de acción prioritario?
        
        Proporciona una evaluación honesta y realista.
        """
        
        return self.query_waf_spd_guidance(readiness_prompt, user_id)
    
    def generate_comprehensive_report(self, partner_data: Dict[str, Any], user_id: str = "waf-spd-user") -> Dict[str, Any]:
        """
        Generar reporte comprensivo usando evaluador + Amazon Q Business
        
        Args:
            partner_data: Datos del partner
            user_id: ID del usuario
            
        Returns:
            Reporte comprensivo con análisis inteligente
        """
        print("🔍 Ejecutando evaluación WAF SPD...")
        evaluation_results = self.evaluator.evaluate_partner_readiness(partner_data)
        
        print("🤖 Analizando resultados con Amazon Q Business...")
        q_analysis = self.analyze_evaluation_with_q(evaluation_results, user_id)
        
        print("📋 Generando plan de remediación...")
        remediation_plan = self.get_gap_remediation_plan(
            evaluation_results.get('critical_gaps', []), user_id
        )
        
        print("🎯 Evaluando preparación para certificación...")
        certification_readiness = self.get_certification_readiness_assessment(
            evaluation_results, user_id
        )
        
        return {
            "evaluation_results": evaluation_results,
            "q_business_analysis": q_analysis,
            "remediation_plan": remediation_plan,
            "certification_readiness": certification_readiness,
            "generated_at": datetime.now().isoformat(),
            "application_id": self.application_id
        }

def create_sample_partner_data() -> Dict[str, Any]:
    """Crear datos de muestra del partner para testing"""
    return {
        "prerequisites": {
            "program_guidelines_read": False,
            "services_path_membership": "Select",  # Needs to be Validated/Differentiated
            "self_assessment_completed": True
        },
        "case_studies": {
            "customer_examples": [
                {
                    "client_name": "TechCorp Inc",
                    "industry": "Financial Services",
                    "use_case": "DDoS Protection and Web Application Security",
                    "aws_services": ["AWS WAF", "CloudFront", "Shield Advanced", "ALB"],
                    "architecture_description": "Multi-tier web application with WAF protection",
                    "documented": True,
                    "architecture_diagram": True
                },
                {
                    "client_name": "RetailMax",
                    "industry": "E-commerce",
                    "use_case": "API Security and Rate Limiting",
                    "aws_services": ["AWS WAF", "API Gateway", "Lambda"],
                    "architecture_description": "Serverless API with WAF protection",
                    "documented": True,
                    "architecture_diagram": True
                }
            ],
            "unique_examples": True,
            "production_deployments": True
        },
        "waf_expertise": {
            "use_case_description": {
                "documented": True,
                "metrics_included": True,
                "rule_sets_defined": True
            },
            "valid_workload_types": {
                "compliance_environment": True,
                "custom_security_application": True,
                "ddos_mitigation_strategy": False,  # Gap
                "security_research_application": True,
                "templatized_rulesets": True
            },
            "automated_security_improvements": {
                "managed_rules": True,
                "lambda_integration": False,  # Partial
                "automated_response": True
            }
        },
        "common_requirements": {
            "architecture_documentation": {
                "scalability_design": True,
                "high_availability": True,
                "best_practices": True
            },
            "account_governance": {
                "secure_practices": True,
                "compliance_framework": True,
                "documentation": True
            },
            "identity_security": {
                "iam_best_practices": True,
                "least_privilege": True,
                "documentation": True
            }
        }
    }

def main():
    """Función principal para demostrar la integración"""
    print("🛡️ AWS WAF SPD Evaluator - Amazon Q Business Integration")
    print("=" * 60)
    
    # Configuración
    APPLICATION_ID = "0fa23d74-2dba-4e5e-8b68-4ab18c263ac1"
    
    # Crear integración
    integration = WAFSPDQBusinessIntegration(APPLICATION_ID)
    
    # Crear datos de muestra
    print("📊 Creando datos de muestra del partner...")
    partner_data = create_sample_partner_data()
    
    # Generar reporte comprensivo
    print("🚀 Generando reporte comprensivo...")
    comprehensive_report = integration.generate_comprehensive_report(partner_data)
    
    # Mostrar resultados
    print("\n📈 RESULTADOS DE EVALUACIÓN")
    print(f"Puntuación General: {comprehensive_report['evaluation_results']['overall_score']}/100")
    print(f"Gaps Críticos: {len(comprehensive_report['evaluation_results'].get('critical_gaps', []))}")
    
    print("\n🤖 ANÁLISIS DE AMAZON Q BUSINESS")
    if comprehensive_report['q_business_analysis']['success']:
        print("✅ Análisis completado exitosamente")
        print(f"Respuesta: {comprehensive_report['q_business_analysis']['response'][:200]}...")
    else:
        print("❌ Error en análisis:", comprehensive_report['q_business_analysis']['error'])
    
    print("\n📋 PLAN DE REMEDIACIÓN")
    if comprehensive_report['remediation_plan']['success']:
        print("✅ Plan generado exitosamente")
        print(f"Respuesta: {comprehensive_report['remediation_plan']['response'][:200]}...")
    else:
        print("❌ Error en plan:", comprehensive_report['remediation_plan']['error'])
    
    print("\n🎯 PREPARACIÓN PARA CERTIFICACIÓN")
    if comprehensive_report['certification_readiness']['success']:
        print("✅ Evaluación completada exitosamente")
        print(f"Respuesta: {comprehensive_report['certification_readiness']['response'][:200]}...")
    else:
        print("❌ Error en evaluación:", comprehensive_report['certification_readiness']['error'])
    
    # Guardar reporte completo
    report_filename = f"comprehensive_waf_spd_report_{int(time.time())}.json"
    with open(report_filename, 'w') as f:
        json.dump(comprehensive_report, f, indent=2, default=str)
    
    print(f"\n✅ Reporte completo guardado en: {report_filename}")
    
    # Ejemplo de consulta específica
    print("\n🔍 EJEMPLO DE CONSULTA ESPECÍFICA")
    specific_question = "¿Cómo puedo implementar WAF-002 para compliance environment con AWS WAF?"
    response = integration.query_waf_spd_guidance(specific_question)
    
    if response['success']:
        print("✅ Consulta exitosa")
        print(f"Respuesta: {response['response'][:300]}...")
    else:
        print("❌ Error en consulta:", response['error'])
    
    print("\n🎉 Integración completada exitosamente!")
    print("💡 Próximos pasos:")
    print("1. Revisar el reporte comprensivo generado")
    print("2. Implementar las recomendaciones de Amazon Q Business")
    print("3. Abordar los gaps críticos identificados")
    print("4. Re-ejecutar evaluación para trackear progreso")

if __name__ == "__main__":
    main()

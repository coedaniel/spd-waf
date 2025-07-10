#!/usr/bin/env python3
"""
🛡️ Ejemplo de uso del AWS WAF SPD Evaluator v2.0
Demuestra cómo usar el evaluador con datos de muestra
"""

import json
import sys
import os

# Agregar el directorio padre al path para importar el evaluador
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evaluator import CompleteWAFSPDEvaluator

def create_sample_partner_data():
    """Crea datos de muestra para un partner ficticio"""
    
    return {
        "partner_info": {
            "name": "ProaTech Solutions",
            "apn_tier": "Select",
            "region": "Latin America"
        },
        
        "prerequisites": {
            "program_guidelines": {
                "program_guidelines_read": True,
                "definitions_understood": True,
                "application_process_understood": False
            },
            "services_path": {
                "current_stage": "select",  # Needs to be "validated" or "differentiated"
                "advancement_in_progress": True
            }
        },
        
        "case_studies": {
            "customer_examples": [
                {
                    "customer_name": "Financial Corp ABC",
                    "project_description": "WAF implementation for PCI compliance",
                    "waf_implementation": True,
                    "production_deployment": True,
                    "within_18_months": True,
                    "unique_customer": True
                },
                {
                    "customer_name": "E-commerce XYZ", 
                    "project_description": "DDoS protection with WAF",
                    "waf_implementation": True,
                    "production_deployment": True,
                    "within_18_months": True,
                    "unique_customer": True
                }
            ],
            "architecture_diagrams": [
                {
                    "aws_services_shown": True,
                    "vpc_az_subnets_shown": True,
                    "external_connections_shown": True,
                    "scalability_demonstrated": False,  # Gap here
                    "high_availability_shown": True
                },
                {
                    "aws_services_shown": True,
                    "vpc_az_subnets_shown": True,
                    "external_connections_shown": True,
                    "scalability_demonstrated": True,
                    "high_availability_shown": True
                }
            ],
            "self_assessment": {
                "completed": True,
                "case_study_1_completed": True,
                "case_study_2_completed": True,
                "all_requirements_addressed": False,  # Gap here
                "submitted_with_application": False
            }
        },
        
        "waf_expertise": {
            "use_case": {
                "use_case_description": {
                    "provided": True,
                    "details": "Application vulnerability protection and PCI compliance"
                },
                "request_volume_metrics": {
                    "provided": True,
                    "details": "10M requests/month average"
                },
                "rule_set_details": {
                    "provided": False  # Gap here
                },
                "rule_implementation_process": {
                    "provided": True,
                    "details": "Automated deployment via CloudFormation"
                }
            },
            "workloads": {
                "compliance_environment": {
                    "implemented": True
                },
                "ddos_mitigation_strategy": {
                    "implemented": True
                },
                "primary_security_objective": {
                    "provided": True,
                    "details": "PCI DSS compliance and DDoS protection"
                },
                "project_outcomes_measurements": {
                    "provided": True,
                    "details": "99.9% uptime, zero security incidents"
                },
                "testing_strategy": {
                    "provided": False  # Gap here
                }
            },
            "automation": {
                "managed_security_rules": {
                    "implemented": True
                },
                "lambda_based_updates": {
                    "implemented": False
                },
                "implementation_details": {
                    "provided": True,
                    "details": "Using AWS Managed Rules with custom rate limiting"
                }
            }
        },
        
        "common_requirements": {
            "documentation": {
                "architecture_diagram_provided": True,
                "failure_recovery_explained": True,
                "auto_scaling_described": False,  # Gap here
                "scalability_demonstrated": True,
                "high_availability_shown": True
            },
            "account_governance": {
                "root_account_usage_defined": True,
                "mfa_enabled_on_root": True,
                "corporate_contact_info_set": True,
                "cloudtrail_enabled_all_regions": True,
                "cloudtrail_logs_protected": True,
                "sop_documentation": {
                    "provided": True
                },
                "customer_implementation": {
                    "described": False  # Gap here
                }
            },
            "identity_security": {
                "console_access_defined": True,
                "programmatic_access_defined": True,
                "temporary_credentials_usage": True,
                "identity_federation_approach": False,  # Gap here
                "iam_least_privilege": True,
                "dedicated_credentials_per_individual": True
            }
        }
    }

def main():
    """Función principal que ejecuta la evaluación de ejemplo"""
    
    print("🛡️ AWS WAF Service Delivery Program Evaluator v2.0")
    print("=" * 60)
    print()
    
    # Crear evaluador
    evaluator = CompleteWAFSPDEvaluator()
    
    # Crear datos de muestra
    print("📊 Creating sample partner data...")
    partner_data = create_sample_partner_data()
    
    # Ejecutar evaluación
    print("🔍 Running WAF SPD evaluation...")
    results = evaluator.evaluate_partner_readiness(partner_data)
    
    # Mostrar resumen
    print(f"\n📈 EVALUATION RESULTS")
    print(f"Overall Score: {results['overall_score']}/100")
    print()
    
    print("📊 Category Scores:")
    for category, score in results['category_scores'].items():
        print(f"  - {category}: {score}/100")
    print()
    
    print("🎯 Compliance Summary:")
    for status, count in results['compliance_summary'].items():
        print(f"  - {status}: {count}")
    print()
    
    # Mostrar gaps críticos
    if results['critical_gaps']:
        print("🚨 CRITICAL GAPS:")
        for gap in results['critical_gaps']:
            print(f"  - {gap['requirement_id']}: {gap['title']}")
            print(f"    Impact: {gap['impact']}")
            print(f"    Effort: {gap['estimated_effort']}")
        print()
    
    # Mostrar recomendaciones principales
    print("💡 TOP RECOMMENDATIONS:")
    for i, rec in enumerate(results['recommendations'][:5], 1):
        print(f"  {i}. {rec}")
    print()
    
    # Generar reporte detallado
    print("📝 Generating detailed report...")
    detailed_report = evaluator.generate_detailed_report(results)
    
    # Guardar reporte
    report_filename = "waf_spd_evaluation_report.md"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(detailed_report)
    
    print(f"✅ Detailed report saved to: {report_filename}")
    
    # Exportar JSON
    json_filename = "waf_spd_evaluation_results.json"
    evaluator.export_results_json(results, json_filename)
    print(f"✅ JSON results saved to: {json_filename}")
    
    print()
    print("🎯 NEXT STEPS:")
    print("1. Review the detailed report")
    print("2. Address critical gaps first")
    print("3. Update partner data as improvements are made")
    print("4. Re-run evaluation to track progress")
    print()
    print("📞 Need help? Contact your AWS PDR/PDM")

if __name__ == "__main__":
    main()

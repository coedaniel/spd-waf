"""
🛡️ AWS WAF SPD Evaluator - Métodos de Evaluación Específicos
Continuación de waf_spd_evaluator_v2.py
"""

from typing import Dict, List
from .waf_spd_evaluator_v2 import ComplianceLevel

class WAFSPDEvaluatorMethods:
    """Métodos de evaluación específicos para cada requisito WAF SPD"""
    
    def _check_program_guidelines(self, guidelines_data: Dict) -> ComplianceLevel:
        """Verifica si se han leído las guías del programa"""
        if not guidelines_data:
            return ComplianceLevel.NON_COMPLIANT
            
        required_items = [
            "program_guidelines_read",
            "definitions_understood", 
            "application_process_understood"
        ]
        
        completed_items = sum(1 for item in required_items if guidelines_data.get(item, False))
        
        if completed_items == len(required_items):
            return ComplianceLevel.COMPLIANT
        elif completed_items > 0:
            return ComplianceLevel.PARTIALLY_COMPLIANT
        else:
            return ComplianceLevel.NON_COMPLIANT
    
    def _check_services_path_membership(self, services_path_data: Dict) -> ComplianceLevel:
        """Verifica el estado en Services Path"""
        current_stage = services_path_data.get("current_stage", "").lower()
        
        if current_stage in ["validated", "differentiated"]:
            return ComplianceLevel.COMPLIANT
        elif current_stage in ["registered", "select"]:
            return ComplianceLevel.NON_COMPLIANT
        else:
            return ComplianceLevel.NEEDS_REVIEW
    
    def _check_customer_case_studies(self, case_studies: List[Dict]) -> ComplianceLevel:
        """Verifica los case studies de clientes"""
        if len(case_studies) < 2:
            return ComplianceLevel.NON_COMPLIANT
            
        valid_studies = 0
        for study in case_studies[:2]:  # Solo evaluar los primeros 2
            if self._validate_case_study(study):
                valid_studies += 1
                
        if valid_studies == 2:
            return ComplianceLevel.COMPLIANT
        elif valid_studies == 1:
            return ComplianceLevel.PARTIALLY_COMPLIANT
        else:
            return ComplianceLevel.NON_COMPLIANT
    
    def _validate_case_study(self, study: Dict) -> bool:
        """Valida un case study individual"""
        required_fields = [
            "customer_name",
            "project_description", 
            "waf_implementation",
            "production_deployment",
            "within_18_months",
            "unique_customer"
        ]
        
        return all(study.get(field, False) for field in required_fields)
    
    def _check_architecture_diagrams(self, diagrams: List[Dict]) -> ComplianceLevel:
        """Verifica los diagramas de arquitectura"""
        if not diagrams:
            return ComplianceLevel.NON_COMPLIANT
            
        valid_diagrams = 0
        for diagram in diagrams:
            if self._validate_architecture_diagram(diagram):
                valid_diagrams += 1
                
        if valid_diagrams >= 2:
            return ComplianceLevel.COMPLIANT
        elif valid_diagrams == 1:
            return ComplianceLevel.PARTIALLY_COMPLIANT
        else:
            return ComplianceLevel.NON_COMPLIANT
    
    def _validate_architecture_diagram(self, diagram: Dict) -> bool:
        """Valida un diagrama de arquitectura"""
        required_elements = [
            "aws_services_shown",
            "vpc_az_subnets_shown",
            "external_connections_shown",
            "scalability_demonstrated",
            "high_availability_shown"
        ]
        
        return all(diagram.get(element, False) for element in required_elements)
    
    def _check_self_assessment(self, assessment_data: Dict) -> ComplianceLevel:
        """Verifica el self-assessment spreadsheet"""
        if not assessment_data.get("completed", False):
            return ComplianceLevel.NON_COMPLIANT
            
        required_sections = [
            "case_study_1_completed",
            "case_study_2_completed", 
            "all_requirements_addressed",
            "submitted_with_application"
        ]
        
        completed_sections = sum(1 for section in required_sections 
                               if assessment_data.get(section, False))
        
        if completed_sections == len(required_sections):
            return ComplianceLevel.COMPLIANT
        elif completed_sections >= 2:
            return ComplianceLevel.PARTIALLY_COMPLIANT
        else:
            return ComplianceLevel.NON_COMPLIANT
    
    def _check_waf_use_case_description(self, use_case_data: Dict) -> ComplianceLevel:
        """Verifica WAF-001: AWS WAF Use Case Description"""
        required_evidence = [
            "use_case_description",  # app vulnerability protection, PCI compliance, DDoS protection
            "request_volume_metrics",
            "rule_set_details",
            "rule_implementation_process"
        ]
        
        provided_evidence = sum(1 for evidence in required_evidence 
                              if use_case_data.get(evidence, {}).get("provided", False))
        
        if provided_evidence == len(required_evidence):
            return ComplianceLevel.COMPLIANT
        elif provided_evidence >= 2:
            return ComplianceLevel.PARTIALLY_COMPLIANT
        else:
            return ComplianceLevel.NON_COMPLIANT
    
    def _check_valid_waf_workloads(self, workload_data: Dict) -> ComplianceLevel:
        """Verifica WAF-002: Valid AWS WAF Workloads"""
        valid_workload_types = [
            "compliance_environment",
            "custom_security_application",
            "ddos_mitigation_strategy", 
            "security_research_application",
            "templatized_rulesets"
        ]
        
        # Verificar que al menos un tipo de workload válido esté implementado
        implemented_workloads = [wt for wt in valid_workload_types 
                               if workload_data.get(wt, {}).get("implemented", False)]
        
        if not implemented_workloads:
            return ComplianceLevel.NON_COMPLIANT
            
        # Verificar evidencia requerida
        required_evidence = [
            "primary_security_objective",
            "project_outcomes_measurements",
            "testing_strategy"
        ]
        
        provided_evidence = sum(1 for evidence in required_evidence 
                              if workload_data.get(evidence, {}).get("provided", False))
        
        if len(implemented_workloads) >= 1 and provided_evidence == len(required_evidence):
            return ComplianceLevel.COMPLIANT
        elif len(implemented_workloads) >= 1 and provided_evidence >= 1:
            return ComplianceLevel.PARTIALLY_COMPLIANT
        else:
            return ComplianceLevel.NON_COMPLIANT
    
    def _check_automated_security_improvements(self, automation_data: Dict) -> ComplianceLevel:
        """Verifica WAF-003: Automated Security Improvements"""
        automation_approaches = [
            "managed_security_rules",
            "lambda_based_updates",
            "automated_ruleset_updates"
        ]
        
        implemented_approaches = [approach for approach in automation_approaches 
                                if automation_data.get(approach, {}).get("implemented", False)]
        
        if not implemented_approaches:
            return ComplianceLevel.NON_COMPLIANT
            
        # Verificar que se proporcione descripción de implementación
        implementation_described = automation_data.get("implementation_details", {}).get("provided", False)
        
        if len(implemented_approaches) >= 1 and implementation_described:
            return ComplianceLevel.COMPLIANT
        elif len(implemented_approaches) >= 1:
            return ComplianceLevel.PARTIALLY_COMPLIANT
        else:
            return ComplianceLevel.NON_COMPLIANT
    
    def _check_architecture_documentation(self, doc_data: Dict) -> ComplianceLevel:
        """Verifica DOC-001: Architecture Documentation"""
        required_elements = [
            "architecture_diagram_provided",
            "failure_recovery_explained",
            "auto_scaling_described",
            "scalability_demonstrated",
            "high_availability_shown"
        ]
        
        provided_elements = sum(1 for element in required_elements 
                              if doc_data.get(element, False))
        
        if provided_elements == len(required_elements):
            return ComplianceLevel.COMPLIANT
        elif provided_elements >= 3:
            return ComplianceLevel.PARTIALLY_COMPLIANT
        else:
            return ComplianceLevel.NON_COMPLIANT
    
    def _check_account_governance(self, governance_data: Dict) -> ComplianceLevel:
        """Verifica ACCT-001: Secure AWS Account Governance"""
        required_practices = [
            "root_account_usage_defined",
            "mfa_enabled_on_root",
            "corporate_contact_info_set",
            "cloudtrail_enabled_all_regions",
            "cloudtrail_logs_protected"
        ]
        
        implemented_practices = sum(1 for practice in required_practices 
                                  if governance_data.get(practice, False))
        
        # También verificar documentación
        documentation_provided = governance_data.get("sop_documentation", {}).get("provided", False)
        customer_example_described = governance_data.get("customer_implementation", {}).get("described", False)
        
        if (implemented_practices == len(required_practices) and 
            documentation_provided and customer_example_described):
            return ComplianceLevel.COMPLIANT
        elif implemented_practices >= 3 and (documentation_provided or customer_example_described):
            return ComplianceLevel.PARTIALLY_COMPLIANT
        else:
            return ComplianceLevel.NON_COMPLIANT
    
    def _check_identity_security(self, identity_data: Dict) -> ComplianceLevel:
        """Verifica ACCT-002: Identity Security Best Practice"""
        required_approaches = [
            "console_access_defined",
            "programmatic_access_defined", 
            "temporary_credentials_usage",
            "identity_federation_approach",
            "iam_least_privilege",
            "dedicated_credentials_per_individual"
        ]
        
        implemented_approaches = sum(1 for approach in required_approaches 
                                   if identity_data.get(approach, False))
        
        if implemented_approaches == len(required_approaches):
            return ComplianceLevel.COMPLIANT
        elif implemented_approaches >= 4:
            return ComplianceLevel.PARTIALLY_COMPLIANT
        else:
            return ComplianceLevel.NON_COMPLIANT
    
    def _compliance_to_score(self, compliance: ComplianceLevel) -> int:
        """Convierte nivel de compliance a puntuación numérica"""
        score_mapping = {
            ComplianceLevel.COMPLIANT: 100,
            ComplianceLevel.PARTIALLY_COMPLIANT: 60,
            ComplianceLevel.NON_COMPLIANT: 0,
            ComplianceLevel.NOT_APPLICABLE: 100,
            ComplianceLevel.NEEDS_REVIEW: 30
        }
        return score_mapping.get(compliance, 0)
    
    def _identify_gaps(self, req_id: str, data: Dict, criteria: Dict) -> List[str]:
        """Identifica gaps específicos para un requisito"""
        gaps = []
        
        # Gaps específicos por requisito
        gap_mapping = {
            "PROG-001": [
                "Program guidelines not read",
                "Definitions not understood", 
                "Application process unclear"
            ],
            "PROG-002": [
                "Not at Validated or Differentiated stage",
                "Services Path membership needs upgrade"
            ],
            "CASE-001": [
                "Less than 2 unique customer case studies",
                "Case studies not in production",
                "Projects older than 18 months",
                "Customers not unique legal entities"
            ],
            "WAF-001": [
                "WAF use case not clearly described",
                "Request volume metrics missing",
                "Rule set details incomplete",
                "Rule implementation process undefined"
            ],
            "WAF-002": [
                "No valid WAF workload type implemented",
                "Primary security objective unclear",
                "Project outcomes not measured",
                "Testing strategy not defined"
            ],
            "WAF-003": [
                "No automated security improvements",
                "Implementation details not provided",
                "Neither managed rules nor automation implemented"
            ]
        }
        
        return gap_mapping.get(req_id, ["Detailed analysis required"])
    
    def _generate_recommendations(self, req_id: str, compliance: ComplianceLevel) -> List[str]:
        """Genera recomendaciones específicas para cada requisito"""
        if compliance == ComplianceLevel.COMPLIANT:
            return ["✅ Requirement met - maintain current implementation"]
            
        recommendation_mapping = {
            "PROG-001": [
                "📖 Read AWS Service Delivery Program guidelines thoroughly",
                "📋 Review program definitions and requirements",
                "🤝 Contact PDR/PDM for clarification if needed"
            ],
            "PROG-002": [
                "⬆️ Upgrade to Validated or Differentiated Services Path stage",
                "🤝 Work with PDR/PDM on Services Path advancement",
                "📈 Complete required competency validations"
            ],
            "CASE-001": [
                "📝 Document 2 unique production WAF implementations",
                "🏢 Ensure customers are separate legal entities", 
                "📅 Verify projects are within 18-month timeframe",
                "🔍 Include detailed WAF-specific implementation details"
            ],
            "WAF-001": [
                "📊 Document specific WAF use case (vulnerability protection, compliance, DDoS)",
                "📈 Provide request volume metrics and analysis",
                "⚙️ Detail implemented rule sets and configurations",
                "📋 Document rule selection and implementation process"
            ],
            "WAF-002": [
                "🎯 Implement at least one valid WAF workload type",
                "🔒 Define clear primary security objectives",
                "📊 Establish measurable project outcomes",
                "🧪 Develop comprehensive testing strategy"
            ],
            "WAF-003": [
                "🤖 Implement managed security rules or automated updates",
                "⚡ Use AWS Lambda for automated ruleset management",
                "📝 Document implementation details for staying current with threats"
            ]
        }
        
        return recommendation_mapping.get(req_id, ["Contact AWS for specific guidance"])
    
    def _determine_priority(self, req_id: str, compliance: ComplianceLevel) -> str:
        """Determina la prioridad de remediation"""
        if compliance == ComplianceLevel.COMPLIANT:
            return "LOW"
            
        high_priority_requirements = ["PROG-002", "CASE-001", "WAF-001", "WAF-002"]
        
        if req_id in high_priority_requirements:
            return "HIGH"
        elif compliance == ComplianceLevel.NON_COMPLIANT:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _estimate_effort(self, req_id: str, compliance: ComplianceLevel) -> str:
        """Estima el esfuerzo requerido para remediation"""
        if compliance == ComplianceLevel.COMPLIANT:
            return "0 HOURS"
            
        effort_mapping = {
            "PROG-001": "4-8 HOURS",
            "PROG-002": "2-4 WEEKS", 
            "CASE-001": "1-2 WEEKS",
            "CASE-002": "3-5 DAYS",
            "CASE-003": "1-2 DAYS",
            "WAF-001": "2-3 DAYS",
            "WAF-002": "1-2 WEEKS",
            "WAF-003": "3-5 DAYS",
            "DOC-001": "2-3 DAYS",
            "ACCT-001": "1-2 DAYS",
            "ACCT-002": "1-2 DAYS"
        }
        
        base_effort = effort_mapping.get(req_id, "1-2 DAYS")
        
        if compliance == ComplianceLevel.NON_COMPLIANT:
            return base_effort
        else:  # PARTIALLY_COMPLIANT
            return f"50% of {base_effort}"

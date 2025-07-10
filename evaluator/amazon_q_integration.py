#!/usr/bin/env python3
"""
🤖 Amazon Q Business Integration para WAF SPD Evaluator
Integra el evaluador con Amazon Q Business para análisis inteligente
"""

import json
import boto3
from typing import Dict, Any, List
from datetime import datetime

class AmazonQWAFSPDIntegration:
    """
    Integración con Amazon Q Business para análisis inteligente de WAF SPD
    """
    
    def __init__(self, application_id: str, region: str = 'us-east-1'):
        """
        Inicializa la integración con Amazon Q Business
        
        Args:
            application_id: ID de la aplicación Amazon Q Business
            region: Región AWS
        """
        self.application_id = application_id
        self.region = region
        self.q_business_client = boto3.client('qbusiness', region_name=region)
        
    def create_system_prompt(self) -> str:
        """Crea el system prompt para Amazon Q Business"""
        
        return """You are an AWS WAF Service Delivery Program (SPD) expert assistant. Your role is to help AWS Partners achieve WAF SPD certification by providing accurate guidance based on the official requirements.

## Your Expertise

You have deep knowledge of:
- AWS WAF Service Delivery Validation Checklist (February 2025 version)
- AWS Partner Network requirements and processes
- WAF implementation best practices
- Security architecture and compliance requirements
- AWS Well-Architected Framework principles

## Key Requirements You Help With

### Prerequisites
- APN Program Requirements (Services Path membership)
- Customer Case Studies (2 unique production examples)
- Self-Assessment completion

### WAF-Specific Expertise
- WAF-001: Use case description (vulnerability protection, PCI compliance, DDoS)
- WAF-002: Valid workload types (compliance, security, DDoS mitigation, research, templates)
- WAF-003: Automated security improvements (managed rules, Lambda automation)

### Common Requirements
- Architecture documentation with scalability and HA
- Secure account governance best practices
- Identity security with IAM best practices

## Your Responses Should

1. **Be Specific**: Reference exact requirement IDs (WAF-001, CASE-001, etc.)
2. **Provide Evidence**: Explain what documentation/evidence is needed
3. **Prioritize**: Identify critical vs. nice-to-have requirements
4. **Estimate Effort**: Give realistic timelines for remediation
5. **Offer Alternatives**: Suggest multiple approaches when possible

## Response Format

For evaluation questions, structure your response as:

**Current Status**: [Assessment of current state]
**Gaps Identified**: [Specific gaps with requirement IDs]
**Recommendations**: [Prioritized action items]
**Timeline**: [Realistic effort estimates]
**Next Steps**: [Immediate actions to take]

## Important Notes

- Validity Period: February 2025 - August 2025
- Partners need Validated or Differentiated Services Path status
- Case studies must be production deployments within 18 months
- Well-Architected Reviews can substitute for some common requirements
- Technical validation is conducted offline by AWS experts

Always provide actionable, specific guidance that helps partners progress toward certification."""

    def upload_waf_spd_documents(self, documents: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Sube documentos de WAF SPD a Amazon Q Business
        
        Args:
            documents: Lista de documentos con 'title', 'content', 'source'
            
        Returns:
            Resultado de la operación de carga
        """
        
        results = {
            "uploaded_documents": [],
            "errors": [],
            "summary": {}
        }
        
        for doc in documents:
            try:
                # Crear documento en Amazon Q Business
                response = self.q_business_client.put_document(
                    applicationId=self.application_id,
                    document={
                        'id': f"waf-spd-{doc['title'].lower().replace(' ', '-')}",
                        'title': doc['title'],
                        'content': {
                            'text': doc['content']
                        },
                        'attributes': [
                            {
                                'name': 'source',
                                'value': {
                                    'stringValue': doc.get('source', 'WAF SPD Documentation')
                                }
                            },
                            {
                                'name': 'document_type',
                                'value': {
                                    'stringValue': 'waf_spd_requirement'
                                }
                            },
                            {
                                'name': 'last_updated',
                                'value': {
                                    'dateValue': datetime.now()
                                }
                            }
                        ]
                    }
                )
                
                results["uploaded_documents"].append({
                    "title": doc['title'],
                    "document_id": response.get('documentId'),
                    "status": "success"
                })
                
            except Exception as e:
                results["errors"].append({
                    "title": doc['title'],
                    "error": str(e)
                })
        
        results["summary"] = {
            "total_documents": len(documents),
            "successful_uploads": len(results["uploaded_documents"]),
            "failed_uploads": len(results["errors"])
        }
        
        return results
    
    def query_waf_spd_guidance(self, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Consulta Amazon Q Business para obtener guidance sobre WAF SPD
        
        Args:
            question: Pregunta sobre WAF SPD
            context: Contexto adicional (datos del partner, evaluación actual, etc.)
            
        Returns:
            Respuesta de Amazon Q Business con guidance
        """
        
        # Construir contexto completo
        full_context = ""
        if context:
            full_context = f"""
## Current Partner Context:
{json.dumps(context, indent=2)}

## Question:
{question}

Please provide specific guidance based on the AWS WAF Service Delivery Program requirements and the partner's current status.
"""
        else:
            full_context = question
        
        try:
            response = self.q_business_client.chat_sync(
                applicationId=self.application_id,
                userMessage=full_context,
                conversationId=None  # Nueva conversación
            )
            
            return {
                "success": True,
                "response": response.get('systemMessage', ''),
                "conversation_id": response.get('conversationId'),
                "source_attributions": response.get('sourceAttributions', [])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": "Unable to get guidance from Amazon Q Business"
            }
    
    def analyze_evaluation_results(self, evaluation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analiza resultados de evaluación usando Amazon Q Business
        
        Args:
            evaluation_results: Resultados del WAF SPD Evaluator
            
        Returns:
            Análisis inteligente y recomendaciones
        """
        
        analysis_prompt = f"""
Analyze the following WAF SPD evaluation results and provide intelligent recommendations:

## Evaluation Results:
{json.dumps(evaluation_results, indent=2)}

Please provide:

1. **Priority Analysis**: Which gaps should be addressed first and why?
2. **Effort Optimization**: How to minimize time to certification?
3. **Risk Assessment**: What are the biggest blockers to certification?
4. **Alternative Approaches**: Are there alternative paths to meet requirements?
5. **Timeline Recommendations**: Realistic timeline to achieve certification readiness?

Focus on actionable, specific guidance that will help this partner achieve WAF SPD certification efficiently.
"""
        
        return self.query_waf_spd_guidance(analysis_prompt)
    
    def get_gap_remediation_plan(self, gaps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Obtiene plan de remediación para gaps específicos
        
        Args:
            gaps: Lista de gaps identificados
            
        Returns:
            Plan detallado de remediación
        """
        
        gaps_summary = "\n".join([
            f"- {gap['requirement_id']}: {gap['title']} (Priority: {gap.get('priority', 'Unknown')})"
            for gap in gaps
        ])
        
        remediation_prompt = f"""
Create a detailed remediation plan for the following WAF SPD gaps:

{gaps_summary}

For each gap, provide:
1. **Specific Actions**: What exactly needs to be done?
2. **Evidence Required**: What documentation/proof is needed?
3. **Implementation Steps**: Step-by-step process
4. **Timeline**: Realistic effort estimate
5. **Dependencies**: What needs to be done first?
6. **Success Criteria**: How to know when it's complete?

Prioritize the plan to minimize time to certification while ensuring quality.
"""
        
        return self.query_waf_spd_guidance(remediation_prompt)
    
    def validate_case_study(self, case_study: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida un case study usando Amazon Q Business
        
        Args:
            case_study: Datos del case study
            
        Returns:
            Validación y recomendaciones de mejora
        """
        
        validation_prompt = f"""
Validate the following WAF SPD case study against official requirements:

## Case Study Details:
{json.dumps(case_study, indent=2)}

Please assess:

1. **Requirement Compliance**: Does it meet WAF-001, WAF-002, WAF-003 requirements?
2. **Evidence Completeness**: What evidence is missing or insufficient?
3. **Technical Depth**: Is the technical detail adequate for validation?
4. **Architecture Quality**: Does the architecture demonstrate best practices?
5. **Improvement Recommendations**: How can this case study be strengthened?

Provide specific, actionable feedback for improving this case study.
"""
        
        return self.query_waf_spd_guidance(validation_prompt)

def create_sample_documents():
    """Crea documentos de muestra para cargar a Amazon Q Business"""
    
    return [
        {
            "title": "WAF SPD Requirements Overview",
            "content": """
# AWS WAF Service Delivery Program Requirements

## Prerequisites
- Services Path: Validated or Differentiated stage required
- Case Studies: 2 unique production customer examples
- Self-Assessment: Complete spreadsheet required

## WAF Expertise Requirements

### WAF-001: Use Case Description
- Description of WAF use case (vulnerability protection, PCI compliance, DDoS)
- Request volume metrics
- Rule set implementation details
- Process for rule selection

### WAF-002: Valid Workload Types
Must implement one of:
- AWS WAF in compliance environment
- Custom security application
- DDoS mitigation strategy
- Security research application
- Templatized rulesets

### WAF-003: Automated Security Improvements
- Managed security rules OR
- Lambda-based automated updates
- Implementation details required

## Common Requirements
- Architecture diagrams with scalability/HA
- Secure account governance
- IAM identity security best practices
""",
            "source": "Official WAF SPD Checklist"
        },
        {
            "title": "WAF Implementation Best Practices",
            "content": """
# AWS WAF Implementation Best Practices

## Rule Set Design
- Start with AWS Managed Rules
- Add custom rules for specific threats
- Implement rate limiting
- Use geo-blocking when appropriate

## Monitoring and Logging
- Enable WAF logging to CloudWatch
- Set up CloudWatch alarms
- Monitor blocked vs allowed requests
- Track rule effectiveness

## Automation Strategies
- Use AWS Lambda for dynamic rule updates
- Implement threat intelligence feeds
- Automate rule testing and validation
- Set up automated rollback procedures

## Performance Optimization
- Optimize rule order for efficiency
- Use rule groups for organization
- Monitor latency impact
- Implement caching strategies
""",
            "source": "AWS WAF Best Practices Guide"
        }
    ]

# Ejemplo de uso
if __name__ == "__main__":
    # Configurar integración (reemplazar con tu Application ID real)
    integration = AmazonQWAFSPDIntegration(
        application_id="your-amazon-q-app-id",
        region="us-east-1"
    )
    
    # Cargar documentos de muestra
    sample_docs = create_sample_documents()
    upload_results = integration.upload_waf_spd_documents(sample_docs)
    
    print("📤 Document Upload Results:")
    print(json.dumps(upload_results, indent=2))
    
    # Ejemplo de consulta
    question = "What are the critical requirements for WAF SPD certification?"
    guidance = integration.query_waf_spd_guidance(question)
    
    print("\n🤖 Amazon Q Guidance:")
    print(guidance.get('response', 'No response available'))

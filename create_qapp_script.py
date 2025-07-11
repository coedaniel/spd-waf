#!/usr/bin/env python3
"""
Script para crear Q App de WAF SPD usando credenciales de Identity Center
"""

import boto3
import json
import sys

def create_waf_spd_qapp():
    """Crear Q App para WAF SPD"""
    
    # Configuración
    INSTANCE_ID = "0fa23d74-2dba-4e5e-8b68-4ab18c263ac1"
    
    # Definición de la Q App
    app_definition = {
        "cards": [
            {
                "textInput": {
                    "title": "📊 Current WAF SPD Status",
                    "id": "current-status",
                    "type": "text-input",
                    "placeholder": "Describe your current situation:\n• Overall evaluation score (if known)\n• Services Path Membership level (Select/Validated/Differentiated)\n• Completed requirements\n• Known gaps or challenges\n• Case studies status\n• Timeline goals\n\nExample: Score 63.6/100, Services Path is Select (need Validated), have 2 case studies documented, missing DDoS mitigation strategy, goal to apply in 3 months"
                }
            },
            {
                "qQuery": {
                    "title": "📋 WAF SPD Requirements Overview",
                    "id": "requirements-overview",
                    "type": "q-query",
                    "prompt": "Based on the AWS WAF Service Delivery Program checklist from February 2025, provide a comprehensive overview of all requirements:\n\n1. **Prerequisites (PROG-001, PROG-002)**:\n   - Program Guidelines understanding\n   - Services Path Membership requirements (Validated/Differentiated)\n\n2. **Case Studies (CASE-001, CASE-002, CASE-003)**:\n   - 2 unique customer examples in production\n   - Architecture diagrams with AWS services\n   - Self-Assessment Spreadsheet completion\n\n3. **WAF Expertise (WAF-001, WAF-002, WAF-003)**:\n   - Use Case Description with metrics and rule sets\n   - Valid Workload Types implementation\n   - Automated Security Improvements\n\n4. **Common Requirements (DOC-001, ACCT-001, ACCT-002)**:\n   - Architecture documentation with HA/scalability\n   - Secure AWS Account Governance\n   - Identity Security best practices\n\nFor each requirement, explain the specific criteria, evidence needed, and evaluation standards."
                }
            },
            {
                "qQuery": {
                    "title": "🎯 Personalized Gap Analysis & Action Plan",
                    "id": "gap-analysis",
                    "type": "q-query",
                    "prompt": "Based on this partner's current WAF SPD status: {{current-status}}\n\nProvide a detailed analysis including:\n\n**1. Current Readiness Assessment:**\n- Evaluate the overall preparation level\n- Identify critical gaps that block certification\n- Assess timeline feasibility\n\n**2. Prioritized Action Plan:**\n- List gaps in order of criticality\n- Provide specific implementation steps for each gap\n- Include realistic timelines (hours/days/weeks)\n- Specify required resources and documentation\n\n**3. Services Path Membership Guidance:**\n- If not at Validated/Differentiated level, provide upgrade path\n- Explain requirements and timeline for advancement\n- Suggest strategies to accelerate the process\n\n**4. Technical Implementation:**\n- Specific guidance for WAF-001, WAF-002, WAF-003\n- Code examples and configuration templates where applicable\n- Best practices for each workload type\n\n**5. Certification Timeline:**\n- Estimate when ready to apply based on current status\n- Provide milestone checkpoints\n- Suggest re-evaluation schedule\n\nBe specific, actionable, and realistic in all recommendations."
                }
            }
        ],
        "initialPrompt": "Welcome to the AWS WAF Service Delivery Program Certification Assistant! 🛡️\n\nThis comprehensive tool will guide you through every step of your WAF SPD certification journey, from initial assessment to final application submission.\n\n**How to use this app:**\n1. Start by describing your current status in the first card\n2. Review the complete requirements overview\n3. Get your personalized gap analysis and action plan\n\n**Based on the official AWS WAF SPD checklist (February 2025)** with validity period through August 2025.\n\nLet's get started on your path to WAF SPD certification! 🚀"
    }
    
    try:
        # Crear cliente Q Apps
        qapps_client = boto3.client('qapps', region_name='us-east-1')
        
        # Crear Q App
        response = qapps_client.create_q_app(
            instanceId=INSTANCE_ID,
            title="🛡️ AWS WAF SPD Certification Assistant",
            description="Comprehensive tool for AWS WAF Service Delivery Program certification preparation, evaluation, and guidance",
            appDefinition=app_definition,
            tags={
                "Purpose": "WAF-SPD-Certification",
                "Type": "Evaluation-Assessment",
                "Version": "2.0",
                "Checklist": "February-2025"
            }
        )
        
        print("✅ Q App creada exitosamente!")
        print(f"App ID: {response['appId']}")
        print(f"App ARN: {response['appArn']}")
        print(f"Title: {response['title']}")
        print(f"Status: {response['status']}")
        
        return response
        
    except Exception as e:
        print(f"❌ Error creando Q App: {str(e)}")
        print("\n💡 Soluciones:")
        print("1. Asegúrate de estar usando credenciales de Identity Center")
        print("2. Verifica que tienes permisos para crear Q Apps")
        print("3. Usa la consola web como alternativa")
        return None

def main():
    """Función principal"""
    print("🚀 Creando Q App para AWS WAF SPD...")
    print("=" * 50)
    
    # Verificar credenciales
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"Usuario actual: {identity['Arn']}")
        
        if "assumed-role/SSMInstanceProfile" in identity['Arn']:
            print("⚠️  Estás usando rol de instancia EC2")
            print("💡 Para crear Q Apps, necesitas usar credenciales de Identity Center")
            print("\n📋 Opciones:")
            print("1. Usar la consola web (recomendado)")
            print("2. Configurar AWS CLI con Identity Center")
            print("3. Usar este script desde una sesión con credenciales correctas")
            return
            
    except Exception as e:
        print(f"Error verificando credenciales: {e}")
        return
    
    # Crear Q App
    result = create_waf_spd_qapp()
    
    if result:
        print("\n🎉 ¡Q App lista para usar!")
        print("Ve a tu aplicación Amazon Q Business y busca en la sección 'Q Apps'")
    else:
        print("\n📋 Usa la guía manual en CREATE_Q_APP_GUIDE.md")

if __name__ == "__main__":
    main()

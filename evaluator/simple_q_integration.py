#!/usr/bin/env python3
"""
AWS WAF SPD Evaluator - Integración Simple con Amazon Q Business
"""

import boto3
import json
import uuid
import time
from datetime import datetime

class SimpleWAFSPDQIntegration:
    """Integración simple del evaluador WAF SPD con Amazon Q Business"""
    
    def __init__(self, application_id: str, region: str = "us-east-1"):
        self.application_id = application_id
        self.region = region
        self.qbusiness_client = boto3.client('qbusiness', region_name=region)
        
    def query_waf_spd_guidance(self, question: str, user_id: str = "waf-spd-user") -> dict:
        """Consultar guidance específico de WAF SPD"""
        try:
            response = self.qbusiness_client.chat_sync(
                applicationId=self.application_id,
                userMessage=question,
                conversationId=str(uuid.uuid4())
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
                "response": f"Error al consultar Amazon Q Business: {str(e)}"
            }

def main():
    """Función principal para probar la integración"""
    print("🛡️ AWS WAF SPD - Amazon Q Business Integration Test")
    print("=" * 55)
    
    # Configuración
    APPLICATION_ID = "0fa23d74-2dba-4e5e-8b68-4ab18c263ac1"
    
    # Crear integración
    integration = SimpleWAFSPDQIntegration(APPLICATION_ID)
    
    # Preguntas de prueba
    test_questions = [
        "¿Cuáles son los requisitos principales para AWS WAF Service Delivery Program?",
        "¿Cómo implementar WAF-001 Use Case Description con métricas?",
        "¿Qué documentación necesito para WAF-002 Valid Workload Types?",
        "¿Cuáles son los criterios para case studies en WAF SPD?",
        "¿Cómo preparar la aplicación para certificación WAF SPD?"
    ]
    
    print("🔍 Ejecutando consultas de prueba...")
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📋 Pregunta {i}: {question}")
        print("-" * 50)
        
        response = integration.query_waf_spd_guidance(question)
        
        if response['success']:
            print("✅ Respuesta exitosa")
            print(f"📝 Respuesta: {response['response'][:300]}...")
            if response['sources']:
                print(f"📚 Fuentes: {len(response['sources'])} documentos referenciados")
        else:
            print("❌ Error en consulta")
            print(f"🚨 Error: {response['error']}")
        
        # Pausa entre consultas
        time.sleep(2)
    
    print("\n🎯 CONSULTA ESPECÍFICA DE EVALUACIÓN")
    print("=" * 40)
    
    evaluation_question = """
    Tengo estos resultados de evaluación WAF SPD:
    - Puntuación general: 63.6/100
    - Gap crítico: PROG-002 Services Path Membership (no estoy en Validated/Differentiated)
    - Tengo 2 case studies documentados
    - WAF expertise parcialmente completo
    
    ¿Cuál es mi plan de acción prioritario para obtener la certificación?
    """
    
    response = integration.query_waf_spd_guidance(evaluation_question)
    
    if response['success']:
        print("✅ Análisis de evaluación completado")
        print(f"📊 Recomendaciones: {response['response']}")
        
        # Guardar respuesta completa
        report = {
            "timestamp": datetime.now().isoformat(),
            "question": evaluation_question,
            "response": response['response'],
            "sources": response['sources'],
            "application_id": APPLICATION_ID
        }
        
        filename = f"waf_spd_q_analysis_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"💾 Análisis guardado en: {filename}")
        
    else:
        print("❌ Error en análisis")
        print(f"🚨 Error: {response['error']}")
    
    print("\n🎉 Prueba de integración completada!")
    print("\n💡 Próximos pasos:")
    print("1. Verificar que el data source esté sincronizado")
    print("2. Hacer más consultas específicas según tus necesidades")
    print("3. Usar las respuestas para mejorar tu preparación WAF SPD")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
AWS WAF SPD Evaluator - Amazon Q Business Integration con Identity Center
"""

import boto3
import json
import uuid
import time
from datetime import datetime

class IdentityCenterWAFSPDQIntegration:
    """Integración WAF SPD con Amazon Q Business usando Identity Center"""
    
    def __init__(self, application_id: str, region: str = "us-east-1"):
        self.application_id = application_id
        self.region = region
        
        # Para Identity Center, necesitamos usar credenciales específicas
        # Primero intentamos con el cliente estándar
        self.qbusiness_client = boto3.client('qbusiness', region_name=region)
        
    def query_waf_spd_guidance(self, question: str) -> dict:
        """Consultar guidance específico de WAF SPD con Identity Center"""
        try:
            # Para aplicaciones con Identity Center, userId debe ser None
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
    
    def check_data_source_sync_status(self, data_source_id: str, index_id: str) -> dict:
        """Verificar estado de sincronización del data source"""
        try:
            response = self.qbusiness_client.list_data_source_sync_jobs(
                applicationId=self.application_id,
                indexId=index_id,
                dataSourceId=data_source_id
            )
            
            if response.get('history'):
                latest_job = response['history'][0]
                return {
                    "success": True,
                    "status": latest_job.get('status'),
                    "metrics": latest_job.get('metrics', {}),
                    "start_time": latest_job.get('startTime'),
                    "end_time": latest_job.get('endTime'),
                    "error": latest_job.get('error', {})
                }
            else:
                return {
                    "success": True,
                    "status": "NO_JOBS",
                    "message": "No hay trabajos de sincronización"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

def main():
    """Función principal para probar la integración con Identity Center"""
    print("🛡️ AWS WAF SPD - Amazon Q Business Integration (Identity Center)")
    print("=" * 65)
    
    # Configuración
    APPLICATION_ID = "0fa23d74-2dba-4e5e-8b68-4ab18c263ac1"
    DATA_SOURCE_ID = "a6e09258-4dd1-48d1-b15e-dc53f3541071"
    INDEX_ID = "24e8627f-28e2-49f1-ab0d-f48fea79e21e"
    
    # Crear integración
    integration = IdentityCenterWAFSPDQIntegration(APPLICATION_ID)
    
    # Verificar estado de sincronización primero
    print("🔍 Verificando estado de sincronización del data source...")
    sync_status = integration.check_data_source_sync_status(DATA_SOURCE_ID, INDEX_ID)
    
    if sync_status['success']:
        print(f"📊 Estado de sincronización: {sync_status.get('status', 'UNKNOWN')}")
        if sync_status.get('metrics'):
            metrics = sync_status['metrics']
            print(f"📄 Documentos procesados:")
            print(f"   - Agregados: {metrics.get('documentsAdded', 0)}")
            print(f"   - Modificados: {metrics.get('documentsModified', 0)}")
            print(f"   - Eliminados: {metrics.get('documentsDeleted', 0)}")
            print(f"   - Fallidos: {metrics.get('documentsFailed', 0)}")
            print(f"   - Escaneados: {metrics.get('documentsScanned', 0)}")
    else:
        print(f"❌ Error verificando sincronización: {sync_status['error']}")
    
    print("\n" + "="*50)
    
    # Si la sincronización no está completa, informar al usuario
    if sync_status.get('status') in ['SYNCING', 'PENDING']:
        print("⏳ La sincronización aún está en progreso.")
        print("💡 Las consultas pueden no tener acceso a todos los documentos aún.")
        print("🔄 Recomendación: Esperar a que la sincronización complete.")
        
        # Preguntar si continuar
        continue_test = input("\n¿Deseas continuar con las pruebas de consulta? (y/n): ")
        if continue_test.lower() != 'y':
            print("👋 Saliendo. Ejecuta nuevamente cuando la sincronización complete.")
            return
    
    print("\n🔍 Ejecutando consultas de prueba...")
    
    # Preguntas de prueba específicas para WAF SPD
    test_questions = [
        "¿Cuáles son los requisitos principales para AWS WAF Service Delivery Program según el checklist de febrero 2025?",
        "Explica los requisitos WAF-001, WAF-002 y WAF-003 del programa WAF SPD",
        "¿Qué documentación necesito para los case studies en WAF Service Delivery Program?",
        "¿Cuáles son los criterios para Services Path Membership en WAF SPD?",
        "¿Cómo debo preparar mi aplicación para la certificación WAF Service Delivery Program?"
    ]
    
    successful_queries = 0
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📋 Pregunta {i}: {question}")
        print("-" * 70)
        
        response = integration.query_waf_spd_guidance(question)
        
        if response['success']:
            print("✅ Respuesta exitosa")
            print(f"📝 Respuesta: {response['response'][:400]}...")
            if response['sources']:
                print(f"📚 Fuentes: {len(response['sources'])} documentos referenciados")
                for j, source in enumerate(response['sources'][:2], 1):  # Mostrar primeras 2 fuentes
                    if 'title' in source:
                        print(f"   {j}. {source.get('title', 'Sin título')}")
            successful_queries += 1
        else:
            print("❌ Error en consulta")
            print(f"🚨 Error: {response['error']}")
        
        # Pausa entre consultas para evitar rate limiting
        if i < len(test_questions):
            time.sleep(3)
    
    print(f"\n📊 Resumen: {successful_queries}/{len(test_questions)} consultas exitosas")
    
    # Si al menos una consulta fue exitosa, hacer una consulta específica de evaluación
    if successful_queries > 0:
        print("\n🎯 CONSULTA ESPECÍFICA DE EVALUACIÓN WAF SPD")
        print("=" * 50)
        
        evaluation_question = """
        Basándote en la documentación de AWS WAF Service Delivery Program, analiza esta situación:
        
        - Puntuación actual de evaluación: 63.6/100
        - Gap crítico: PROG-002 Services Path Membership (actualmente en Select, necesito Validated/Differentiated)
        - Tengo 2 case studies documentados con arquitecturas
        - WAF expertise parcialmente completo (falta DDoS mitigation strategy)
        - Documentación de arquitectura completa
        
        ¿Cuál es mi plan de acción prioritario paso a paso para obtener la certificación WAF SPD?
        ¿Cuánto tiempo estimado necesitaría para estar listo?
        """
        
        response = integration.query_waf_spd_guidance(evaluation_question)
        
        if response['success']:
            print("✅ Análisis de evaluación completado")
            print(f"📊 Recomendaciones detalladas:")
            print(f"{response['response']}")
            
            # Guardar respuesta completa
            report = {
                "timestamp": datetime.now().isoformat(),
                "application_id": APPLICATION_ID,
                "sync_status": sync_status,
                "evaluation_question": evaluation_question,
                "response": response['response'],
                "sources": response['sources'],
                "successful_queries": successful_queries,
                "total_queries": len(test_questions)
            }
            
            filename = f"waf_spd_q_analysis_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            print(f"\n💾 Análisis completo guardado en: {filename}")
            
        else:
            print("❌ Error en análisis específico")
            print(f"🚨 Error: {response['error']}")
    
    print("\n🎉 Prueba de integración completada!")
    print("\n💡 Próximos pasos recomendados:")
    print("1. ✅ Verificar que la sincronización del data source esté completa")
    print("2. 🔄 Re-ejecutar este script cuando todos los documentos estén indexados")
    print("3. 📋 Usar las respuestas para crear tu plan de acción WAF SPD")
    print("4. 🎯 Hacer consultas más específicas según tus gaps identificados")
    print("5. 📊 Integrar las recomendaciones con tu evaluación local")
    
    if successful_queries == 0:
        print("\n🚨 TROUBLESHOOTING:")
        print("- Verificar que el data source esté sincronizado completamente")
        print("- Confirmar que los documentos se subieron correctamente al bucket S3")
        print("- Verificar permisos del rol IAM para Amazon Q Business")
        print("- Contactar soporte si el problema persiste")

if __name__ == "__main__":
    main()

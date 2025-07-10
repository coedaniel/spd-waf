# 🚀 Guía de Configuración Amazon Q Business para WAF SPD

## 📋 Requisitos Previos

### AWS Account Setup
- ✅ Cuenta AWS con permisos administrativos
- ✅ Región recomendada: **us-east-1** (Virginia)
- ✅ IAM Identity Center configurado (recomendado)

### Costos Estimados
- **Amazon Q Business**: $20/usuario/mes
- **S3 Storage**: ~$5/mes para documentos
- **Total mensual**: ~$25-30

---

## 🔧 Paso 1: Crear Amazon Q Business Application

### 1.1 Acceso a la Consola
```bash
# URL directa
https://console.aws.amazon.com/amazonq/business/
```

### 1.2 Configuración Inicial
- **Application name**: `WAF-SPD-Evaluator`
- **Description**: `Evaluador interno para AWS WAF Service Delivery Program`
- **Access management**: `IAM Identity Center` (recomendado)

### 1.3 Configuración de Usuarios
- Crear grupo: `WAF-SPD-Team`
- Asignar usuarios del equipo técnico
- Permisos: `Admin` para configuración inicial

---

## 📁 Paso 2: Configurar Data Sources

### 2.1 S3 Bucket para Documentos
```bash
# Crear bucket para documentos
aws s3 mb s3://waf-spd-documents-[tu-empresa]

# Subir documentos del proyecto
aws s3 sync ./docs/ s3://waf-spd-documents-[tu-empresa]/docs/
aws s3 sync ./templates/ s3://waf-spd-documents-[tu-empresa]/templates/
```

### 2.2 Configurar S3 Data Source
- **Data source name**: `WAF-SPD-Documents`
- **S3 bucket**: `s3://waf-spd-documents-[tu-empresa]`
- **Sync schedule**: `Daily at 2:00 AM`
- **Include patterns**: `*.md, *.csv, *.txt`

### 2.3 Web Crawler para AWS Docs
- **Data source name**: `AWS-WAF-Documentation`
- **Start URLs**:
  ```
  https://docs.aws.amazon.com/waf/
  https://docs.aws.amazon.com/waf/latest/developerguide/
  https://aws.amazon.com/waf/features/
  ```
- **Crawl depth**: `3 levels`
- **Sync schedule**: `Weekly`

---

## 🤖 Paso 3: Configurar Custom Prompt

### 3.1 Acceder a Customizations
- Amazon Q Business Console → `Applications` → `WAF-SPD-Evaluator`
- Ir a `Customizations` → `Prompts`

### 3.2 Crear System Prompt
- **Prompt name**: `WAF-SPD-Evaluator-System`
- **Prompt type**: `System`
- **Content**: Copiar desde `/prompts/amazon-q-system-prompt.txt`

### 3.3 Configurar Response Templates
```json
{
  "evaluation_template": {
    "structure": "🛡️ EVALUACIÓN WAF SPD",
    "sections": [
      "📊 PUNTUACIÓN TOTAL",
      "✅ REQUISITOS CUMPLIDOS", 
      "❌ REQUISITOS PENDIENTES",
      "📋 PLAN DE ACCIÓN",
      "💰 INVERSIÓN ESTIMADA",
      "🎯 RECOMENDACIÓN FINAL"
    ]
  }
}
```

---

## 📊 Paso 4: Subir Datos de Evaluación

### 4.1 Preparar Plantillas Excel
```bash
# Convertir CSV a formato compatible
cd templates/
# Editar waf-evaluation-template.csv con tus datos reales
```

### 4.2 Estructura de Datos Requerida
```
CERTIFICACIONES:
- Empleado, Certificación, Fecha, Estado

EXPERIENCIA_TECNICA:
- Servicio, Nivel, Proyectos, Años

CASOS_EXITO:
- Proyecto, Cliente, Servicios, Valor, Referencias

COMPETENCIAS:
- Competencia, Estado, Fecha Renovación

PERSONAL:
- Nombre, Rol, Certificaciones, Disponibilidad
```

### 4.3 Upload a S3
```bash
# Subir datos actualizados
aws s3 cp waf-evaluation-template.csv s3://waf-spd-documents-[tu-empresa]/data/
```

---

## 🔍 Paso 5: Testing y Validación

### 5.1 Preguntas de Prueba
```
1. "Evalúa mi elegibilidad para WAF SPD"
2. "¿Qué certificaciones me faltan?"
3. "Genera un plan de acción para los próximos 90 días"
4. "¿Cuál es mi puntuación actual?"
5. "¿Qué casos de éxito necesito desarrollar?"
```

### 5.2 Validar Respuestas
- ✅ Formato correcto con emojis y estructura
- ✅ Puntuación calculada correctamente
- ✅ Gaps identificados específicamente
- ✅ Plan de acción priorizado
- ✅ Costos realistas

---

## ⚙️ Paso 6: Configuración Avanzada

### 6.1 Integrations
- **Slack**: Para notificaciones de evaluación
- **Teams**: Para colaboración del equipo
- **Email**: Para reportes automáticos

### 6.2 Monitoring
- **CloudWatch**: Métricas de uso
- **CloudTrail**: Auditoría de accesos
- **Cost Explorer**: Control de costos

### 6.3 Security
- **Encryption**: Datos en reposo y tránsito
- **Access Control**: Principio de menor privilegio
- **Audit Logs**: Registro de todas las consultas

---

## 📋 Paso 7: Uso Operacional

### 7.1 Workflow Recomendado
1. **Actualizar datos** → Subir Excel actualizado a S3
2. **Ejecutar evaluación** → Hacer pregunta específica
3. **Revisar resultados** → Analizar gaps y recomendaciones
4. **Seguir plan** → Implementar acciones prioritarias
5. **Re-evaluar** → Repetir proceso mensualmente

### 7.2 Preguntas Frecuentes
```
EVALUACIÓN GENERAL:
- "¿Estoy listo para WAF SPD?"
- "¿Cuál es mi puntuación actual?"

GAPS ESPECÍFICOS:
- "¿Qué certificaciones me faltan?"
- "¿Qué experiencia técnica necesito desarrollar?"

PLANIFICACIÓN:
- "¿Cuánto tiempo necesito para estar listo?"
- "¿Cuál es la inversión total estimada?"

CASOS DE ÉXITO:
- "¿Qué tipos de casos necesito?"
- "¿Cómo documento mejor mis proyectos?"
```

---

## 🚨 Troubleshooting

### Problemas Comunes

**Error: "No data found"**
- ✅ Verificar que S3 sync completó
- ✅ Revisar permisos de bucket
- ✅ Confirmar formato de datos

**Respuestas incompletas**
- ✅ Verificar system prompt configurado
- ✅ Revisar límites de tokens
- ✅ Actualizar data sources

**Puntuación incorrecta**
- ✅ Validar datos de entrada
- ✅ Revisar criterios en prompt
- ✅ Verificar cálculos manualmente

---

## 📞 Soporte y Recursos

### AWS Support
- [Amazon Q Business Documentation](https://docs.aws.amazon.com/amazonq/latest/business-use-dg/)
- [WAF Service Delivery Program](https://aws.amazon.com/partners/programs/service-delivery/)

### Contactos Internos
- **Technical Lead**: [Tu nombre]
- **AWS Account Manager**: [Contacto AWS]
- **Partner Development**: [Contacto Partner]

---

**Versión**: 1.0  
**Última actualización**: Julio 2025  
**Próxima revisión**: Agosto 2025

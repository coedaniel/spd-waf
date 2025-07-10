# 🔍 Preguntas Técnicas para Evaluación WAF SPD

## 📋 Cuestionario de Evaluación Técnica

### 🛡️ AWS WAF v2 vs Classic

**Pregunta 1:** ¿Cuáles son las principales diferencias arquitecturales entre AWS WAF Classic y WAF v2?

**Respuesta Esperada:**
- WAF v2 usa Web ACLs con reglas más flexibles
- Mejor integración con CloudFormation
- Pricing por Web ACL, no por regla
- Soporte para JSON body inspection
- Mejor performance y escalabilidad

**Puntuación:** 0-10 puntos

---

### ⚡ Rate Limiting y API Protection

**Pregunta 2:** ¿Cómo configurarías rate limiting para proteger una API crítica que maneja 1000 requests/minuto normalmente?

**Respuesta Esperada:**
- Rate-based rule con threshold apropiado
- Configuración de time window (5 minutos)
- Action: Block o Count para testing
- Integración con CloudWatch para monitoreo
- Consideraciones de IP whitelisting

**Puntuación:** 0-10 puntos

---

### 🛡️ Shield Advanced Integration

**Pregunta 3:** ¿Cuándo recomendarías Shield Advanced y cómo se integra con WAF?

**Respuesta Esperada:**
- Para aplicaciones críticas con riesgo DDoS
- Protección L3/L4 + L7 con WAF
- DDoS Response Team 24/7
- Cost protection para scaling
- Advanced attack diagnostics

**Puntuación:** 0-10 puntos

---

### 📊 Managed vs Custom Rule Groups

**Pregunta 4:** ¿Cuándo usarías Managed Rule Groups vs Custom Rules? Da ejemplos específicos.

**Respuesta Esperada:**
- Managed: Core Rule Set, Known Bad Inputs para protección básica
- Custom: Reglas específicas del negocio, patrones únicos
- Combinación para defensa en profundidad
- Ejemplos: SQL injection (managed) + business logic (custom)

**Puntuación:** 0-10 puntos

---

### 🔧 Firewall Manager Multi-Account

**Pregunta 5:** ¿Cómo configurarías Firewall Manager para gestionar WAF en múltiples cuentas AWS?

**Respuesta Esperada:**
- AWS Organizations setup
- Security policies centralizadas
- Compliance monitoring
- Automatic remediation
- Cross-account role configuration

**Puntuación:** 0-10 puntos

---

### 🌐 CloudFront + WAF Integration

**Pregunta 6:** ¿Qué consideraciones especiales tienes para WAF con CloudFront global?

**Respuesta Esperada:**
- Edge locations y latencia
- Geographic restrictions
- Cache behavior impact
- Real IP forwarding
- Regional vs Global Web ACLs

**Puntuación:** 0-10 puntos

---

### 🔍 Custom Rules y Regex Patterns

**Pregunta 7:** ¿Cómo crearías una regla custom para bloquear patrones específicos en URLs?

**Respuesta Esperada:**
- Regex pattern sets
- URI path matching
- Query string inspection
- Body content analysis
- Performance considerations

**Puntuación:** 0-10 puntos

---

### 📈 Monitoring y Alerting

**Pregunta 8:** ¿Qué métricas de CloudWatch monitorizarías para WAF y cómo configurarías alertas?

**Respuesta Esperada:**
- AllowedRequests, BlockedRequests
- SampledRequests para análisis
- CloudWatch Alarms para anomalías
- Integration con SNS/Lambda
- Dashboard personalizado

**Puntuación:** 0-10 puntos

---

### 🔄 Migration Strategy

**Pregunta 9:** ¿Cuál sería tu estrategia para migrar de WAF Classic a WAF v2 sin downtime?

**Respuesta Esperada:**
- Parallel deployment
- Traffic splitting/testing
- Rule mapping y validation
- Rollback plan
- Monitoring durante migración

**Puntuación:** 0-10 puntos

---

### 🏗️ Architecture Best Practices

**Pregunta 10:** ¿Cómo diseñarías una arquitectura WAF para una aplicación multi-tier con frontend, APIs y microservicios?

**Respuesta Esperada:**
- CloudFront + WAF para frontend
- ALB + WAF para APIs
- API Gateway + WAF para microservicios
- Centralized logging
- Layered security approach

**Puntuación:** 0-10 puntos

---

## 📊 Sistema de Puntuación

### Niveles de Competencia:
- **90-100 puntos:** Experto - Listo para casos complejos
- **75-89 puntos:** Avanzado - Apto para WAF SPD
- **60-74 puntos:** Intermedio - Necesita más experiencia
- **< 60 puntos:** Básico - Requiere training intensivo

### Criterios de Evaluación:
- **Precisión técnica** (40%)
- **Experiencia práctica** (30%)
- **Best practices** (20%)
- **Troubleshooting** (10%)

---

## 🎯 Preguntas de Casos de Éxito

### Caso 1: E-commerce Protection
"Describe un caso donde implementaste WAF para proteger una tienda online. ¿Qué reglas usaste y qué resultados obtuviste?"

### Caso 2: API Security
"¿Cómo protegiste APIs críticas con rate limiting? ¿Qué desafíos enfrentaste?"

### Caso 3: DDoS Mitigation
"Cuenta sobre una implementación de Shield Advanced. ¿Cómo se integró con WAF?"

### Caso 4: Migration Project
"Describe una migración de WAF Classic a v2. ¿Qué estrategia seguiste?"

### Caso 5: Multi-Region Deployment
"¿Has implementado WAF en múltiples regiones? ¿Cómo gestionaste la consistencia?"

---

## 📝 Template de Respuesta para Casos

```
CASO: [Nombre del proyecto]
CLIENTE: [Industria/Sector]
DESAFÍO: [Problema específico]
SOLUCIÓN: [Implementación técnica]
SERVICIOS: [WAF, Shield, CloudFront, etc.]
RESULTADOS: [Métricas de éxito]
APRENDIZAJES: [Lecciones aprendidas]
REFERENCIA: [Contacto verificable]
```

---

**Nota:** Estas preguntas deben ser respondidas por el equipo técnico durante la evaluación. Las respuestas servirán para validar la experiencia real y identificar gaps de conocimiento.

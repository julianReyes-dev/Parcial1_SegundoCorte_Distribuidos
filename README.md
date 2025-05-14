# Parcial segundo corte distri

## Arquitectura

### 1. Número de réplicas de workers
Hemos configurado 3 réplicas de workers para:
- Manejar picos de carga: Cuando llegan muchas imágenes simultáneamente
- Tolerancia a fallos: Si un worker falla, los otros pueden continuar procesando
- Balance de carga: RabbitMQ distribuye los mensajes entre los workers disponibles

El número 3 es un buen punto de partida que puede ajustarse según métricas de carga.

### 2. Configuración de RabbitMQ

**Work Queues:**
- Cola durable (`image_processing`) para sobrevivir a reinicios
- Prefetch count = 1 para distribución equitativa
- ACK manual para evitar pérdida de mensajes

**Publish/Subscribe:**
- Exchange tipo FANOUT (`processed_images`) para broadcast
- Bindings automáticos para fácil escalamiento de consumidores
- Mensajes persistentes para garantizar entrega

### 3. Manejo de errores y reintentos

Estrategia implementada:
- ACK manual solo después de procesamiento exitoso
- Mensajes persistentes para sobrevivir a reinicios
- Reintentos implícitos mediante cola (mensaje no ACK vuelve a la cola)
- Registro de errores para diagnóstico
- Estado explícito en la API ("failed" con motivo)

### 4. Persistencia

**Opciones elegidas:**
- RabbitMQ: Discos para colas (consistencia > performance)
- API: Sistema de archivos para imágenes originales
- Workers: Sistema de archivos para imágenes procesadas

**Justificación:**
- Las imágenes son datos críticos que no deben perderse
- El acceso a disco es aceptable dada la naturaleza asíncrona
- En producción, considerar almacenamiento distribuido (S3)

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

##USO
### 1. Clonar el Repositorio

Para obtener el código fuente del proyecto, ejecute los siguientes comandos en la terminal:

```bash
git clone https://github.com/julianReyes-dev/Parcial1_SegundoCorte_Distribuidos.git
```
```bash
cd Parcial1_SegundoCorte_Distribuidos
```

### 2. Correr el proyecto

```bash
docker-compose up -d --build
```
Esto creará:

- 1 contenedor para RabbitMQ (con la interfaz de gestión en http://localhost:15672)
- 1 contenedor para la API (en http://localhost:8000)
- 3 réplicas de workers
- 1 contenedor para el servicio de notificaciones

### 3. Probar la funcionalidad

Subir una imagen
```bash
curl -X POST -F "file=@image.jpg" http://localhost:8000/upload
```
Verificar el estado (use el id devuelto)
```bash
curl http://localhost:8000/status/id
```

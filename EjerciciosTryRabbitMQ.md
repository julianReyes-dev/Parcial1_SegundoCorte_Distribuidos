# RabbitMQ - Sistema de Noticias por Categoría (Topic Exchange)

Este proyecto demuestra el uso de RabbitMQ con un exchange de tipo **topic** para filtrar y distribuir noticias según su categoría.

## Configuración

### Exchange
- **Nombre:** `news.topic`
- **Tipo:** `topic` (permite enrutamiento basado en patrones)

### Colas y Bindings
| Nombre Cola      | Binding Key  | Descripción                     |
|------------------|-------------|---------------------------------|
| `sports_queue`   | `sports.*`  | Recibe todas las noticias deportivas |
| `ai_queue`       | `*.ai`      | Recibe noticias sobre inteligencia artificial |

## Mensajes de Prueba Enviados

Se enviaron 3 mensajes con diferentes routing keys:

1. 🏈 `sports.football`: "El Barcelona ganó 3-0 last night"
2. 🤖 `tech.ai`: "Nuevos avances en inteligencia artificial"
3. � `sports.basketball`: "Los Lakers pierden en overtime"

## Resultados Esperados

| Routing Key        | Cola Destino     | Razón                         |
|-------------------|-----------------|-------------------------------|
| `sports.football` | `sports_queue`  | Coincide con patrón `sports.*` |
| `tech.ai`         | `ai_queue`      | Coincide con patrón `*.ai`     |
| `sports.basketball` | `sports_queue` | Coincide con patrón `sports.*` |
| `business.ai`     | `ai_queue`      | Coincide con patrón `*.ai`     |

## Capturas de Pantalla

1. **Configuración Inicial**  
   ![image](https://github.com/user-attachments/assets/0a2c8567-1eda-4ac3-b614-049c4eba8b90)


2. **Envío de Mensajes**  
   ![image](https://github.com/user-attachments/assets/712b3814-ef8f-40f7-9884-8c915dbc7f41)


3. **Mensajes Recibidos**  
   ![image](https://github.com/user-attachments/assets/61099eeb-ada4-4a23-b54e-b5113822aaab)
   ![image](https://github.com/user-attachments/assets/178a93e0-5ab8-48a2-8138-4d825b548303)

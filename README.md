# ayuda-dana
Aplicación web sencilla para localizar peticiones de ayuda en el mapa. Basado en [ayudaterreta.com](https://ayudaterreta.com).

> [!WARNING]
> El código que se encuentra en este repositorio está bajo construcción. Por favor, para cualquier duda o si quieres colaborar contacta conmigo en <hello@mianfg.me>

## Propósito y motivación

Este código lo he creado viendo que la web [ayudaterra.com](https://ayudaterra.com) llevaba bastante tiempo caída por estar desarrollada en WordPress, no pudiendo soportar el tráfico de gente. He hecho esto en un par de horas para crear una app web con una arquitectura más escalable. La intención es:

## Tareas

### Programación

- [x] Crear un backend FastAPI que gestione las peticiones y la autenticación con iniciar sesión con Google y almacenar la información en MongoDB.
- [ ] Crear un frontend sencillo con Vue.js y OpenLayers.

### Infraestructura

- [ ] Despliegue de FastAPI en AWS Lambda mediante Mangum.
- [ ] Despliegue del frontend.
- [ ] Caché Redis (en caso de muchas peticiones).

### Machine learning

- [ ] Crear un panel donde aparezcan en tiempo real las diversas necesidades (es capaz de saber cuántas personas están pidiendo cada cosa)
- [ ] Agrupamientos de peticiones y otras optimizaciones para facilitar la búsqueda

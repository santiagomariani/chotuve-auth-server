# Chotuve - Auth Server

![Grupo](https://img.shields.io/badge/grupo-11-blue) [![Build Status](https://travis-ci.com/santiagomariani/chotuve-auth-server.svg?token=JK2YBuuGjqNcqiY3N6nH&branch=master)](https://travis-ci.com/github/santiagomariani/chotuve-auth-server)
![api](https://img.shields.io/badge/api-v0.1-blueviolet)
[![sv](https://img.shields.io/badge/view-app%20sv-important)](https://github.com/Franco-Giordano/chotuve-appserver)
[![sv](https://img.shields.io/badge/view-media%20sv-important)](https://github.com/sebalogue/chotuve-mediaserver)
[![sv](https://img.shields.io/badge/view-web%20front-important)](https://github.com/santiagomariani/chotuve-web-front)
[![sv](https://img.shields.io/badge/view-auth%20sv-important)](https://github.com/santiagomariani/chotuve-auth-server)
[![sv](https://img.shields.io/badge/view-android-important)](https://github.com/javier2409/Chotuve-Android)

# Instrucciones

## Desarrollo local

1. Instalar [Docker Engine](https://docs.docker.com/engine/install/) y [Docker Compose](https://docs.docker.com/compose/install/)

2. Asegurarse de tener el archivo 'chotuve-videos-firebase-adminsdk.json' en la raiz con las credenciales de firebase. Despues seguro tengamos una cuenta de firebase para desarrollo y otra para produccion, hay que ver esto bien.

3. Levantar server + database
```docker-compose up```

3. Probar la REST API en `0.0.0.0:4000`

## API

Todos los endpoints en negrita deben recibir el token id (otorgado por firebase) en el header x-access-token.

- **Sign-up (registro):**
`POST 0.0.0.0:4000/sign-up` con body:
```json
{
	
	"email": "juanperez@gmail.com",
	"display_name":"Juan Perez",
	"phone_number": "+5492267452235",
	"image_location":"https://image.freepik.com/foto-gratis/playa-tropical_74190-188.jpg"
	
}
```

- **Sign in:**
`POST 0.0.0.0:4000/sign-in` solo enviar token.

- **Obtener datos de un usuario:**
`GET 0.0.0.0:4000/users/<id>`

- **Modificar datos de un usuario:**
`PUT 0.0.0.0:4000/users/<id>` con body (pueden enviarse solo los datos que cambian):
```json
{
	
	"email": "juanperez@gmail.com",
	"display_name":"Matias Perez",
	"phone_number": "+5492264511422",
	"image_location":"https://image.freepik.com/foto-gratis/playa-tropical_74190-188.jpg"
	
}
```

- Crear reset code para generar una nueva contraseña:
`POST 0.0.0.0:4000/reset-codes` con body:
```json
{
	
    "email": "juanperez@gmail.com"
    
}


```

- Cambiar contraseña usando el reset code (el email es el mismo que con /reset-codes):
`POST 0.0.0.0:4000/change-password-with-reset-code` con body:
```json
{
	
	"email": "juanperez@gmail.com",
	"reset_code":"KnPlDQ",
	"password": "Unacontraseña123"
	
}
```

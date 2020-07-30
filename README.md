# Chotuve - Auth Server

![Grupo](https://img.shields.io/badge/grupo-11-blue) [![Build Status](https://travis-ci.com/santiagomariani/chotuve-auth-server.svg?token=JK2YBuuGjqNcqiY3N6nH&branch=master)](https://travis-ci.com/github/santiagomariani/chotuve-auth-server)
![api](https://img.shields.io/badge/api-v0.1-blueviolet)
[![Coverage Status](https://coveralls.io/repos/github/santiagomariani/chotuve-auth-server/badge.svg?branch=development&t=MBcBZ7)](https://coveralls.io/github/santiagomariani/chotuve-auth-server?branch=development)
[![sv](https://img.shields.io/badge/view-app%20sv-important)](https://github.com/Franco-Giordano/chotuve-appserver)
[![sv](https://img.shields.io/badge/view-media%20sv-important)](https://github.com/sebalogue/chotuve-mediaserver)
[![sv](https://img.shields.io/badge/view-web%20front-important)](https://github.com/santiagomariani/chotuve-web-front)
[![sv](https://img.shields.io/badge/view-auth%20sv-important)](https://github.com/santiagomariani/chotuve-auth-server)
[![sv](https://img.shields.io/badge/view-android-important)](https://github.com/javier2409/Chotuve-Android)

# Instrucciones

## Desarrollo local

1. Instalar [Docker Engine](https://docs.docker.com/engine/install/) y [Docker Compose](https://docs.docker.com/compose/install/)

2. Asegurarse de tener el archivo 'chotuve-videos-firebase-adminsdk.json' en la raiz con las credenciales de firebase.

3. Levantar server + database con  ```docker-compose up``` o con ```make up```.

3. Probar la REST API en `0.0.0.0:4000`

## API 1.0.0

[Especificacion Open Api 2.0](https://app.swaggerhub.com/apis-docs/chotuvevideos/api-auth_server/1.0.0#/)
[Open Api - archivo ymaml](https://github.com/santiagomariani/chotuve-auth-server/blob/master/OPENAPI.yaml)

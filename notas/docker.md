# Curso de Docker - Platzi

#Conceptos

### ¿Qué es un contenedor?

- Es como una máquina virtual pero libiana
- Es una agrupación de procesos que corren nativamente en la máquina, pero están aislados del resto del sistema.
- Un contenedor es una unidad lógica y por eso puede correr de manera nativa en la máquina. 
- Tiene limitaciones

## Comandos
- con `docker run`se corre un nuevo contenedor. Crea un contendor y lo ejecuta.
- Se utiliza el comado `docker inspect [container id]`. Tambien se puede utilizar el `name` en lugar del docker id.
- Con `docker rm [nombre o id del docker]` de borran los contendores.
- Para borrar todolos contenedores que estan parados se utiliza `docker container prune`
- Este comando sirve para entrar al modo interactivi de un docker de ubunto y poder entrar a la shell de ese SO.

```bash
docker run -it ubuntu
```

### Ciclo de vida de un contenedor
- Mientras el proceso principal del contenedor esta corriente, el docker estará corriendo, de lo contrario, no. 
- El proceso tambien se puede matar desde fuera del contender.

```bas
docker kill <ID o nombre del contenedor>
```

### Exponer o usar un contenedor desde afuera

- Comando para ejecutar el docker del proxy
```bash
docker run -d --name proxy nginx
```

```bash 
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS     NAMES
7461da1f5718   nginx     "/docker-entrypoint.…"   3 minutes ago   Up 3 minutes   80/tcp    proxy
```
- En este caso el docker se supone que esta escuchando en el pkuerto 80, pero no de mi maquina sino del docker. 
- Para poder hacerlo al comando que crea el docker le tendo que hacer algunos cambios. Se le agrega -p 8080:80 El primer puesto es el de la maquina anfitiriona y el segun, que esta despues de `:` qué puerto del contender se quiere exponer en ese puerto.


```bash
docker run -d --name proxy -p 8080:80 nginx
```

### Manejo de datos con docker

- Ejecutamos este comando que crea un cotender de mongo.

```bash
docker run -d --name db mongo
```
- Para poder ingresar a la base de datos
```bash
docker exec -it db bash
```
-  Pero para montar el docker de la base de datos y que al morir este docker no muera la bd, es necesario montarlo en un directorio específico

```bash
docker run -d --name db -v /home/mongar/Escritorio/curso_docker/docker_data/mongodata:/data/db mongo
```
- Antes de los `:` es la ruta en la maquina anfitriona, y depsues `:` es la ruta dentro del contenedor
- Si dentro del bash de ese docker, utiliozando mongo, creo una base de datos y luego mato ese docker, la informacion ahora uqedará en esa carpeta que se indicó al inicio del comando. Ya solo restaria volver a ejectar el mismo comando para crear el docker en ese mismo directorio, y mongo reconocerá la informacion de la carpta y montará de misma base d edatos con la informacion del directorio. A este proceso se le llama `bind mounts`. 


### Volumes o Volumenes

- Es otra manera distinta de manejar datos que ofrece docker. 
- Para crear un volumen se ejecura:
```bash
docker volume create [nombre del volume]
```

- El paso a seguir es crear un nuevo docker y se le va a montar ese volumen en el directorio donde la base de datos escribe sus datos
```bash
docker run -d --name db --mount src=dbdata,dst=/data/ mongo
```
- en src o source se pone el nombre de volumen, puede este existir o no, in dst o destino, el destino, que para este caso es donde se sabe que mongo guarda sus datos.




# **Sheet cheat docker**

## ***Instalacion***
```bash
sudo apt-get update
sudo apt-get install docker.io

sudo usermod -aG docker <user>
```
> Si el daemon no se configura solo:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```
> Si systemctl falla:
```bash
sudo service docker start
```
## ***Comandos***
> Si añades docker al grupo del sudo no hace falta poner sudo siempre
  ### ***Contenedores***
  * Ver contenedores en uso: `sudo docker ps`
  > Para eliminar contenedores tienes que detenerlos primero:
  * Detener un contenedor `sudo docker stop <container_id>`
  * Eliminar contenedores por nombre o id: `sudo docker rm <id or name>`:   Puedes poner solo un numero y eliminará el id que empiece por dicho numero, si hay mas de 1 fallará.
  * Eliminar contenedores sin usar: `sudo docker container prune`
  ### ***Imagenes***
  * Ver imagenes: `sudo docker images`
  * Eliminar imagenes por nombre o id: `sudo docker rmi <image_name_or_id>` 
  * Eliminar todas las imagenes untagged: `sudo docker image prune --filter "dangling=true"`
  ### ***Build an run an image***
  > Para dockerizar la app hace falta que exista el Pipfile.lock
  * Build: `sudo docker build -t <image_name> <work directory where Docker file it's>` 
  * Ejecutar en segundo plano exponiendo el puerto 3000: `sudo docker run -d -p 3000:3000 <image_name>`
  * Entrar a la imagen: `sudo docker exec -it <container-id> /bin/bash`
  * Comprobar que funciona en el contenedor: `curl http://localhost:3000`
  * Cuidado con los host en los host ya que si definimos: `app.run(host='127.0.0.1', port=3000, debug=True)` no podremos acceder a la app dentro del contenedor ya que solo se permite desde el local host por lo que tenemos que tenemos: `app.run(host='0.0.0.0', port=3000, debug=True)`

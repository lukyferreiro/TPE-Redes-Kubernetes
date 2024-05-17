# TPE-Redes-Kubernetes

## Autores - Grupo 13

- [Tomas Alvarez Escalante](https://github.com/tomalvarezz)
- [Alejo Caeiro](https://github.com/AleCaeiro)
- [Lucas Agustin Ferreiro](https://github.com/lukyferreiro)
- [Roman Gomez Kiss](https://github.com/rgomezkiss)

## Consigna

- Crear un cluster de Kubernetes de un Master y al menos dos slave, que exponga
una API en un puerto genérico (distinto a 80)
- Implementar una base de datos local en un servidor (por fuera del cluster) y
exponer un servicio que redireccione el tráfico del cluster al servidor.
- Deployar un web server (nginx o Apache HTTPD escuchando en el 80) y hacer
un proxy reverso a la API.
- Mostrar dos versiones de API distintas conviviendo.
- Integrar los servicios de Istio y Kiali al cluster

# Instalación

## Entorno utilizado

...

## Intalación de Docker

A continuación se presentan los comandos para instalar [Docker en Ubuntu](https://docs.docker.com/engine/install/ubuntu/) (para la [instalación en otros SO's](https://docs.docker.com/engine/install/))

Antes de instalar Docker desde 0, nos aseguraremos de que el entorno no cuente con versiones/paquetes que entren en conflicto.

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

Para comenzar la instalacion primero se agrega la clave GPG oficial de Docker y se agregue el repositorio a las fuentes de Apt:

```bash
sudo apt-get update
```

```bash
sudo apt-get install ca-certificates curl gnupg
```

```bash
sudo install -m 0755 -d /etc/apt/keyrings
```

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

```bash
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

```bash
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Luego se instalan los paquetes de Docker y se verifica la correcta instalación:

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

```bash
sudo docker run --rm hello-world
```

### Crear usuario y grupo de Docker

Los comandos de esta sección tiene como objetivo evitar ejecutar los contedores como root

```bash
sudo groupadd docker
```

```bash
sudo usermod -aG docker ${USER}
```

Para aplicar los cambios se debe reiniciar la sesión del usuario. Adicionalmente, podemos verificar nuevamente ejecutando la siguiente imagen (y luego borrarla)

```bash
docker run --rm hello-world
```

```bash
docker rmi hello-world
```

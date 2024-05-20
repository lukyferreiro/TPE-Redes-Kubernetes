# TPE-Redes-Kubernetes

Kubernetes es una plataforma de orquestación de contenedores de código abierto que automatiza la implementación, el escalado y la operación de aplicaciones en contenedores

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

## Entorno

Descripcion del entorno a usar...

## Instalaciones previas

### Docker

Docker es una plataforma de software que permite crear, ejecutar y gestionar contenedores, que son entornos ligeros y portátiles para ejecutar aplicaciones. Los contenedores encapsulan todo lo necesario para que una aplicación se ejecute, incluyendo el código, las bibliotecas y las dependencias, garantizando que funcionen de manera consistente en cualquier entorno. Docker facilita el desarrollo, la implementación y la escalabilidad de aplicaciones, mejorando la eficiencia y la flexibilidad del desarrollo de software.

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

#### Crear usuario y grupo de Docker

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

### Kubectl

Kubectl es una herramienta de línea de comandos utilizada para interactuar y gestionar clusters de Kubernetes. Permite a los usuarios desplegar aplicaciones, inspeccionar y administrar recursos del cluster, y realizar tareas de mantenimiento y depuración.

A continuación se presentan los comandos para descargar e instalar [Kubectl en Ubuntu](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) (para la [instalación en otros SO's](https://kubernetes.io/docs/tasks/tools/#kubectl))

- Para AMD64 / x86_64:

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```

- Para ARM64:

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl" 
```

Una vez descargado, se debe instalar:

```bash
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

Se verifica la correcta instalación:

```bash
kubectl version --client
```

### Kind (Kubernetes IN Docker)

Kind es una herramienta diseñada para ejecutar clusters de Kubernetes locales utilizando contenedores Docker como nodos. Es ideal para pruebas, desarrollo y aprendizaje de Kubernetes sin necesidad de configurar una infraestructura compleja. Kind permite crear y administrar clusters de Kubernetes en cuestión de minutos, facilitando la experimentación y el desarrollo de aplicaciones en un entorno controlado y reproducible. Tambien permite especificar la cantidad de nodos worker y de nodos del control plane del clúster sin necesidad de infraestructura compleja ni recursos adicionales.

AA continuación se presentan los comandos para descargar e instalar [Kind en Linux (u otros SO's)](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)

Primero, deberá descargarse el ejecutable compatible:

- Para AMD64 / x86_64:

```bash
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.19.0/kind-linux-amd64
```

- Para ARM64:

```bash
[ $(uname -m) = aarch64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.19.0/kind-linux-arm64
```

Una vez descargado, se deberá ejecutar:

```bash
chmod +x ./kind
```

```bash
sudo mv ./kind /usr/local/bin/kind
```

## Guia de Uso del TPE

Como primer paso sedeberá clonar el [repositorio](https://github.com/lukyferreiro/TPE-Redes-Kubernetes) y posicionarse en la carpeta correspondiente

```bash
git clone https://github.com/lukyferreiro/TPE-Redes-Kubernetes
```

```bash
cd ./TPE-Redes-Kubernetes
```

A continuación, se presentaran todos los pasos para levantar un clúster de Kubernetes que cumpla con lo solicitado en la consigna. El objetivo es lograr la siguiente arquitectura:

![Arquitectura del cluster de Kubernetes](...png "Arquitectrura del cluster de Kubernetes")

### Base de datos externa

Primero se debe crear un archivo .env dentro de la carpeta  **database** (el que se encuentra a la misma altura que **docs** y **kubernetes**) con las siguientes variables:

```bash
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

Luego se creará el container de Docker que contará con una imagen de una base de datos PostgreSQL, con un volumen persistente para almacenamiento y cargado con registros de información de ... . Cabe destacar que este container se encontrara fuera del cluster de Kubernetes (el clúster se comunicará con la BD mediante un servicio de Kubernetes encargado de exponerla, esto se explicará en secciones posteriores).

```bash
docker compose  -f ./database/docker-compose.yml up -d
```

### Levantar el cluster de Kubernetes

Seguidamente, se creará el clúster de Kubernetes denominado *redes-cluster*, utilizando la configuración que se encuentra en el archivo *kubernetes/cluster-config.yaml*. Dicho cluster se configurará con un nodo master y dos slaves-

```bash
kind create cluster --config kind-config/multi-cluster-config.yaml --name redes-cluster
```

Una vez inicializado el clúster, se podrán visualizar la siguiente información:

- Clústers disponibles:

```bash
kind get clusters
```

- Información específica del clúster:

```bash
kubectl cluster-info
```

- Los 3 nodos en ejecución:

```bash
kubectl get nodes
```

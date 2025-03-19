# FlatcarMicroCloud - Arquitectura de Infraestructura

Este repositorio contiene el diagrama de arquitectura de **FlatcarMicroCloud**, representado utilizando la librería [`diagrams`](https://diagrams.mingrammer.com/) de Mingrammer.

## 📌 Descripción

FlatcarMicroCloud es una infraestructura optimizada para Kubernetes, diseñada con seguridad, escalabilidad y eficiencia. El diagrama generado muestra la estructura de red, balanceo de carga, seguridad y nodos del clúster.

## 🚀 Instalación y Uso

### 1️⃣ Clonar el repositorio

Clona este repositorio en tu máquina local:
```sh
 git clone https://github.com/vhgalvez/arquitectura_FlatcarMicroCloud.git
 cd arquitectura_FlatcarMicroCloud
```

### 2️⃣ Instalar dependencias
Necesitas tener **Python 3.x** y **Graphviz** instalado:
```sh
pip install diagrams
```

#### Instalar `graphviz` según tu sistema:
- **Ubuntu/Debian**:
  ```sh
  sudo apt install graphviz
  ```
- **macOS (Homebrew)**:
  ```sh
  brew install graphviz
  ```
- **Windows**:
  Descarga e instala Graphviz desde [graphviz.org](https://graphviz.gitlab.io/download/).

### 3️⃣ Generar el diagrama
Ejecuta el script para generar la imagen:
```sh
python infra_diagram.py
```
Esto generará un archivo `FlatcarMicroCloud.png` con la arquitectura visualizada.

## 🏗️ Arquitectura de la Infraestructura

### 📡 Usuarios Públicos y Seguridad Externa
- **Usuarios Públicos** acceden mediante **Cloudflare CDN**, que actúa como proxy y cache.
- **VPS con IP Pública** expone servicios de forma segura a través de **WireGuard VPN Gateway**.

### 🔀 Balanceo de Carga
- **Traefik Load Balancers** manejan el tráfico interno.
- Integración con **Kubernetes y FreeIPA**.

### 🖥️ Infraestructura Base
- **Bastion Node**: Control de acceso seguro.
- **FreeIPA Node**: Autenticación y DNS.
- **PostgreSQL Node**: Base de datos principal.

### ☸️ Clúster Kubernetes
- **3 Master Nodes (etcd)**: Control y coordinación del clúster.
- **3 Worker Nodes**: Procesamiento y ejecución de contenedores.
- **Storage Node**: Almacenamiento distribuido.


## 📜 License

This project is **Licencia MIT** under the [MIT License](LICENSE).

---
📧 **Contacto:** Si tienes dudas o sugerencias, ¡abre un issue o contribuye al proyecto! 🚀
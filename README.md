# FlatcarMicroCloud - Arquitectura de Infraestructura

Este repositorio contiene el diagrama de arquitectura de **FlatcarMicroCloud**, representado utilizando la librería [`diagrams`](https://diagrams.mingrammer.com/) de Mingrammer.

## 📌 Descripción

FlatcarMicroCloud es una infraestructura optimizada para Kubernetes, diseñada con seguridad, escalabilidad y eficiencia. El diagrama generado muestra la estructura de red, balanceo de carga, seguridad y nodos del clúster.

## 🚀 Instalación y Uso

### 1️⃣ Clonar el repositorio
```sh
 git clone https://github.com/tuusuario/FlatcarMicroCloud.git
 cd FlatcarMicroCloud
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

## 📜 Licencia
Este proyecto está bajo la **Licencia MIT**. Puedes utilizarlo, modificarlo y distribuirlo libremente. 

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---
📧 **Contacto:** Si tienes dudas o sugerencias, ¡abre un issue o contribuye al proyecto! 🚀
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.network import Traefik
from diagrams.onprem.security import FreeIPA
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.container import Kubernetes
from diagrams.generic.network import VPN, Users
from diagrams.generic.cloud import CDN

# Creación del diagrama con título mejorado
with Diagram("FlatcarMicroCloud - Arquitectura de Infraestructura", show=False, direction="TB"):
    # Usuarios y seguridad externa
    users = Users("Usuarios Públicos")
    cloudflare = CDN("Cloudflare CDN")
    vps = Server("VPS (IP Pública)")
    wireguard = VPN("WireGuard VPN Gateway (10.17.0.1)")
    
    users >> Edge(label="Acceso HTTPS") >> cloudflare >> Edge(label="Proxy y Cache") >> vps >> Edge(label="Tunel VPN: Seguridad") >> wireguard
    
    # Red interna
    with Cluster("Red Interna Local (192.168.0.0/24)"):
        with Cluster("Balanceo de Carga"):
            lb1 = Traefik("Load Balancer 1 (10.17.3.12)")
            lb2 = Traefik("Load Balancer 2 (10.17.3.13)")
        
        with Cluster("Infraestructura Base"):
            bastion = Server("Bastion Node (10.17.5.2) - Seguridad/Gestión")
            freeipa = FreeIPA("FreeIPA Node (10.17.3.11) - DNS/Auth")
            db = PostgreSQL("PostgreSQL Node (10.17.3.14) - Base de Datos")
        
        with Cluster("Clúster Kubernetes"):
            with Cluster("Master Nodes (etcd)"):
                master1 = Kubernetes("Master Node 1 (10.17.4.21)")
                master2 = Kubernetes("Master Node 2 (10.17.4.22)")
                master3 = Kubernetes("Master Node 3 (10.17.4.23)")
            
            with Cluster("Worker Nodes"):
                worker1 = Kubernetes("Worker Node 1 (10.17.4.24)")
                worker2 = Kubernetes("Worker Node 2 (10.17.4.25)")
                worker3 = Kubernetes("Worker Node 3 (10.17.4.26)")
                storage = Kubernetes("Storage Node (10.17.4.27) - Almacenamiento")
            
        # Conexiones entre componentes
        wireguard >> lb1 >> [master1, master2, master3]
        wireguard >> lb2 >> [worker1, worker2, worker3, storage]
        lb1 >> [bastion, freeipa, db]
        lb2 >> [bastion, freeipa, db]
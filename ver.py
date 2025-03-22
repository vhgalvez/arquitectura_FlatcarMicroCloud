from diagrams import Diagram
from diagrams.onprem.compute import Server

with Diagram("Simple Diagram", show=False):
    Server("Test Server")
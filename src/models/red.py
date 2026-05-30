import networkx as nx
import random
from typing import List
from models.mujer import Mujer
from models.cliente import Cliente  # Lo crearemos ahora

class RedPreferencias:
    """Red de clientes con preferencias realistas"""
    
    def __init__(self, mujeres: List[Mujer], num_clientes=800):
        self.num_clientes = num_clientes
        self.clientes = [Cliente(i) for i in range(num_clientes)]
        self.G = self._crear_red(mujeres)

    def _crear_red(self, mujeres):
        G = nx.Graph()
        for m in mujeres:
            G.add_node(f"M{m.id}")
        for c in self.clientes:
            G.add_node(f"C{c.id}")
            for m in mujeres:
                score = m.atractivo * 0.4
                if c.preferencia_madres and m.hijos >= 2:
                    score += 0.45
                if m.es_viuda:
                    score += 0.4
                if m.economia.deuda > 300:
                    score += 0.25  # Clientes de alto riesgo buscan mujeres desesperadas
                
                if random.random() < min(0.42, score):
                    G.add_edge(f"C{c.id}", f"M{m.id}")
        return G

    def actualizar(self, mujeres):
        """Actualiza la red cada cierto tiempo"""
        self.G = self._crear_red(mujeres)
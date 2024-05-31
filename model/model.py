import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.nodi = []
        self.ottimo = []
        self.pesoMax = 0

    def newGraph(self, nodi):
        self.grafo = nx.Graph()
        self.nodi = nodi
        self.grafo.add_nodes_from(nodi)

    def addPesi(self, year):
        for n1 in self.nodi:
            for n2 in self.nodi:
                if n1 != n2:
                    peso = DAO.getPesi(n1.Retailer_code, n2.Retailer_code, year)[0]
                    if peso > 0:
                        self.grafo.add_edge(n1, n2, weight=peso)

    def getPercorsoPesoMax(self, N):
        self.ottimo = []
        self.pesoMax = 0
        for nodo in self.nodi:
            parziale = [nodo]
            self._ricorsione2(parziale, N)
        return self.ottimo, self.pesoMax

    def _ricorsione(self, parziale, N):
        if len(parziale) > N:
            return
        if parziale[0] == parziale[-1]:
            if len(parziale[1:-1]) == len(set(parziale[1:-1])):
                if self.calcolaPeso(parziale) > self.pesoMax:
                    self.ottimo = copy.deepcopy(parziale)
                    self.pesoMax = self.calcolaPeso(parziale)
                    return
        for v in self.grafo.neighbors(parziale[-1]):
            parziale.append(v)
            self._ricorsione(parziale, N)
            parziale.pop()

    def _ricorsione2(self, parziale, N):
        if len(parziale) > N+1:
            return
        if len(parziale) == N+1 and parziale[0] == parziale[-1]:
            if (len(parziale) - 1) == len(set(parziale)):
                if self.calcolaPeso(parziale) > self.pesoMax:
                    self.ottimo = copy.deepcopy(parziale)
                    self.pesoMax = self.calcolaPeso(parziale)
                    return
        for v in self.grafo.neighbors(parziale[-1]):
            parziale.append(v)
            self._ricorsione2(parziale, N)
            parziale.pop()

    def calcolaPeso(self, lista):
        peso = 0
        for i in range(len(lista) - 1):
            peso += self.grafo[lista[i]][lista[i + 1]]["weight"]
        return peso

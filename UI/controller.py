import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        pass

    def fillddYear(self):
        for i in range(2015, 2019):
            self._view.ddyear.options.append(ft.dropdown.Option(str(i)))

    def fillddCountry(self):
        years = DAO.getAllCountry()
        print(years)
        for y in years:
            self._view.ddcountry.options.append(ft.dropdown.Option(y))

    def handle_graph(self, e):
        nodi = DAO.getRetailers(self._view.ddcountry.value)
        self._model.newGraph(nodi)
        self._model.addPesi(self._view.ddyear.value)
        self._view.txt_result.controls.append(
            ft.Text(f"{len(self._model.grafo.nodes)} vertici, {len(self._model.grafo.edges)} archi"))
        self._view._page.update()

    def handle_volume(self, e):
        output = {}
        for n in self._model.grafo.nodes:
            tot = 0
            iter = list(self._model.grafo.neighbors(n))
            for nei in iter:
                sp = self._model.grafo[n][nei]['weight']
                if sp > 0:
                    tot += sp
            if tot > 0:
                output[n] = tot
        sorted_nodes = sorted(output, key=output.get, reverse=True)
        for n in sorted_nodes:
            self._view.txtOut2.controls.append(ft.Text(f"{n} --> {output[n]}"))
        self._view._page.update()

    def handle_path(self, e):
        n = int(self._view.txtN.value)
        if n <= 1:
            self._view.create_alert("Troppo piccolo come numero inserito")
            return
        print("premuto")
        ottimo, peso = self._model.getPercorsoPesoMax(n)
        self._view.txtOut3.controls.append(ft.Text(f"peso: {peso}, \n {ottimo}"))
        self._view.update_page()

    # da view il numero massimo valido di numero di archi: terminale per il parziale
    # itero su tutti i nodi
    # per ogni nodo chiamo il metodo ricorsivo
    #
    # se parziale[0] = parziale[-1]
    #   se è quella col peso massimo copy.deepcopy
    #
    # nodo not in parziale
    # append parziale
    # ricorsione
    # pop

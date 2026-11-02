import flet as ft
from UI.view import View
from model.model import DepositoStrumenti

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: DepositoStrumenti):
        self._model = model
        self._view = view

    def get_nome(self):
        return self._model.nome

    def get_responsabile(self):
        return self._model.responsabile

    def set_responsabile(self, responsabile):
        self._model.responsabile = responsabile

    def conferma_responsabile(self, e):
        self._model.responsabile = self._view.input_responsabile.value
        self._view.txt_responsabile.value = f"Responsabile: {self._model.responsabile}"
        self._view.update()

    # Altre Funzioni Event Handler
    def handle_mostra_tutti(self, e):
        """Handler collegato al pulsante 'Mostra' della Sezione 3."""
        # === MIO COMMENTO DI SPIEGAZIONE ===
        # 1. Chiedo al modello la lista di tutti gli strumenti letti dal DB
        strumenti = self._model.get_strumenti()

        # 2. Controllo se c'è stato un errore di connessione col database
        if strumenti is None:
            self._view.show_alert("❌ Impossibile connettersi al database o recuperare gli strumenti!")
            return

        # 3. Pulisco la ListView nella vista prima di ripopolarla
        self._view.lista_strumenti.controls.clear()

        # 4. Popolo la ListView
        if len(strumenti) == 0:
            self._view.lista_strumenti.controls.append(ft.Text("Nessuno strumento presente nel deposito."))
        else:
            for s in strumenti:
                # Aggiungo un'icona visiva a seconda della disponibilità
                stato_icona = "✅" if s.disponibile else "⛔"
                self._view.lista_strumenti.controls.append(ft.Text(f"{stato_icona} {s}"))

        # 5. Aggiorno l'interfaccia grafica per rendere visibili i cambiamenti
        self._view.update()

    def handle_cerca_tipo(self, e):
        """Handler collegato al pulsante 'Cerca' della Sezione 4."""
        
        # Recupero la stringa inserita dall'utente nel TextField
        tipo_inserito = self._view.input_tipo_strumento.value

        # Validazione di input: verifico che il campo non sia vuoto
        if not tipo_inserito or tipo_inserito.strip() == "":
            self._view.show_alert("⚠️ Inserire un tipo di strumento per avviare la ricerca!")
            return

        tipo_clean = tipo_inserito.strip()

        # Invoco la ricerca nel modello
        risultati = self._model.cerca_strumenti_per_tipo(tipo_clean)

        if risultati is None:
            self._view.show_alert("❌ Errore durante la ricerca nel database!")
            return

        # Pulisco e aggiorno la ListView dei risultati filtrati
        self._view.lista_strumenti_ricerca.controls.clear()

        if len(risultati) == 0:
            self._view.lista_strumenti_ricerca.controls.append(
                ft.Text(f"Nessuno strumento di tipo '{tipo_clean}' trovato nel deposito.")
            )
        else:
            for s in risultati:
                stato_icona = "✅" if s.disponibile else "⛔"
                self._view.lista_strumenti_ricerca.controls.append(ft.Text(f"{stato_icona} {s}"))

        # Svuoto la casella di testo di ricerca e aggiorno la pagina
        self._view.input_tipo_strumento.value = ""
        self._view.update()

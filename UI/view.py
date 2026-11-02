import flet as ft
from UI.alert import AlertManager

'''
    VIEW:
    - Rappresenta l'interfaccia utente
    - Riceve i dati dal MODELLO e li presenta senza modificarli
'''

class View:
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "Lab06"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.DARK

        # Alert
        self.alert = AlertManager(page)

        # Controller
        self.controller = None

        # Elementi UI
        self.txt_titolo = None
        self.txt_responsabile = None

    def show_alert(self, messaggio):
        self.alert.show_alert(messaggio)

    def set_controller(self, controller):
        """ Imposta il controller alla pagina """
        self.controller = controller

    def update(self):
        self.page.update()

    def load_interface(self):
        """ Crea e aggiunge Elementi di UI alla pagina e la aggiorna. """
        self.txt_titolo = ft.Text(value=self.controller.get_nome(), size=38, weight=ft.FontWeight.BOLD)
        self.txt_responsabile = ft.Text(
            value=f"Responsabile: {self.controller.get_responsabile()}",
            size=16,
            weight=ft.FontWeight.BOLD
        )

        # TextField per responsabile
        self.input_responsabile = ft.TextField(value=self.controller.get_responsabile(), label="Responsabile")

        # ListView per mostrare la lista di strumenti aggiornata
        self.lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

        # TextField per ricerca strumento per tipo
        self.input_tipo_strumento = ft.TextField(label="Tipo")

        # ListView per mostrare il risultato della ricerca strumenti per tipo
        self.lista_strumenti_ricerca = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

        # --- PULSANTI e TOGGLE associati a EVENTI ---
        self.toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=self.cambia_tema)
        pulsante_conferma_responsabile = ft.Button("Conferma", on_click=self.controller.conferma_responsabile)

        
        # Creo i pulsanti "Mostra" e "Cerca" collegandoli ai rispettivi handler del Controller
        pulsante_mostra_strumenti = ft.Button("Mostra", on_click=self.controller.handle_mostra_tutti)
        pulsante_cerca_strumenti = ft.Button("Cerca", on_click=self.controller.handle_cerca_tipo)

        # --- LAYOUT ---
        self.page.add(
            self.toggle_cambia_tema,

            # Sezione 1
            self.txt_titolo,
            self.txt_responsabile,
            ft.Divider(),

            # Sezione 2
            ft.Text("Modifica Informazioni", size=20),
            ft.Row(spacing=200,
                   controls=[self.input_responsabile, pulsante_conferma_responsabile],
                   alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),

            #SEZIONE 3: LISTA COMPLETA DEGLI STRUMENTI
            ft.Text("Strumenti", size=20),
            pulsante_mostra_strumenti,
            self.lista_strumenti,
            ft.Divider(),

            #SEZIONE 4: RICERCA STRUMENTO PER TIPO
            ft.Text("Cerca Strumento per Tipo", size=20),
            ft.Row(
                spacing=20,
                controls=[self.input_tipo_strumento, pulsante_cerca_strumenti],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            self.lista_strumenti_ricerca,
        )

    def cambia_tema(self, e):
        self.page.theme_mode = ft.ThemeMode.DARK if self.toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        self.toggle_cambia_tema.label = "Tema scuro" if self.toggle_cambia_tema.value else "Tema chiaro"
        self.page.update()

import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    # TODO
    marca_input = ft.TextField(label='Marca')
    modello_input = ft.TextField(label='Modello')
    anno_input = ft.TextField(label='Anno')
    txt_posti = ft.Text(value='0', width=60, disabled=True, text_align=ft.TextAlign.CENTER)

    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    # TODO
    def aggiungi_auto(e):
        try:
            anno = int(anno_input.value)
            posti = int(txt_posti.value)
            autonoleggio.aggiungi_automobile(marca_input.value, modello_input.value, anno, posti)
            marca_input.value = modello_input.value = anno_input.value = txt_posti.value = ''
            aggiorna_lista_auto()
        except ValueError:
            alert.show_alert("❌ Errore: inserisci valori numerici validi per anno e posti.")

    def incrementa_posti(e):
        current_val = txt_posti.value
        txt_posti.value = f"{int(current_val) + 1}"
        txt_posti.update()

    def decrementa_posti(e):
        current_val = txt_posti.value
        txt_posti.value = f"{int(current_val) - 1}"
        txt_posti.update()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO
    pulsante_aggiungi_auto = ft.ElevatedButton("Aggiungi automobile", on_click=aggiungi_auto)
    pulsante_incrementa_posti = ft.IconButton(icon=ft.Icons.ADD, icon_color="green", on_click=incrementa_posti)
    pulsante_decrementa_posti = ft.IconButton(icon=ft.Icons.REMOVE, icon_color="red", on_click=decrementa_posti)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Divider(),
        ft.Text("Aggiungi nuova automobile", size=20),
        ft.Row(spacing=30,
               controls=[marca_input, modello_input, anno_input,
                         ft.Row([pulsante_decrementa_posti, txt_posti, pulsante_incrementa_posti])],
               alignment=ft.MainAxisAlignment.CENTER),
        pulsante_aggiungi_auto,

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
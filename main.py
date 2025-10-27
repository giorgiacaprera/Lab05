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
    txt_aggiungi_auto = ft.Text('Aggiungi Nuova Automobile', size=20)
    input_marca = ft.TextField(label='Marca', width=150)
    input_modello = ft.TextField(label='Modello', width=150)
    input_anno = ft.TextField(label='Anno', width=150)
    num_posti = ft.Text(value='4', size=18, weight=ft.FontWeight.BOLD)

    def incrementa_posti(e):
        try:
            valore = int(num_posti.value)
            num_posti.value = str(valore + 1)
            page.update()
        except:
            alert.show_alert('Errore nel contare i posti')

    def decrementa_posti(e):
        try:
            valore = int(num_posti.value)
            if valore > 1:
                num_posti.value = str(valore - 1)
                page.update()
        except:
            alert.show_alert('Errore nel contare i posti')

    btn_minus = ft.IconButton(icon=ft.Icons.REMOVE, on_click=decrementa_posti)
    btn_plus = ft.IconButton(icon=ft.Icons.ADD, on_click=incrementa_posti)



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
        marca = input_marca.value.strip()
        modello = input_modello.value.strip()
        anno_str = input_anno.value.strip()
        posti_str = num_posti.value.strip()

        if not marca or not modello or not anno_str or not posti_str:
            alert.show_alert('Errore nei campi obbligatori')
            return

        try:
            anno = int(anno_str)
            posti = int(posti_str)
        except:
            alert.show_alert('I valori dovrebbero essere numerici')
            return

        try:
            autonoleggio.aggiungi_automobile(marca, modello, anno, posti)
            input_marca.value = ''
            input_modello.value = ''
            input_anno.value = ''
            num_posti.value = '4'
            aggiorna_lista_auto()
            page.update()
        except Exception as err:
            alert.show_alert(f'Errore: {err}')



    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO
    btn_aggiungi_auto = ft.ElevatedButton('Aggiungi Automobile', on_click=aggiungi_auto)

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
        txt_aggiungi_auto,
        ft.Row(controls=[input_marca, input_modello, input_anno], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(controls=[ft.Text('Numero Posti:', size=16), btn_minus, num_posti, btn_plus, btn_aggiungi_auto], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)

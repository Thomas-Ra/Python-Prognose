import ctypes
import sys
import tkinter as tk
import tkinter.messagebox
import threading
import pandas as pd
from tkinter import *
from cefpython3 import cefpython as cef
from io import StringIO
from finance.prediction import predictTicker

def start_gui():
    root = Tk()
    cef.Initialize()

    #Fenstergröße setzen und Titel geben
    root.geometry("1350x700")
    root.title("Stock Market Prediction")

    # DEF
    def quit(event=None):
        root.destroy()
        return

    #Teil der GUI-Element
    mainside = Frame(root, bg='black', width=1100)
    mainside.grid(row=0, column=0, columnspan=1, rowspan=1, sticky='NSWE', pady=5, padx=5)

    # URL zum abrufen der Diagramme (web-server), beruht auf localhost-IP
    baseUrl = "http://127.0.0.1:8080/"

    # zeigt das Hauptelement an und übergibt den Wert der Liste;
    def display():
        global url1
        selected = gui_list.get(ANCHOR)
        browser_frame = BrowserFrame(mainside)
        
        #URL setzt sich aus der ausgewählten Aktie zusammen
        url1 = baseUrl + selected +".html"
        browser_frame = BrowserFrame(mainside)
        browser_frame.place(x=0, y=0, anchor='nw', relwidth=1.0, relheight=1.0)

        return url1

    # EVENTS
    root.bind("<Alt-q>", quit)

    #Startseite (Webseite wird abgerufen)
    def display_start():
        global url1
        url1 = "https://i.imgur.com/wxjO2l1.png"
        browser_frame = BrowserFrame(mainside)
        browser_frame.place(x=0, y=0, anchor='nw', relwidth=1.0, relheight=1.0)
        return url1

    # Öffnet das Popup des Generations-Konfigurator
    def display_popup():
        global pop
        pop = Toplevel(root)
        pop.title("Prognosen-Konfigurator")
        pop.geometry("620x340")
        pop.config(bg="#a8eda6")
        pop_label_width = 14

        #Funktion für die Hilfe-Text-Darstellung
        def display_info(plain_info="Ändern Sie die Parameter, um die Prognose anzupassen. Je nach Wert wird das Ergebnis und der Zeitaufwand verändert."
                                    " Klicken Sie auf den Info-Button, falls sie sich unsicher sind. "
                                    "Die Standardwerte sind empfohlene Durchschnittswerte"):
            plain_info1 = plain_info
            info_label = Label(pop, text=plain_info1, bg="#6f8f75", fg="white", width=45, height=15, wraplength=280)
            info_label.grid(row=0, column=3, rowspan=10, padx=15, pady=5)

        display_info()

        #Erstelen der Labels / Titel
        pop_label = Label(pop, text="Ticker", fg="white", bg="#4c754b", width=pop_label_width)
        pop_label.grid(row = 0, column=0)
        pop_label1 = Label(pop, text="N_STEPS", fg="white", bg="#4c754b", width=pop_label_width)
        pop_label1.grid(row=1, column=0)
        pop_label2 = Label(pop, text="LOOKUP_STEP", fg="white", bg="#4c754b", width=pop_label_width)
        pop_label2.grid(row=2, column=0)
        pop_label3 = Label(pop, text="TEST_SIZE", fg="white", bg="#4c754b", width=pop_label_width)
        pop_label3.grid(row=3, column=0)
        pop_label4 = Label(pop, text="N_LAYERS", fg="white", bg="#4c754b", width=pop_label_width)
        pop_label4.grid(row=4, column=0)
        pop_label5 = Label(pop, text="BIDIRECTIONAL", fg="white", bg="#4c754b", width=pop_label_width)
        pop_label5.grid(row=5, column=0)
        pop_label6 = Label(pop, text="BATCH_SIZE", fg="white", bg="#4c754b", width=pop_label_width)
        pop_label6.grid(row=6, column=0)
        pop_label7 = Label(pop, text="EPOCHS", fg="white", bg="#4c754b", width=pop_label_width)
        pop_label7.grid(row=7, column=0)

        #Erstellen der Eingabefelder 
        selected_chart = gui_list.get(ANCHOR)
        pop_input = Entry(pop)
        pop_input.insert(END, selected_chart)
        pop_input.grid(row=0, column=1)
        pop_input1 = Entry(pop)
        pop_input1.insert(END, "50")
        pop_input1.grid(row=1, column=1)
        pop_input2 = Entry(pop)
        pop_input2.insert(END, "15")
        pop_input2.grid(row=2, column=1)
        pop_input3 = Entry(pop)
        pop_input3.insert(END, "0.2")
        pop_input3.grid(row=3, column=1)
        pop_input4 = Entry(pop)
        pop_input4.insert(END, "2")
        pop_input4.grid(row=4, column=1)
        pop_input5 = Entry(pop)
        pop_input5.insert(END, "True")
        pop_input5.grid(row=5, column=1)
        pop_input6 = Entry(pop)
        pop_input6.insert(END, "64")
        pop_input6.grid(row=6, column=1)
        pop_input7 = Entry(pop)
        pop_input7.insert(END, "500")
        pop_input7.grid(row=7, column=1)

        #Info-Panel einfügen und den jeweiligen Text
        ticker_info = "Ticker \n Aktiensymbol, das zu untersuchen ist [str]"
        n_steps_info = "n_steps \n Die Länge der historischen Sequenz (d. h. die Größe des Fensters), die für die Vorhersage verwendet wird [int]"
        lookup_step_info = "lookup_step \n der vorauszusagende zukünftige Suchschritt, default: 1 (z. B. nächster Tag) [int]"
        test_size_info = "test_size \n Anteil der Testdaten [int]"
        n_layers_info = "n_layers \n Anzahl RNN layers die wir nutzen [int]"
        bidirectional_info = "bidirectional_info \n bidirectional RNNs nutzen [bool]"
        batch_size_info = "batch_size_info \n Anzahl der in jeder Trainingsiteration verwendeten Datenproben [int]"
        epochs_info = "epochs_info \n Anzahl der Durchläufe des Algorithmus durch die gesamte Trainingsmenge; eine hohe Zahl wird empfohlen [int]"

        # Text wird durch diese Info-Buttons überschrieben
        popup_text = "?"
        pop_info = Button(pop, text=popup_text, command=lambda: display_info(ticker_info))
        pop_info.grid(row=0, column=2)
        pop_info1 = Button(pop, text=popup_text, command=lambda: display_info(n_steps_info))
        pop_info1.grid(row=1, column=2)
        pop_info2 = Button(pop, text=popup_text, command=lambda: display_info(lookup_step_info))
        pop_info2.grid(row=2, column=2)
        pop_info3 = Button(pop, text=popup_text, command=lambda: display_info(test_size_info))
        pop_info3.grid(row=3, column=2)
        pop_info4 = Button(pop, text=popup_text, command=lambda: display_info(n_layers_info))
        pop_info4.grid(row=4, column=2)
        pop_info5 = Button(pop, text=popup_text, command=lambda: display_info(bidirectional_info))
        pop_info5.grid(row=5, column=2)
        pop_info6 = Button(pop, text=popup_text, command=lambda: display_info(batch_size_info))
        pop_info6.grid(row=6, column=2)
        pop_info7 = Button(pop, text=popup_text, command=lambda: display_info(epochs_info))
        pop_info7.grid(row=7, column=2)

        #Button zum Absenden der eingegeben Parameter: Input wird in korrekten Datentyp umgewandelt
        def submit():
            info_label = Label(pop, text="", bg="#6f8f75", fg="white", width=45, height=15, wraplength=280, justify="left")
            info_label.grid(row=0, column=3, rowspan=10, padx=15, pady=5)
            pl = PrintLogger(info_label)
            pop_button.configure(state=DISABLED)
            # replace sys.stdout with our object
            sys.stdout = pl
            predictTicker(str(pop_input.get()), int(pop_input1.get()), int(pop_input2.get()), float(pop_input3.get()), int(pop_input4.get()), bool(pop_input5.get()), int(pop_input6.get()), int(pop_input7.get()))


        #Definieren vom Threading: Verhindern von User-Interaktionen beim generieren neuer Daten
        def start_submit_thread(event):
            global submit_thread
            submit_thread = threading.Thread(target=submit)
            submit_thread.daemon = True
            submit_thread.start()

        #button- einbinden zum submitten
        pop_button = Button(pop, text="Generate", command=lambda: start_submit_thread(None))
        pop_button.grid(row=9, column=0, columnspan=3, sticky=NSEW)
        pop_button.configure(state=NORMAL)

    #Buttom zum Konfigurator
    def display_generate():
        selected_chart = gui_list.get(ANCHOR)
        if (selected_chart == ""):
            tkinter.messagebox.showerror(title="ERROR", message="Du hast keine Aktie ausgewählt.")
        else:
            display_popup()
            #predictTicker(selected_chart)

    display_start()


    # Menüband erzeugen
    menu = Menu(root)
    root.config(menu=menu)
    # obere Leiste - menu
    filemenu = Menu(menu)
    menu.add_cascade(label="Home", menu=filemenu)
    filemenu.add_command(label="Startseite", command=display_start)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)

    gachamenu = Menu(menu)
    menu.add_cascade(label="Aktien", menu=gachamenu)
    gachamenu.add_command(label="AMZN", command=display)
    gachamenu.add_separator()
    gachamenu.add_command(label="AAPL", command=display)
    gachamenu.add_separator()
    gachamenu.add_command(label="GME", command=display)
    gachamenu.add_separator()
    gachamenu.add_command(label="GOOG", command=display)
    gachamenu.add_separator()
    gachamenu.add_command(label="MSFT", command=display)
    gachamenu.add_separator()
    gachamenu.add_command(label="TSLA", command=display)

    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="Quit", command=quit, accelerator="Alt+q")

    # Rechten Kasten #1 erzeugen
    rightside = Frame(root, width=220)
    rightside.grid(row=0,  column=1)

    # Rechten Kasten #2 erzeugen
    rightside1 = Frame(rightside, width=220, height=200, bg='#bed1bc')
    rightside1.grid(row=0, column=0, rowspan=1, sticky='N', pady=5)

    # Rechten kasten #3 erzeugen
    rightside2 = Frame(rightside, width=220, height=100, bg='#bed1bc')
    rightside2.grid(row=1, column=0, rowspan=1, sticky='NSEW', pady=5)

    # create Kasten #4 erzeugen
    rightside3 = Frame(rightside, width=220, height=300, bg='#bed1bc')
    rightside3.grid(row=2, column=0, rowspan=1, sticky='S', pady=5)

    # Untere Leiste erzeugen
    lowerside = Frame(root, height=50, width=1330,bg="#7c877b")
    lowerside.grid(row=1, column=0, columnspan=2)

    # Unteren Text einbinden
    lowerside_text = Label(root, text="Entwicklung und Implementierung eines Prognose-Systems für augewählte Kurse.")
    lowerside_text.grid(row=1, column=0, columnspan=2, sticky=NSEW)

    # Liste der Aktien erstellen
    gui_list = Listbox(rightside, bg="#a4bfa1", width=30, height=6)
    gui_list.grid(row=0, column=0, rowspan=1, pady=35, sticky=N)

    # Liste befüllen >>>
    list_main_stocks = ["AMZN", "AAPL", "GME", "GOOG", "MSFT", "TSLA"]

    for item in list_main_stocks:
        gui_list.insert(END, item)

    # Darstellung und Aktualisierung der Generierungs-Ergebnisse (Auslesung der CSV mittels relativen Pfad)
    def csv_reading():
        selected = gui_list.get(ANCHOR)
        if (selected == ""):
            text_info = "Keine Aktie ausgewählt"
        else:
            text_info = pd.read_csv(
                "./market_prediction/finance/displayResults/" + selected + ".csv", usecols=[1,2], index_col=0)
        rightside3_text = Label(rightside, text=text_info, bg="#bed1bc", wraplength=280, justify="left", font=('Helvetica, 10'))
        rightside3_text.grid(row=2, column=0, sticky=NSEW)
        rightside4_text = Label(rightside, text="Ergebnisse der Prognosen-Generierung", wraplength=280, justify="center", font='Helvetica 12 bold', bg="#bed1bc")
        rightside4_text.grid(row=2, column=0, sticky=N, pady=25)

    # Button und Text erstellen
    rightside1_text = Label(rightside, text="Auswahl der Aktie", bg="#bed1bc", font=("times",14, "bold"))
    rightside1_text.grid(row=0, column=0, sticky=N, pady=5)
    rightside2_text = Button(rightside, text="regenerate data", bg="#bed1bc", font=('Helvetica',12, "bold"), command= display_generate)
    rightside2_text.grid(row=1, column=0)

    # Button zum auswählen der Daten
    # Button führt die Anzeige des Charts aus; Liest erst dann CSV (Prognoseergebnsse) aus ausgewähltem Listenelement aus 
    button_confirm = Button(rightside,  text="Aktie auswählen", bg="#bed1bc", font=('Helvetica',12, "bold"), command=lambda: [display(), csv_reading()])
    button_confirm.grid(column=0, row=0, sticky=S, pady=20)


    root.mainloop()
    cef.Shutdown()

# ab hier: Klasse aus cefpython3. Aus cefpython-3-Github importiert;
# Klasse wird benötigt, um mithilfe der übergebenen URL (url1), die Webseite anzuzeigen und in TKinter anzuzeigen
class BrowserFrame(tk.Frame):

    def __init__(self, mainframe, navigation_bar=None):
        self.navigation_bar = navigation_bar
        self.closing = False
        self.browser = None
        tk.Frame.__init__(self, mainframe)
        self.mainframe = mainframe
        #self.bind("<FocusIn>", self.on_focus_in)
        #self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<Configure>", self.on_configure)
        """For focus problems see Issue #255 and Issue #535. """
        self.focus_set()


    # url1 wird als globale Variable eingelesen und entspricht den vorher definierten Werten
    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        window_info.SetAsChild(self.get_window_handle(), rect)
        self.browser = cef.CreateBrowserSync(window_info,
                                             url=url1)



        assert self.browser
        # self.browser.SetClientHandler(LifespanHandler(self))
        # self.browser.SetClientHandler(LoadHandler(self))
        # self.browser.SetClientHandler(FocusHandler(self))
        self.message_loop_work()


    def get_window_handle(self):
        if self.winfo_id() > 0:
            return self.winfo_id()
        else:
            raise Exception("Couldn't obtain window handle")

    def message_loop_work(self):
        cef.MessageLoopWork()
        self.after(10, self.message_loop_work)

    def on_configure(self, _):
        if not self.browser:
            self.embed_browser()


    def on_root_configure(self):
        # Root <Configure> event will be called when top window is moved
        if self.browser:
            self.browser.NotifyMoveOrResizeStarted()


    def on_mainframe_configure(self, width, height):
        if self.browser:
            if WINDOWS:
                ctypes.windll.user32.SetWindowPos(
                    self.browser.GetWindowHandle(), 0,
                    0, 0, width, height, 0x0002)
            self.browser.NotifyMoveOrResizeStarted()


    def on_focus_in(self, _):
        # logger.debug("BrowserFrame.on_focus_in")
        if self.browser:
            self.browser.SetFocus(True)


    def on_focus_out(self, _):
        # logger.debug("BrowserFrame.on_focus_out")
        """For focus problems see Issue #255 and Issue #535. """
        pass

    def on_root_close(self):
        # logger.info("BrowserFrame.on_root_close")
        if self.browser:
            # logger.debug("CloseBrowser")
            self.browser.CloseBrowser(True)
            self.clear_browser_references()
        else:
            # logger.debug("tk.Frame.destroy")
            self.destroy()

    def clear_browser_references(self):
        # Clear browser references that you keep anywhere in your
        # code. All references must be cleared for CEF to shutdown cleanly.
        self.browser = None

class LifespanHandler(object):

    def __init__(self, tkFrame):
        self.tkFrame = tkFrame

    def OnBeforeClose(self, browser, **_):
        #logger.debug("LifespanHandler.OnBeforeClose")
        self.tkFrame.quit()

class LoadHandler(object):

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnLoadStart(self, browser, **_):
        if self.browser_frame.master.navigation_bar:
            self.browser_frame.master.navigation_bar.set_url(browser.GetUrl())


class FocusHandler(object):
    """For focus problems see Issue #255 and Issue #535. """

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnTakeFocus(self, next_component, **_):
        pass#logger.debug("FocusHandler.OnTakeFocus, next={next}".format(next=next_component))

    def OnSetFocus(self, source, **_):
            return True

    def OnGotFocus(self, **_):
        #logger.debug("FocusHandler.OnGotFocus")
        pass

class PrintLogger(): # create file like object
    def __init__(self, label): # pass reference to text widget
        self.label = label # keep ref

    def write(self, text):
        self.label['text'] += text # write text to textbox
            # could also scroll to end of textbox here to make sure always visible

    def flush(self): # needed for file like object
        pass
    
# ENDE von cefpython-importierter Klasse
start_gui()

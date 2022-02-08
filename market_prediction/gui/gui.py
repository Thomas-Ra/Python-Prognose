import tkinter as tk
import tkinter.messagebox
from tkinter import *
from cefpython3 import cefpython as cef
import ctypes
import os
from finance.prediction import predictTicker
#from PIL import ImageTk, Image

def start_gui():
    root = Tk()
    cef.Initialize()

    root.geometry("1350x700")
    #Grid.columnconfigure(root, 0, weight=1)
    #Grid.rowconfigure(root, 0, weight=1)
    #Grid.columnconfigure(root, 1, weight=1)
    #Grid.rowconfigure(root, 1, weight=1)
    #Grid.columnconfigure(root, 2, weight=1)
    #Grid.columnconfigure(root, 3, weight=1)
    #Grid.columnconfigure(root, 4, weight=1)

    root.title("Stock Market Prediction")


    # DEF
    def quit(event=None):
        root.destroy()
        return

    mainside = Frame(root, bg='black', width=1100)
    mainside.grid(row=0, column=0, columnspan=1, rowspan=1, sticky='NSWE', pady=5, padx=5)

    baseUrl = "http://127.0.0.1:8080/"

    def display_apple():
        global url1
        url1 = baseUrl + "Apple.html"
        browser_frame = BrowserFrame(mainside)
        browser_frame.place(x=0, y=0, anchor='nw', relwidth=1.0, relheight=1.0)
        return url1

    def display_amazon():
        global url1
        url1 = baseUrl + "Amazon.html"
        browser_frame = BrowserFrame(mainside)
        browser_frame.place(x=0, y=0, anchor='nw', relwidth=1.0, relheight=1.0)
        return url1

    def display_gamestop():
        global url1
        url1 = baseUrl + "GameStop.html"
        browser_frame = BrowserFrame(mainside)
        browser_frame.place(x=0, y=0, anchor='nw', relwidth=1.0, relheight=1.0)
        return url1

    def display_microsoft():
        global url1
        url1 = baseUrl + "Microsoft.html"
        browser_frame = BrowserFrame(mainside)
        browser_frame.place(x=0, y=0, anchor='nw', relwidth=1.0, relheight=1.0)
        return url1

    def display_tesla():
        global url1
        url1 = baseUrl + "Tesla.html"
        browser_frame = BrowserFrame(mainside)
        browser_frame.place(x=0, y=0, anchor='nw', relwidth=1.0, relheight=1.0)
        return url1

    def display_google():
        global url1
        url1 = baseUrl + "Google.html"
        browser_frame = BrowserFrame(mainside)
        browser_frame.place(x=0, y=0, anchor='nw', relwidth=1.0, relheight=1.0)
        return url1

    def display():
        global url1
        chart_selected = gui_list.get(ANCHOR)
        browser_frame = BrowserFrame(mainside)
        #if (chart_selected == ""):
            #browser_frame.pack(fill=tk.BOTH, expand=tk.YES)
        if (chart_selected == "Tesla"):
            display_tesla()
        if (chart_selected == "Amazon"):
            display_amazon()
        if (chart_selected == "Apple"):
            display_apple()
        if (chart_selected == "Gamestop"):
            display_gamestop()
        if (chart_selected == "Google"):
            display_google()
        if (chart_selected == "Microsoft"):
            display_microsoft()


    #--------------------------


    # EVENTS
    root.bind("<Alt-q>", quit)

    def display_start():
        global url1
        url1 = "https://i.ytimg.com/vi/if-2M3K1tqk/maxresdefault.jpg"
        browser_frame = BrowserFrame(mainside)
        browser_frame.place(x=0, y=0, anchor='nw', relwidth=1.0, relheight=1.0)
        return url1

    def display_popup():
        tkinter.messagebox.showwarning(title="Daten neu berechnen",message="Das könnte eine Weile dauern...")

    def display_generate():
        selected_chart = gui_list.get(ANCHOR)
        if (selected_chart == ""):
            tkinter.messagebox.showerror(title="ERROR", message="Du hast keine Aktie ausgewählt.")
        else:
            predictTicker(selected_chart)



    display_start()

        #img123 = Image.open("stonks_picture-Kopie.png")
        #my_imk = ImageTk.PhotoImage(img123)
        #my_imk = Label(mainside, image=my_imk)
        #my_imk.place(x=0, y=0, anchor='center', relwidth=1.0, relheight=1.0)
        #Label(mainside, image=img123).place(x=0, y=0, anchor='nw', relwidth=1.0, relheight=1.0)

    # MENU
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
    gachamenu.add_command(label="Amazon [AMZN]", command=display_amazon)
    gachamenu.add_separator()
    gachamenu.add_command(label="Apple [APPL]", command=display_apple)
    gachamenu.add_separator()
    gachamenu.add_command(label="Gamestop [GME]", command=display_gamestop)
    gachamenu.add_separator()
    gachamenu.add_command(label="Google [GOOG]", command=display_google)
    gachamenu.add_separator()
    gachamenu.add_command(label="Microsoft [MSFT]", command=display_microsoft)
    gachamenu.add_separator()
    gachamenu.add_command(label="Tesla [TSLA]", command=display_tesla)

    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="Features and Help", command="")
    helpmenu.add_command(label="The data", command="")
    helpmenu.add_command(label="About us", command="")
    helpmenu.add_command(label="Quit", command=quit, accelerator="Alt+q")




    # -------------------------------------------------------------------------------------------------------------

    # create left lower frame
    #leftside = Frame(root, width=120, height=400, bg='red')
    #leftside.grid(row=3, column=0, sticky="N", pady=15)

    # create main/standard site


    # Create right span
    rightside = Frame(root, width=220)
    rightside.grid(row=0,  column=1)

    # create right thing)
    rightside1 = Frame(rightside, width=220, height=200, bg='#bed1bc')
    rightside1.grid(row=0, column=0, rowspan=1, sticky='N', pady=5)

    # create right thing)
    rightside2 = Frame(rightside, width=220, height=100, bg='#bed1bc')
    rightside2.grid(row=1, column=0, rowspan=1, sticky='NSEW', pady=5)

    # create right thing)
    rightside3 = Frame(rightside, width=220, height=300, bg='#bed1bc')
    rightside3.grid(row=2, column=0, rowspan=1, sticky='S', pady=5)

    # create upper buttonpack Datum) erstellen
    #template_buttonpack_filter = Frame(root, bg="")
    #template_buttonpack_filter.grid(row=0, column=1, sticky='NSEW', pady=5, padx=5)

    # create lower bracket
    lowerside = Frame(root, height=50, width=1330,bg="#7c877b")
    lowerside.grid(row=1, column=0, columnspan=2)

    # create lower text
    lowerside_text = Label(root, text="Entwicklung und Implementierung eines Prognose-Systems für augewählte Kurse - prototyp",bg="#7c877b")
    lowerside_text.grid(row=1, column=0, columnspan=2, sticky=NSEW)

    # Liste der Aktien erstellen
    gui_list = Listbox(rightside, bg="#a4bfa1", width=30, height=6)
    gui_list.grid(row=0, column=0, rowspan=1, pady=35, sticky=N)

    # Liste befüllen >>>
    list_main_stocks = ["Amazon", "Apple", "Gamestop", "Google", "Microsoft", "Tesla"]

    for item in list_main_stocks:
        gui_list.insert(END, item)

    # text (rightside)
    rightside1_text = Label(rightside, text="Auswahl der Aktie", bg="#bed1bc", font=("times",14, "bold"))
    rightside1_text.grid(row=0, column=0, sticky=N, pady=5)
    rightside2_text = Button(rightside, text="regenerate data", bg="#bed1bc", font=('Helvetica',12, "bold"), command=display_generate)
    rightside2_text.grid(row=1, column=0)
    rightside3_text = Label(rightside, text="", bg="#bed1bc")
    rightside3_text.grid(row=2, column=0, sticky=W, padx=5)


        # standardmäßig klasse als Vorlage nehmen, die keinen Graph zeigt
    button_confirm = Button(rightside,  text="Aktie auswählen", bg="#bed1bc", font=('Helvetica',12, "bold"), command=display)
    button_confirm.grid(column=0, row=0, sticky=S, pady=20)


    #window.title("Displaying a Website")
    #window.geometry("1600x500")
    root.mainloop()
    cef.Shutdown()

#class BlankFrame():


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


    # URLURLURL
    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        window_info.SetAsChild(self.get_window_handle(), rect)
        self.browser = cef.CreateBrowserSync(window_info,
                                             url=url1)


                                            # url ändern, je nach flash-funktion

        #target -> HTML bei github hochgeladen & per Pages gepublished (vorerst/provisorisch)
        #https://stackoverflow.com/questions/67996093/how-to-use-cefpython-to-add-a-webbrowser-widget-in-a-tkinter-window
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

start_gui()
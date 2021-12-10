import tkinter as tk
from tkinter import *
from cefpython3 import cefpython as cef
import ctypes




def main():
    root = Tk()
    cef.Initialize()

    root.geometry("1400x700")
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

    # EVENTS
    root.bind("<Alt-q>", quit)

    # MENU
    menu = Menu(root)
    root.config(menu=menu)
    # obere Leiste - menu
    filemenu = Menu(menu)
    menu.add_cascade(label="Aktien", menu=filemenu)
    filemenu.add_command(label="A", command="")
    filemenu.add_command(label="B", command="")
    filemenu.add_command(label="C", command="")
    filemenu.add_command(label="Open...", command="")
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)

    gachamenu = Menu(menu)
    menu.add_cascade(label="Kurs", menu=gachamenu)
    gachamenu.add_command(label="Bla", command="")

    steammenu = Menu(menu)
    menu.add_cascade(label="???", menu=steammenu)
    steammenu.add_command(label="a", command="")

    servermenu = Menu(menu)
    menu.add_cascade(label="Hello there", menu=servermenu)
    servermenu.add_command(label="asda", command="")

    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="Keybinds", command="")
    helpmenu.add_command(label="Resolution", command="")
    helpmenu.add_command(label="About...", command="")
    helpmenu.add_command(label="Quit", command=quit, accelerator="Alt+q")



    # -------------------------------------------------------------------------------------------------------------

    # create left lower frame
    #leftside = Frame(root, width=120, height=400, bg='red')
    #leftside.grid(row=3, column=0, sticky="N", pady=15)

    # create frame main with chart packed
    mainside = Frame(root, bg='black', height=500)
    mainside.grid(row=1, column=1, columnspan=1, rowspan=3, sticky='NSWE', pady=5, padx=5)

    # Create right span
    rightside = Frame(root, width=220)
    rightside.grid(row=1,  column=2, rowspan=3)

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
    template_buttonpack_filter = Frame(root, bg="")
    template_buttonpack_filter.grid(row=0, column=1, sticky='NSEW', pady=5, padx=5)

    # create lower bracket
    lowerside = Frame(root, height=50, width=1350,bg="#7c877b")
    lowerside.grid(row=4, column=1, columnspan=2)

    # create lower text
    lowerside_text = Label(root, text="prototyp",bg="#7c877b")
    lowerside_text.grid(row=4, column=1, sticky=N)

    # Liste der Aktien erstellen
    gui_list = Listbox(rightside, bg="#a4bfa1", width=30)
    gui_list.grid(row=0, column=0, rowspan=1, pady=10, sticky=S)

    # Liste befüllen >>>
    list_main_stocks = ["Amazon", "Whatever", "Gamestop", "Tesla", "bla", "ayo"]

    for item in list_main_stocks:
        gui_list.insert(END, item)

    # text (rightside)
    rightside1_text = Label(rightside, text="Auswahl der Aktie", bg="#bed1bc", font=("times",14, "bold"))
    rightside1_text.grid(row=0, column=0, sticky=N, pady=5)
    rightside2_text = Label(rightside, text="TODO", bg="#bed1bc", font=('Helvetica',12, "bold"))
    rightside2_text.grid(row=1, column=0)
    rightside3_text = Label(rightside, text="+ dynamische SKalierung \n\n + Zeitfilter \n\n + Get information \n\n + Listenabhängigkeit", bg="#bed1bc")
    rightside3_text.grid(row=2, column=0, sticky=W, padx=5)


    # create functional buttons
    button_filter_time_width = 30
    button_filter_time_height = 1
    button_filter_day = Button(template_buttonpack_filter, height=button_filter_time_height, width=button_filter_time_width, text="1 Day", command="")
    button_filter_week = Button(template_buttonpack_filter, height=button_filter_time_height, width=button_filter_time_width, text="1 Week", command="")
    button_filter_month = Button(template_buttonpack_filter, height=button_filter_time_height, width=button_filter_time_width, text="1 Month", command="")
    button_filter_year = Button(template_buttonpack_filter, height=button_filter_time_height, width=button_filter_time_width, text="1 Year", command="")
    button_filter_all = Button(template_buttonpack_filter, height=button_filter_time_height, width=button_filter_time_width, text="All", command="")

    # GUI-Button-ERSTELLUNG
    button_filter_day.grid(column=0, row=0, padx=2)
    button_filter_week.grid(column=1, row=0, padx=2)
    button_filter_month.grid(column=2, row=0, padx=2)
    button_filter_year.grid(column=3, row=0, padx=2)
    button_filter_all.grid(column=4, row=0, padx=2)


    # create frame right
    #if(gui_list.get(ANCHOR)=="Tesla"):
    browser_frame = BrowserFrame(mainside)
    browser_frame.pack(fill=tk.BOTH, expand=tk.YES)


    #window.title("Displaying a Website")
    #window.geometry("1600x500")
    root.mainloop()
    cef.Shutdown()


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
        #self.focus_set()

    # URLURLURL
    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        window_info.SetAsChild(self.get_window_handle(), rect)
        self.browser = cef.CreateBrowserSync(window_info,
                                             url="https://1m4g3r.github.io/pythonWiSe21/fig.html")  #target -> HTML bei github hochgeladen & per Pages gepublished (vorerst/provisorisch)
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


'''
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
'''

main()
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from numpy import *
from pandas import *
from statistics import mode
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import insights
import db.db
import menu

class Graphs:
    def __init__(self):
        # creating tkinter window
        self.root = Tk()

        # setting window title
        self.root.title("Sunville Properties | Insights | Graphs")

        # determining size of window
        self.windowWidth = self.root.winfo_screenwidth() / 2
        self.windowHeight = self.root.winfo_screenheight() / 2

        # determining the the positon to set the window
        self.positionRight = int(self.root.winfo_screenwidth() / 2 - self.windowWidth / 2)
        self.positionDown = int(self.root.winfo_screenheight() / 2 - self.windowHeight / 2)

        # Positions the window in the center of the page.
        self.root.geometry(
            "{}x{}+{}+{}".format(int(self.windowWidth), int(self.windowHeight), self.positionRight, self.positionDown))

        # disable resize of window
        self.root.resizable(False, False)

    def graphs(self):
        self.df = read_csv('D:/python/classes/Internship/property(dataset).csv')

        """# getting image
        self.image1 = Image.open("D:/python/classes/Internship/property-consultants-mumbai.jpg")
        self.image1 = self.image1.resize((int(self.windowWidth), int(self.windowHeight)), Image.ANTIALIAS)
        self.image_bg = ImageTk.PhotoImage(self.image1, master=self.root)

        self.root.columnconfigure(3, minsize=100)
        # placing image
        self.background_label = Label(self.root, image=self.image_bg)
        self.background_label.place(x=0, y=0)"""

        self.Menu = Button(self.root, text="Menu", bg="Black", fg="Red", command=self.menu, width=5)
        self.Menu.place(x=0, y=0)

        self.Back = Button(self.root, text="Back", bg="Black", fg="Red", command=self.back, width=5)
        self.Back.place(x=0, y=30)

        self.parent_frame = Frame(self.root, bg = "White")
        self.parent_frame.pack()


        self.graph_chg = Button(self.parent_frame, text="Time Series", bg="Black", fg="Red", command=lambda :self.next(self.graph_chg), width=10)
        self.graph_chg.pack(side = LEFT, anchor=N)

        self.frame = Frame(self.parent_frame, bg = "White")
        self.frame.pack()

        self.frame1 = LabelFrame(self.frame, text = "Agent performance", bg = "White")
        self.frame1.pack(side = LEFT, expand = True, fill = BOTH)

        agent_year = ['2017', '2018', '2019', '2020', '2017-2020']
        self.year_agent = ttk.Combobox(self.frame1, values=agent_year, state='readonly')
        self.year_agent.current(0)
        self.year_agent.bind('<<ComboboxSelected>>', self.agent_performance)
        self.year_agent.pack()

        self.agent_performance()

        self.root.mainloop()

    def agent_performance(self, event=None):
        year = self.year_agent.get()
        df = self.df.infer_objects()
        db.db.cursor.execute("SELECT `AGENT_NAME` from `agents`")
        records = db.db.cursor.fetchall()
        self.agents_list = []
        area = 0
        self.area_list = []
        a = df['Tenure'].size
        for i in records:
            for j in i:
                self.agents_list.append(j)

        if year == '2017' or year == '2018' or year == '2019' or year == '2020':

            try:
                self.canvas.get_tk_widget().pack_forget()
                self.toolbar.pack_forget()
            except AttributeError:
                pass
            for i in self.agents_list:
                area = 0
                for j in range(a):
                    if df['Year'][j] == year:
                        if df['Agent'][j] == i:
                            if df['UoM'][j] == 'HA':
                                area += (df['Area'][j] * 10000)

                            elif df['UoM'][j] == 'SQ-M':
                                area += df['Area'][j]
                self.area_list.append('%0.2f' % area)
            self.area_list = [float(i) for i in self.area_list]

            x = arange(len(self.agents_list))
            f = plt.Figure(figsize=(5,5), dpi=100, tight_layout=True)
            a = f.add_subplot(111)
            a.bar(x, self.area_list)
            a.set_xticks(x)
            a.set_xticklabels(self.agents_list, rotation=60)
            a.set_xlabel('Agents')
            a.set_ylabel('Area(owned+leased) SQ-M')


            #plt.show()
            self.canvas = FigureCanvasTkAgg(f, self.frame1)
            self.canvas.draw()
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame1)
            self.toolbar.update()
            self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)



        elif year == '2017-2020':
            try:
                self.canvas.get_tk_widget().pack_forget()
                self.toolbar.pack_forget()
            except AttributeError:
                pass
            for i in self.agents_list:
                area = 0
                for j in range(a):
                    if df['Agent'][j] == i:
                        if df['UoM'][j] == 'HA':
                            area += (df['Area'][j] * 10000)

                        elif df['UoM'][j] == 'SQ-M':
                            area += df['Area'][j]
                self.area_list.append('%0.2f' % area)
            self.area_list = [float(i) for i in self.area_list]

            x = arange(len(self.agents_list))
            f = plt.Figure(figsize=(5,6), dpi=100)
            a = f.add_subplot(111)
            f.subplots_adjust(bottom =0.338, top = 0.945, left=0.171, right=0.94)
            a.bar(x, self.area_list)
            a.set_xticks(x)
            a.set_xticklabels(self.agents_list, rotation=60)
            a.set_xlabel('Agents')
            a.set_ylabel('Area(owned+leased) SQ-M')

            # plt.show()
            self.canvas = FigureCanvasTkAgg(f, self.frame1)
            self.canvas.draw()
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame1)
            self.toolbar.update()
            self.canvas.get_tk_widget().pack()


    def time_analysis(self):

        try:
            self.canvas1.get_tk_widget().pack_forget()
            self.toolbar1.pack_forget()
        except AttributeError:
            pass

        db.db.cursor.execute("SELECT `ORD_DATE` FROM `orders` ORDER BY `orders`.`ORD_DATE` ASC")
        records1 = db.db.cursor.fetchall()

        date = []

        for i in records1:
            for j in i:
                date.append(j)

        db.db.cursor.execute("SELECT `ORD_AMOUNT` FROM `orders` ORDER BY `orders`.`ORD_DATE` ASC")
        records2 = db.db.cursor.fetchall()

        ord_amt = []

        for i in records2:
            for j in i:
                ord_amt.append(j)
        ord_amt = [float(i) for i in ord_amt]

        #plt.plot_date(date, ord_amt, linestyle = 'solid')
        #plt.gcf().autofmt_xdate()
        #plt.tight_layout()
        fig = plt.Figure(figsize=(5.5,5),dpi=100)
        fig.add_subplot(111).plot(date, ord_amt,"bo", linestyle = "solid")
        fig.subplots_adjust(top=0.93, left=0.09, right=0.988)
        fig.autofmt_xdate()
        self.canvas1 = FigureCanvasTkAgg(fig, self.frame2)
        self.canvas1.draw()
        self.toolbar1 = NavigationToolbar2Tk(self.canvas1, self.frame2)
        self.toolbar1.update()
        self.canvas1.get_tk_widget().pack()
        #plt.show()

    def menu(self):
        self.root.destroy()
        x = menu.Menu()
        x.menu()

    def back(self):
        self.root.destroy()
        x = insights.Insights()
        x.insights()
    def next(self, widget):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        self.frame2 = LabelFrame(self.frame, text="Time series analysis of orders", bg = "White")
        self.frame2.pack(side=LEFT, expand=True, fill=BOTH)

        widget.config(text="Agent performance", width=15, command=lambda :self.next1(widget))
        self.time_analysis()

    def next1(self, widget):
        for widgets in self.frame.winfo_children():
            widgets.destroy()

        self.frame1 = LabelFrame(self.frame, text="Agent performance", bg = "White")
        self.frame1.pack(side=LEFT, expand=True, fill=BOTH)

        agent_year = ['2017', '2018', '2019', '2020', '2017-2020']
        self.year_agent = ttk.Combobox(self.frame1, values=agent_year, state='readonly')
        self.year_agent.current(0)
        self.year_agent.bind('<<ComboboxSelected>>', self.agent_performance)
        self.year_agent.pack()

        widget.config(text="Time Series", width=10, command=lambda: self.next(widget))
        self.agent_performance()


if __name__ == "__main__":
    x = Graphs()
    x.graphs()
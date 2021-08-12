from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
from numpy import *
from pandas import *
from statistics import mode
import matplotlib.pyplot as plt
import db.db
import menu


class Insights:

    def __init__(self):
        # creating tkinter window
        self.root = Tk()

        # Setting title
        self.root.title("Sunville Properties | Insights")

        # determining size of the window
        self.windowWidth = self.root.winfo_screenwidth() / 2
        self.windowHeight = self.root.winfo_screenheight() / 2

        # determining the the positon to set the window
        self.positionRight = int(self.root.winfo_screenwidth() / 2 - self.windowWidth / 2)
        self.positionDown = int(self.root.winfo_screenheight() / 2 - self.windowHeight / 2)

        # Positions the window in the center of the page.
        self.root.geometry(
            "{}x{}+{}+{}".format(int(self.windowWidth), int(self.windowHeight), self.positionRight, self.positionDown))

        # disable resize of window
        # self.root.resizable(False, False)

    def insights(self):
        self.df = read_csv('D:/python/classes/Internship/property(dataset).csv')
        self.leased_var = StringVar()
        self.owned_var = StringVar()
        self.CA_var = StringVar()
        self.WS_var = StringVar()
        self.agent_var = StringVar()
        self.area_var = StringVar()
        # getting image
        self.image1 = Image.open("D:/python/classes/Internship/property-consultants-mumbai.jpg")
        self.image1 = self.image1.resize((int(self.windowWidth), int(self.windowHeight)), Image.ANTIALIAS)
        self.image_bg = ImageTk.PhotoImage(self.image1, master=self.root)

        # placing image
        self.background_label = Label(self.root, image=self.image_bg)
        self.background_label.place(x=0, y=0)

        self.Menu = Button(self.root, text="Menu", bg="Black", fg="Red", command=self.menu, width=5)
        self.Menu.place(x=0, y=0)

        self.head0_lab = Label(self.root, text="Total area owned/leased", bg="beige")
        self.head0_lab.grid(row=0, column=0, columnspan=3, padx=40, pady=(20, 0))

        self.date_lab = Label(self.root, text="Year", bg="White")
        self.date_lab.grid(row=1, column=0, padx=(40, 0))

        self.date = ttk.Combobox(self.root, values=[2017, 2018, 2019], state="readonly")
        self.date.grid(row=1, column=1)
        self.date.current(0)
        self.date.focus()
        self.date.bind('<Return>', self.data)
        self.data()
        self.ok = Button(self.root, text="Okay", bg="black", fg="Red", command=self.data,
                         font=("times new roman", 10, 'bold'), relief=RIDGE, width=10)
        self.ok.grid(row=1, column=2, padx=10)

        self.leased_lab = Label(self.root, text="Leased", bg="white")
        self.leased_lab.grid(row=2, column=0, padx=(40, 0), pady=5)

        self.leased = Entry(self.root, textvariable=self.leased_var, relief=RIDGE, bd=2, state="readonly")
        self.leased.grid(row=2, column=1, pady=5)

        self.owned_lab = Label(self.root, text="Owned", bg="white")
        self.owned_lab.grid(row=3, column=0, padx=(40, 0), pady=5)

        self.owned = Entry(self.root, textvariable=self.owned_var, relief=RIDGE, bd=2, state="readonly")
        self.owned.grid(row=3, column=1, pady=5)

        self.head_label = Label(self.root, text="Max Area leased", bg="beige")
        self.head_label.grid(row=4, column=0, columnspan=2, pady=10, padx=40)

        self.CA_lab = Label(self.root, text="CA Countries", bg="White")
        self.CA_lab.grid(row=5, column=0, pady=5, padx=(40, 0))

        self.CA = Entry(self.root, textvariable=self.CA_var, relief=RIDGE, bd=2, state="readonly")
        self.CA.grid(row=5, column=1, pady=5)

        self.WS_lab = Label(self.root, text="WS Countries", bg="White")
        self.WS_lab.grid(row=6, column=0, pady=5, padx=(40, 0))

        self.WS = Entry(self.root, textvariable=self.WS_var, relief=RIDGE, bd=2, state="readonly")
        self.WS.grid(row=6, column=1, pady=5)
        self.CA_WS()

        self.head2_lab = Label(self.root, text="Agents with deals as owned", bg="beige")
        self.head2_lab.grid(row=7, column=0, columnspan=4, pady=10, )

        self.agents_table = ttk.Treeview(self.root, height=5, show="headings")
        self.agents_table['columns'] = ['column 1', 'column 2', 'column 3', 'column 4']

        self.agents_table.column("column 1", width=80, minwidth=65, stretch=NO)
        self.agents_table.column("column 2", width=100, minwidth=90, stretch=NO)
        self.agents_table.column("column 3", width=100, minwidth=90, stretch=NO)
        self.agents_table.column("column 4", width=90, minwidth=70, stretch=NO)

        self.agents_table.heading("column 1", text="AGENT_CODE")
        self.agents_table.heading("column 2", text="AGENT_NAME")
        self.agents_table.heading("column 3", text="WORKING_AREA")
        self.agents_table.heading("column 4", text="PHONE_NO")

        self.agents_table.grid(row=8, column=0, columnspan=4, rowspan=6, padx=10)

        self.agents()

        self.head3_lab = Label(self.root, text="Maximums deals leased", bg="beige")
        self.head3_lab.grid(row=0, column=4, padx=10, pady=(20, 5), columnspan=3)
        self.city_lab = Label(self.root, text="City", bg="White")
        self.city_lab.grid(row=1, column=4, pady=5)

        df = self.df.infer_objects()

        a = df['City'].size
        my_dict = {}
        city1 = []
        for i in range(a):
            my_dict[df['City'][i]] = i

        for keys in my_dict.keys():
            city1.append(keys)
        c = city1.index('Chilliwack')
        city = []
        city.append(city1[c])
        city1.pop(c)
        for citys in city1:
            city.append(citys)

        self.city = ttk.Combobox(self.root, values=city, state='readonly', font=('times new roman', 10, ''))
        self.city.grid(row=1, column=5, pady=5)
        self.city.current(0)
        self.city.bind('<Return>', self.citys)

        self.ok1 = Button(self.root, text="Okay", bg="black", fg="Red", command=self.citys,
                          font=("times new roman", 10, 'bold'), relief=RIDGE, width=10)
        self.ok1.grid(row=1, column=6, padx=10)

        self.agent_lab = Label(self.root, text="Agent", bg="White")
        self.agent_lab.grid(row=2, column=4, pady=5)
        self.agent = Entry(self.root, textvariable=self.agent_var, relief=RIDGE, bd=2, state="readonly")
        self.agent.grid(row=2, column=5, pady=5)
        self.citys()

        self.head4_lab = Label(self.root, text="Agent performance", bg="beige")
        self.head4_lab.grid(row=3, column=4, columnspan=3, pady=5)

        self.year_agent_lab = Label(self.root, text="Year", bg="White")
        self.year_agent_lab.grid(row=4, column=4)

        agent_year= ['2017', '2018', '2019', '2020', '2017-2020']
        years = [2017, 2018, 2019, 2020]

        self.year_agent = ttk.Combobox(self.root, values= agent_year, state='readonly')
        self.year_agent.current(0)
        self.year_agent.bind('<Return>', self.agent_performance)
        self.year_agent.grid(row=4, column=5)

        self.agent_perf = Button(self.root, text="Agent Performance", bg="Black", fg="Red", width=15, relief=RIDGE,
                                 font=("times new roman", 10, 'bold'), command=self.agent_performance)
        self.agent_perf.grid(row=5, column=4, columnspan=3, pady=5)

        self.head5_lab = Label(self.root, text="Area sold in July", bg="beige")
        self.head5_lab.grid(row=6, column=4, columnspan=3, pady=5)


        self.year_lab = Label(self.root, text="Year", bg="White")
        self.year_lab.grid(row=7, column=4)
        self.year = ttk.Combobox(self.root, values=years, state='readonly')
        self.year.current(0)
        self.year.bind('<Return>', self.area_sold)
        self.year.grid(row=7, column=5)
        self.area_sold()

        self.ok2 = Button(self.root, text="Okay", bg="black", fg="Red", command=self.area_sold,
                          font=("times new roman", 10, 'bold'), relief=RIDGE, width=10)
        self.ok2.grid(row=7, column=6, padx=10)

        self.area_lab = Label(self.root, text="Area Sold", bg="white")
        self.area_lab.grid(row=8, column=4)

        self.area = Entry(self.root, textvariable=self.area_var, bg="White", relief=RIDGE, state='readonly', bd=2)
        self.area.grid(row=8, column=5)

        self.head6_lab = Label(self.root, text="Time analysis of orders", bg="beige")
        self.head6_lab.grid(row=9, column=4, columnspan=3, pady=5)

        self.time_ana = Button(self.root, text="Time Analysis", bg="Black", fg="Red", width=15, relief=RIDGE,
                               font=("times new roman", 10, 'bold'), command=self.time_analysis)
        self.time_ana.grid(row=10, column=4, columnspan=3, pady=5)

        self.root.mainloop()

    def data(self, event=None):

        year = self.date.get()
        leased = 0
        owned = 0
        df = self.df.infer_objects()
        a = df['Tenure'].size
        for i in range(a):
            if df['Year'][i] == year:
                if df['Tenure'][i] == "Leased":
                    if df['UoM'][i] == 'HA':
                        leased += (df['Area'][i] * 10000)
                    else:
                        leased += df['Area'][i]
                else:
                    if df['UoM'][i] == 'HA':
                        owned += (df['Area'][i] * 10000)
                    else:
                        owned += df['Area'][i]
        self.leased_var.set('%.2f' % leased)
        self.owned_var.set('%.2f' % owned)

    def CA_WS(self):

        sum17 = 0
        sum18 = 0
        sum19 = 0
        sum20 = 0
        sum17_WS = 0
        sum18_WS = 0
        sum19_WS = 0
        sum20_WS = 0
        df = self.df.infer_objects()
        a = df['Country'].size
        for i in range(a):
            if df['Country'][i] == "CA":
                if df['Year'][i] == '2017':
                    if df['UoM'][i] == 'HA':
                        sum17 += (df['Area'][i] * 10000)
                    else:
                        sum17 += df['Area'][i]
                elif df['Year'][i] == '2018':
                    if df['UoM'][i] == 'HA':
                        sum18 += (df['Area'][i] * 10000)
                    else:
                        sum18 += df['Area'][i]
                elif df['Year'][i] == '2019':
                    if df['UoM'][i] == 'HA':
                        sum19 += (df['Area'][i] * 10000)
                    else:
                        sum19 += df['Area'][i]
                elif df['Year'][i] == '2020':
                    if df['UoM'][i] == 'HA':
                        sum20 += (df['Area'][i] * 10000)
                    else:
                        sum20 += df['Area'][i]
            elif df['Country'][i] == "WS":
                if df['Year'][i] == '2017':
                    if df['UoM'][i] == 'HA':
                        sum17_WS += (df['Area'][i] * 10000)
                    else:
                        sum17_WS += df['Area'][i]
                elif df['Year'][i] == '2018':
                    if df['UoM'][i] == 'HA':
                        sum18_WS += (df['Area'][i] * 10000)
                    else:
                        sum18_WS += df['Area'][i]
                elif df['Year'][i] == '2019':
                    if df['UoM'][i] == 'HA':
                        sum19_WS += (df['Area'][i] * 10000)
                    else:
                        sum19_WS += df['Area'][i]
                elif df['Year'][i] == '2020':
                    if df['UoM'][i] == 'HA':
                        sum20_WS += (df['Area'][i] * 10000)
                    else:
                        sum20_WS += df['Area'][i]
        ans_c = '%.2f' % max(sum20, sum19, sum18, sum17) + '        SQ-M'
        ans_w = '%.2f' % max(sum20_WS, sum19_WS, sum18_WS, sum17_WS) + '          SQ-M'
        self.CA_var.set(ans_c)
        self.WS_var.set(ans_w)

    def agents(self):
        df = self.df.infer_objects()
        a = df['Tenure'].size
        my_dict = {}
        my_list = []
        for i in range(a):
            if df['Tenure'][i] == 'Owned':
                my_dict[df['Agent'][i]] = df['Identifier'][i]
        for keys in my_dict.keys():
            my_list.append(keys)

        db.db.cursor.execute("SELECT `AGENT_CODE`, `AGENT_NAME`, `WORKING_AREA`, `PHONE_NO` FROM `agents` WHERE "
                             "`AGENT_NAME` IN " + str(tuple(tuple(my_list))))
        record = db.db.cursor.fetchall()

        for i in record:
            self.agents_table.insert("", 'end', values=i)

    def citys(self, event=None):
        df = self.df.infer_objects()
        a = df['Tenure'].size
        city = self.city.get()
        agent = []
        for i in range(a):
            if df['Tenure'][i] == 'Leased' and df['City'][i] == city:
                agent.append(df['Agent'][i])
        agent_mode = mode(agent)
        self.agent_var.set(agent_mode)

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
            # plt.figure(num=None, figsize=(10, 8), dpi=80, facecolor='w', edgecolor='k')
            plt.bar(x, self.area_list)
            plt.xticks(x, self.agents_list, rotation=60, fontfamily='corbel', fontsize=12)
            plt.xlabel('Agents')
            plt.ylabel('Area(owned+leased) SQ-M')
            plt.tight_layout()
            plt.show()

        elif year == '2017-2020':
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
            # plt.figure(num=None, figsize=(10, 8), dpi=80, facecolor='w', edgecolor='k')
            plt.bar(x, self.area_list)
            plt.xticks(x, self.agents_list, rotation=60, fontfamily='corbel', fontsize=12)
            plt.xlabel('Agents')
            plt.ylabel('Area(owned+leased) SQ-M')
            plt.tight_layout()
            plt.show()


    def area_sold(self, event=None):
        df = self.df.infer_objects()
        area = 0
        year = self.year.get()
        for i in range(len(df['Area'])):
            if df['Year'][i] == year:
                if df['UoM'][i] == 'HA':
                    area += (df['Area'][i] * 10000)

                elif df['UoM'][i] == 'SQ-M':
                    area += df['Area'][i]
        ans = '%0.2f' % area + '     SQ-M'
        self.area_var.set(ans)


    def time_analysis(self):

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

        plt.plot_date(date, ord_amt, linestyle = 'solid')
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.show()

    def menu(self):
        self.root.destroy()
        x = menu.Menu()
        x.menu()


if __name__ == "__main__":
    x = Insights()
    x.insights()

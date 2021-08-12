from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
from datetime import *
import db.db
import menu


class orders_lookup:
    def __init__(self):

        # creating tkinter window
        self.root = Tk()
        self.top = Toplevel(self.root)
        self.top.destroy()

        # Setting title
        self.root.title("Sunville Properties | Orders")

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
        self.root.resizable(False, False)
        self.date = 1
        self.firstclick = 1

    def validate_num(self, number):
        try:
            float('%s' % number)
            # messagebox.showinfo("ok", "number")
            return True
        except ValueError:
            return False
    def Num_validate(self, num, widget, event=None):
        if self.validate_num(num) or num == "":
            widget.config(bg="White")
        else:
            widget.config(bg="Red")

    def validate_date(self, date):
        if date=='yyyy-mm-dd':
            return True
        else:
            try:
                datetime.strptime(date, '%Y-%m-%d')
                return True
            except ValueError:
                return False

    def Date_validate(self, date, widget, event=None):
        if self.validate_date(date) or date == "":
            widget.config(bg="White")
        else:
            widget.config(bg="Red")

    def cal_func(self, event=None):
        def calval(event=None):
            self.date_var.set(cal.get_date())
            self.top.destroy()
            self.order_date.config(bg="White")
            self.date = 1

        if self.firstclick == 1:
            self.date_var.set("")
            self.firstclick = 2

        if self.date == 1:
            self.top = Toplevel(self.root)
            # Positions the window in the center of the page.
            self.top.geometry(
                "+{0}+{1}".format(self.positionRight,
                                  self.positionDown))
            cal = Calendar(self.top, font="Arial 14", selectmode="day", year=datetime.today().year,
                           month=datetime.today().month, day=datetime.today().day, date_pattern='yyyy-mm-dd')
            cal.pack()
            btn = Button(self.top, text="Ok", command=calval)
            btn.pack()
            self.date = 2

    def destroycal(self, event=None):
        if self.top.winfo_exists():
            self.top.destroy()
            self.date = 1

    def orders(self):

        self.query = "SELECT * from `orders` WHERE 1"

        # getting image
        self.image1 = Image.open("D:/python/classes/Internship/property-consultants-mumbai.jpg")
        self.image1 = self.image1.resize((int(self.windowWidth), int(self.windowHeight)), Image.ANTIALIAS)
        self.image_bg = ImageTk.PhotoImage(self.image1, master=self.root)

        # placing image
        self.background_label = Label(self.root, image=self.image_bg)
        self.background_label.place(x=0, y=0)

        self.Menu = Button(self.root, text="Menu", bg="Black", fg="Red", command=self.menu, width=5)
        self.Menu.place(x=0, y=0)

        # Entry fields and labels for search
        self.order_no_lab = Label(self.root, text="Order number", bg="White")
        self.order_no_lab.grid(row=0, column=0, sticky=E, padx=10, pady=(50, 0))

        self.order_no = Entry(self.root, bd=2, relief=RIDGE)
        self.order_no.bind("<Return>", self.search)
        self.order_no.bind('<FocusIn>', self.destroycal)
        self.order_no.bind('<FocusOut>', lambda e:self.Num_validate(self.order_no.get(),self.order_no))
        self.order_no.grid(row=0, column=1, sticky=W, padx=(0, 10), pady=(50, 0))

        self.order_date_lab = Label(self.root, text="Order date ", bg="White")
        self.order_date_lab.grid(row=0, column=2, sticky=E, pady=(50, 0))
        self.date_var = StringVar()
        self.date_var.set("yyyy-mm-dd")

        self.order_date = Entry(self.root, bd=2, relief=RIDGE, textvariable=self.date_var)
        #self.order_date.bind('<FocusIn>', self.clear_date)
        self.order_date.bind('<Button-1>', lambda e: self.cal_func())
        self.order_date.bind("<Return>", self.search)
        self.order_date.bind('<FocusOut>', lambda e: self.Date_validate(self.date_var.get(), self.order_date))
        self.order_date.grid(row=0, column=3, sticky=W, pady=(50, 0))

        self.cus_code_lab = Label(self.root, text="Customer code", bg="White")
        self.cus_code_lab.grid(row=0, column=4, sticky=E, pady=(50, 0))

        self.cus_code = Entry(self.root, bd=2, relief=RIDGE)
        self.cus_code.bind("<Return>", self.search)
        self.cus_code.bind('<FocusIn>', self.destroycal)
        self.cus_code.grid(row=0, column=5, sticky=W, pady=(50, 0))

        # search button

        self.search_btn = Button(self.root, text="Search", font=("times new roman", 10, "bold"), bg="#1C1B1B", fg="red",
                                 width=10, command=self.search, relief=RAISED, bd=3)
        self.search_btn.grid(row=1, column=0, columnspan=6, pady=(10, 0))

        # clear button
        self.clear_btn = Button(self.root, text="Clear", font=("times new roman", 10, "bold"), bg="#1C1B1B", fg="red",
                            width=10, command=self.clear, relief=RAISED, bd=3)
        self.clear_btn.grid(row=2, column=0, columnspan=6, pady=(10, 0))

        # creating treeview for table
        self.table = ttk.Treeview(self.root, height=10)

        # creating columns
        self.table["columns"] = ("column 2", "column 3", "column 4", "column 5", "column 6", "column 7")

        # formating columns
        self.table.column("#0", width=80, minwidth=65, stretch=NO)
        self.table.column("column 2", width=100, minwidth=90, stretch=NO)
        self.table.column("column 3", width=140, minwidth=120, stretch=NO)
        self.table.column("column 4", width=90, minwidth=70, stretch=NO)
        self.table.column("column 5", width=100, minwidth=80, stretch=NO)
        self.table.column("column 6", width=100, minwidth=80, stretch=NO)
        self.table.column("column 7", width=140, minwidth=120, stretch=NO)

        # defining headings
        self.table.heading("#0", text="ORD_NUM")
        self.table.heading("column 2", text="ORD_AMOUNT")
        self.table.heading("column 3", text="ADVANCE_AMOUNT")
        self.table.heading("column 4", text="ORD_DATE")
        self.table.heading("column 5", text="CUST_CODE")
        self.table.heading("column 6", text="AGENT_CODE")
        self.table.heading("column 7", text="ORD_DESCRIPTION")

        # getting records to insert into treeview
        db.db.cursor.execute(self.query)
        records = db.db.cursor.fetchall()

        # inserting records into treeview
        for i in records:
            self.table.insert("", 'end', text=i[0], values=i[1:])

        # placing the treeview
        self.table.grid(row=3, column=0, columnspan=6, padx=(10, 10), pady=(20, 0))

        self.root.mainloop()

    def search(self, Event=None):
        self.order_num = self.order_no.get()
        self.ord_dated = self.order_date.get()
        self.cus_cod = self.cus_code.get()

        # 1 search field is used

        if self.order_num != "" and self.ord_dated == "" and self.cus_cod == "":
            self.one("ORD_NUM", self.order_num)

        if self.order_num == "" and self.ord_dated != "" and self.cus_cod == "":
            self.one("ORD_DATE", self.ord_dated)

        if self.order_num == "" and self.ord_dated == "" and self.cus_cod != "":
            self.one("CUST_CODE", self.cus_cod)

        # 2 search fields are used

        if self.order_num != "" and self.ord_dated != "" and self.cus_cod == "":
            self.two("ORD_NUM", "ORD_DATE", self.order_num, self.ord_dated)

        if self.order_num != "" and self.ord_dated == "" and self.cus_cod != "":
            self.two("ORD_NUM", "CUST_CODE", self.order_num, self.cus_cod)

        if self.order_num == "" and self.ord_dated != "" and self.cus_cod != "":
            self.two("ORD_DATE", "CUST_CODE", self.ord_dated, self.cus_cod)

        # all 3 search fields are used
        if self.order_num != "" and self.ord_dated != "" and self.cus_cod != "":
            self.three("ORD_NUM", "ORD_DATE", "CUST_CODE", self.order_num, self.ord_dated, self.cus_cod)

    def one(self, column, value):

        self.query = "SELECT * FROM `orders` WHERE `%s` = '%s'"

        db.db.cursor.execute(self.query % (column, value))
        records = db.db.cursor.fetchall()

        if records:
            self.table.delete(*self.table.get_children())
            for i in records:
                self.table.insert("", 'end', text=i[0], values=i[1:])
        else:
            messagebox.showerror("error", "No Record Exists")

    def two(self, column1, column2, value1, value2):

        self.query = "SELECT * FROM `orders` WHERE `%s` = '%s' AND `%s` = '%s'"

        db.db.cursor.execute(self.query % (column1, value1, column2, value2))
        records = db.db.cursor.fetchall()

        if records:
            self.table.delete(*self.table.get_children())
            for i in records:
                self.table.insert("", 'end', text=i[0], values=i[1:])
        else:
            messagebox.showerror("error", "No Record Exists")

    def three(self, column1, column2, column3, value1, value2, value3):

        self.query = "SELECT * FROM `orders` WHERE `%s` = '%s' AND `%s` = '%s' AND `%s` = '%s'"

        db.db.cursor.execute(self.query % (column1, value1, column2, value2, column3, value3))
        records = db.db.cursor.fetchall()

        if records:
            self.table.delete(*self.table.get_children())
            for i in records:
                self.table.insert("", 'end', text=i[0], values=i[1:])
        else:
            messagebox.showerror("error", "No Record Exists")

    def clear(self):
        self.order_no.delete(0, 'end')
        self.order_date.delete(0, 'end')
        self.order_date.insert(0,"yyyy-mm-dd")
        self.cus_code.delete(0, 'end')

        self.order_no.config(bg = "white")
        self.order_date.config(bg = "white")
        self.cus_code.config(bg = "white")

        # reseting treeview
        self.table.delete(*self.table.get_children())

        # setting query
        self.query = "SELECT * from `orders` WHERE 1"

        # getting records to insert into treeview
        db.db.cursor.execute(self.query)
        records = db.db.cursor.fetchall()

        # inserting records into treeview
        for i in records:
            self.table.insert("", 'end', text=i[0], values=i[1:])
        self.order_date.config(bg="White")
        self.firstclick=1

    def menu(self):
        self.root.destroy()
        x = menu.Menu()
        x.menu()


if __name__ == "__main__":
    x = orders_lookup()
    x.orders()

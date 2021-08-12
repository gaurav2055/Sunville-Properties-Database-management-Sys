from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import ttk
import db.db
import menu


class ballance_amt:
    def __init__(self):

        # creating tkinter window
        self.root = Tk()

        self.root.config(bg="white")

        # Setting title
        self.root.title("Sunville Properties | Balance Amt")

        # determining size of window
        self.windowWidth = self.root.winfo_screenwidth() / 2
        self.windowHeight = self.root.winfo_screenheight() / 2

        # detriming the postion to set the window
        self.positionRight = int(self.root.winfo_screenwidth() / 2 - self.windowWidth / 2)
        self.positionDown = int(self.root.winfo_screenheight() / 2 - self.windowHeight / 2)

        # Positions the window in the center of the page.
        self.root.geometry("{0}x{1}+{2}+{3}".format(int(self.windowWidth), int(self.windowHeight), self.positionRight,
                                                    self.positionDown))

        # disable resize of window
        self.root.resizable(False, False)

    def validate_num(self, number):
        try:
            float('%s' % number)
            # messagebox.showinfo("ok", "number")
            return True
        except ValueError:
            return False

    def validate_str(self, string):
        if not (bool(re.search('\d', string))) or string == "":
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            if (regex.search(string) == None):
                return True
            else:
                return False
        else:
            return False

    def Num_validate(self, num, widget, event=None):
        if self.validate_num(num) or num == "":
            widget.config(bg="White")
        else:
            widget.config(bg="Red")

    def Str_validate(self, num, widget, event=None):
        if self.validate_str(num):
            widget.config(bg="White")
        else:
            widget.config(bg="Red")

    def balance(self):

        # getting image
        self.image1 = Image.open("D:/python/classes/Internship/property-consultants-mumbai.jpg")
        self.image1 = self.image1.resize((int(self.windowWidth), int(self.windowHeight)), Image.ANTIALIAS)
        self.image_bg = ImageTk.PhotoImage(self.image1, master=self.root)

        # placing image
        self.background_label = Label(self.root, image=self.image_bg)
        self.background_label.place(x=0, y=0)
        self.Menu = Button(self.root, text="Menu", bg="Black", fg="Red", command=self.menu, width=5)
        self.Menu.place(x=0, y=0)

        self.frame1 = Frame(self.root, bg="White")
        self.frame1.pack(pady=10, padx=75, fill=BOTH, expand=True)
        self.frame2 = Frame(self.root, bg="white")
        self.frame2.pack(padx=(0, 320), fill=BOTH, expand=True)

        self.background_label = Label(self.frame2, image=self.image_bg)
        self.background_label.place(x=0, y=-258)

        # creating search fields
        # order num search field
        # order num Label
        self.order_num_lab = Label(self.frame1, text="Order Num", bg="White")
        self.order_num_lab.grid(row=0, column=0, pady=(0, 10))

        self.var_order_num = StringVar()
        self.var_order_num.set("")

        self.order_num = Entry(self.frame1, bd=2, relief=RIDGE, textvariable =self.var_order_num)
        self.order_num.bind('<Return>', self.search)
        self.order_num.grid(row=0, column=1, pady=(0, 10))

        # agent code
        self.age_code_lab = Label(self.frame1, text="Agent Code", bg="White")
        self.age_code_lab.grid(row=0, column=2, pady=(0, 10))

        self.var_age_code = StringVar()
        self.var_age_code.set("")

        self.age_code = Entry(self.frame1, bd=2, relief=RIDGE, textvariable = self.var_age_code)
        self.age_code.bind('<Return>', self.search)
        self.age_code.grid(row=0, column=3, pady=(0, 10))

        # Agent name
        self.age_name_lab = Label(self.frame1, text="Agent Name", bg="White")
        self.age_name_lab.grid(row=0, column=4, pady=(0, 10))

        self.var_age_name = StringVar()
        self.var_age_name.set("")

        self.age_name = Entry(self.frame1, bd=2, relief=RIDGE, textvariable=self.var_age_name)
        self.age_name.bind('<Return>', self.search)
        self.age_name.bind('<FocusOut>', lambda e:self.Str_validate(self.var_age_name.get(),self.age_name))
        self.age_name.grid(row=0, column=5, pady=(0, 10))

        # search button
        self.search_btn = Button(self.frame1, text = "Search", font = ("calibri",10,"bold"), command=self.search,
                             relief=RAISED, bd=3, bg="Black", fg = "Red", width = 10)
        self.search_btn.grid(row=1, column=0, columnspan=6)

        # clear button
        self.clear_btn = Button(self.frame1, text = "Clear", font = ("calibri",10,"bold"), command=self.clear,
                             relief=RAISED, bd=3, bg="Black", fg = "Red", width = 10)
        self.clear_btn.grid(row=2, column=0, columnspan=6, pady=(10, 0))

        # creating treeview for table
        self.table = ttk.Treeview(self.frame1, show="headings", height=5)

        # creating columns
        self.table["columns"] = ("column 1", "column 2", "column 3", "column 4", "column 5", "column 6")

        # formating columns
        self.table.column("column 1", width=80, minwidth=65, stretch=NO)
        self.table.column("column 2", width=100, minwidth=90, stretch=NO)
        self.table.column("column 3", width=140, minwidth=120, stretch=NO)
        self.table.column("column 4", width=90, minwidth=70, stretch=NO)
        self.table.column("column 5", width=100, minwidth=80, stretch=NO)
        self.table.column("column 6", width=100, minwidth=80, stretch=NO)

        # defining headings
        self.table.heading("column 1", text="ORD_NUM")
        self.table.heading("column 2", text="ORD_AMOUNT")
        self.table.heading("column 3", text="ADVANCE_AMOUNT")
        self.table.heading("column 4", text="BAL_AMOUNT")
        self.table.heading("column 5", text="AGENT_CODE")
        self.table.heading("column 6", text="AGENT_NAME")

        self.query = "SELECT `ORD_NUM` , `ORD_AMOUNT`, `ADVANCE_AMOUNT`, orders.AGENT_CODE, `AGENT_NAME` FROM orders " \
                     "INNER JOIN agents ON orders.AGENT_CODE=agents.AGENT_CODE "
        db.db.cursor.execute(self.query)
        records = db.db.cursor.fetchall()
        data = []

        for i in records:
            data.append([i[0], i[1], i[2], i[1] - i[2], i[3], i[4]])

        # inserting records into treeview
        for i in data:
            self.table.insert("", 'end', values=i)

        self.table.bind('<Double 1>', self.get_row)
        self.table.grid(row=3, column=0, columnspan=6)

        # data fields

        self.ord_num_ord = StringVar()
        self.ord_amt_ord = StringVar()
        self.adv_amt_ord = StringVar()
        self.bal_amt_ord = StringVar()
        self.agent_code_ord = StringVar()
        self.agent_name_ord = StringVar()

        # order num

        self.ord_num_lab = Label(self.frame2, text="ORD_NUM", bg="White")
        self.ord_num_lab.grid(row=0, column=0, pady=10)

        self.ord_num = Entry(self.frame2, textvariable=self.ord_num_ord, bg="White", relief=RIDGE, bd=2)
        self.ord_num.grid(row=0, column=1, pady=10)
        self.ord_num.bind('<FocusOut>', lambda e: self.Num_validate(self.ord_num_ord.get(), self.ord_num))

        # order amt
        self.ord_amt_lab = Label(self.frame2, text="ORD_AMT", bg="White")
        self.ord_amt_lab.grid(row=1, column=0, pady=10)

        self.ord_amt = Entry(self.frame2, textvariable=self.ord_amt_ord, bg="White", relief=RIDGE, bd=2)
        self.ord_amt.grid(row=1, column=1, pady=10)
        self.ord_amt.bind('<FocusOut>', lambda e: self.Num_validate(self.ord_amt_ord.get(), self.ord_amt))

        # adv amt
        self.adv_amt_lab = Label(self.frame2, text="ADVANCE_AMT", bg="White")
        self.adv_amt_lab.grid(row=2, column=0, pady=10)

        self.adv_amt = Entry(self.frame2, textvariable=self.adv_amt_ord, bg="White", relief=RIDGE, bd=2)
        self.adv_amt.grid(row=2, column=1, pady=10)
        self.adv_amt.bind('<FocusOut>', lambda e: self.Num_validate(self.adv_amt_ord.get(), self.adv_amt))

        # bal amt
        self.bal_amt_lab = Label(self.frame2, text="BAL_AMT", bg="White")
        self.bal_amt_lab.grid(row=0, column=2, pady=10, padx=(20, 0))

        self.bal_amt = Entry(self.frame2, textvariable=self.bal_amt_ord, bg="White", relief=RIDGE, bd=2)
        self.bal_amt.grid(row=0, column=3, pady=10)
        self.bal_amt.bind('<FocusOut>', lambda e: self.Num_validate(self.bal_amt_ord.get(), self.bal_amt))

        # agent code
        self.agent_code_lab = Label(self.frame2, text="AGENT_CODE", bg="White")
        self.agent_code_lab.grid(row=1, column=2, pady=10, padx=(20, 0))

        self.agent_code = Entry(self.frame2, textvariable=self.agent_code_ord, bg="White", relief=RIDGE, bd=2)
        self.agent_code.grid(row=1, column=3, pady=10)

        # agent name
        self.agent_name_lab = Label(self.frame2, text="AGENT_NAME", bg="White")
        self.agent_name_lab.grid(row=2, column=2, pady=10)

        self.agent_name = Entry(self.frame2, textvariable=self.agent_name_ord, bg="White", relief=RIDGE, bd=2)
        self.agent_name.grid(row=2, column=3, pady=10)
        self.agent_name.bind('<FocusOut>', lambda e: self.Str_validate(self.agent_name_ord.get(), self.agent_name))

        self.update = Button(self.frame2, text="Update", font=("times new roman", 10, 'bold'), bg="black",
                             fg="red", command=self.btn_update, width=10)
        self.update.grid(row=3, column=0, columnspan=2, pady=10)

        self.clear_btn1 = Button(self.frame2, text="Clear", font=("times new roman", 10, 'bold'), bg="black",
                             fg="red", command=self.clear1, width=10)
        self.clear_btn1.grid(row=3, column=2, columnspan=2, pady=10)

        self.root.mainloop()

    def clear1(self):
        self.ord_num_ord.set("")
        self.ord_amt_ord.set("")
        self.adv_amt_ord.set("")
        self.bal_amt_ord.set("")
        self.agent_code_ord.set("")
        self.agent_name_ord.set("")

        self.ord_num.config(bg = "white")
        self.ord_amt.config(bg = "white")
        self.adv_amt.config(bg = "white")
        self.bal_amt.config(bg = "white")
        self.agent_name.config(bg = "white")
        self.agent_code.config(bg = "white")


    def search(self, Event=None):
        self.order_num_var = self.var_order_num.get()
        self.age_code_var = self.var_age_code.get()
        self.age_name_var = self.age_name.get()
        # 1 search field is used

        if self.order_num_var != "" and self.age_code_var == "" and self.age_name_var == "":
            self.one("ORD_NUM", self.order_num_var)

        if self.order_num_var == "" and self.age_code_var != "" and self.age_name_var == "":
            self.one("orders.AGENT_CODE", self.age_code_var)

        if self.order_num_var == "" and self.age_code_var == "" and self.age_name_var != "":
            self.one("agents.AGENT_NAME", self.age_name_var)

        # 2 search fields are used

        if self.order_num_var != "" and self.age_code_var != "" and self.age_name_var == "":
            self.two("ORD_NUM", "orders.AGENT_CODE", self.order_num_var, self.age_code_var)

        if self.order_num_var != "" and self.age_code_var == "" and self.age_name_var != "":
            self.two("ORD_NUM", "AGENT_NAME", self.order_num, self.age_name_var)

        if self.order_num_var == "" and self.age_code_var != "" and self.age_name_var != "":
            self.two("orders.AGENT_CODE", "AGENT_NAME", self.age_code_var, self.age_name_var)

        # all 3 search fields are used
        if self.order_num_var != "" and self.age_code_var != "" and self.age_name_var != "":
            self.three("ORD_NUM", "orders.AGENT_CODE", "AGENT_NAME", self.order_num, self.age_code_var, self.age_name_var)

    def one(self, column, value):
        self.query = "SELECT `ORD_NUM` , `ORD_AMOUNT`, `ADVANCE_AMOUNT`, orders.AGENT_CODE, `AGENT_NAME` FROM orders " \
                     "INNER JOIN agents ON orders.AGENT_CODE=agents.AGENT_CODE WHERE %s = '%s' "
        db.db.cursor.execute(self.query % (column, value))
        records = db.db.cursor.fetchall()

        if bool(records):
            self.table.delete(*self.table.get_children())
            data = []

            for i in records:
                data.append([i[0], i[1], i[2], i[1] - i[2], i[3], i[4]])

            # inserting records into treeview
            for i in data:
                self.table.insert("", 'end', values=i)
        elif len(records) ==0:
            messagebox.showerror("error", "No Record Exists")

    def two(self, column1, column2, value1, value2):

        self.query = "SELECT `ORD_NUM` , `ORD_AMOUNT`, `ADVANCE_AMOUNT`, orders.AGENT_CODE, `AGENT_NAME` FROM orders " \
                     "INNER JOIN agents ON orders.AGENT_CODE=agents.AGENT_CODE WHERE %s = '%s' AND %s = '%s'"
        db.db.cursor.execute(self.query % (column1, value1, column2, value2))
        records = db.db.cursor.fetchall()

        if records:
            self.table.delete(*self.table.get_children())
            data = []

            for i in records:
                data.append([i[0], i[1], i[2], i[1] - i[2], i[3], i[4]])

            # inserting records into treeview
            for i in data:
                self.table.insert("", 'end', values=i)
        else:
            messagebox.showerror("error", "No Record Exists")

    def three(self, column1, column2, column3, value1, value2, value3):

        self.query = "SELECT `ORD_NUM` , `ORD_AMOUNT`, `ADVANCE_AMOUNT`, orders.AGENT_CODE, `AGENT_NAME` FROM orders " \
                     "INNER JOIN agents ON orders.AGENT_CODE=agents.AGENT_CODE WHERE %s = '%s' AND %s = '%s' AND %s = '%s' "
        db.db.cursor.execute(self.query % (column1, value1, column2, value2, column3, value3))
        records = db.db.cursor.fetchall()
        if records:
            self.table.delete(*self.table.get_children())
            data = []

            for i in records:
                data.append([i[0], i[1], i[2], i[1] - i[2], i[3], i[4]])

            # inserting records into treeview
            for i in data:
                self.table.insert("", 'end', values=i)
        else:
            messagebox.showerror("error", "No Record Exists")


    def clear(self):
        self.order_num.delete(0, 'end')
        self.age_name.delete(0, 'end')
        self.age_code.delete(0, 'end')

        self.order_num.config(bg = "white")
        self.age_code.config(bg = "white")
        self.age_name.config(bg = "white")

        # reseting treeview
        self.table.delete(*self.table.get_children())

        self.query = "SELECT `ORD_NUM` , `ORD_AMOUNT`, `ADVANCE_AMOUNT`, orders.AGENT_CODE, `AGENT_NAME` FROM orders " \
                     "INNER JOIN agents ON orders.AGENT_CODE=agents.AGENT_CODE "
        db.db.cursor.execute(self.query)
        records = db.db.cursor.fetchall()
        data = []

        for i in records:
            data.append([i[0], i[1], i[2], i[1] - i[2], i[3], i[4]])

        # inserting records into treeview
        for i in data:
            self.table.insert("", 'end', values=i)

    def btn_update(self):
        ord_num = self.ord_num_ord.get()
        ord_amt = self.ord_amt_ord.get()
        adv_amt = self.adv_amt_ord.get()

        if self.validate_num(ord_num) and self.validate_num(ord_amt) and self.validate_num(adv_amt):
            db.db.cursor.execute("SELECT * FROM `orders` WHERE `ORD_NUM` = '%s'" % ord_num)
            record = db.db.cursor.fetchall()
            if record:
                response = messagebox.askyesno("Confirmation", "Are you sure you want to update")
                if response:
                    db.db.cursor.execute(
                        "UPDATE `orders` SET `ORD_AMOUNT` = '%s', `ADVANCE_AMOUNT` = '%s' WHERE `ORD_NUM` "
                        "= '%s'" % (ord_amt, adv_amt, ord_num))
                    db.db.con.commit()
                    messagebox.showinfo("Success", "Record updated successfully")
                    # reseting treeview
                    self.table.delete(*self.table.get_children())

                    self.query = "SELECT `ORD_NUM` , `ORD_AMOUNT`, `ADVANCE_AMOUNT`, orders.AGENT_CODE, `AGENT_NAME` FROM orders " \
                                 "INNER JOIN agents ON orders.AGENT_CODE=agents.AGENT_CODE "
                    db.db.cursor.execute(self.query)
                    records = db.db.cursor.fetchall()
                    data = []

                    for i in records:
                        data.append([i[0], i[1], i[2], i[1] - i[2], i[3], i[4]])

                    # inserting records into treeview
                    for i in data:
                        self.table.insert("", 'end', values=i)
            else:
                messagebox.showerror("error", "No such Oreder Number exist")
        else:
            messagebox.showerror("Error", "Error in data entry")

    def get_row(self, event):
        rowid = self.table.identify_row(event.y)
        item = self.table.item(self.table.focus())
        self.ord_num_ord.set(item['values'][0])
        self.ord_amt_ord.set(item['values'][1])
        self.adv_amt_ord.set(item['values'][2])
        self.bal_amt_ord.set(item['values'][3])
        self.agent_code_ord.set(item['values'][4])
        self.agent_name_ord.set(item['values'][5])

    def menu(self):
        self.root.destroy()
        x = menu.Menu()
        x.menu()


if __name__ == "__main__":
    x = ballance_amt()
    x.balance()

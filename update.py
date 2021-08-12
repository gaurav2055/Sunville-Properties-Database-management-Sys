from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
from datetime import *
import re
import db.db
import menu


class Update:
    def __init__(self):

        # creating tkinter window
        self.root = Tk()
        self.top = Toplevel(self.root)
        self.top.destroy()

        self.root.config(bg="white")

        # Setting title
        self.root.title("Sunville Properties | Update")

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

        self.date = 1

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

    def validate_phone(self, number):
        regex = '^[0-9]{3}\-[0-9]{8}'
        Pattern = re.compile(regex)
        if number == "":
            return True
        else:
            return Pattern.match(number)

    def validate_date(self, date):
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

    def Phone_validate(self, phone, widget, event=None):
        if self.validate_phone(phone):
            widget.config(bg="White")
        else:
            widget.config(bg="Red")

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

    def cal_func(self, event=None):
        def calval(event=None):
            self.ord_order_date.set(cal.get_date())
            self.top.destroy()
            self.order_date.config(bg = "White")
            self.date = 1

        if self.date == 1:
            self.top = Toplevel(self.root)
            # Positions the window in the center of the page.
            self.top.geometry(
                "+{0}+{1}".format(self.positionRight,
                                  self.positionDown))
            cal = Calendar(self.top, font="Arial 14", selectmode="day", year=datetime.today().year,
                           month=datetime.today().month, day=datetime.today().day, date_pattern='yyyy-mm-dd')
            cal.bind_all('<Double-Button-1>', calval)
            cal.pack()
            btn = Button(self.top, text="Ok", command=calval)
            btn.pack()
            self.date = 2

    def destroycal(self, event=None):
        if self.top.winfo_exists():
            self.top.destroy()
            self.date = 1

    def update(self):

        # setting variables

        self.frame1 = Frame(self.root, bg='white')
        self.frame1.place(x=0, y=0, width=int(self.windowWidth / 3 * 2), height=int(self.windowHeight))

        # creating frame for image
        self.frame2 = Frame(self.root, bg="blue")
        self.frame2.place(x=int(self.windowWidth / 3 * 2), y=0, width=int(self.windowWidth / 3),
                          height=int(self.windowHeight))

        # getting image
        self.image1 = Image.open("D:/python/classes/Internship/property-consultants-mumbai.jpg")
        self.image1 = self.image1.resize((int(self.windowWidth / 3), int(self.windowHeight)), Image.ANTIALIAS)
        self.image_bg = ImageTk.PhotoImage(self.image1, master=self.root)

        # placing image
        self.background_label = Label(self.frame2, image=self.image_bg)
        self.background_label.place(x=0, y=0)

        self.Menu = Button(self.frame1, text="Menu", bg="Black", fg="Red", command=self.menu, width=5)
        self.Menu.place(x=0, y=0)

        # select table option
        self.table_lab = Label(self.frame1, text="Table", bg="white", font=("calibri", 12, "bold"))
        self.table_lab.grid(row=0, column=0, padx=(0, 20), pady=(40, 10), sticky=E)

        self.table = ttk.Combobox(self.frame1, values=["agents", "company", "customer", "orders"], state="readonly")
        self.table.grid(row=0, column=1, pady=(40, 10))
        self.table.current(0)
        self.table.bind("<<ComboboxSelected>>", self.get_table)

        '''# get table button
        self.get = Button(self.frame1, text="Get Table", command=self.get_table, bg='black', fg='red',
                          font=("times new roman", 10, "bold"), width=20)
        self.get.grid(row=1, column=0, columnspan=2)'''

        # clear button
        self.clear = Button(self.frame1, text="clear", command=self.clear_btn, bg="black", fg="red",
                            font=("times new roman", 10, "bold"), width=20)
        self.clear.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        self.frame = Frame(self.frame1, bg="white", width=self.windowWidth / 3 * 2)
        self.frame.grid(row=3, column=0, columnspan=6, pady=20)
        self.agents()

        self.root.mainloop()

    def clear_btn(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()

    def get_table(self, event=None):

        for widgets in self.frame.winfo_children():
            widgets.destroy()

        self.frame.focus()

        self.table_ch = self.table.get()

        if self.table_ch == "agents":

            self.agents()

        elif self.table_ch == "company":
            self.company()

        elif self.table_ch == "customer":
            self.customer()

        else:
            self.orders()

    def agents(self):
        # defining variables
        self.agent_code = StringVar()
        self.agent_name = StringVar()
        self.working_area = StringVar()
        self.commission = StringVar()
        self.phone_no = StringVar()
        self.country = StringVar()

        self.agent_frame = Frame(self.frame, bg='white')
        self.agent_frame.pack()

        # Agent code entry
        self.code_lab = Label(self.agent_frame, text="AGENT_CODE", bg="white")
        self.code_lab.grid(row=0, column=0, pady=5)

        self.code = Entry(self.agent_frame, textvariable=self.agent_code, bd=2, relief=RIDGE)
        self.code.focus()
        self.code.bind('<Return>', lambda e: self.get_data("agents", "AGENT_CODE", str(self.code.get()), variables))
        self.code.grid(row=0, column=1, pady=5)

        # get button
        self.get_val = Button(self.agent_frame, text="Get", bg="black", fg="red", width=10,
                              command=lambda: self.get_data("agents", "AGENT_CODE", str(self.code.get()), variables))
        self.get_val.grid(row=0, column=2, padx=10, pady=5)

        # agent name
        self.name_lab = Label(self.agent_frame, text="AGENT_NAME", bg="white")
        self.name_lab.grid(row=1, column=0, pady=20)

        self.name = Entry(self.agent_frame, textvariable=self.agent_name, bd=2, relief=RIDGE)
        self.name.grid(row=1, column=1, pady=20)
        self.name.bind('<FocusOut>', lambda e: self.Str_validate(self.agent_name.get(), self.name))

        # working area
        self.working_lab = Label(self.agent_frame, text="WORKING_AREA", bg="white")
        self.working_lab.grid(row=2, column=0, pady=20)

        self.working = Entry(self.agent_frame, textvariable=self.working_area, bd=2, relief=RIDGE)
        self.working.grid(row=2, column=1, pady=20)
        self.working.bind('<FocusOut>', lambda e: self.Str_validate(self.working_area.get(), self.working))

        # commission
        self.comm_lab = Label(self.agent_frame, text="COMMISSION", bg="white")
        self.comm_lab.grid(row=3, column=0, pady=20)

        self.comm = Entry(self.agent_frame, textvariable=self.commission, bd=2, relief=RIDGE)
        self.comm.grid(row=3, column=1, pady=20)
        self.comm.bind('<FocusOut>', lambda e: self.Num_validate(self.commission.get(), self.comm))

        # phone no
        self.phone_lab = Label(self.agent_frame, text="PHONE_NO", bg="white")
        self.phone_lab.grid(row=1, column=2, pady=20, padx=(20, 0))

        self.phone = Entry(self.agent_frame, textvariable=self.phone_no, bd=2, relief=RIDGE)
        self.phone.grid(row=1, column=3, pady=20)
        self.phone.bind('<FocusOut>', lambda e: self.Phone_validate(self.phone_no.get(), self.phone))

        # Country

        self.ctry_lab = Label(self.agent_frame, text="COUNTRY", bg="white")
        self.ctry_lab.grid(row=2, column=2, pady=20, padx=(20, 0))

        self.ctry = Entry(self.agent_frame, textvariable=self.country, bd=2, relief=RIDGE)
        self.ctry.grid(row=2, column=3, pady=20)
        self.ctry.bind('<FocusOut>', lambda e: self.Str_validate(self.ctry.get(), self.ctry))

        variables = [self.code, self.name, self.working, self.comm, self.phone, self.ctry]

        self.clear_data_age = Button(self.agent_frame, text="clear", bg="black", fg="red",
                                 font=("times new roman", 10, 'bold'), command=lambda: self.clear_data(variables),
                                 width=10)
        self.clear_data_age.grid(row=0, column=3, padx=10, pady=5)

        # update button
        self.update_btn = Button(self.agent_frame, text="Update", bg="black", fg="red",
                                 font=("times new roman", 10, 'bold'), command=lambda: self.btn_update("agents", variables),
                                 width=10)
        self.update_btn.grid(row=4, column=0, pady=5, padx=5, columnspan=2)

        # add new record button
        self.add = Button(self.agent_frame, text="ADD", bg="black", fg="red",
                          font=("times new roman", 10, 'bold'), command=lambda: self.btn_add("agents", variables),
                          width=10)
        self.add.grid(row=4, column=1, pady=5, padx=5, columnspan=2)

        self.delete_age = Button(self.agent_frame, text="Delete", bg="black", fg="red",
                                 font=("times new roman", 10, 'bold'),
                                 command=lambda: self.btn_delete("agents", "AGENT_CODE",
                                                                 str(self.code.get()),variables), width=10)
        self.delete_age.grid(row=4, column=2, pady=5, padx=5, columnspan=2)

    def company(self):
        # defining variables
        self.company_id = StringVar()
        self.company_name = StringVar()
        self.company_city = StringVar()

        self.company_frame = Frame(self.frame, bg="white")
        self.company_frame.pack()

        # company id
        self.comp_id_lab = Label(self.company_frame, text="COMPANY_ID", bg="white")
        self.comp_id_lab.grid(row=0, column=0, rowspan=2, pady=5)

        self.comp_id = Entry(self.company_frame, textvariable=self.company_id, bg="white", relief=RIDGE, bd=2)
        self.comp_id.focus()
        self.comp_id.bind('<Return>', lambda e: self.get_data("company", "COMPANY_ID", str(self.comp_id.get()),
                                                              records))
        self.comp_id.grid(row=0, column=1, rowspan=2, pady=5)

        # get button
        self.get_val_comp = Button(self.company_frame, text="Get", bg="black", fg="red", width=10,
                                   command=lambda: self.get_data("company", "COMPANY_ID", str(self.comp_id.get()),
                                                                 records))
        self.get_val_comp.grid(row=0, column=2, padx=10, pady=5)

        # company name
        self.comp_name_lab = Label(self.company_frame, text="COMPANY_NAME", bg="white")
        self.comp_name_lab.grid(row=2, column=0, rowspan=2, pady=5, padx=(10, 0))

        self.comp_name = Entry(self.company_frame, textvariable=self.company_name, bg="white", relief=RIDGE, bd=2)
        self.comp_name.grid(row=2, column=1, rowspan=2, pady=5)
        self.comp_name.bind('<FocusOut>', lambda e: self.Str_validate(self.company_name.get(), self.comp_name))

        # Company city
        self.comp_city_lab = Label(self.company_frame, text="COMPANY_CITY", bg="white")
        self.comp_city_lab.grid(row=2, column=2, rowspan=2, pady=5)

        self.comp_city = Entry(self.company_frame, textvariable=self.company_city, bg="white", relief=RIDGE, bd=2)
        self.comp_city.grid(row=2, column=3, rowspan=2, pady=5)
        self.comp_city.bind('<FocusOut>', lambda e: self.Str_validate(self.company_city.get(), self.comp_city))

        self.company_frame.rowconfigure(4, minsize=185)

        records = [self.comp_id, self.comp_name, self.comp_city]

        self.clear_data_comp = Button(self.company_frame, text="clear", bg="black", fg="red",
                                     font=("times new roman", 10, 'bold'), command=lambda: self.clear_data(records),
                                     width=10)
        self.clear_data_comp.grid(row=0, column=3, padx=10, pady=5)

        # update button
        self.update_btn_comp = Button(self.company_frame, text="Update", bg="black", fg="red",
                                      font=("times new roman", 10, 'bold'), command=lambda: self.btn_update('company',records),
                                      width=10)
        self.update_btn_comp.grid(row=4, column=0, pady=5, padx=5, columnspan=2, sticky=S)

        # add new record button
        self.add_comp = Button(self.company_frame, text="ADD", bg="black", fg="red",
                               font=("times new roman", 10, 'bold'), command=lambda: self.btn_add("company", records),
                               width=10)
        self.add_comp.grid(row=4, column=1, pady=5, padx=5, columnspan=2, sticky=S)

        self.delete_comp = Button(self.company_frame, text="Delete", bg="black", fg="red",
                                  font=("times new roman", 10, 'bold'),
                                  command=lambda: self.btn_delete("company","COMPANY_ID",str(self.comp_id.get()),records),
                                  width=10)
        self.delete_comp.grid(row=4, column=2, pady=5, padx=5, columnspan=2, sticky=S)

    def customer(self):

        # defining variables
        self.cust_code = StringVar()
        self.cust_name = StringVar()
        self.cust_city = StringVar()
        self.cust_working_area = StringVar()
        self.cust_country = StringVar()
        self.cust_grade = StringVar()
        self.cust_opening_amt = StringVar()
        self.cust_receive_amt = StringVar()
        self.cust_payment_amt = StringVar()
        self.cust_outstanding_amt = StringVar()
        self.cust_phone_no = StringVar()
        self.cust_agent_code = StringVar()

        self.customer_frame = Frame(self.frame, bg="white")
        self.customer_frame.pack()

        # customer code
        self.customer_code_lab = Label(self.customer_frame, text="CUST_CODE", bg="white")
        self.customer_code_lab.grid(row=0, column=0, pady=5)

        self.customer_code = Entry(self.customer_frame, textvariable=self.cust_code, bg="white", relief=RIDGE, bd=2)
        self.customer_code.focus()
        self.customer_code.bind('<Return>',
                                lambda e: self.get_data("customer", "CUST_CODE", str(self.customer_code.get()),
                                                        records))
        self.customer_code.grid(row=0, column=1, pady=5)

        # get button
        self.get_val_cust = Button(self.customer_frame, text="Get", bg="black", fg="red", width=10,
                                   command=lambda: self.get_data("customer", "CUST_CODE", str(self.customer_code.get()),
                                                                 records))
        self.get_val_cust.grid(row=0, column=2, padx=10, pady=5)

        # customer name

        self.customer_name_lab = Label(self.customer_frame, text="CUST_NAME", bg="white")
        self.customer_name_lab.grid(row=1, column=0, pady=5)

        self.customer_name = Entry(self.customer_frame, textvariable=self.cust_name, bg="white", relief=RIDGE, bd=2)
        self.customer_name.grid(row=1, column=1, padx=5)
        self.customer_name.bind('<FocusOut>', lambda e: self.Str_validate(self.cust_name.get(), self.customer_name))

        # customer city

        self.customer_city_lab = Label(self.customer_frame, text="CUST_CITY", bg="white")
        self.customer_city_lab.grid(row=2, column=0, pady=5)

        self.customer_city = Entry(self.customer_frame, textvariable=self.cust_city, bg="white", relief=RIDGE, bd=2)
        self.customer_city.grid(row=2, column=1, pady=5)
        self.customer_city.bind('<FocusOut>', lambda e: self.Str_validate(self.cust_city.get(), self.customer_city))

        # working area
        self.working_area_cust_lab = Label(self.customer_frame, text="WORKING_AREA", bg="white")
        self.working_area_cust_lab.grid(row=3, column=0, pady=5)

        self.working_area_cust = Entry(self.customer_frame, textvariable=self.cust_working_area, bg="white",
                                       relief=RIDGE, bd=2)
        self.working_area_cust.grid(row=3, column=1, pady=5)
        self.working_area_cust.bind('<FocusOut>',
                                    lambda e: self.Str_validate(self.cust_working_area.get(), self.working_area_cust))

        # customer country
        self.customer_country_lab = Label(self.customer_frame, text="CUST_COUNTRY", bg="white")
        self.customer_country_lab.grid(row=4, column=0, pady=5)

        self.customer_country = Entry(self.customer_frame, textvariable=self.cust_country, bg="white",
                                      relief=RIDGE, bd=2)
        self.customer_country.grid(row=4, column=1, pady=5)
        self.customer_country.bind('<FocusOut>',
                                   lambda e: self.Str_validate(self.cust_country.get(), self.customer_country))

        # grade
        self.grade_lab = Label(self.customer_frame, text="GRADE", bg="white")
        self.grade_lab.grid(row=5, column=0, pady=5)

        self.grade = Entry(self.customer_frame, textvariable=self.cust_grade, bg="white", relief=RIDGE, bd=2)
        self.grade.grid(row=5, column=1, padx=5)
        self.grade.bind('<FocusOut>', lambda e: self.Num_validate(self.cust_grade.get(), self.grade))

        # opening amount
        self.opening_amt_cust_lab = Label(self.customer_frame, text="OPENING_AMT", bg="white")
        self.opening_amt_cust_lab.grid(row=6, column=0, pady=5)

        self.opening_amt_cust = Entry(self.customer_frame, textvariable=self.cust_opening_amt, bg="white",
                                      relief=RIDGE, bd=2)
        self.opening_amt_cust.grid(row=6, column=1, pady=5)
        self.opening_amt_cust.bind('<FocusOut>',
                                   lambda e: self.Num_validate(self.cust_opening_amt.get(), self.opening_amt_cust))

        # recieve amount

        self.receive_amt_cust_lab = Label(self.customer_frame, text="RECEIVE_AMT", bg="white")
        self.receive_amt_cust_lab.grid(row=1, column=2, padx=(20, 0), pady=5)

        self.receive_amt_cust = Entry(self.customer_frame, textvariable=self.cust_receive_amt, bg="white",
                                      relief=RIDGE, bd=2)
        self.receive_amt_cust.grid(row=1, column=3, pady=5)
        self.receive_amt_cust.bind('<FocusOut>',
                                   lambda e: self.Num_validate(self.cust_receive_amt.get(), self.receive_amt_cust))

        # payment amount
        self.payment_amt_cust_lab = Label(self.customer_frame, text="PAYMENT_AMT", bg="white")
        self.payment_amt_cust_lab.grid(row=2, column=2, padx=(20, 0), pady=5)

        self.payment_amt_cust = Entry(self.customer_frame, textvariable=self.cust_payment_amt, bg="white",
                                      relief=RIDGE, bd=2)
        self.payment_amt_cust.grid(row=2, column=3, pady=5)
        self.payment_amt_cust.bind('<FocusOut>',
                                   lambda e: self.Num_validate(self.cust_payment_amt.get(), self.payment_amt_cust))

        # outstanding amt
        self.outstanding_amt_cust_lab = Label(self.customer_frame, text="OUTSTANDING_AMT", bg="white")
        self.outstanding_amt_cust_lab.grid(row=3, column=2, padx=(20, 0), pady=5)

        self.outstanding_amt_cust = Entry(self.customer_frame, textvariable=self.cust_outstanding_amt, bg="white",
                                          relief=RIDGE, bd=2)
        self.outstanding_amt_cust.grid(row=3, column=3, pady=5)
        self.outstanding_amt_cust.bind('<FocusOut>', lambda e: self.Num_validate(self.cust_outstanding_amt.get(),
                                                                                 self.outstanding_amt_cust))

        # phone no
        self.phone_no_cust_lab = Label(self.customer_frame, text="PHONE_NO", bg="white")
        self.phone_no_cust_lab.grid(row=4, column=2, padx=(20, 0), pady=5)

        self.phone_no_cust = Entry(self.customer_frame, textvariable=self.cust_phone_no, bg="white",
                                   relief=RIDGE, bd=2)
        self.phone_no_cust.grid(row=4, column=3, pady=5)


        # agent code

        self.agent_code_cust_lab = Label(self.customer_frame, text="AGENT_CODE", bg="white")
        self.agent_code_cust_lab.grid(row=5, column=2, padx=(20, 0), pady=5)

        self.agent_code_cust = Entry(self.customer_frame, textvariable=self.cust_agent_code, bg="white",
                                     relief=RIDGE, bd=2)
        self.agent_code_cust.grid(row=5, column=3, pady=5)

        records = [self.customer_code, self.customer_name, self.customer_city, self.working_area_cust,
                   self.customer_country,
                   self.grade, self.opening_amt_cust, self.receive_amt_cust, self.payment_amt_cust,
                   self.outstanding_amt_cust,
                   self.phone_no_cust, self.agent_code_cust]

        self.clear_data_cus = Button(self.customer_frame, text="clear", bg="black", fg="red",
                                     font=("times new roman", 10, 'bold'), command=lambda: self.clear_data(records),
                                     width=10)
        self.clear_data_cus.grid(row=0, column=3, padx=10, pady=5)

        # update btn
        self.update_btn_cust = Button(self.customer_frame, text="Update", bg="black", fg="red",
                                      font=("times new roman", 10, 'bold'), command=lambda: self.btn_update("customer", records),
                                      width=10)
        self.update_btn_cust.grid(row=7, column=0, pady=5, padx=5, columnspan=2)

        self.add_cust = Button(self.customer_frame, text="ADD", bg="black", fg="red",
                               font=("times new roman", 10, 'bold'), command=lambda: self.btn_add("customer", records),
                               width=10)
        self.add_cust.grid(row=7, column=1, pady=5, padx=5, columnspan=2)
        self.delete_cust = Button(self.customer_frame, text="Delete", bg="black", fg="red",
                                  font=("times new roman", 10, 'bold'),
                                  command=lambda: self.btn_delete('customer','CUST_CODE',str(self.customer_code), records),
                                  width=10)
        self.delete_cust.grid(row=7, column=2, pady=5, padx=5, columnspan=2)

    def orders(self):
        # setting variables
        self.ord_order_num = StringVar()
        self.ord_order_amount = StringVar()
        self.ord_advance_amt = StringVar()
        self.ord_order_date = StringVar()
        self.ord_cust_code = StringVar()
        self.ord_agent_code = StringVar()
        self.ord_order_desc = StringVar()

        self.orders_frame = Frame(self.frame, bg="White")
        self.orders_frame.pack()

        self.order_num_lab = Label(self.orders_frame, text="ORD_NUM", bg="White")
        self.order_num_lab.grid(row=0, column=0, pady=5)

        self.order_num = Entry(self.orders_frame, textvariable=self.ord_order_num, bg="white",
                               relief=RIDGE, bd=2)
        self.order_num.focus()
        self.order_num.bind('<Return>', lambda e: self.get_data("orders", "ORD_NUM", str(self.order_num.get()),
                                                                records))
        self.order_num.grid(row=0, column=1, pady=5)
        self.order_num.bind('<FocusOut>', lambda e: self.Num_validate(self.ord_order_num.get(), self.order_num))

        # get button
        self.get_val_ord = Button(self.orders_frame, text="Get", bg="black", fg="red", width=10,
                                  command=lambda: self.get_data("orders", "ORD_NUM", str(self.order_num.get()),
                                                                records))
        self.get_val_ord.grid(row=0, column=2, padx=10, pady=5)

        # order amount
        self.order_amt_lab = Label(self.orders_frame, text="ORD_AMOUNT", bg="White")
        self.order_amt_lab.grid(row=1, column=0, pady=20)

        self.order_amt = Entry(self.orders_frame, textvariable=self.ord_order_amount, bg="white",
                               relief=RIDGE, bd=2)
        self.order_amt.grid(row=1, column=1, pady=20)
        self.order_amt.bind('<FocusIn>', self.destroycal)
        self.order_amt.bind('<FocusOut>', lambda e: self.Num_validate(self.ord_order_amount.get(), self.order_amt))

        # advance amount
        self.advance_amt_lab = Label(self.orders_frame, text="ADVANCE_AMT", bg="White")
        self.advance_amt_lab.grid(row=2, column=0, pady=20)

        self.advance_amt = Entry(self.orders_frame, textvariable=self.ord_advance_amt, bg="white",
                                 relief=RIDGE, bd=2)
        self.advance_amt.grid(row=2, column=1, pady=20)
        self.advance_amt.bind('<FocusIn>', self.destroycal)
        self.advance_amt.bind('<FocusOut>', lambda e: self.Num_validate(self.ord_advance_amt.get(), self.advance_amt))

        # order date
        self.order_date_lab = Label(self.orders_frame, text="	ORD_DATE", bg="White")
        self.order_date_lab.grid(row=3, column=0, pady=20)

        self.order_date = Entry(self.orders_frame, textvariable=self.ord_order_date, bg="White",
                                relief=RIDGE, bd=2)
        self.order_date.grid(row=3, column=1, pady=20)
        self.order_date.bind('<Button-1>', self.cal_func)
        self.order_date.bind('<FocusOut>', lambda e: self.Date_validate(self.ord_order_date.get(), self.order_date))

        # customer code
        self.customer_code_ord_lab = Label(self.orders_frame, text="CUST_CODE", bg="white")
        self.customer_code_ord_lab.grid(row=1, column=2, pady=20, padx=(20, 0))

        self.customer_code_ord = Entry(self.orders_frame, textvariable=self.ord_cust_code, bg="white",
                                       relief=RIDGE, bd=2)
        self.customer_code_ord.bind('<FocusIn>', self.destroycal)
        self.customer_code_ord.grid(row=1, column=3, pady=20)

        # agent code
        self.agent_code_ord_lab = Label(self.orders_frame, text="AGENT_CODE", bg="White")
        self.agent_code_ord_lab.grid(row=2, column=2, pady=20, padx=(20, 0))

        self.agent_code_ord = Entry(self.orders_frame, textvariable=self.ord_agent_code, bg="white",
                                    relief=RIDGE, bd=2)
        self.agent_code_ord.bind('<FocusIn>', self.destroycal)
        self.agent_code_ord.grid(row=2, column=3, pady=20)

        # order description
        self.order_desc_lab = Label(self.orders_frame, text="ORD_DESCRIPTION", bg="White")
        self.order_desc_lab.grid(row=3, column=2, padx=(20, 0), pady=20)

        self.order_desc = Entry(self.orders_frame, textvariable=self.ord_order_desc, bg="white",
                                relief=RIDGE, bd=2)
        self.order_desc.grid(row=3, column=3, pady=20)
        self.order_desc.bind('<FocusIn>', self.destroycal)
        self.order_desc.bind('<FocusOut>', lambda e: self.Num_validate(self.ord_order_desc.get(), self.order_desc))

        records = [self.order_num, self.order_amt, self.advance_amt, self.order_date,
                   self.customer_code_ord, self.agent_code_ord, self.order_desc]

        self.clear_data_ord = Button(self.orders_frame, text="clear", bg="black", fg="red",
                                     font=("times new roman", 10, 'bold'), command=lambda: self.clear_data(records),
                                     width=10)
        self.clear_data_ord.grid(row=0, column=3, padx=10, pady=5)

        # update button
        self.update_btn_ord = Button(self.orders_frame, text="Update", bg="black", fg="red",
                                     font=("times new roman", 10, 'bold'), command=lambda: self.btn_update("orders",records),
                                     width=10)
        self.update_btn_ord.grid(row=4, column=0, pady=5, padx=5, columnspan=2)

        # add new record button
        self.add_ord = Button(self.orders_frame, text="ADD", bg="black", fg="red",
                              font=("times new roman", 10, 'bold'), command=lambda: self.btn_add("orders",records),
                              width=10)
        self.add_ord.grid(row=4, column=1, pady=5, padx=5, columnspan=2)

        self.delete_ord = Button(self.orders_frame, text="Delete", bg="black", fg="red",
                                 font=("times new roman", 10, 'bold'),
                                 command=lambda: self.btn_delete("orders","ORD_NUM", str(self.order_num.get()),records),
                                 width=10)
        self.delete_ord.grid(row=4, column=2, pady=5, padx=5, columnspan=2)

    def get_data(self, table, column, value, records, event=None):

        db.db.cursor.execute("SELECT * from `%s` WHERE `%s` = '%s'" % (table, column, value))
        data = db.db.cursor.fetchall()

        if data:
            for j in data:
                for i, k in zip(records, j):
                    i.delete(0, 'end')
                    i.insert(0, k)
                    i.config(bg="White")
        else:
            messagebox.showerror("Error", "No such record exist")

    def clear_data(self,records):
        for i in records:
            i.delete(0,'end')
            i.config(bg = "white")
        records[0].focus()

    def btn_update(self, table, widgets):

        if table == "agents":
            agent_code_age = self.agent_code.get()
            agent_name_age = self.agent_name.get()
            working_area_age = self.working_area.get()
            commission_age = self.commission.get()
            phone_no_age = self.phone_no.get()
            country_age = self.country.get()

            if self.validate_str(agent_name_age) and self.validate_str(working_area_age) and self.validate_num(
                    commission_age) and self.validate_phone(phone_no_age) and self.validate_str(country_age):

                db.db.cursor.execute("SELECT * from `agents` WHERE `AGENT_CODE` = '%s'" % (agent_code_age))
                records = db.db.cursor.fetchall()
                query1 = "UPDATE `agents` SET `AGENT_NAME`='%s',`WORKING_AREA`='%s',`COMMISSION`='%s'," \
                         "`PHONE_NO`='%s',`COUNTRY`='%s' WHERE `AGENT_CODE`='%s' "
                if records:
                    db.db.cursor.execute(query1 % (
                        agent_name_age, working_area_age, commission_age, phone_no_age, country_age, agent_code_age))
                    db.db.con.commit()
                    messagebox.showinfo("success", "Record updated successfully!")
                    self.clear_data(widgets)
            else:
                messagebox.showerror("Error!", "data entered in incorrect format")

        elif table == "company":
            company_id_comp = self.company_id.get()
            company_name_comp = self.company_name.get()
            company_city_comp = self.company_city.get()

            if self.validate_str(company_name_comp) and self.validate_str(company_city_comp):

                db.db.cursor.execute("SELECT * from `company` WHERE `COMPANY_ID` = '%s'" % company_id_comp)
                records = db.db.cursor.fetchall()
                query2 = "UPDATE `company` SET `COMPANY_NAME` = '%s', `COMPANY_CITY` = '%s' WHERE `COMPANY_ID` = '%s'"
                if records:
                    db.db.cursor.execute(query2 % (company_name_comp, company_city_comp, company_id_comp))
                    db.db.con.commit()
                    messagebox.showinfo("success", "Record updated successfully!")
                    self.clear_data(widgets)
            else:
                messagebox.showerror("Error!", "data entered in incorrect format")

        elif table == "customer":
            cust_code_cust = self.cust_code.get()
            cust_name_cust = self.cust_name.get()
            cust_city_cust = self.cust_city.get()
            cust_woring_cust = self.cust_working_area.get()
            cust_country_cust = self.cust_country.get()
            cust_grade_cust = self.cust_grade.get()
            cust_opening_amt_cust = self.cust_opening_amt.get()
            cust_recieve_amt_cust = self.cust_receive_amt.get()
            cust_payment_amt_cust = self.cust_payment_amt.get()
            cust_outstanding_amt_cust = self.cust_outstanding_amt.get()
            cust_phone_no_cust = self.cust_phone_no.get()
            cust_agent_code_cust = self.cust_agent_code.get()

            if self.validate_str(cust_name_cust) and self.validate_str(cust_city_cust) and self.validate_str(
                    cust_woring_cust) and self.validate_str(cust_country_cust) and self.validate_num(
                cust_grade_cust) and self.validate_num(cust_opening_amt_cust) and self.validate_num(
                cust_recieve_amt_cust) and self.validate_num(cust_payment_amt_cust) and self.validate_num(
                cust_outstanding_amt_cust):

                db.db.cursor.execute("SELECT * from `customer` WHERE `CUST_CODE` = '%s'" % (cust_code_cust))
                records = db.db.cursor.fetchall()

                query3_1 = "UPDATE `customer` SET `CUST_NAME`='%s',`CUST_CITY`='%s',`WORKING_AREA`='%s'," \
                           "`CUST_COUNTRY`='%s',`GRADE`='%s', "
                query3_2 = "`OPENING_AMT`='%s',`RECEIVE_AMT`='%s',`PAYMENT_AMT`='%s',`OUTSTANDING_AMT`='%s'," \
                           "`PHONE_NO`='%s',`AGENT_CODE`='%s' WHERE `CUST_CODE`='%s' "
                query3 = query3_1 + query3_2
                if records:
                    db.db.cursor.execute(
                        query3 % (cust_name_cust, cust_city_cust, cust_woring_cust, cust_country_cust, cust_grade_cust,
                                  cust_opening_amt_cust, cust_recieve_amt_cust, cust_payment_amt_cust,
                                  cust_outstanding_amt_cust,
                                  cust_phone_no_cust, cust_agent_code_cust, cust_code_cust))
                    db.db.con.commit()
                    messagebox.showinfo("success", "Record updated successfully!")
                    self.clear_data(widgets)
            else:
                messagebox.showerror("Error!", "data entered in incorrect format")

        else:
            order_num = self.ord_order_num.get()
            order_amt = self.ord_order_amount.get()
            advance_amt = self.ord_advance_amt.get()
            order_date = self.ord_order_date.get()
            cust_code = self.ord_cust_code.get()
            agent_code = self.ord_agent_code.get()
            order_desc = self.ord_order_desc.get()

            if self.validate_num(order_num) and self.validate_num(order_amt) and self.validate_num(advance_amt) and self.validate_date(
                    order_date) and self.validate_str(order_desc):

                db.db.cursor.execute("SELECT * from `orders` WHERE `ORD_NUM` = '%s'" % (order_num))
                records = db.db.cursor.fetchall()

                query4 = "UPDATE `orders` SET `ORD_AMOUNT`='%s',`ADVANCE_AMOUNT`='%s',`ORD_DATE`='%s',`CUST_CODE`='%s'," \
                         "`AGENT_CODE`='%s',`ORD_DESCRIPTION`= '%s' WHERE `ORD_NUM`='%s'"

                if records:
                    db.db.cursor.execute(
                        query4 % (order_amt, advance_amt, order_date, cust_code, agent_code, order_desc, order_num))
                    db.db.con.commit()
                    messagebox.showinfo("success", "Record updated successfully!")
                    self.clear_data(widgets)
            else:
                messagebox.showerror("Error!", "data entered in incorrect format")

    def btn_add(self, table, widgets):
        if table == "agents":
            agent_code_age = self.agent_code.get()
            agent_name_age = self.agent_name.get()
            working_area_age = self.working_area.get()
            commission_age = self.commission.get()
            phone_no_age = self.phone_no.get()
            country_age = self.country.get()
            if self.validate_str(agent_name_age) and self.validate_str(working_area_age) and self.validate_num(
                    commission_age) and self.validate_phone(phone_no_age) and self.validate_str(country_age):

                db.db.cursor.execute("SELECT * from `agents` WHERE `AGENT_CODE` = '%s'" % (agent_code_age))
                records = db.db.cursor.fetchall()
                query1 = "UPDATE `agents` SET `AGENT_NAME`='%s',`WORKING_AREA`='%s',`COMMISSION`='%s',`PHONE_NO`='%s',`COUNTRY`='%s' WHERE `AGENT_CODE`='%s'"
                query2 = "INSERT INTO `agents`(`AGENT_CODE`, `AGENT_NAME`, `WORKING_AREA`, `COMMISSION`, `PHONE_NO`, `COUNTRY`) VALUES " \
                         "('%s','%s','%s','%s','%s','%s')"
                if records:
                    response = messagebox.askyesno("alert", "The record already exist, do yoy wish to update")
                    if response:
                        db.db.cursor.execute(query1 % (
                            agent_name_age, working_area_age, commission_age, phone_no_age, country_age,
                            agent_code_age))
                        db.db.con.commit()
                        messagebox.showinfo("success", "Record updated successfully!")
                        self.clear_data(widgets)
                else:
                    db.db.cursor.execute(query2 % (
                        agent_code_age, agent_name_age, working_area_age, commission_age, phone_no_age, country_age))
                    db.db.con.commit()
                    messagebox.showinfo("success", "Record added successfully!")
                    self.clear_data(widgets)
            else:
                messagebox.showerror("Error!", "data entered in incorrect format")

        elif table == "company":
            company_id_comp = self.company_id.get()
            company_name_comp = self.company_name.get()
            company_city_comp = self.company_city.get()

            if self.validate_str(company_name_comp) and self.validate_str(company_city_comp):

                db.db.cursor.execute("SELECT * from `company` WHERE `COMPANY_ID` = '%s'" % (company_id_comp))
                records = db.db.cursor.fetchall()
                query1 = "UPDATE `company` SET `COMPANY_NAME` = '%s', 'COMPANY_CITY' = '%s' WHERE `COMPANY_ID` = '%s'"
                query2 = "INSERT INTO `company`(`COMPANY_ID`, `COMPANY_NAME`, `COMPANY_CITY`) VALUES ('%s','%s','%s')"
                if records:
                    response = messagebox.askyesno("alert", "The record already exist, do yoy wish to update")
                    if response:
                        db.db.cursor.execute(query1 % (company_name_comp, company_city_comp, company_id_comp))
                        db.db.con.commit()
                        messagebox.showinfo("success", "Record updated successfully!")
                        self.clear_data(widgets)
                else:
                    db.db.cursor.execute(query2 % (company_id_comp, company_name_comp, company_city_comp))
                    db.db.con.commit()
                    messagebox.showinfo("success", "Record added successfully!")
                    self.clear_data(widgets)
            else:
                messagebox.showerror("Error!", "data entered in incorrect format")

        elif table == "customer":
            cust_code_cust = self.cust_code.get()
            cust_name_cust = self.cust_name.get()
            cust_city_cust = self.cust_city.get()
            cust_woring_cust = self.cust_working_area.get()
            cust_country_cust = self.cust_country.get()
            cust_grade_cust = self.cust_grade.get()
            cust_opening_amt_cust = self.cust_opening_amt.get()
            cust_recieve_amt_cust = self.cust_receive_amt.get()
            cust_payment_amt_cust = self.cust_payment_amt.get()
            cust_outstanding_amt_cust = self.cust_outstanding_amt.get()
            cust_phone_no_cust = self.cust_phone_no.get()
            cust_agent_code_cust = self.cust_agent_code.get()

            if self.validate_str(cust_name_cust) and self.validate_str(cust_city_cust) and self.validate_str(
                    cust_woring_cust) and self.validate_str(cust_country_cust) and self.validate_num(
                cust_grade_cust) and self.validate_num(cust_opening_amt_cust) and self.validate_num(
                cust_recieve_amt_cust) and self.validate_num(cust_payment_amt_cust) and self.validate_num(
                cust_outstanding_amt_cust):

                db.db.cursor.execute("SELECT * from `customer` WHERE `CUST_CODE` = '%s'" % (cust_code_cust))
                records = db.db.cursor.fetchall()

                query3_1 = "UPDATE `customer` SET `CUST_NAME`='%s',`CUST_CITY`='%s',`WORKING_AREA`='%s'," \
                           "`CUST_COUNTRY`='%s',`GRADE`='%s', "
                query3_2 = "`OPENING_AMT`='%s',`RECEIVE_AMT`='%s',`PAYMENT_AMT`='%s',`OUTSTANDING_AMT`='%s'," \
                           "`PHONE_NO`='%s',`AGENT_CODE`='%s' WHERE `CUST_CODE`='%s' "
                query1 = query3_1 + query3_2
                query2 = "INSERT INTO `customer`(`CUST_CODE`, `CUST_NAME`, `CUST_CITY`, `WORKING_AREA`, `CUST_COUNTRY`, " \
                         "`GRADE`, `OPENING_AMT`, `RECEIVE_AMT`, `PAYMENT_AMT`, `OUTSTANDING_AMT`, `PHONE_NO`, " \
                         "`AGENT_CODE`) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') "
                if records:
                    response = messagebox.askyesno("alert", "The record already exist, do yoy wish to update")
                    if response:
                        db.db.cursor.execute(
                            query1 % (
                                cust_name_cust, cust_city_cust, cust_woring_cust, cust_country_cust, cust_grade_cust,
                                cust_opening_amt_cust, cust_recieve_amt_cust, cust_payment_amt_cust,
                                cust_outstanding_amt_cust,
                                cust_phone_no_cust, cust_agent_code_cust, cust_code_cust))
                        db.db.con.commit()
                        messagebox.showinfo("success", "Record updated successfully!")
                        self.clear_data(widgets)

                else:
                    db.db.cursor.execute(query2 % (
                        cust_code_cust, cust_name_cust, cust_city_cust, cust_woring_cust, cust_country_cust,
                        cust_grade_cust,
                        cust_opening_amt_cust, cust_recieve_amt_cust, cust_payment_amt_cust, cust_outstanding_amt_cust,
                        cust_phone_no_cust, cust_agent_code_cust))
                    db.db.con.commit()
                    messagebox.showinfo("success", "Record added successfully!")
                    self.clear_data(widgets)
            else:
                messagebox.showerror("Error!", "data entered in incorrect format")

        else:
            order_num = self.ord_order_num.get()
            order_amt = self.ord_order_amount.get()
            advance_amt = self.ord_advance_amt.get()
            order_date = self.ord_order_date.get()
            cust_code = self.ord_cust_code.get()
            agent_code = self.ord_agent_code.get()
            order_desc = self.ord_order_desc.get()

            if self.validate_num(order_num) and self.validate_num(order_amt) and self.validate_num(advance_amt) and self.validate_date(
                    order_date) and self.validate_str(order_desc):

                db.db.cursor.execute("SELECT * from `orders` WHERE `ORD_NUM` = '%s'" % (order_num))
                records = db.db.cursor.fetchall()

                query1 = "UPDATE `orders` SET `ORD_AMOUNT`='%s',`ADVANCE_AMOUNT`='%s',`ORD_DATE`='%s',`CUST_CODE`='%s'," \
                         "`AGENT_CODE`='%s',`ORD_DESCRIPTION`= '%s' WHERE `ORD_NUM`='%s'"
                query2 = "INSERT INTO `orders`(`ORD_NUM`, `ORD_AMOUNT`, `ADVANCE_AMOUNT`, `ORD_DATE`, `CUST_CODE`, " \
                         "`AGENT_CODE`, `ORD_DESCRIPTION`) VALUES ('%s','%s','%s','%s','%s'," \
                         "'%s','%s') "

                if records:
                    response = messagebox.askyesno("alert", "The record already exist, do yoy wish to update")
                    if response:
                        db.db.cursor.execute(
                            query1 % (order_amt, advance_amt, order_date, cust_code, agent_code, order_desc, order_num))
                        db.db.con.commit()
                        messagebox.showinfo("success", "Record updated successfully!")
                        self.clear_data(widgets)
                else:
                    db.db.cursor.execute(query2 % (order_num, order_amt, advance_amt, order_date, cust_code, agent_code,
                                                   order_desc))
                    db.db.con.commit()
                    messagebox.showinfo("success", "Record added successfully!")
                    self.clear_data(widgets)
            else:
                messagebox.showerror("Error!", "data entered in incorrect format")

    def btn_delete(self, table, column, value, widgets):
        if table == "agents":
            response = messagebox.askyesno("confirm", "Are you sure you want to delete the record")
            if response:
                db.db.cursor.execute("DELETE FROM `%s` WHERE `%s` = '%s'" % (table, column, value))
                messagebox.showinfo("Success", "Record has been deleted")
                self.clear_data(widgets)
        elif table == "company":
            response = messagebox.askyesno("confirm", "Are you sure you want to delete the record")
            if response:
                db.db.cursor.execute("DELETE FROM `%s` WHERE `%s` = '%s'" % (table, column, value))
                db.db.con.commit()
                messagebox.showinfo("Success", "Record has been deleted")
                self.clear_data(widgets)
        elif table == "customer":
            response = messagebox.askyesno("confirm", "Are you sure you want to delete the record")
            if response:
                db.db.cursor.execute("DELETE FROM `%s` WHERE `%s` = '%s'" % (table, column, value))
                db.db.con.commit()
                messagebox.showinfo("Success", "Record has been deleted")
                self.clear_data(widgets)
        else:
            response = messagebox.askyesno("confirm", "Are you sure you want to delete the record")
            if response:
                db.db.cursor.execute("DELETE FROM `%s` WHERE `%s` = '%s'" % (table, column, value))
                db.db.con.commit()
                messagebox.showinfo("Success", "Record has been deleted")
                self.clear_data(widgets)

    def menu(self):
        self.root.destroy()
        x = menu.Menu()
        x.menu()


if __name__ == "__main__":
    x = Update()
    x.update()

from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import Login
import Register
import update
import orders_lookup
import balance_amount
import customers
import insights


class Menu:
    def __init__(self):
        # creating tkinter window
        self.root = Tk()

        # Setting title
        self.root.title("Sunville Properties | Menu")

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

    def menu(self):

        # getting image
        self.image1 = Image.open("D:/python/classes/Internship/property-consultants-mumbai.jpg")
        self.image1 = self.image1.resize((int(self.windowWidth), int(self.windowHeight)), Image.ANTIALIAS)
        self.image_bg = ImageTk.PhotoImage(self.image1, master = self.root)

        # placing image
        self.background_label = Label(self.root, image=self.image_bg)
        self.background_label.place(x=0, y=0)

        self.head_lab = Label(self.root, text = "Sunville Properties", font = ("corbel", 30,"bold italic"), bg = "beige", fg = "red")
        self.head_lab.grid(row = 0, column = 0, columnspan = 2, padx = 100, pady = (30,30))

        self.root.rowconfigure(0, minsize=int(self.windowHeight / 4))
        self.root.columnconfigure(0, minsize = (self.windowWidth/ 2))
        self.root.columnconfigure(1, minsize=(self.windowWidth / 2))

        self.update_btn = Button(self.root, text="Update", font=("times new roman", 15, "bold"), bg="#1C1B1B", fg="red",
                                 width=10, command=self.update, relief=RAISED, bd=3)
        self.update_btn.grid(row=1, column=0, pady = 20, sticky = E, padx = 20)

        self.orders_btn = Button(self.root, text = "Orders", font=("times new roman", 15, "bold"), bg="#1C1B1B", fg="red",
                                 width=10, command=self.orders, relief=RAISED, bd=3)
        self.orders_btn.grid(row=2, column=0, pady = 20, sticky = E, padx = 20)

        self.balance_amt_btn = Button(self.root, text = "Ballance_Amt", font=("times new roman", 15, "bold"), bg="#1C1B1B", fg="red",
                                 width=10, command=self.balamce_amt, relief=RAISED, bd=3)
        self.balance_amt_btn.grid(row=3, column=0, pady = 20, sticky = E, padx = 20)

        self.customers_btn = Button(self.root, text = "Customers", font=("times new roman", 15, "bold"), bg="#1C1B1B", fg="red",
                                 width=10, command=self.customers, relief=RAISED, bd=3)
        self.customers_btn.grid(row=1, column=1, pady = 20, sticky = W, padx = 20)

        self.insights_btn = Button(self.root, text = "Insights", font=("times new roman", 15, "bold"), bg="#1C1B1B", fg="red",
                                 width=10, command=self.insights, relief=RAISED, bd=3)
        self.insights_btn.grid(row = 2, column = 1, pady = 20, sticky = W, padx = 20)

        self.register_btn = Button(self.root, text = "Register", font=("times new roman", 15, "bold"), bg="#1C1B1B", fg="red",
                                 width=10, command=self.register, relief=RAISED, bd=3)
        self.register_btn.grid(row = 3, column = 1, pady = 20, sticky = W, padx = 20)

        self.log_out_btn = Button(self.root, text = "Log Out", font=("times new roman", 15, "bold"), bg="#1C1B1B", fg="red",
                                 width=10, command=self.log_out, relief=RAISED, bd=3)
        self.log_out_btn.grid(row = 4, column = 0, pady = 10, columnspan=2)
        self.root.mainloop()

    def update(self):
        self.root.destroy()
        Update = update.Update()
        Update.update()
    def orders(self):
        self.root.destroy()
        orders = orders_lookup.orders_lookup()
        orders.orders()
    def balamce_amt(self):
        self.root.destroy()
        bal = balance_amount.ballance_amt()
        bal.balance()

    def customers(self):
        self.root.destroy()
        cus = customers.Customers()
        cus.customers()

    def insights(self):
        self.root.destroy()
        ins = insights.Insights()
        ins.insights()

    def register(self):
        self.root.destroy()
        reg = Register.Register()
        reg.register()

    def log_out(self):
        response = messagebox.askquestion("Conifirmation","Are you sure you want to Log outt?")
        if response:
            self.root.destroy()
            log = Login.Login()
            log.login()

if __name__ == "__main__":
    x = Menu()
    x.menu()

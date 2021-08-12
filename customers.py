from tkinter import *
from PIL import ImageTk, Image
import db.db
import menu


class Customers:
    def __init__(self):
        # creating tkinter window
        self.root = Tk()

        # setting window title
        self.root.title("Sunville Properties | Customers")

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

    def customers(self):
        self.name = StringVar()
        self.payment_amt = StringVar()
        self.outstanding_amt = StringVar()

        # creating frame for customers
        self.frame1 = Frame(self.root, bg="White")
        self.frame1.place(x=0, y=0, width=int(self.windowWidth / 3), height=int(self.windowHeight))

        # creating frame for image
        self.frame2 = Frame(self.root, bg="blue", )
        self.frame2.place(x=int(self.windowWidth / 3), y=0)

        # getting image
        self.image1 = Image.open("D:/python/classes/Internship/property-consultants-mumbai.jpg")
        self.image1 = self.image1.resize((int(self.windowWidth / 3 * 2), int(self.windowHeight)), Image.ANTIALIAS)
        self.image_bg = ImageTk.PhotoImage(self.image1, master=self.root)

        # placing image
        self.background_label = Label(self.frame2, image=self.image_bg)
        self.background_label.pack()

        self.Menu = Button(self.root, text="Menu", bg="Black", fg="Red", command=self.menu, width=5)
        self.Menu.place(x=0, y=0)

        self.country_lab = Label(self.frame1, text="Max Customers", bg="White")
        self.country_lab.grid(row=0, column=0, sticky=W + S, padx=(10, 5))

        self.country = Entry(self.frame1, textvariable=self.name, bg="White", relief=RIDGE,
                             bd=2, state="readonly")
        self.country.focus()
        self.country.bind('<FocusIn>', self.cust_max())
        self.country.grid(row=0, column=1, sticky=S)

        self.pay_amt_lab = Label(self.frame1, text="Total Payment", bg="White", )
        self.pay_amt_lab.grid(row=1, column=0, padx=(10, 5), pady=10, sticky=W)

        self.pay_amt = Entry(self.frame1, textvariable=self.payment_amt, bg="White", relief=RIDGE,
                             bd=2, state="readonly")
        self.pay_amt.grid(row=1, column=1, pady=10)

        self.out_amt_lab = Label(self.frame1, text="Total Outstanding", bg="White", )
        self.out_amt_lab.grid(row=2, column=0, padx=(10, 5), pady=10)

        self.out_amt = Entry(self.frame1, textvariable=self.outstanding_amt, bg="White", relief=RIDGE,
                             bd=2, state="readonly")
        self.out_amt.grid(row=2, column=1, pady=10)

        self.frame1.rowconfigure(0, minsize=int(self.windowHeight / 3))

        self.root.mainloop()

    def cust_max(self, event=None):
        Australia = []
        Canada = []
        India = []
        UK = []
        USA = []
        country = [Australia, Canada, India, UK, USA]
        country_name = ["Australia", "Canada", "India", "UK", "USA"]
        self.query = "SELECT `CUST_COUNTRY` FROM `customer` WHERE `CUST_COUNTRY` = '%s'"

        for (i, j) in zip(country, country_name):
            db.db.cursor.execute(self.query % j)
            i.append(db.db.cursor.fetchall())
        max = 0
        name = ""
        for i in country:
            for j in i:
                if len(j) > max:
                    max = len(j)
                    name = j[0]
        self.name.set(name)

        pay_amt = 0

        db.db.cursor.execute("SELECT `PAYMENT_AMT` FROM `customer` WHERE `CUST_COUNTRY` = '%s'" % name)
        records = db.db.cursor.fetchall()
        for i in records:
            pay_amt += i[0]
        print(pay_amt)
        self.payment_amt.set(pay_amt)

        out_amt = 0
        db.db.cursor.execute("SELECT `OUTSTANDING_AMT` FROM `customer` WHERE `CUST_COUNTRY` = '%s'" % name)
        records = db.db.cursor.fetchall()
        for i in records:
            out_amt += i[0]

        self.outstanding_amt.set(out_amt)

    def menu(self):
        self.root.destroy()
        x = menu.Menu()
        x.menu()


if __name__ == "__main__":
    x = Customers()
    x.customers()

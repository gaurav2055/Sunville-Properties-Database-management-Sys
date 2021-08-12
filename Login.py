from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import db.db
import menu
import forgot_password


class Login:
    def __init__(self):

        # creating tkinter window
        self.root = Tk()

        # setting window title
        self.root.title("Sunville Properties | Login")

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

        self.FirstClick = True

    def login(self):

        # variable of entry fields
        self.username_e = StringVar()
        self.username_e.set("Username")
        self.password_e = StringVar()
        self.password_e.set("password")

        # creating frame for login form
        self.frame1 = Frame(self.root, bg="White")
        self.frame1.place(x=0, y=0, width=int(self.windowWidth / 2.5), height=int(self.windowHeight))

        # creating frame for image
        self.frame2 = Frame(self.root, bg="blue", )
        self.frame2.place(x=int(self.windowWidth / 2.5), y=0)

        # getting image
        self.image1 = Image.open("img/property-consultants-mumbai.jpg")
        self.image1 = self.image1.resize((int(self.windowWidth -(self.windowWidth/2.5)), int(self.windowHeight)), Image.ANTIALIAS)
        self.image_bg = ImageTk.PhotoImage(self.image1, master=self.root)

        # placing image
        self.background_label = Label(self.frame2, image=self.image_bg)
        self.background_label.pack()

        # heading
        self.heading = Label(self.frame1, text="Sunville Properties", font=("corbel", 15, "bold italic"), bg="beige",
                             fg="red")
        self.heading.grid(row=0, column=0, columnspan=4, ipadx=5)

        # login image for entry form
        self.image2 = Image.open("D:/python/classes/Internship/user.png")
        self.image2 = self.image2.resize((25, 25), Image.ANTIALIAS)
        self.login_img = ImageTk.PhotoImage(self.image2, master=self.root)

        # placing login image and heading
        self.label1 = Label(self.frame1, image=self.login_img, text="LOGIN", compound=LEFT,
                            font=("calibri", 15, "bold"), pady=10, anchor=CENTER, bg='White')
        self.label1.grid(row=1, column=0, columnspan=4, padx=(30, 0), sticky=S)

        self.frame1.rowconfigure(0, minsize=int(self.windowHeight / 4))

        # username label
        self.username_lab = Label(self.frame1, text="Username", font=("calibri", 10, "bold"), bg="White")
        self.username_lab.grid(row=2, column=0, pady=(0, 10), padx=(20, 10))

        # username entry field
        self.username = Entry(self.frame1, textvariable=self.username_e, relief=SUNKEN, bd=2, )
        self.username.bind('<FocusIn>', self.on_entry_click)
        self.username.bind('<Return>', self.login_verify)
        self.username.grid(row=2, column=1, columnspan=3, pady=(0, 10))

        # password label
        self.password_lab = Label(self.frame1, text="Password", font=("calibri", 10, "bold"), bg="white")
        self.password_lab.grid(row=3, column=0, padx=(20, 10))

        # password entry field
        self.password = Entry(self.frame1, textvariable=self.password_e, relief=SUNKEN, bd=2, show="*")
        self.password.bind('<FocusIn>', self.on_entry_click)
        self.password.bind('<Return>', self.login_verify)
        self.password.grid(row=3, column=1, columnspan=3)

        self.show_btn = Button(self.frame1, text = "Show", font=("times new roman", 10, "bold"), bg="Black",
                                   fg="red", width=7, command=lambda :self.show(self.password, self.show_btn))
        self.show_btn.grid(row=3, column=4, padx = 10)

        # forgot password
        self.forgot_lab = Label(self.frame1, text = "Forgot password", font = ("Calibri", 10, "bold"), bg = "White", fg = "Blue")
        self.forgot_lab.grid(row=4, column = 3, sticky = N+E)
        self.forgot_lab.bind('<Button-1>', self.forgot)

        # login button
        self.login_button = Button(self.frame1, text="Login", font=("times new roman", 10, "bold"), bg="Black",
                                   fg="red",
                                   width=20, command=self.login_verify)
        self.login_button.grid(row=5, column=0, columnspan=4, padx=(30, 0), pady=10, sticky=N)

        self.root.mainloop()
    def show(self, widget, widget1, event=None):
        widget.config(show="")
        widget1.config(text = "Hide", command = lambda :self.hide(widget,widget1))

    def hide(self, widget, widget1, event=None):
        widget.config(show="*")
        widget1.config(text = "Show", command = lambda :self.show(widget,widget1))

    def on_entry_click(self, event):

        if self.FirstClick:
            self.FirstClick = False
            # delete all the text in entry fields
            self.username.delete(0, 'end')
            self.password.delete(0, 'end')

    def login_verify(self, event=None):

        # getting username and password entered
        self.username_info = self.username.get()
        self.password_info = self.password.get()

        # checking if all fields are full
        if self.username_info == "":
            messagebox.showerror("error", "username can not be blank")
            self.username_e.set("Username")
            self.password_e.set("Password")
            self.FirstClick = True
            self.username_lab.focus()

        elif self.password_info == "":
            messagebox.showerror("error", "Password can not be blank")
            self.password.focus()

        else:

            db.db.cursor.execute("SELECT * FROM `login` WHERE `Username` = '%s' AND `Password`= md5('%s')" % (
            self.username_info, self.password_info))
            records = db.db.cursor.fetchall()

            if records:
                # destroy current window
                self.root.destroy()

                # open new window
                Menu = menu.Menu()
                Menu.menu()
            else:
                messagebox.showerror("Error", "Wrong Username or Password")
                # self.username_e.set("Username")
                self.password.delete(0, 'end')
                self.password.focus()

    def forgot(self, event=None):
        self.root.destroy()
        forgot = forgot_password.Forgot()
        forgot.forgot()


if __name__ == "__main__":
    x = Login()
    x.login()

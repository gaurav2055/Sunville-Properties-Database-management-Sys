from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import ttk
import db.db
import Login
import menu


class Register:
    def __init__(self):

        # creating tkinter window
        self.root = Tk()

        # setting window title
        self.root.title("Sunville Properties | Register")

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

    def register(self):

        # variable of entry fields
        self.username_e = StringVar()
        self.username_e.set("Username")
        self.password_e = StringVar()
        self.password_e.set("password")
        self.answer_var = StringVar()
        self.answer_var.set("Answer")
        self.password_e1 = StringVar()
        self.password_e1.set("password")

        # creating frame for register form
        self.frame1 = Frame(self.root, bg="White")
        self.frame1.place(x=0, y=0, width=int(self.windowWidth / 2), height=int(self.windowHeight))

        # creating frame for image
        self.frame2 = Frame(self.root, bg="blue", )
        self.frame2.place(x=int(self.windowWidth / 2), y=0)

        # getting image
        self.image1 = Image.open("D:/python/classes/Internship/property-consultants-mumbai.jpg")
        self.image1 = self.image1.resize((int(self.windowWidth / 2), int(self.windowHeight)), Image.ANTIALIAS)
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
        self.login_img = ImageTk.PhotoImage(self.image2, master = self.root)

        # placing login image and heading
        self.label1 = Label(self.frame1, image=self.login_img, text="Register", compound=LEFT,
                            font=("calibri", 15, "bold"), pady=10, anchor=CENTER, bg='White')
        self.label1.grid(row=1, column=0, columnspan=4, padx=(30, 0), sticky=S)

        self.frame1.rowconfigure(0, minsize=int(self.windowHeight / 4))

        # username label
        self.username_lab = Label(self.frame1, text="Username", font=("calibri", 10, "bold"), bg="White")
        self.username_lab.grid(row=2, column=0, pady=(0, 10))

        # username entry field
        self.username = Entry(self.frame1, textvariable=self.username_e, relief=SUNKEN, bd=2, )
        self.username.bind('<FocusIn>', self.on_entry_click)
        self.username.bind('<Return>', self.register_user)
        self.username.grid(row=2, column=1, columnspan=3, pady=(0, 10))

        # Question label
        self.question_lab = Label(self.frame1, text="question", font=("calibri", 10, "bold"), bg="white")
        self.question_lab.grid(row=3, column=0, pady = (0,10), padx = (10, 20))

        # questions list
        questions = ["What is your mother's maiden name", "What is the name of your first pet", "What is the name of "
                                                                                                "your first pet",
                     "What is your father's middle name"]

        # questions drop down
        self.question = ttk.Combobox(self.frame1, width = 33, values = questions, state = "readonly")
        self.question.grid(row=3, column=3, columnspan=5, pady = (0, 10))
        self.question.current(0)

        # answer Label
        self.answer_lab = Label(self.frame1, text="Answer", font=("calibri", 10, "bold"), bg="white")
        self.answer_lab.grid(row = 4, column = 0, padx = (20, 10), pady = (0, 10))

        # answer entry field
        self.answer = Entry(self.frame1, textvariable = self.answer_var, relief=SUNKEN, bd=2)
        self.answer.bind('<FocusIn>', self.on_entry_click)
        self.answer.bind('<Return>', self.register_user)
        self.answer.grid(row=4, column=1, columnspan=3, pady = (0, 10))

        # password label
        self.password_lab = Label(self.frame1, text="Password", font=("calibri", 10, "bold"), bg="white")
        self.password_lab.grid(row=5, column=0, padx=(20, 10), pady=(0, 10))

        # password entry field
        self.password = Entry(self.frame1, textvariable=self.password_e, relief=SUNKEN, bd=2, show="*")
        self.password.bind('<FocusIn>', self.on_entry_click)
        self.password.bind('<Return>', self.register_user)
        self.password.grid(row=5, column=1, columnspan=3)

        # show password button1
        self.show_btn1 = Button(self.frame1, text="Show", font=("times new roman", 10, "bold"), bg="Black",
                                fg="red", width=7, command=lambda: self.show(self.password, self.show_btn1))
        self.show_btn1.grid(row=5, column=4)

        # password confirmation label
        self.password_lab1 = Label(self.frame1, text="Password", font=("calibri", 10, "bold"), bg="white")
        self.password_lab1.grid(row=6, column=0, padx=(20, 10), pady=(0, 10))

        # password confirmation entry field
        self.password_1 = Entry(self.frame1, textvariable=self.password_e1, relief=SUNKEN, bd=2, show="*")
        self.password_1.bind('<FocusIn>', self.on_entry_click)
        self.password_1.bind('<FocusOut>', lambda e: self.password_confirmation(self.password_1))
        self.password_1.bind('<Return>', self.register_user)
        self.password_1.grid(row=6, column=1, columnspan=3)

        # show password button2
        self.show_btn2 = Button(self.frame1, text="Show", font=("times new roman", 10, "bold"), bg="Black",
                                fg="red", width=7, command=lambda: self.show(self.password_1, self.show_btn2))
        self.show_btn2.grid(row=6, column=4)

        # register button
        self.register_button = Button(self.frame1, text="Register", font=("times new roman", 10, "bold"), bg="Black",
                                   fg="red",
                                   width=20, command=self.register_user)
        self.register_button.grid(row=7, column=0, columnspan=4, padx=(30, 0), pady=10, sticky=N)

        # back to login button
        self.login_pg = Button(self.frame1, text = "Login Pg", font=("times new roman", 10, "bold"), bg="Black",
                                   fg="red",
                                   width=20, command=self.login)
        self.login_pg.grid(row=8, column=0, columnspan=4, padx=(30, 0), pady=10, sticky=N)
        # Menu page
        self.Menu = Button(self.frame1, text="Menu", bg="Black", fg="Red", command=self.menu, width=5)
        self.Menu.place(x=0, y=0)

        self.root.mainloop()

    def show(self, widget, widget1, event=None):
        widget.config(show="")
        widget1.config(text = "Hide", command = lambda :self.hide(widget,widget1))

    def hide(self, widget, widget1, event=None):
        widget.config(show="*")
        widget1.config(text = "Show", command = lambda :self.show(widget,widget1))

    def menu(self):
        self.root.destroy()
        x = menu.Menu()
        x.menu()

    def login(self):
        self.root.destroy()
        login = Login.Login()
        login.login()

    def password_confirmation(self, widget):
        if self.password_e.get() != self.password_e1.get() or self.password_e1.get() =="":
            widget.config(bg="red")
        else:
            widget.config(bg="White")

    def on_entry_click(self, event):

        if self.FirstClick:
            self.FirstClick = False
            # delete all the text in entry fields
            self.username.delete(0, 'end')
            self.password.delete(0, 'end')
            self.answer.delete(0, 'end')
            self.password_1.delete(0, 'end')

    def register_user(self, event=None):

        # getting username and password entered
        self.username_info = self.username_e.get()
        self.password_info = self.password_e.get()
        self.answer_info = self.answer_var.get()
        self.password_info1 = self.password_e1.get()
        self.question_info = self.question.get()

        # checking if all fields are full
        if self.username_info == "":
            messagebox.showerror("error", "username can not be blank")
            self.username_e.set("Username")
            self.password_e.set("Password")
            self.password_e1.set("Password")
            self.answer_var.set("Answer")
            self.FirstClick = True
            self.username_lab.focus()

        elif self.answer_info =="":
            messagebox.showerror("error", "Answer can not be blank")
            self.answer.focus()

        elif self.password_info == "":
            messagebox.showerror("error", "Password can not be blank")
            self.password.focus()

        elif self.password_info1 == "":
            messagebox.showerror("error", "Password can not be blank")
            self.password_1.focus()

        else:

            db.db.cursor.execute("SELECT * FROM `login` WHERE `Username` = '%s'" % self.username_info)
            records = db.db.cursor.fetchall()

            if records:
                messagebox.showerror("Error", "Username already exist")

            else:
                if self.password_info == self.password_info1:
                    query = """INSERT INTO `login`(`Username`, `Password`, `Question`, `Answer`) 
                    VALUES ("%s",md5("%s"), "%s","%s")"""

                    db.db.cursor.execute(query % (self.username_info, self.password_info, self.question_info, self.answer_info))
                    db.db.con.commit()
                    messagebox.showinfo("Success", "Registered successfully")
                else:
                    messagebox.showerror("Error", "Passwords don't match")



if __name__ == "__main__":
    x = Register()
    x.register()

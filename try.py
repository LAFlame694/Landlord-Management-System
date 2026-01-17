from tkinter import *
from tkinter import messagebox
import tkinter as tk
import random
import time

root = Tk()
root.geometry("1600x800+0+0")
root.title("RESTAURANT MANAGEMENT SYSTEM")
root.withdraw()

text_input = StringVar()


# Function to handle the login
def handle_login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "password":
        login_window.destroy()
        root.deiconify()  # Show the main window
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

login_window = tk.Toplevel(root)
login_window.title("Login Page")
login_window.geometry("400x300")
login_window.configure(bg="cyan4")

# Create the login form in the login window
login_frame = tk.Frame(login_window, bg="cyan4")
login_frame.pack(pady=50)

username_label = tk.Label(login_frame, text="Username:", font=("verdana", 20, "bold italic"))
username_label.grid(row=0, column=0, padx=10, pady=10)

username_entry = tk.Entry(login_frame,  highlightthickness=10)
username_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = tk.Label(login_frame, text="Password:", font=("verdana", 20, "bold italic"))
password_label.grid(row=1, column=0, padx=10, pady=10)

password_entry = tk.Entry(login_frame, show="*",  highlightthickness=10)
password_entry.grid(row=1, column=1, padx=10, pady=10)

login_button = tk.Button(login_frame, text="Login", command=handle_login)
login_button.grid(row=2, columnspan=2, pady=20)

# create frames
frame = Frame(root, width=1600, height=50, bg="powder blue", relief=SUNKEN)
frame.pack(side=TOP)

frame1 = Frame(root, width=800, height=700, relief=SUNKEN)
frame1.pack(side=LEFT)

frame2 = Frame(root, width=300, height=700, relief=SUNKEN)
frame2.pack(side=RIGHT)

#============================time=======================================================================================
# create localtime variable
localtime = time.asctime(time.localtime(time.time()))

#============================info=======================================================================================
# create labels
lbltitle = Label(frame, text="Restaurant Management System", font=("verdana", 50, "bold"), fg="steel blue", bd=10)
lbltitle.grid(row=0)

lbltime = Label(frame, text=localtime, font=("verdana", 20, "bold"), fg="steel blue", bd=10)
lbltime.grid(row=1)

#============================calculator=================================================================================
operator = ""
def btnclick(number):
    global operator
    operator = operator + str(number)
    text_input.set(operator)

def btnclr():
    global operator
    operator = ""
    text_input.set(operator)

def btnexecute():
    global operator
    execute = str(eval(operator))
    operator = ""
    text_input.set(execute)

def Ref():
    x = random.randint(12908, 50876)
    randomRef = str(x)
    rand.set(randomRef)

    cost_fries = float(fries.get())
    cost_drinks = float(drinks.get())
    cost_filet = float(filet.get())
    cost_burger = float(burger.get())
    cost_chicken_burger = float(chicken_burger.get())
    cost_cheese_burger = float(cheese_burger.get())

# declare local variables for the cost of whatever is entered in the entry widget
    cost_of_fries = cost_fries * 0.99
    cost_of_drinks = cost_drinks * 1.00
    cost_of_filet = cost_filet * 2.99
    cost_of_burger = cost_burger * 2.87
    cost_of_chickenburger = cost_chicken_burger * 2.89
    cost_of_cheeseburger = cost_cheese_burger * 2.69

    cost_of_meal = "$" + str("%.2f" % (cost_of_fries + cost_of_drinks + cost_of_filet +
                                      cost_of_burger + cost_of_chickenburger + cost_of_cheeseburger))

    pay_tax = ((cost_of_fries + cost_of_drinks + cost_of_filet +
                cost_of_burger + cost_of_chickenburger + cost_of_cheeseburger) * 0.2)

    total_cost = (cost_of_fries + cost_of_drinks + cost_of_filet +
                                      cost_of_burger + cost_of_chickenburger + cost_of_cheeseburger)

    ser_charge = ((cost_of_fries + cost_of_drinks + cost_of_filet +
                                      cost_of_burger + cost_of_chickenburger + cost_of_cheeseburger) / 99)

    service = "$" + str("%.2f" % ser_charge)

    overall_cost = "$" + str("%.2f" % (pay_tax + total_cost + ser_charge))

    paid_tax = "$" + str("%.2f" % pay_tax)

    service_charge.set(service)
    cost.set(cost_of_meal)
    tax.set(paid_tax)
    subtotal.set(cost_of_meal)
    total.set(overall_cost)


def qExit():
   root.destroy()

def Reset():
    rand.set("")
    fries.set("")
    burger.set("")
    filet.set("")
    subtotal.set("")
    total.set("")
    service_charge.set("")
    drinks.set("")
    tax.set("")
    cost.set("")
    chicken_burger.set("")
    cheese_burger.set("")

# create entry field for calculator
txtdisplay = Entry(frame2, font=("verdana", 15, "bold"), textvariable = text_input, bd=30, insertwidth=2, bg="powder blue", justify="right")
txtdisplay.grid(columnspan=4)

# create calculator buttons
btn7 = Button(frame2, text="7", bd=8, font=("verdana", 15, "bold"), padx=10, pady=20, fg="black", bg="powder blue", command=lambda :btnclick(7))
btn7.grid(row = 2, column = 0)

btn8 = Button(frame2, text="8", bd=8, font=("verdana", 15, "bold"), padx=10, pady=20, fg="black", bg="powder blue", command=lambda :btnclick(8))
btn8.grid(row = 2, column = 1)

btn9 = Button(frame2, text="9", bd=8, font=("verdana", 15, "bold"), padx=10, pady=20, fg="black", bg="powder blue", command=lambda :btnclick(9))
btn9.grid(row = 2, column = 2)

addition = Button(frame2, text="+", bd=8, font=("verdana", 15, "bold"), padx=10, pady=20, fg="black", bg="powder blue", command=lambda :btnclick("+"))
addition.grid(row = 2, column = 3)
#=======================================================================================================================
btn4 = Button(frame2, text="4", bd=8, font=("verdana", 15, "bold"), padx=10, pady=20, fg="black", bg="powder blue", command=lambda :btnclick(4))
btn4.grid(row = 3, column = 0)

btn5 = Button(frame2, text="5", bd=8, font=("verdana", 15, "bold"), padx=10, pady=20, fg="black", bg="powder blue", command=lambda :btnclick(5))
btn5.grid(row = 3, column = 1)

btn9 = Button(frame2, text="6", bd=8, font=("verdana", 15, "bold"), padx=10, pady=20, fg="black", bg="powder blue", command=lambda :btnclick(6))
btn9.grid(row = 3, column = 2)

subtraction = Button(frame2, text="-", bd=8, font=("verdana", 15, "bold"), padx=10, pady=20, fg="black", bg="powder blue", command=lambda :btnclick("-"))
subtraction.grid(row = 3, column = 3)
#=======================================================================================================================
btn1 = Button(frame2, text="1", bd=8, font=("verdana", 15, "bold"), padx=10, pady=20, fg="black", bg="powder blue", command=lambda :btnclick(1))
btn1.grid(row = 4, column = 0)

btn2 = Button(frame2, text="2", bd=8, font=("verdana", 15, "bold"), padx=10, pady=20, fg="black", bg="powder blue", command=lambda :btnclick(2))
btn2.grid(row = 4, column = 1)

btn3 = Button(frame2, text="3", bd=8, font=("verdana", 15, "bold"), padx=10, pady=20, fg="black", bg="powder blue", command=lambda :btnclick(3))
btn3.grid(row = 4, column = 2)

multiplication = Button(frame2, text="x", bd=8, font=("verdana", 15, "bold"), padx=10, pady=20, fg="black", bg="powder blue", command=lambda :btnclick("*"))
multiplication.grid(row = 4, column = 3)
#=======================================================================================================================
btn0 = Button(frame2, text="0", bd=8, font=("verdana", 15, "bold"), padx=10, pady=20, fg="black", bg="powder blue", command=lambda :btnclick(0))
btn0.grid(row = 5, column = 0)

clear = Button(frame2, text="c", bd=8, font=("verdana", 15, "bold"), padx=10, pady=20, fg="black", bg="powder blue", command=btnclr)
clear.grid(row = 5, column = 1)

equals = Button(frame2, text="=", bd=8, font=("verdana", 15, "bold"), padx=10, pady=20, fg="black", bg="powder blue", command=btnexecute)
equals.grid(row = 5, column = 2)

division = Button(frame2, text="/", bd=8, font=("verdana", 15, "bold"), padx=10, pady=20, fg="black", bg="powder blue", command=lambda :btnclick("/"))
division.grid(row = 5, column = 3)
#===============================Restaurant Info 1=======================================================================
rand = StringVar()
fries = StringVar()
burger = StringVar()
filet = StringVar()
subtotal = StringVar()
total = StringVar()
service_charge = StringVar()
drinks = StringVar()
tax = StringVar()
cost = StringVar()
chicken_burger = StringVar()
cheese_burger = StringVar()

lblreference = Label(frame1, font=("verdana", 16, "bold"), text="Reference", bd=16, anchor="w")
lblreference.grid(row = 0, column = 0, sticky = W)
entryreference = Entry(frame1, font=("verdana", 16, "bold"), textvariable=rand, bd=10, insertwidth=4, bg="powder blue", justify="right")
entryreference.grid(row = 0, column = 1)

lblfries = Label(frame1, font=("verdana", 16, "bold"), text="Large Fries", bd=16, anchor="w")
lblfries.grid(row = 1, column = 0, sticky = W)
entryfries = Entry(frame1, font=("verdana", 16, "bold"), textvariable=fries, bd=10, insertwidth=4, bg="powder blue", justify="right")
entryfries.grid(row = 1, column = 1)

lblburger = Label(frame1, font=("verdana", 16, "bold"), text="Burger Meal", bd=16, anchor="w")
lblburger.grid(row = 2, column = 0, sticky = W)
entryburger = Entry(frame1, font=("verdana", 16, "bold"), textvariable=burger, bd=10, insertwidth=4, bg="powder blue", justify="right")
entryburger.grid(row = 2, column = 1)

lblfilet = Label(frame1, font=("verdana", 16, "bold"), text="Filet_o_Meal", bd=16, anchor="w")
lblfilet.grid(row = 3, column = 0, sticky = W)
entryfilet= Entry(frame1, font=("verdana", 16, "bold"), textvariable=filet, bd=10, insertwidth=4, bg="powder blue", justify="right")
entryfilet.grid(row = 3, column = 1)

lblchicken= Label(frame1, font=("verdana", 16, "bold"), text="Chicken Meal", bd=16, anchor="w")
lblchicken.grid(row = 4, column = 0, sticky = W)
entrychicken = Entry(frame1, font=("verdana", 16, "bold"), textvariable=chicken_burger, bd=10, insertwidth=4, bg="powder blue", justify="right")
entrychicken.grid(row = 4, column = 1)

lblcheese= Label(frame1, font=("verdana", 16, "bold"), text="Cheese Meal", bd=16, anchor="w")
lblcheese.grid(row = 5, column = 0, sticky = W)
entrycheese = Entry(frame1, font=("verdana", 16, "bold"), textvariable=cheese_burger, bd=10, insertwidth=4, bg="powder blue", justify="right")
entrycheese.grid(row = 5, column = 1)

#===============================Restaurant Info 2=======================================================================
lbldrinks = Label(frame1, font=("verdana", 16, "bold"), text="Drinks", bd=16, anchor="w")
lbldrinks.grid(row = 0, column = 2, sticky = W)
entrydrinks = Entry(frame1, font=("verdana", 16, "bold"), textvariable=drinks, bd=10, insertwidth=4, bg="#ffffff", justify="right")
entrydrinks.grid(row = 0, column = 3)

lblcost = Label(frame1, font=("verdana", 16, "bold"), text="Cost of Meal", bd=16, anchor="w")
lblcost.grid(row = 1, column = 2, sticky = W)
entrycost = Entry(frame1, font=("verdana", 16, "bold"), textvariable=cost, bd=10, insertwidth=4, bg="#ffffff", justify="right")
entrycost.grid(row = 1, column = 3)

lblservice = Label(frame1, font=("verdana", 16, "bold"), text="Service Charge", bd=16, anchor="w")
lblservice.grid(row = 2, column = 2, sticky = W)
entryservice = Entry(frame1, font=("verdana", 16, "bold"), textvariable=service_charge, bd=10, insertwidth=4, bg="#ffffff", justify="right")
entryservice.grid(row = 2, column = 3)

lbltax = Label(frame1, font=("verdana", 16, "bold"), text="State Tax", bd=16, anchor="w")
lbltax.grid(row = 3, column = 2, sticky = W)
entrytax= Entry(frame1, font=("verdana", 16, "bold"), textvariable=tax, bd=10, insertwidth=4, bg="#ffffff", justify="right")
entrytax.grid(row = 3, column = 3)

lblsubtotal= Label(frame1, font=("verdana", 16, "bold"), text="Sub Total", bd=16, anchor="w")
lblsubtotal.grid(row = 4, column = 2, sticky = W)
entrysubtotal= Entry(frame1, font=("verdana", 16, "bold"), textvariable=subtotal, bd=10, insertwidth=4, bg="#ffffff", justify="right")
entrysubtotal.grid(row = 4, column = 3)

lbltotalcost= Label(frame1, font=("verdana", 16, "bold"), text="Total Cost", bd=16, anchor="w")
lbltotalcost.grid(row = 5, column = 2, sticky = W)
entrytotalcost = Entry(frame1, font=("verdana", 16, "bold"), textvariable=total, bd=10, insertwidth=4, bg="#ffffff", justify="right")
entrytotalcost.grid(row = 5, column = 3)

#============================================Buttons====================================================================
btntotal = Button(frame1, bd=16, padx=16, pady=8, font=("verdana", 16, "bold"), text="Total", fg="black", bg="powder blue", width=10, command=Ref)
btntotal.grid(row = 7, column = 1)

btnreset= Button(frame1, bd=16, padx=16, pady=8, font=("verdana", 16, "bold"), text="Reset", fg="black", bg="powder blue", width=10, command=Reset)
btnreset.grid(row = 7, column = 2)
btnexit = Button(frame1, bd=16, padx=16, pady=8, font=("verdana", 16, "bold"), text="Exit", fg="black", bg="powder blue", width=10, command=qExit)
btnexit.grid(row = 7, column = 3)

root.mainloop()
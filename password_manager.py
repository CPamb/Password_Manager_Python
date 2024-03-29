import pyperclip

from tkinter import *
from tkinter import messagebox
import random
import string
from tkinter import font
import json

FONT_NAME = "Jetbrains Mono"
FONT = (FONT_NAME, 12 ,"bold")
LETTERS = string.ascii_letters
NUMBERS = string.digits
SYMBOLS = string.punctuation
COMBINED_LIST = list(LETTERS + NUMBERS + SYMBOLS)
BLACK = "#1A1A1B"
BUTTON_COLOR = "#00D1CD"
CYAN = "#7DEDFF"
GREY = "#393E46"
WHITE = "#BBBFCA"
BG = "#353941"


#Windows formatting

window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50, bg=BLACK)

canvas = Canvas(width=200, height=200, highlightthickness=0,  bg=BLACK)
canvas.grid(row=0, column=1)

#label
website_label = Label(text="Website:", font=FONT, fg=CYAN, bg=BLACK)
website_label.grid(row=1, column=0)

email_label= Label(text="Email/username:", font=FONT, fg=CYAN, bg=BLACK)
email_label.config(padx=35)
email_label.grid(row=2, column=0)

password_label = Label(text="Password", font=FONT, fg=CYAN, bg=BLACK)
password_label.grid(row=3, column=0)



#ENTRIES
website_entry = Entry(width=38, bg=BG, fg="white", bd=0)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=56, bg=BG, fg="white", bd=0)
email_entry.insert(0, "example@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2)

password_entry = Entry(width=38, bg=BG, fg="white", bd=0)
password_entry.grid(row=3, column=1)

#Generate Password Function

def generate_password():
    password_entry.delete(0,END)
    random.shuffle(COMBINED_LIST)
    max_length = 12
    password_list = []
    for _ in range(max_length):
        password_list.append(random.choice(COMBINED_LIST))
    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


#Saving Password function


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Warning", message="Make sure you don't have any empty fields.")
    else:
        new_data = {
            website: {
                "email": email,
                "password": password
            }
        }
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data,data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


#Finding Password function

def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=f"info about {website}",
                                message=f"Email = {email}|nPassword = {password}")
            pyperclip.copy(password)
        else:
            messagebox.showingo(title="Error", message=f"No details for {website} exists.")



#Showing all the details function

def show_all_details():
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            details_windows = Tk()
            details_windows.title("Password Details")
            details_windows.config(bg=BLACK)
            details_windows.config(padx=10, pady=10)
            row_index = 1

            title = Label(details_windows, text="Passwords: ", font=(FONT_NAME, 16, "bold"), bg=BLACK, fg=WHITE)
            title.grid(column=0, row=0)

            for key in data.keys():
                website_string = Label(details_windows, text=f"{key}:", font=FONT, bg=BLACK, fg=CYAN)
                website_string.grid(column=0, row=row_index)

                email = data[key]["email"]
                password = data[key]["password"]
                details_label = Label(details_windows, text=f" Email: {email}\nPassword: {password}",
                                    font=(FONT_NAME, 11), bg=BLACK, fg=WHITE)
                details_label.config(padx=10, pady=15)
                details_label.grid(column=1, row=row_index)

                row_index += 1

#Search Button

search_button = Button(text="Search", width=13, command=find_password, fg=WHITE, bg=GREY, bd=0, font=(FONT_NAME, 9))
search_button.grid(row=1, column=2)

generate_password_button = Button(width=13, text="Generate", command=generate_password,fg=WHITE,bg=GREY, bd=0, font=(FONT_NAME, 9))
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=48, command=save, fg=WHITE, bg=GREY, bd=0, font=(FONT_NAME, 9))
add_button.grid(row=4, column=1, columnspan=2, pady=7)

show_details_button = Button(text="Show all passwords", width=48, command=show_all_details, fg=WHITE, bg=GREY, bd=0, font=(FONT_NAME, 9))
show_details_button.grid(row=5, column=1, columnspan=2)

window.mainloop()




import random
from tkinter import *
import pandas
from PIL import ImageTk, Image

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/Port.csv", encoding='latin-1')
except FileNotFoundError:
    original_data = pandas.read_csv("data/Port.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="White")
    canvas.itemconfig(card_background, image=card_back_img)

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    print(current_card["Portuguese"])
    canvas.itemconfig(card_title, text="Portuguese", fill="black")
    canvas.itemconfig(card_word, text=current_card["Portuguese"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

window = Tk()
window.title("Portuguese Flash Cards!")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)

card_front_img = ImageTk.PhotoImage(file="Images/card_front.png")
card_back_img = ImageTk.PhotoImage(file="Images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Aerial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Aerial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)
cross_image = ImageTk.PhotoImage(file="Images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = ImageTk.PhotoImage(file="Images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()

print("hello")

window.mainloop()
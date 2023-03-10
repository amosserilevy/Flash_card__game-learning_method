from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"

FRONT_CARD_PATH = "images/card_front.png"
BACK_CARD_PATH = "images/card_back.png"
RIGHT_BUTTON_PATH = "images/right.png"
WRONG_BUTTON_PATH = "images/wrong.png"

DATA_FILE_PATH = "./data/french_words.csv"



try:
    saved_data = pandas.read_csv("./data/words to learn.csv")
    print("saved file")
    # pass
except FileNotFoundError:
    original_data = pandas.read_csv(DATA_FILE_PATH)
    to_learn = original_data.to_dict(orient='records')
    print("original file")
    # pass
else:
    to_learn = saved_data.to_dict(orient='records')
    # pass
#
# ---------------------------- GENERATE RANDOM WORD FROM DATA ------------------------------- #

current_card = {}


def next_card():
    global current_card, time_flipper

    window.after_cancel(time_flipper)
    current_card = random.choice(to_learn)

    french_word = current_card["French"]

    canvas.itemconfig(tagOrId=canvas_title, text="French", fill="black")
    canvas.itemconfig(tagOrId=canvas_word, text=french_word, fill="black")

    canvas.itemconfig(tagOrId=curr_canvas, image=front_card_img)

    print(f"length of word list = {len(to_learn)}")
    time_flipper = window.after(ms=3000, func=flip_card)


def flip_card():
    global current_card

    english_word = current_card["English"]

    window.after_cancel(window.winfo_id())
    canvas.itemconfig(tagOrId=curr_canvas, image=back_card_img)

    print("flipped the card")

    canvas.itemconfig(tagOrId=canvas_title, text="English", fill="white")
    canvas.itemconfig(tagOrId=canvas_word, text=english_word, fill="white")

    print(english_word)


def known_card():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv(path_or_buf="data/words to learn.csv", index=False)
    # words_to_learn.to_csv(index=False)
    next_card()

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

time_flipper = window.after(ms=3000, func=flip_card)
# ---------------------------- IMAGE ------------------------------- #

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

# just an image interpreter of tkinter
back_card_img = PhotoImage(file=BACK_CARD_PATH)
front_card_img = PhotoImage(file=FRONT_CARD_PATH)

curr_canvas = canvas.create_image(400, 263, image=front_card_img)

canvas_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
canvas_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# activating the function to get input text
next_card()

# ---------------------------- BUTTONS ------------------------------- #

wrong_button_img = PhotoImage(file=WRONG_BUTTON_PATH)
wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

right_button_img = PhotoImage(file=RIGHT_BUTTON_PATH)
right_button = Button(image=right_button_img, highlightthickness=0, command=known_card)
right_button.grid(column=1, row=1)

window.mainloop()

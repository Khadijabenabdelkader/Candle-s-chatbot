import tkinter as tk
from tkinter import ttk
from chatbot import get_response

# ================= COLORS =================
BG_COLOR = "#f8f1f4"        # rose très clair
HEADER_COLOR = "#d8a7b1"    # rose poudré
USER_COLOR = "#e75480"      # rose foncé
BOT_COLOR = "#ffffff"       # blanc chic
TEXT_COLOR = "#4a4a4a"
GOLD_COLOR = "#c6a75e"      # doré

# ================= WINDOW =================
window = tk.Tk()
window.title("Luxe Candle Boutique 🕯️")
window.geometry("500x650")
window.configure(bg=BG_COLOR)
window.resizable(False, False)

# ================= HEADER =================
header = tk.Frame(window, bg=HEADER_COLOR, height=70)
header.pack(fill=tk.X)

title = tk.Label(
    header,
    text="🕯️ Luxe Candle Boutique",
    bg=HEADER_COLOR,
    fg="white",
    font=("Georgia", 18, "bold")
)
title.pack(pady=20)

# ================= CHAT AREA =================
chat_frame = tk.Frame(window, bg=BG_COLOR)
chat_frame.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

canvas = tk.Canvas(chat_frame, bg=BG_COLOR, highlightthickness=0)
scrollbar = ttk.Scrollbar(chat_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ================= MESSAGE FUNCTION =================
def add_message(message, sender):
    bubble_frame = tk.Frame(scrollable_frame, bg=BG_COLOR)

    if sender == "user":
        bubble = tk.Label(
            bubble_frame,
            text=message,
            bg=USER_COLOR,
            fg="white",
            wraplength=320,
            justify="left",
            font=("Helvetica", 11),
            padx=12,
            pady=8
        )
        bubble_frame.pack(anchor="e", pady=6)

    else:
        bubble = tk.Label(
            bubble_frame,
            text=message,
            bg=BOT_COLOR,
            fg=TEXT_COLOR,
            wraplength=320,
            justify="left",
            font=("Helvetica", 11),
            padx=12,
            pady=8,
            highlightbackground=GOLD_COLOR,
            highlightthickness=1
        )
        bubble_frame.pack(anchor="w", pady=6)

    bubble.pack()
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

# ================= SEND FUNCTION =================
def send_message(event=None):
    user_message = entry.get().strip()
    if not user_message:
        return

    add_message(user_message, "user")
    entry.delete(0, tk.END)

    bot_response = get_response(user_message)
    add_message(bot_response, "bot")

# ================= INPUT AREA =================
input_frame = tk.Frame(window, bg=BG_COLOR)
input_frame.pack(fill=tk.X, pady=10)

entry = tk.Entry(
    input_frame,
    font=("Helvetica", 12),
    bg="white",
    fg=TEXT_COLOR,
    relief=tk.FLAT,
    width=30
)
entry.pack(side=tk.LEFT, padx=15, pady=10, fill=tk.X, expand=True)
entry.bind("<Return>", send_message)

send_button = tk.Button(
    input_frame,
    text="Send",
    command=send_message,
    bg=GOLD_COLOR,
    fg="white",
    font=("Helvetica", 11, "bold"),
    relief=tk.FLAT,
    padx=20,
    pady=5
)
send_button.pack(side=tk.RIGHT, padx=15)

add_message("✨ Welcome to Luxe Candle Boutique 🕯️\nHow may I assist you today?", "bot")

window.mainloop()

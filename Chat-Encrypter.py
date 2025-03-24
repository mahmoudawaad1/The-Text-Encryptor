import os
import pyperclip
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, Frame, ttk
from tkinter.font import Font
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"

def load_or_generate_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key

key = load_or_generate_key()
cipher = Fernet(key)

def encrypt_text():
    text = input_var.get().strip()
    if text:
        encrypted = cipher.encrypt(text.encode()).decode()
        output_var.set(encrypted)
        update_status("Encryption successful!", "success")
    else:
        update_status("Error: Enter text to encrypt", "error")

def decrypt_text():
    encrypted_text = output_var.get().strip()
    try:
        decrypted = cipher.decrypt(encrypted_text.encode()).decode()
        output_var.set(decrypted)
        update_status("Decryption successful!", "success")
    except Exception:
        update_status("Error: Invalid encrypted text!", "error")

def copy_to_clipboard():
    text = output_var.get()
    if text:
        pyperclip.copy(text)
        update_status("Copied to clipboard!", "info")

def update_status(message, type_):
    status_var.set(message)
    if type_ == "error":
        status_label.config(fg="#ff4444")
    elif type_ == "success":
        status_label.config(fg="#00aa00")
    else:
        status_label.config(fg="#5555ff")
    root.after(5000, lambda: status_var.set("Ready"))

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        bg_color = "#2d2d2d"
        fg_color = "#ffffff"
        entry_bg = "#3d3d3d"
        readonly_bg = "#3d3d3d"
    else:
        bg_color = "#f0f0f0"
        fg_color = "#000000"
        entry_bg = "#ffffff"
        readonly_bg = "#ffffff"
    
    root.config(bg=bg_color)
    main_frame.config(bg=bg_color)
    input_frame.config(bg=bg_color)
    output_frame.config(bg=bg_color)
    button_frame.config(bg=bg_color)
    status_frame.config(bg=bg_color)
    
    for label in all_labels:
        label.config(bg=bg_color, fg=fg_color)
    
    for entry in all_entries:
        entry.config(bg=entry_bg, fg=fg_color, insertbackground="white" if dark_mode else "black")
    
    output_entry.config(readonlybackground=readonly_bg)
    theme_btn.config(text="☀️ Light Mode" if dark_mode else "🌙 Dark Mode")

root = Tk()
root.title("Ultimate Text Encryptor/Decryptor")
root.geometry("550x400")
root.minsize(500, 350)
root.config(bg="#f0f0f0")

title_font = Font(family="Helvetica", size=16, weight="bold")
label_font = Font(family="Segoe UI", size=10)
entry_font = Font(family="Consolas", size=10)
button_font = Font(family="Segoe UI", size=10, weight="bold")

input_var = StringVar()
output_var = StringVar()
status_var = StringVar()
status_var.set("Ready")
dark_mode = False
all_labels = []
all_entries = []

main_frame = Frame(root, padx=25, pady=20, bg="#f0f0f0")
main_frame.pack(expand=True, fill="both")

title_label = Label(main_frame, text="🔒 Ultimate Text Encryptor/Decryptor", font=title_font, bg="#f0f0f0", pady=5)
title_label.pack()
all_labels.append(title_label)

input_frame = Frame(main_frame, bg="#f0f0f0")
input_frame.pack(fill="x", pady=(10, 5))

input_label = Label(input_frame, text="Enter Text:", font=label_font, anchor="w", bg="#f0f0f0")
input_label.pack(fill="x")
all_labels.append(input_label)

input_entry = Entry(input_frame, textvariable=input_var, font=entry_font, bd=2, relief="groove")
input_entry.pack(fill="x", ipady=5, pady=(0, 5))
all_entries.append(input_entry)

output_frame = Frame(main_frame, bg="#f0f0f0")
output_frame.pack(fill="x", pady=(10, 5))

output_label = Label(output_frame, text="Result:", font=label_font, anchor="w", bg="#f0f0f0")
output_label.pack(fill="x")
all_labels.append(output_label)

output_entry = Entry(output_frame, textvariable=output_var, font=entry_font, state="readonly", readonlybackground="#ffffff", fg="#0000aa", bd=2, relief="groove")
output_entry.pack(fill="x", ipady=5)
all_entries.append(output_entry)

button_frame = Frame(main_frame, bg="#f0f0f0")
button_frame.pack(fill="x", pady=(15, 10))

btn_style = "TButton"
encrypt_btn = ttk.Button(button_frame, text="🔒 Encrypt", command=encrypt_text, style=btn_style)
encrypt_btn.pack(side="left", expand=True, padx=5)

decrypt_btn = ttk.Button(button_frame, text="🔓 Decrypt", command=decrypt_text, style=btn_style)
decrypt_btn.pack(side="left", expand=True, padx=5)

copy_btn = ttk.Button(button_frame, text="📋 Copy", command=copy_to_clipboard, style=btn_style)
copy_btn.pack(side="left", expand=True, padx=5)

theme_btn = ttk.Button(button_frame, text="🌙 Dark Mode", command=toggle_theme, style=btn_style)
theme_btn.pack(side="right", padx=5)

status_frame = Frame(main_frame, bg="#f0f0f0")
status_frame.pack(fill="x", pady=(10, 0))

status_label = Label(status_frame, textvariable=status_var, font=label_font, fg="#555555", bg="#f0f0f0", anchor="w")
status_label.pack(fill="x")
all_labels.append(status_label)

style = ttk.Style()
style.configure("TButton", font=button_font, padding=8)
style.map("TButton", foreground=[('pressed', 'white'), ('active', 'white')], background=[('pressed', '#0066cc'), ('active', '#0066cc')])

input_entry.focus()

root.mainloop()

#Note: the first encrypt should be the key between you and the one your chatting with and you both should type the same key and the first encrypt command (Have fun)

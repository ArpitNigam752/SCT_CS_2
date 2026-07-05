import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageOps, ImageTk
import numpy as np
import os

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Image Encryption Tool")
root.geometry("700x500")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

# ---------------- VARIABLES ----------------
selected_file = ""

# ---------------- TITLE ----------------
title = tk.Label(
    root,
    text="🖼️ Image Encryption Tool",
    font=("Arial", 22, "bold"),
    bg="#1e1e1e",
    fg="white"
)
title.pack(pady=15)

# ---------------- STATUS ----------------
status_label = tk.Label(
    root,
    text="Status : Ready",
    font=("Arial", 10),
    bg="#1e1e1e",
    fg="lightgreen"
)
status_label.pack(pady=5)

# ---------------- IMAGE PREVIEW ----------------
preview_label = tk.Label(root, bg="#1e1e1e")
preview_label.pack(pady=10)

# ---------------- FILE LABEL ----------------
file_label = tk.Label(
    root,
    text="No Image Selected",
    font=("Arial", 10),
    bg="#1e1e1e",
    fg="white",
    wraplength=600
)
file_label.pack()

# ---------------- KEY INPUT ----------------
tk.Label(
    root,
    text="Secret Key",
    font=("Arial", 12, "bold"),
    bg="#1e1e1e",
    fg="white"
).pack(pady=(15, 5))

key_entry = tk.Entry(root, font=("Arial", 12), width=10, justify="center")
key_entry.insert(0, "50")
key_entry.pack()

# ---------------- BROWSE FUNCTION ----------------
def browse_image():
    global selected_file

    selected_file = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )

    if selected_file:
        file_label.config(text=f"Selected: {os.path.basename(selected_file)}")

        image = Image.open(selected_file)
        image = ImageOps.exif_transpose(image)
        image.thumbnail((220, 220))

        photo = ImageTk.PhotoImage(image)
        preview_label.config(image=photo)
        preview_label.image = photo

# ---------------- ENCRYPT FUNCTION ----------------
def encrypt_image():
    if not selected_file:
        messagebox.showerror("Error", "Please select an image first!")
        return

    try:
        key = int(key_entry.get())
    except:
        messagebox.showerror("Error", "Key must be a number!")
        return

    image = Image.open(selected_file)
    image = ImageOps.exif_transpose(image)

    img_array = np.array(image)

    encrypted_array = (img_array.astype(np.int16) + key) % 256
    encrypted_array = encrypted_array.astype(np.uint8)

    encrypted_img = Image.fromarray(encrypted_array)
    encrypted_img.save("encrypted.png")

    preview = Image.open("encrypted.png")
    preview.thumbnail((220, 220))

    photo = ImageTk.PhotoImage(preview)
    preview_label.config(image=photo)
    preview_label.image = photo

    status_label.config(text="Status : Image Encrypted Successfully")
    messagebox.showinfo("Success", "Image Encrypted Successfully!")

# ---------------- DECRYPT FUNCTION ----------------
def decrypt_image():
    if not os.path.exists("encrypted.png"):
        messagebox.showerror("Error", "No encrypted image found!")
        return

    try:
        key = int(key_entry.get())
    except:
        messagebox.showerror("Error", "Key must be a number!")
        return

    encrypted_image = Image.open("encrypted.png")
    encrypted_array = np.array(encrypted_image)

    decrypted_array = (encrypted_array.astype(np.int16) - key) % 256
    decrypted_array = decrypted_array.astype(np.uint8)

    decrypted_img = Image.fromarray(decrypted_array)
    decrypted_img.save("decrypted.png")

    preview = Image.open("decrypted.png")
    preview.thumbnail((220, 220))

    photo = ImageTk.PhotoImage(preview)
    preview_label.config(image=photo)
    preview_label.image = photo

    status_label.config(text="Status : Image Decrypted Successfully")
    messagebox.showinfo("Success", "Image Decrypted Successfully!")

# ---------------- BUTTONS ----------------
btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=20)

tk.Button(
    btn_frame,
    text="📂 Browse Image",
    font=("Arial", 12, "bold"),
    bg="#0d6efd",
    fg="white",
    width=15,
    command=browse_image
).grid(row=0, column=0, padx=10)

tk.Button(
    btn_frame,
    text="🔒 Encrypt",
    font=("Arial", 12, "bold"),
    bg="green",
    fg="white",
    width=15,
    command=encrypt_image
).grid(row=0, column=1, padx=10)

tk.Button(
    btn_frame,
    text="🔓 Decrypt",
    font=("Arial", 12, "bold"),
    bg="red",
    fg="white",
    width=15,
    command=decrypt_image
).grid(row=0, column=2, padx=10)

# ---------------- FOOTER ----------------
footer = tk.Label(
    root,
    text="Developed by Arpit",
    font=("Arial", 10),
    bg="#1e1e1e",
    fg="gray"
)
footer.pack(side="bottom", pady=10)

# ---------------- RUN APP ----------------
root.mainloop()
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, Toplevel
from PIL import Image, ImageTk, ImageOps
import os
import random
import string

class VotingApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Visual Cryptography for Voting System')
        self.master.geometry('500x300')

        self.voter_id = self.ask_voter_id()
        if not self.voter_id:
            messagebox.showerror("Error", "No Voter ID provided. Exiting.")
            self.master.destroy()
            return

        tk.Button(master, text="Create Shares", command=self.create_shares, height=2, width=20).pack(pady=5)
        tk.Button(master, text="Combine Shares", command=self.combine_action, height=2, width=20).pack(pady=5)
        self.view_button = tk.Button(master, text="View Images", command=self.view_images, height=2, width=20, state='disabled')
        self.view_button.pack(pady=5)

        self.share1_path = ''
        self.share2_path = ''
        self.combined_path = ''

    def ask_voter_id(self):
        return simpledialog.askstring("Voter ID", "Please enter your Voter ID:")

    def verify_captcha(self):
        characters = string.ascii_letters + string.digits
        captcha = ''.join(random.choice(characters) for _ in range(6))
        user_input = simpledialog.askstring("CAPTCHA Verification", f"Please enter the text to verify you are human: {captcha}")
        return user_input == captcha

    def create_shares(self):
        if self.verify_captcha():
            file_path = filedialog.askopenfilename()
            if file_path:
                self.generate_share(file_path)
                messagebox.showinfo("Shares Created", "Shares have been successfully created.")
                self.view_button['state'] = 'normal'
        else:
            messagebox.showwarning("Verification Failed", "Failed to verify CAPTCHA. Please try again.")

    def generate_share(self, image_path):
        original_image = Image.open(image_path).convert('1')
        width, height = original_image.size

        share1 = Image.new('1', (width, height))
        share2 = Image.new('1', (width, height))

        for x in range(width):
            for y in range(height):
                original_pixel = original_image.getpixel((x, y))
                share1_pixel = random.randint(0, 1)
                share2_pixel = original_pixel ^ share1_pixel
                share1.putpixel((x, y), share1_pixel * 255)
                share2.putpixel((x, y), share2_pixel * 255)

        self.share1_path = f'{self.voter_id}_share1.png'
        share1.save(self.share1_path)
        self.share2_path = f'{self.voter_id}_share2.png'
        share2.save(self.share2_path)

    def combine_action(self):
        if self.verify_captcha():
            share1_path = filedialog.askopenfilename(title="Select Share 1")
            share2_path = filedialog.askopenfilename(title="Select Share 2")
            if share1_path and share2_path:
                self.combine_shares(share1_path, share2_path)
                messagebox.showinfo("Shares Combined", "Shares have been successfully combined.")
                self.view_button['state'] = 'normal'
        else:
            messagebox.showwarning("Verification Failed", "Failed to verify CAPTCHA. Please try again.")

    def combine_shares(self, share1_path, share2_path):
        share1 = Image.open(share1_path).convert('1')
        share2 = Image.open(share2_path).convert('1')
        width, height = share1.size

        combined_image = Image.new('1', (width, height))
        for x in range(width):
            for y in range(height):
                combined_pixel = share1.getpixel((x, y)) ^ share2.getpixel((x, y))
                combined_image.putpixel((x, y), combined_pixel * 255)

        self.combined_path = f'{self.voter_id}_combined.png'
        combined_image.save(self.combined_path)

    def view_images(self):
        response = messagebox.askyesnocancel("View Images", "Would you like to view the shares? (Yes)\nOr the combined image? (No)")
        if response is True:  # User chose to view shares
            self.open_image_window(self.share1_path, "Share 1")
            self.open_image_window(self.share2_path, "Share 2")
        elif response is False:  # User chose to view the combined image
            self.open_image_window(self.combined_path, "Combined Image")

    def open_image_window(self, image_path, title):
        if os.path.exists(image_path):
            new_window = Toplevel(self.master)
            new_window.title(title)

            img = Image.open(image_path)
            base_width = 250
            w_percent = (base_width / float(img.size[0]))
            h_size = int((float(img.size[1]) * float(w_percent)))
            img = img.resize((base_width, h_size), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)

            label = tk.Label(new_window, image=img)
            label.image = img  # Keep a reference to avoid garbage collection
            label.pack()
        else:
            messagebox.showerror("Error", f"File {image_path} not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VotingApp(root)
    root.mainloop()

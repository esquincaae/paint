import tkinter as tk
from ui_handler import UIHandler

def main():
    window = tk.Tk()
    ui_handler = UIHandler(window, 600, 300)
    window.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter.messagebox import showinfo
from PIL import ImageGrab, ImageTk, Image
import pyautogui
from keyboard import add_hotkey
from sys import exit
import os

class ScreenMagnifier:
    def __init__(self):
        def reini():
            self.scale = 40

        self.root = tk.Toplevel()
        self.root.title("Экранная лупа")
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        
        self.root.configure(bg='white', relief='solid', bd=1)
        
        self.root.columnconfigure(index=0, weight=0)
        
        self.magnification = 5
        
        self.size = 400
        self.update_delay = 50
        
        self.canvas = tk.Canvas(self.root, width=self.size, height=self.size, 
                               bg='white', highlightthickness=0)
        self.canvas.grid()      
        
        self.root.bind('<MouseWheel>', self.zoom)
        self.root.bind('<Button-3>', self.close)
        self.root.bind('<Button-1>', self.start_move)
        self.root.bind('<B1-Motion>', self.move)
        
        self.last_x = 0
        self.last_y = 0
        
        self.scale = 40
        
        ins = tk.Frame(self.root, bg='white', relief='flat', height=30)
        
        button_style = {
            'bg': '#0078D4', 
            'fg': 'white',
            'relief': 'flat',
            'bd': 0,
            'padx': 12,
            'pady': 4,
            'font': ('Segoe UI', 9),
            'cursor': 'hand2'
        }
        
        exbutton_style = {
            'bg': "#D40000", 
            'fg': 'white',
            'relief': 'flat',
            'bd': 0,
            'padx': 12,
            'pady': 4,
            'font': ('Segoe UI', 9),
            'cursor': 'hand2'
        }
        
        tk.Button(ins, text="Вернуть масштаб", command=reini, **button_style).grid(column=0, row=0, padx=3, sticky="ns")
        tk.Button(ins, text="Помощь", command=lambda : showinfo("Подсказка", "После нажатия ПКМ приложение останется в режиме ожидания. \nДля запуска нажмите Shift + alt + w\nДля полного закрытия нажмите 'Выйти'"), **button_style).grid(column=1, row=0, padx=3, sticky="ns")
        tk.Button(ins, text="Выйти", command=lambda: exit(0), **exbutton_style).grid(column=2, row=0, padx=3, sticky="ew")
        
        
        
        ins.grid(padx=3, pady=3, sticky="nsew")
        self.update()
        
    def start_move(self, event):
        self.last_x = event.x_root
        self.last_y = event.y_root
        
    def move(self, event):
        x = self.root.winfo_x() + (event.x_root - self.last_x)
        y = self.root.winfo_y() + (event.y_root - self.last_y)
        self.root.geometry(f"+{x}+{y}")
        self.last_x = event.x_root
        self.last_y = event.y_root
        
    def zoom(self, event):
            if event.delta > 0:
                self.scale += 10
            elif self.scale>=11:
                self.scale -= 10
        
            
    def close(self, event):
        self.root.destroy()
        
    def update(self):
        try:
            x, y = pyautogui.position()
            
            bbox = (x - self.scale, y - self.scale, x + self.scale, y + self.scale)
            screenshot = ImageGrab.grab(bbox)
            
            new_size = int(100 * self.magnification)
            screenshot = screenshot.resize((new_size, new_size))            
            
            self.photo = ImageTk.PhotoImage(screenshot)            
            
            self.canvas.delete("all")
            
            self.canvas.create_image(self.size//2, self.size//2, image=self.photo)
            
            self.cursor = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.abspath(__file__))+r"/cur.png"))
            self.canvas.create_image(self.size//2, self.size//2, image=self.cursor)
            
            self.root.after(self.update_delay, self.update)
        except tk.TclError:
            pass
   

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  
    showinfo("Внимание!", "Экранная лупа в режиме ожидания. Нажмите Shift + alt + w для открытия.")
    add_hotkey("Shift+alt+w", ScreenMagnifier)
    
    root.mainloop()
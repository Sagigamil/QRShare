import tkinter as tk
import qrcode
from PIL import ImageTk

from .ViewInterface import ViewInterface

class QRView(ViewInterface):
    def __init__(self, *args):
        pass
    
    @staticmethod
    def validate_init_params(**params):
        if len(params.keys()) > 0:
            raise Exception("not expect params, but params were given")

    def view(self, str):
        width, height = (250, 250)
        
        qr = qrcode.make(str)
        qr = qr.resize((width, height))
        
        root = tk.Tk()
        root.title(str)
        root.resizable(False, False) 
        root.lift()
        
        canvas = tk.Canvas(root, width=width, height=height)
        canvas.pack()
        image = ImageTk.PhotoImage(qr)
        canvas.create_image(0, 0, image=image, anchor=tk.NW)
        
        root.mainloop()
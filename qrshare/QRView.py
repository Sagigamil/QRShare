"""
This file defines the QRView class, which is a concrete implementation of the ViewInterface class.

The QRView class displays a QR code image using tkinter and the qrcode module. It has a single method, 'view', which takes a string as input and displays a QR code image with the given data.
"""

import tkinter as tk
import qrcode
from PIL import ImageTk

from .ViewInterface import ViewInterface

class QRView(ViewInterface):
    """
    A concrete implementation of the ViewInterface class that displays a QR code image using tkinter and the qrcode module.
    """
    def __init__(self, *args):
        """
        Initializes the QRView instance.

        Args:
            *args: Additional arguments (not used).
        """
        pass
    
    @staticmethod
    def validate_init_params(**params):
        """
        Validates the initialization parameters.

        Args:
            **params: The initialization parameters (not used).

        Raises:
            Exception: If any initialization parameters are provided.
        """
        if len(params.keys()) > 0:
            raise ValueError("not expect params, but params were given")

    def view(self, str):
        """
        Displays a QR code image with the given data.

        Args:
            str (str): The data to be encoded in the QR code.

        Returns:
            None

        Examples:
            >>> view = QRView()
            >>> view.view('This is the data that will be encoded in the QR code')
            (QR code image is displayed)

        Notes:
            The QR code image is 250x250 pixels in size.
        """
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

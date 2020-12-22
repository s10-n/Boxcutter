import tkinter
import time
from tkinter import filedialog
from PIL import Image, ImageGrab, ImageTk

class SnippingTool:
    def __init__(self, main_window):
        self.main_window = main_window
        main_window.title("Snipping Tool")
        
        self.snip_button = tkinter.Button(main_window, text='New snip', command=self.enterSnippingMode)
        self.snip_button.grid(row=0,column=0,sticky="NEWS")
        
        self.options_button = tkinter.Button(main_window, text='Options', command=self.options)
        self.options_button.grid(row=0,column=2,sticky="NEWS")

        self.dimensions = [0, 0, 500, 500]       
       
    def enterSnippingMode(self):
        self.overlay = tkinter.Toplevel(self.main_window)
#        self.main_window.withdraw()
        self.overlay.wait_visibility()
        self.overlay.wm_attributes('-alpha',0.3,'-fullscreen',True)
        self.createCanvas()        

    def createCanvas(self):
        self.drawing_surface = tkinter.Canvas(self.overlay, cursor='cross')
        self.drawing_surface.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.drawing_surface.bind("<ButtonPress-1>", self.mouseClicked)
        self.drawing_surface.bind("<ButtonRelease-1>",self.mouseReleased)

    def mouseClicked(self,event):
        self.start_x = int(self.drawing_surface.canvasx(event.x))
        self.start_y = int(self.drawing_surface.canvasx(event.y))
        self.dimensions[0],self.dimensions[1] = self.start_x, self.start_y
        print(self.start_x)
        print(self.start_y)

    def mouseReleased(self, event):
        self.end_x = int(self.drawing_surface.canvasx(event.x))
        self.end_y = int(self.drawing_surface.canvasx(event.y))
        self.dimensions[2],self.dimensions[3] = self.end_x, self.end_y
        print(self.end_x)
        print(self.end_y)
        self.overlay.destroy()
        self.snipScreen()

    def mouseMoving(self):
        pass
    
    def snipScreen(self):
        time.sleep(0.25)
        self.snipped_image_file = ImageGrab.grab(bbox=self.dimensions)
        self.snipped_image = ImageTk.PhotoImage(self.snipped_image_file)
        self.snipped_image_label = tkinter.Label(self.main_window, image=self.snipped_image,borderwidth=0)
        self.main_window.geometry(f'{self.dimensions[2]-self.dimensions[0]}x{self.dimensions[3]-self.dimensions[1]}')
        self.snipped_image_label.image = self.snipped_image
        self.snipped_image_label.grid(row=1,column=0,columnspan=3)
        self.save_button = tkinter.Button(self.main_window, text='Save', command=self.save)
        self.save_button.grid(row=0,column=1,sticky="NEWS")
        
    def save(self):
        self.saved_image = filedialog.asksaveasfile(mode='wb',
                                               title='Save image as',
                                               filetypes = [('PNG','*.png'),('JPEG','*.jpeg *.jpg')])
        self.snipped_image_file.save(self.saved_image)

    def options():
        pass
        
root = tkinter.Tk()
snipping_tool = SnippingTool(root)
root.mainloop()

import tkinter
import subprocess
import pyperclip
import time
import io
from tkinter import filedialog,ttk
from PIL import Image, ImageGrab, ImageTk

class BoxCutter:
    def __init__(self, main_window):
        self.main_window = main_window
        main_window.title("Boxcutter")
        
        self.snip_button = ttk.Button(main_window, text='New snip', command=self.enterSnippingMode)
        self.snip_button.grid(row=0,column=0,sticky="NEWS")
        self.options_button = ttk.Button(main_window)
        #self.options_button = ttk.Button(main_window, text='Options', command=self.options) TODO
        self.options_button.grid(row=0,column=2,sticky="NEWS")
        self.dimensions = [0,0,0,0]
        try:
            self.copy_menu = ttk.Button(self.snipped_image_label,text="Copy image to clipboard")
        except:
            pass
       
    def enterSnippingMode(self):
        self.overlay = tkinter.Toplevel(self.main_window)
        self.main_window.withdraw()
        self.overlay.wait_visibility()
        self.overlay.wm_attributes('-alpha',0.3,'-fullscreen',True)
        self.createCanvas()        

    def createCanvas(self):
        self.drawing_surface = tkinter.Canvas(self.overlay, cursor='cross')
        self.drawing_surface.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.drawing_surface.bind("<ButtonPress-1>", self.mouseClicked)
        self.drawing_surface.bind("<ButtonRelease-1>", self.mouseReleased)
        self.drawing_surface.bind("<B1-Motion>", self.mouseMoving)

    def mouseClicked(self,event):
        self.dimensions = [0,0,0,0]
        self.start_x = int(self.drawing_surface.canvasx(event.x))
        self.start_y = int(self.drawing_surface.canvasx(event.y))
        try:
            self.snipped_image_label.destroy()
        except:
            pass

    def mouseReleased(self, event):
        self.end_x = int(self.drawing_surface.canvasx(event.x))
        self.end_y = int(self.drawing_surface.canvasx(event.y))
        self.overlay.destroy()
        self.snipScreen()

    def mouseMoving(self,event):
        self.drawing_surface.delete("all")
        self.current_x = self.drawing_surface.canvasx(event.x)
        self.current_y = self.drawing_surface.canvasy(event.y)
        self.drawing_surface.create_rectangle(self.start_x,self.start_y,
                                              self.current_x,self.current_y,
                                              outline="red",
                                              dash=(3,5),
                                              width=2)
    
    def snipScreen(self):
        self.x_list = [self.start_x, self.end_x]
        self.y_list = [self.start_y, self.end_y]
        self.x_list.sort()
        self.y_list.sort()
        self.dimensions[0],self.dimensions[1],self.dimensions[2],self.dimensions[3] = self.x_list[0],self.y_list[0],self.x_list[1],self.y_list[1]
        time.sleep(0.25)
        self.snipped_image_file = ImageGrab.grab(bbox=self.dimensions)
        print(self.dimensions)
        self.snipped_image = ImageTk.PhotoImage(self.snipped_image_file,master=root)
        self.snipped_image_label = ttk.Label(self.main_window, image=self.snipped_image,borderwidth=0)
        self.image_width = self.snipped_image.width()
        self.image_height = self.snipped_image.height()
        try:
            self.image_size.destroy()
        except:
            pass
        self.image_size = ttk.Label(self.main_window, text=f'{self.image_width}x{self.image_height}')
        self.main_window.geometry(f'{self.dimensions[2]-self.dimensions[0]}x{self.dimensions[3]-self.dimensions[1] + self.options_button.winfo_reqheight() + self.image_size.winfo_reqheight()}')
        self.snipped_image_label.image = self.snipped_image
        self.snipped_image_label.grid(row=1,column=0,columnspan=3)

        self.image_size.grid(row=2, column=2,stick='E')
        self.save_button = ttk.Button(self.main_window, text='Save', command=self.save)
        self.save_button.grid(row=0,column=1,sticky="NEWS")
        self.min_width = self.snip_button.winfo_width() + self.save_button.winfo_width() + self.options_button.winfo_width()
        if self.min_width > (self.dimensions[2] - self.dimensions[0]):
            self.main_window.geometry(f'{self.min_width}x{self.dimensions[3]-self.dimensions[1] + self.options_button.winfo_reqheight() + self.image_size.winfo_reqheight()}')
        self.main_window.deiconify()
        self.copy_menu = ttk.Button(self.snipped_image_label,text="Copy image to clipboard")
        self.snipped_image_label.bind('<Button-3>', self.rightClickImage)
        self.snipped_image_label.bind('<Button-1>', self.clickImage)

    def clickImage(self,event):
        self.copy_menu.destroy()
        
    def rightClickImage(self,event):
        self.copy_menu.destroy()
        self.mouse_x = int(event.x)
        self.mouse_y = int(event.y)
        print('Image right clicked')
        self.copy_menu = ttk.Button(self.main_window,
                                    text="Copy image",
                                    command=self.copyImage
                                    )
        self.copy_menu.place(x=self.mouse_x,y=self.mouse_y)

    def copyImage(self):
        memory = io.BytesIO()
        self.snipped_image_file.save(memory, format="png")
        output = subprocess.Popen(("xclip", "-selection", "clipboard", "-t", "image/png", "-i"),
                                  stdin=subprocess.PIPE)
        output.stdin.write(memory.getvalue())
        output.stdin.close()
        self.copy_menu.destroy()
#        self.status_bar = ttk.Label(self.main_window, text='Image copied to clipboard.', width=self.snip_button.winfo_reqwidth())
 #       self.status_bar.grid(row=2, column=0,sticky='W',columnspan=3)
        
    def save(self):
        self.saved_image = filedialog.asksaveasfile(mode='wb',
                                               title='Save image as',
                                               filetypes = [('PNG','*.png'),('JPEG','*.jpeg *.jpg')])
        self.snipped_image_file.save(self.saved_image)

    def options(self):
        self.options_menu = tkinter.Toplevel()
    
root = tkinter.Tk(className='Boxcutter')
root.resizable(width=False, height=False)
for y in range(3):
    tkinter.Grid.columnconfigure(root, y, weight=1)
icon = tkinter.PhotoImage(file = '/home/sean/projects/boxcutter/Boxcutter icon.png')
root.iconphoto(False, icon)
    
boxcutter = BoxCutter(root)
root.mainloop()

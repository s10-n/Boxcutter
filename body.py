#! python3
import tkinter
import time
from tkinter import filedialog
from PIL import Image, ImageGrab, ImageTk

image = None

dimensions = None

def screenshot():
    area_selected = False
    def get_origin(eventorigin):
        global start_x, start_y
        start_x = eventorigin.x
        start_y = eventorigin.y
        print(start_x,start_y)
        

    def get_destination(eventdestination):
        global end_x, end_y
        end_x = eventdestination.x
        end_y = eventdestination.y
        print(end_x,end_y)
        area_selected = True
        
    
    # capture the entire screen to use as a canvas for the bounding box
    global image, start_x, start_y, end_x, end_y
#    main_window.withdraw() # minimize the main window so it's not caught inthe screenshot
    time.sleep(0.25)
    fullscreen_screenshot_image = ImageGrab.grab()
    fullscreen_screenshot = ImageTk.PhotoImage(fullscreen_screenshot_image)
    overlay = tkinter.Toplevel(main_window)
    overlay.bind("<ButtonPress-1>",get_origin)
    overlay.bind("<ButtonRelease-1>",get_destination)
    overlay.attributes('-fullscreen',True)
    overlay_canvas = tkinter.Canvas(overlay, bd=0,highlightthickness=0)
    overlay_canvas.image = fullscreen_screenshot
    overlay_canvas.pack(expand=tkinter.YES, fill=tkinter.BOTH)
    overlay_canvas.create_image(0,0,image=fullscreen_screenshot,anchor='nw')
    
    dimensions = [start_x,start_y,end_x,end_y]
 #   main_window.deiconify()
    image = ImageGrab.grab(bbox=dimensions)
    image_screenshot = ImageTk.PhotoImage(image)
    img = tkinter.Label(main_window, image=image_screenshot)
    main_window.geometry(f'{dimensions[2]-dimensions[0]}x{dimensions[3]-dimensions[1]}')
    img.image = image_screenshot
    img.grid(row=1,column=0,columnspan=3)
    save_button.grid(row=0,column=2,sticky="NEWS")

def save():
    global image
    saved_image = filedialog.asksaveasfile(mode='wb',
                                           title='Save image as',
                                           filetypes = [('PNG','*.png'),('JPEG','*.jpeg *.jpg')])
    image.save(saved_image)

def options():
    pass

main_window = tkinter.Tk(className='Snipping Tool')
main_window.title('Snipping Tool')

snip_button = tkinter.Button(main_window, text='New snip', command=screenshot)

save_button = tkinter.Button(main_window, text='Save', command=save)

options_button = tkinter.Button(main_window, text='Options', command=options)

startup_buttons = [snip_button,options_button]

for index,button in enumerate(startup_buttons):
    button.grid(row=0,column=index,sticky='NEWS')

main_window.mainloop()



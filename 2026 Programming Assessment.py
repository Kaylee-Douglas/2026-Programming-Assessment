import tkinter as tk

Main_Image = "testimg.png"

def create_widget():
    root = tk.Tk() #create window
    root.title("Wellbeing Widget") #name window
    root.attributes('-transparentcolor', 'white')  # Make background color transparent
    root.overrideredirect(True) #remove window title
    root.attributes("-topmost", False) #ensure windows can open over

    # Load image
    img = tk.PhotoImage(file=Main_Image) #load image in window

    label = tk.Label(root, image=img, borderwidth=0, highlightthickness=0)
    label.image = img
    label.pack()

    # Screen and image size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    img_width = img.width() #define width of img
    img_height = img.height() #define height of img

    # place on screen
    x = screen_width - img_width - 10
    y = screen_height - img_height - 40  # w/ taskbar considered

    root.geometry(f"{img_width}x{img_height}+{x}+{y}") #sets window using x, y and image size values

    # widget closes on left click (temp.)
    label.bind("<Button-1>", lambda e: root.destroy())

    root.mainloop() 

create_widget()


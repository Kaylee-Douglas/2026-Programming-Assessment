import tkinter as tk # import gui so graphical interface can be used
import mysql.connector as mysql # connect database to vscode
# note: database is LOCAL and will not work on other computers without seperate setup
import datetime # allow for time to be tracked

# Creates the widget as a class (allows for more features)
class WellbeingWidget:
    def __init__(self, image_path="testimg.png"):
        self.image_path = image_path
        self.root = tk.Tk()
        
        # adds class function that..
        self.setup_window() # creates the main window
        self.load_image() # loads the main image so that it can be used
        self.place_widget() # places the widget on the screen
        self.bind_events() # causes the widget to close when clicked

    def setup_window(self):
        self.root.title("Wellbeing Widget") # name window
        self.root.attributes('-transparentcolor', 'white') #removes plain white color, allowing backgrounds to be transparent
        self.root.overrideredirect(True) # removes framing
        self.root.attributes("-topmost", False) # allows other tabs to open over, keeping it on the desktop.

    def load_image(self):
        self.img = tk.PhotoImage(file=self.image_path) # loads image as whatever file was specified 
        self.label = tk.Label(self.root, image=self.img) # names the image for use
        self.label.image = self.img # ensures the image is not labeled unused and not displayed (thanks tkinter)
        self.label.pack() # make the image actually display using all the information it has been given

    def place_widget(self):
        screen_width = self.root.winfo_screenwidth() # find width of the screen
        screen_height = self.root.winfo_screenheight() #find height of the screen

        img_width = self.img.width() # find width of the image
        img_height = self.img.height() # find height of the image

        x = screen_width - img_width - 10 # store image placement as 10 pixels from the right side of the screen
        y = screen_height - img_height - 40 # store image placement as 40 pixels from the bottom of the screen (greater b/c of the taskbar)

        self.root.geometry(f"{img_width}x{img_height}+{x}+{y}") #set the image to the right size and place it

    # lets the widget close when clicked rather than forcing the user to end the code manually
    def bind_events(self):
        self.label.bind("<Button-1>", lambda e: self.close())

    def close(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()


# Run the widget
if __name__ == "__main__": #if the program is run
    widget = WellbeingWidget("testimg.png") # create a widget using the test image (changeable for skins/states later!)
    widget.run() # go go go !!

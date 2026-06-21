import tkinter as tk  # import gui so graphical interface can be used
import mysql.connector as mysql  # connect database to vscode
import datetime  # allow for time to be tracked
import random  # for random task generation

# Creates the widget as a class (allows for more features)
class WellbeingWidget:
    def __init__(self, image_path="testimg.png"):
        self.image_path = image_path
        self.root = tk.Tk()
        
        # adds class function that..
        self.setup_window()  # creates the main window
        self.load_image()  # loads the main image so that it can be used
        self.place_widget()  # places the widget on the screen
        self.bind_events()  # causes the widget to close when clicked

        # Delay bubble creation so the window has time to appear
        self.root.after(50, self.create_speech_bubble)

    def setup_window(self):
        self.root.title("Wellbeing Widget")  # name window
        self.root.attributes('-transparentcolor', 'white')  # removes plain white color, allowing backgrounds to be transparent
        self.root.overrideredirect(True)  # removes framing
        self.root.attributes("-topmost", False)  # allows other tabs to open over, keeping it on the desktop.

    def load_image(self):
        self.img = tk.PhotoImage(file=self.image_path)  # loads image as whatever file was specified 
        self.label = tk.Label(self.root, image=self.img)  # names the image for use
        self.label.image = self.img  # ensures the image is not labeled unused and not displayed (thanks tkinter)
        self.label.pack()  # make the image actually display using all the information it has been given

    def place_widget(self):
        screen_width = self.root.winfo_screenwidth()  # find width of the screen
        screen_height = self.root.winfo_screenheight()  # find height of the screen

        img_width = self.img.width()  # find width of the image
        img_height = self.img.height()  # find height of the image

        x = screen_width - img_width - 10  # store image placement as 10 pixels from the right side of the screen
        y = screen_height - img_height - 40  # store image placement as 40 pixels from the bottom of the screen (greater b/c of the taskbar)

        self.root.geometry(f"{img_width}x{img_height}+{x}+{y}")  # set the image to the right size and place it

    # lets the widget close when clicked rather than forcing the user to end the code manually
    def bind_events(self):
        # closes both windows when clicked
        self.label.bind("<Button-1>", lambda e: self.close())

    def close(self):
        # Close bubble too if it exists
        if hasattr(self, "bubble"):
            self.bubble.destroy()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

    # creates the section that holds the tasks
    def create_speech_bubble(self):
        # Creates a new window for the bubble
        self.bubble = tk.Toplevel(self.root) # creates a new window that groups/is attached to the main widget
        self.bubble.overrideredirect(True) # removes framing
        self.bubble.attributes("-topmost", False) # place below other windows, just like main window
        self.bubble.configure(bg="white") # make it white

        # Places bubble
        bubble_x = self.root.winfo_x() - 210  # place it 210 pixels to the left of the main widget (accounting for the size of the bubble)
        bubble_y = self.root.winfo_y() - 50  # place it 50 pixels above the main widget

        self.bubble.geometry(f"200x80+{bubble_x}+{bubble_y}") # place the speech bubble!

        # store information about the bubble
        self.bubble_label = tk.Label(
            self.bubble,
            bg="white",
            fg="black",
            font=("Arial", 9),
            justify="left"
        )
        self.bubble_label.pack(padx=10, pady=10)

        # initial task generates
        self.refresh_tasks()

        # refresh tasks when bubble clicked
        self.bubble_label.bind("<Button-1>", lambda e: self.refresh_tasks())

    # refreshes tasks inside bubble
    def refresh_tasks(self):
        # Create a list of tasks
        tasks = [
            "Drink some water",
            "Take a second to stretch",
            "Take a deep breath",
            "Posture check!!",
            "Take a 5 minute break",
            "Go for a walk",
            "Tidy your workspace",
            "Message one of your friends",
            "Remind yourself of your goals",
            "Think of three things you're grateful for",
        ]

        chosen = random.sample(tasks, 3) # randomly select 3 tasks from the list to display

        # Display tasks inside bubble
        text = "\n".join(f"• {t}" for t in chosen) # bullet point the tasks on their own lines

        # update the bubble
        self.bubble_label.config(text=text)


# Run the widget
if __name__ == "__main__":  # if the program is run
    widget = WellbeingWidget("testimg.png")  # create a widget using the test image (changeable for skins/states later!)
    widget.run()  # go go go !!




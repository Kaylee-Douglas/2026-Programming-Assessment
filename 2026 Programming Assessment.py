import tkinter as tk  # import gui so graphical interface can be used
import mysql.connector as mysql  # connect database to vscode
import datetime  # allow for time to be tracked
import random  # for random task generation

# Creates the widget as a class (allows for more features)
class WellbeingWidget: #create class
    def __init__(self, image_path="testimg.png"): # create image path (for main widget image)
        self.image_path = image_path # store the image path for later use

    # set up for user input
        self.user_name = None # create name variable
        self.selected_categories = [] # create list to store categories
        self.open_question_window() # create window event to ask for input

    # create name input/task preference window
    def open_question_window(self):
        self.setup_win = tk.Tk()
        self.setup_win.title("Personalize Your Widget!")

        tk.Label(self.setup_win, text="Enter your Name:").pack(pady=5)
        self.name_entry = tk.Entry(self.setup_win)
        self.name_entry.pack(pady=5)

        tk.Label(self.setup_win, text="Select task categories:").pack(pady=10)

        # Checkboxes for categories
        self.food_var = tk.IntVar()
        self.exercise_var = tk.IntVar()
        self.school_var = tk.IntVar()
        self.personal_var = tk.IntVar()

        tk.Checkbutton(self.setup_win, text="Food-related tasks", variable=self.food_var).pack(anchor="w")
        tk.Checkbutton(self.setup_win, text="Exercise-related tasks", variable=self.exercise_var).pack(anchor="w")
        tk.Checkbutton(self.setup_win, text="School-related tasks", variable=self.school_var).pack(anchor="w")
        tk.Checkbutton(self.setup_win, text="Personal/Other tasks", variable=self.personal_var).pack(anchor="w")

        tk.Button(self.setup_win, text="Start Widget", command=self.finish_setup).pack(pady=15)

        self.setup_win.mainloop()

    # load widget with user's chosen input
    def finish_setup(self):
        self.user_name = self.name_entry.get().strip()

        # Store selected categories
        if self.food_var.get() == 1:
            self.selected_categories.append("food")
        if self.exercise_var.get() == 1:
            self.selected_categories.append("exercise")
        if self.school_var.get() == 1:
            self.selected_categories.append("school")
        if self.personal_var.get() == 1:
            self.selected_categories.append("personal")

        # Close setup window
        self.setup_win.destroy()

        # Continue loading widget
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
        # Create categorised task lists
        food_tasks = [
            "Eat a meal",
            "Have a healthy snack",
            "Drink some water",
            "Meal Prep",
        ]

        exercise_tasks = [
            "Pause to stretch",
            "Go for a walk",
            "Go for a run",
            "Go to the gym",
            "Do a breathing exercise",
        ]

        school_tasks = [
            "Review your notes",
            "Finish an assignment",
            "Organize your workspace",
            "Check in with a classmate",
        ]

        personal_tasks = [
            "Take a deep breath",
            "Message a friend",
            "Relax for a moment",
        ]

        # Combine tasks based on user selection
        tasks = []

        if "food" in self.selected_categories:
            tasks.extend(food_tasks)
        if "exercise" in self.selected_categories:
            tasks.extend(exercise_tasks)
        if "school" in self.selected_categories:
            tasks.extend(school_tasks)
        if "personal" in self.selected_categories:
            tasks.extend(personal_tasks)

        # If Invalid input (no categories are selected)
        if not tasks:
            print('no tasks selected (placeholder)!')
        chosen = random.sample(tasks, min(3, len(tasks))) # randomly select tasks

        # Display tasks inside text bubble
        text = "\n".join(f"• {t}" for t in chosen) # bullet point the tasks on their own lines

        # update the speech bubble
        self.bubble_label.config(text=text)


# Run the widget
if __name__ == "__main__":  # if the program is run
    widget = WellbeingWidget("testimg.png")  # create a widget using the test image (changeable for skins/states later!)
    widget.run()  # go go go !!

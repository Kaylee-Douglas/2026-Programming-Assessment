import tkinter as tk  # import gui so graphical interface can be used
import mysql.connector as mysql  # connect database to vscode
import datetime  # allow for time to be tracked
import random  # for random task generation

# Creates the widget as a class (allows for more features)
class WellbeingWidget: #create class
    def __init__(self, image_path="living_plant.png"): # create image path (for main widget image)
        self.image_path = image_path # store the image path for later use

        # plant state system
        self.plant_states = ["living_plant.png", "wilting_plant.png", "dead_plant.png"]
        self.current_state_index = 0  # start at living plant

        # default wilt time (replaced when user enters their preferredtime)
        self.wilt_time_seconds = 5

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

        # wilt timer input
        tk.Label(self.setup_win, text="Enter plant wilt time (seconds, max 6000):").pack(pady=10)
        self.wilt_entry = tk.Entry(self.setup_win)
        self.wilt_entry.pack(pady=5)

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

        # check whether wilt time is acceptable
        wilt_text = self.wilt_entry.get().strip()

        try:
            value = int(wilt_text)
            if value <= 0 or value > 6000:
                raise ValueError
            self.wilt_time_seconds = value
        except:
            self.show_wilt_error()
            return

        # Close setup window
        self.setup_win.destroy()

        # Continue loading widget
        self.root = tk.Tk()
        
        self.setup_window()  # creates the main window
        self.load_image()  # loads the main image so that it can be used
        self.place_widget()  # places the widget on the screen
        self.bind_events()  # causes the widget to close when clicked

        # start plant wilting timer using user input
        self.root.after(self.wilt_time_seconds * 1000, self.wilt_plant)

        # Delay bubble creation so the window has time to appear
        self.root.after(50, self.create_speech_bubble)

    # popup for invalid wilt input
    def show_wilt_error(self):
        popup = tk.Tk()
        popup.title("Invalid Input")

        tk.Label(
            popup,
            text="Wilt time must be a number 1 and 6000",
            font=("Arial", 10),
            padx=20,
            pady=20
        ).pack()

        tk.Button(
            popup,
            text="OK",
            font=("Arial", 10),
            command=popup.destroy
        ).pack(pady=10)

        popup.mainloop()

    def setup_window(self):
        self.root.title("Wellbeing Widget")  # name window
        self.root.attributes('-transparentcolor', 'white')  # removes plain white color, allowing backgrounds to be transparent
        self.root.overrideredirect(True)  # removes framing
        self.root.attributes("-topmost", False)  # allows other tabs to open over, keeping it on the desktop.

    def load_image(self):
        self.img = tk.PhotoImage(file=self.plant_states[self.current_state_index])  # loads image based on plant state
        self.label = tk.Label(self.root, image=self.img)  # names the image for use
        self.label.image = self.img  # ensures the image is not labeled unused and not displayed (thanks tkinter)
        self.label.pack()  # make the image actually display using all the information it has been given

    def update_plant_image(self):
        """Reloads the plant image after state change."""
        self.img = tk.PhotoImage(file=self.plant_states[self.current_state_index])
        self.label.configure(image=self.img)
        self.label.image = self.img

    # plant wilting timer
    def wilt_plant(self):
        if self.current_state_index < len(self.plant_states) - 1:
            self.current_state_index += 1
            self.update_plant_image()

        # plan/set next wilt
        self.root.after(self.wilt_time_seconds * 1000, self.wilt_plant)

    # revive plant one stage when task done
    def revive_plant(self):
        if self.current_state_index > 0:
            self.current_state_index -= 1
            self.update_plant_image()

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
        self.label.bind("<Button-1>", lambda e: self.close())

    def close(self):
        if hasattr(self, "bubble"):
            self.bubble.destroy()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

    # creates the section that holds the tasks
    def create_speech_bubble(self):
        self.bubble = tk.Toplevel(self.root)
        self.bubble.overrideredirect(True)
        self.bubble.attributes("-topmost", False)
        self.bubble.configure(bg="white")

        bubble_x = self.root.winfo_x() - 210
        bubble_y = self.root.winfo_y() - 50

        self.bubble.geometry(f"200x120+{bubble_x}+{bubble_y}")

        self.task_frame = tk.Frame(self.bubble, bg="white")
        self.task_frame.pack(padx=10, pady=10)

        self.refresh_tasks()

    # refreshes tasks inside bubble
    def refresh_tasks(self):
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

        tasks = []

        if "food" in self.selected_categories:
            tasks.extend(food_tasks)
        if "exercise" in self.selected_categories:
            tasks.extend(exercise_tasks)
        if "school" in self.selected_categories:
            tasks.extend(school_tasks)
        if "personal" in self.selected_categories:
            tasks.extend(personal_tasks)

        if not tasks:
            if hasattr(self, "bubble"):
                self.bubble.destroy()

            self.root.destroy()

            popup = tk.Tk()
            popup.title("Selection Required")

            tk.Label(
                popup,
                text="You must select at least one type of task.",
                font=("Arial", 10),
                padx=20,
                pady=20
            ).pack()

            tk.Button(
                popup,
                text="OK",
                font=("Arial", 10),
                command=lambda: [popup.destroy(), self.reopen_selection_window()]
            ).pack(pady=10)

            popup.mainloop()
            return

        for widget in self.task_frame.winfo_children():
            widget.destroy()

        chosen = random.sample(tasks, min(3, len(tasks)))

        self.category_pools = {
            "food": food_tasks,
            "exercise": exercise_tasks,
            "school": school_tasks,
            "personal": personal_tasks
        }

        self.task_rows = []
        for task in chosen:
            row = tk.Frame(self.task_frame, bg="white")

            var = tk.IntVar()

            cb = tk.Checkbutton(
                row,
                variable=var,
                command=lambda t=task, r=row: self.replace_task(t, r),
                bg="white"
            )
            cb.pack(side="left")

            label = tk.Label(
                row,
                text=f"• {task}",
                bg="white",
                fg="black",
                font=("Arial", 9),
                justify="left"
            )
            label.pack(side="left", padx=5)

            row.pack(anchor="w", pady=2)
            self.task_rows.append((task, row))

    # replaces a task when its checkbox is clicked
    def replace_task(self, old_task, row):
        self.revive_plant()

        for category, pool in self.category_pools.items(): 
            if old_task in pool: 
                new_task = random.choice(pool)
                break

        for widget in row.winfo_children():
            widget.destroy()

        var = tk.IntVar()
        cb = tk.Checkbutton(
            row,
            variable=var,
            command=lambda t=new_task, r=row: self.replace_task(t, r),
            bg="white"
        )
        cb.pack(side="left")

        label = tk.Label(
            row,
            text=f"• {new_task}",
            bg="white",
            fg="black",
            font=("Arial", 9),
            justify="left"
        )
        label.pack(side="left", padx=5)

    def reopen_selection_window(self):
        self.selected_categories = []
        self.open_question_window()


# Run the widget
if __name__ == "__main__":
    widget = WellbeingWidget("living_plant.png")
    widget.run()


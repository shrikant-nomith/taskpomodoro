import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import json
import os
from PIL import Image, ImageTk

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Productivity Suite")
        self.root.geometry("1200x800")
        self.root.configure(bg="yellow")
        
        # variables ka initialization
        self.tasks = []
        self.resources = {"reading": [], "practice": [], "links": []}
        self.pomodoro_count = 0
        self.work_time = 25 * 60  # 25 minutes in seconds
        self.break_time = 5 * 60   # 5 minutes in seconds
        self.current_time = self.work_time
        self.is_running = False
        self.timer_id = None
        
        # Create main notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Create tabs
        self.timer_tab = ttk.Frame(self.notebook)
        self.tasks_tab = ttk.Frame(self.notebook)
        self.progress_tab = ttk.Frame(self.notebook)
        self.resources_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.timer_tab, text="Pomodoro Timer")
        self.notebook.add(self.tasks_tab, text="Tasks")
        self.notebook.add(self.progress_tab, text="Progress")
        self.notebook.add(self.resources_tab, text="Resources")
        
        # Initialize all components
        self.setup_timer_tab()
        self.setup_tasks_tab()
        self.setup_progress_tab()
        self.setup_resources_tab()
        
        # Load saved data
        self.load_data()
        
        # Bind tab change event to update progress plots
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_tab_change(self, event):
        if self.notebook.select() == self.notebook.tabs()[2]:  # Progress tab
            self.update_progress_plots()

    def setup_timer_tab(self):
        # Timer frame
        timer_frame = ttk.Frame(self.timer_tab)
        timer_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Timer display
        self.timer_label = ttk.Label(timer_frame, text="25:00", font=("Helvetica", 56))
        self.timer_label.pack(pady=20)
        
        # Control buttons
        control_frame = ttk.Frame(timer_frame)
        control_frame.pack(pady=10)
        
        self.start_button = ttk.Button(control_frame, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = ttk.Button(control_frame, text="Pause", command=self.pause_timer, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = ttk.Button(control_frame, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(timer_frame, text="Ready to start", font=("Helvetica", 14))
        self.status_label.pack(pady=10)

    def setup_tasks_tab(self):
        # Tasks frame
        tasks_frame = ttk.Frame(self.tasks_tab)
        tasks_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Task input
        input_frame = ttk.Frame(tasks_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        self.task_entry = ttk.Entry(input_frame)
        self.task_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        self.deadline_entry = ttk.Entry(input_frame, width=15)
        self.deadline_entry.pack(side=tk.LEFT, padx=5)
        self.deadline_entry.insert(0, "YYYY-MM-DD")
        
        add_button = ttk.Button(input_frame, text="Add Task", command=self.add_task)
        add_button.pack(side=tk.LEFT, padx=5)
        
        # Tasks list
        self.tasks_listbox = tk.Listbox(tasks_frame, height=15)
        self.tasks_listbox.pack(expand=True, fill=tk.BOTH, pady=10)
        
        # Task controls
        controls_frame = ttk.Frame(tasks_frame)
        controls_frame.pack(fill=tk.X, pady=10)
        
        complete_button = ttk.Button(controls_frame, text="Mark Complete", command=self.mark_task_complete)
        complete_button.pack(side=tk.LEFT, padx=5)
        
        delete_button = ttk.Button(controls_frame, text="Delete Task", command=self.delete_task)
        delete_button.pack(side=tk.LEFT, padx=5)

    def setup_progress_tab(self):
        # Progress frame
        progress_frame = ttk.Frame(self.progress_tab)
        progress_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Create matplotlib figure
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            
            self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 4))
            self.canvas = FigureCanvasTkAgg(self.fig, master=progress_frame)
            self.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)
            
            # Update plots
            self.update_progress_plots()
        except ImportError:
            error_label = ttk.Label(progress_frame, text="Error: matplotlib not installed. Please install it using 'pip install matplotlib'")
            error_label.pack(pady=20)

    def setup_resources_tab(self):
        # Resources frame
        resources_frame = ttk.Frame(self.resources_tab)
        resources_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Resource type selection
        self.resource_type = ttk.Combobox(resources_frame, values=["Reading", "Practice", "Links"])
        self.resource_type.pack(pady=10)
        self.resource_type.set("Reading")
        
        # Resource input
        input_frame = ttk.Frame(resources_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        self.resource_name = ttk.Entry(input_frame)
        self.resource_name.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        self.resource_url = ttk.Entry(input_frame)
        self.resource_url.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        add_button = ttk.Button(input_frame, text="Add Resource", command=lambda: self.add_resource(self.resource_type.get()))
        add_button.pack(side=tk.LEFT, padx=5)
        
        # Resources list
        self.resources_listbox = tk.Listbox(resources_frame, height=15)
        self.resources_listbox.pack(expand=True, fill=tk.BOTH, pady=10)
        
        # Resource controls
        controls_frame = ttk.Frame(resources_frame)
        controls_frame.pack(fill=tk.X, pady=10)
        
        open_button = ttk.Button(controls_frame, text="Open Resource", command=self.open_resource)
        open_button.pack(side=tk.LEFT, padx=5)
        
        delete_button = ttk.Button(controls_frame, text="Delete Resource", command=self.delete_resource)
        delete_button.pack(side=tk.LEFT, padx=5)

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.update_timer()

    def pause_timer(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            if self.timer_id:
                self.root.after_cancel(self.timer_id)

    def reset_timer(self):
        self.pause_timer()
        self.current_time = self.work_time
        self.update_timer_display()
        self.status_label.config(text="Ready to start")

    def update_timer(self):
        if self.is_running:
            if self.current_time > 0:
                self.current_time -= 1
                self.update_timer_display()
                self.timer_id = self.root.after(1000, self.update_timer)
            else:
                self.pomodoro_count += 1
                if self.current_time == 0:
                    self.current_time = self.break_time
                    self.status_label.config(text="Break Time!")
                else:
                    self.current_time = self.work_time
                    self.status_label.config(text="Work Time!")
                self.update_timer_display()

    def update_timer_display(self):
        minutes = self.current_time // 60
        seconds = self.current_time % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

    def add_task(self):
        task = self.task_entry.get()
        deadline = self.deadline_entry.get()
        if task and deadline:
            try:
                # Validate date format
                datetime.datetime.strptime(deadline, "%Y-%m-%d")
                self.tasks.append({"task": task, "deadline": deadline, "completed": False})
                self.update_tasks_list()
                self.task_entry.delete(0, tk.END)
                self.deadline_entry.delete(0, tk.END)
                self.deadline_entry.insert(0, "YYYY-MM-DD")
                self.save_data()
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter the date in YYYY-MM-DD format")

    def mark_task_complete(self):
        selection = self.tasks_listbox.curselection()
        if selection:
            index = selection[0]
            self.tasks[index]["completed"] = True
            self.update_tasks_list()
            self.save_data()

    def delete_task(self):
        selection = self.tasks_listbox.curselection()
        if selection:
            index = selection[0]
            del self.tasks[index]
            self.update_tasks_list()
            self.save_data()

    def update_tasks_list(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✓" if task["completed"] else "○"
            days_left = self.calculate_days_left(task["deadline"])
            self.tasks_listbox.insert(tk.END, f"{status} {task['task']} - Deadline: {task['deadline']} ({days_left} days left)")

    def calculate_days_left(self, deadline):
        try:
            deadline_date = datetime.datetime.strptime(deadline, "%Y-%m-%d")
            today = datetime.datetime.now()
            days_left = (deadline_date - today).days
            return max(0, days_left)
        except ValueError:
            return "Invalid date"

    def add_resource(self, resource_type):
        name = self.resource_name.get()
        url = self.resource_url.get()
        if name and url:
            try:
                self.resources[resource_type.lower()].append({"name": name, "url": url})
                self.update_resources_list()
                self.resource_name.delete(0, tk.END)
                self.resource_url.delete(0, tk.END)
                self.save_data()
            except KeyError:
                messagebox.showerror("Error", "Invalid resource type")

    def open_resource(self):
        selection = self.resources_listbox.curselection()
        if selection:
            index = selection[0]
            resource = self.resources_listbox.get(index)
            try:
                import webbrowser
                # Extract URL from the resource string
                url = resource.split(" - ")[-1]
                webbrowser.open(url)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open resource: {str(e)}")

    def delete_resource(self):
        selection = self.resources_listbox.curselection()
        if selection:
            index = selection[0]
            try:
                resource_type = self.resource_type.get().lower()
                del self.resources[resource_type][index]
                self.update_resources_list()
                self.save_data()
            except (KeyError, IndexError):
                messagebox.showerror("Error", "Could not delete resource")

    def update_resources_list(self):
        self.resources_listbox.delete(0, tk.END)
        for resource_type, resources in self.resources.items():
            self.resources_listbox.insert(tk.END, f"--- {resource_type.capitalize()} ---")
            for resource in resources:
                self.resources_listbox.insert(tk.END, f"{resource['name']} - {resource['url']}")

    def update_progress_plots(self):
        try:
            import matplotlib.pyplot as plt
            # Clear previous plots
            self.ax1.clear()
            self.ax2.clear()
            
            if self.tasks:
                # Line graph for completed tasks over time
                dates = [task["deadline"] for task in self.tasks]
                completed = [1 if task["completed"] else 0 for task in self.tasks]
                self.ax1.plot(dates, completed, marker='o')
                self.ax1.set_title("Task Completion Progress")
                self.ax1.set_xlabel("Deadline")
                self.ax1.set_ylabel("Completed")
                
                # Pie chart for task completion ratio
                completed_count = sum(1 for task in self.tasks if task["completed"])
                remaining_count = len(self.tasks) - completed_count
                self.ax2.pie([completed_count, remaining_count], 
                            labels=["Completed", "Remaining"],
                            autopct='%1.1f%%')
                self.ax2.set_title("Task Completion Ratio")
            else:
                self.ax1.text(0.5, 0.5, "No tasks available", 
                            horizontalalignment='center', 
                            verticalalignment='center')
                self.ax2.text(0.5, 0.5, "No tasks available", 
                            horizontalalignment='center', 
                            verticalalignment='center')
            
            self.canvas.draw()
        except Exception as e:
            print(f"Error updating plots: {str(e)}")

    def save_data(self):
        data = {
            "tasks": self.tasks,
            "resources": self.resources,
            "pomodoro_count": self.pomodoro_count
        }
        try:
            with open("pomodoro_data.json", "w") as f:
                json.dump(data, f)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save data: {str(e)}")

    def load_data(self):
        try:
            with open("pomodoro_data.json", "r") as f:
                data = json.load(f)
                self.tasks = data.get("tasks", [])
                self.resources = data.get("resources", {"reading": [], "practice": [], "links": []})
                self.pomodoro_count = data.get("pomodoro_count", 0)
                self.update_tasks_list()
                self.update_resources_list()
        except FileNotFoundError:
            pass
        except Exception as e:
            messagebox.showerror("Error", f"Could not load data: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop() 
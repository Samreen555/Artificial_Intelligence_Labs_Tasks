"""
Lab 09: Employee Registration and Salary Utility System
A complete Tkinter application for HR management
"""

import tkinter as tk
from tkinter import messagebox, ttk
import re

class EmployeeSystem:
    def __init__(self, root):
        """
        Initialize the main application window
        """
        self.root = root
        self.root.title("Employee Registration and Salary Utility System")
        self.root.geometry("800x600")
        self.root.configure(bg='#e8f0f8')
        
        # Center the window on screen
        self.center_window()
        
        # Create menu bar
        self.create_menu()
        
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg='#e8f0f8')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Show welcome notice
        self.show_welcome_notice()
    
    def center_window(self):
        """
        Center the window on the screen
        """
        self.root.update_idletasks()
        width = 800
        height = 600
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_menu(self):
        """
        Create menu bar with different options
        """
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Employee Registration", command=self.show_registration_form)
        file_menu.add_command(label="Salary Calculator", command=self.show_salary_calculator)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_application)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Instructions", command=self.show_instructions)
    
    def exit_application(self):
        """
        Exit the application with confirmation
        """
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()
            self.root.destroy()
    
    def show_welcome_notice(self):
        """
        Display welcome notice with different sticky positions
        Demonstrates sticky options (N, E, S, W)
        """
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create a frame for the notice
        notice_frame = tk.Frame(self.main_frame, bg='#ffffff', relief=tk.RAISED, bd=2)
        notice_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title label
        title_label = tk.Label(notice_frame, 
                               text="HR Management System",
                               font=('Arial', 24, 'bold'),
                               bg='#ffffff',
                               fg='#1a5276')
        title_label.pack(pady=20)
        
        # Demonstration of sticky positions using grid
        demo_frame = tk.Frame(notice_frame, bg='#ffffff')
        demo_frame.pack(pady=20)
        
        # Create a frame to demonstrate sticky positions
        sticky_label = tk.Label(demo_frame, text="Demonstration of Sticky Positions (N, E, S, W)",
                               font=('Arial', 14, 'bold'),
                               bg='#ffffff',
                               fg='#2c3e50')
        sticky_label.pack(pady=10)
        
        sticky_demo = tk.Frame(demo_frame, bg='#d5dbdb', width=500, height=250, 
                              relief=tk.SUNKEN, bd=3)
        sticky_demo.pack(pady=10)
        sticky_demo.pack_propagate(False)
        
        # Create grid inside sticky_demo
        for i in range(3):
            sticky_demo.grid_rowconfigure(i, weight=1)
        for i in range(3):
            sticky_demo.grid_columnconfigure(i, weight=1)
        
        # Label with sticky='N' (North/Top)
        label_n = tk.Label(sticky_demo, text="STICKY N (North)",
                          bg='#2471a3', fg='white', 
                          font=('Arial', 11, 'bold'),
                          padx=10, pady=5)
        label_n.grid(row=0, column=0, sticky='n', padx=5, pady=5)
        
        # Label with sticky='S' (South/Bottom)
        label_s = tk.Label(sticky_demo, text="STICKY S (South)",
                          bg='#2e86c1', fg='white', 
                          font=('Arial', 11, 'bold'),
                          padx=10, pady=5)
        label_s.grid(row=2, column=1, sticky='s', padx=5, pady=5)
        
        # Label with sticky='E' (East/Right)
        label_e = tk.Label(sticky_demo, text="STICKY E (East)",
                          bg='#1f618d', fg='white', 
                          font=('Arial', 11, 'bold'),
                          padx=10, pady=5)
        label_e.grid(row=1, column=2, sticky='e', padx=5, pady=5)
        
        # Label with sticky='W' (West/Left)
        label_w = tk.Label(sticky_demo, text="STICKY W (West)",
                          bg='#3498db', fg='white', 
                          font=('Arial', 11, 'bold'),
                          padx=10, pady=5)
        label_w.grid(row=1, column=0, sticky='w', padx=5, pady=5)
        
        # Center label
        label_center = tk.Label(sticky_demo, text="CENTER (NSEW)",
                               bg='#5dade2', fg='white',
                               font=('Arial', 11, 'bold'),
                               padx=10, pady=5)
        label_center.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        
        # Explanation
        explanation = tk.Label(demo_frame,
                              text="N (North): Widget sticks to top | S (South): Widget sticks to bottom\n"
                                   "E (East): Widget sticks to right | W (West): Widget sticks to left\n"
                                   "Center: Widget expands in all directions (NSEW)",
                              font=('Arial', 10), bg='#ffffff',
                              justify=tk.CENTER)
        explanation.pack(pady=10)
        
        # Welcome message
        welcome_msg = tk.Label(notice_frame,
                               text="Welcome to Employee Registration and Salary Utility System",
                               font=('Arial', 16, 'bold'),
                               bg='#ffffff',
                               fg='#1a5276',
                               wraplength=700)
        welcome_msg.pack(pady=20)
        
        # Description
        desc_msg = tk.Label(notice_frame,
                           text="This system helps HR departments manage employee registration and salary calculations efficiently.",
                           font=('Arial', 11),
                           bg='#ffffff',
                           fg='#34495e',
                           wraplength=700)
        desc_msg.pack(pady=5)
        
        # Instruction buttons
        btn_frame = tk.Frame(notice_frame, bg='#ffffff')
        btn_frame.pack(pady=30)
        
        # Styled buttons
        register_btn = tk.Button(btn_frame, text="Register Employee", 
                                command=self.show_registration_form,
                                bg='#2471a3', fg='white', 
                                font=('Arial', 12, 'bold'),
                                padx=20, pady=10,
                                cursor='hand2',
                                relief=tk.RAISED,
                                bd=2,
                                width=18)
        register_btn.pack(side=tk.LEFT, padx=10)
        
        salary_btn = tk.Button(btn_frame, text="Salary Calculator",
                              command=self.show_salary_calculator,
                              bg='#1f618d', fg='white', 
                              font=('Arial', 12, 'bold'),
                              padx=20, pady=10,
                              cursor='hand2',
                              relief=tk.RAISED,
                              bd=2,
                              width=18)
        salary_btn.pack(side=tk.LEFT, padx=10)
        
        exit_btn = tk.Button(btn_frame, text="Exit",
                            command=self.exit_application,
                            bg='#c0392b', fg='white',
                            font=('Arial', 12, 'bold'),
                            padx=20, pady=10,
                            cursor='hand2',
                            relief=tk.RAISED,
                            bd=2,
                            width=18)
        exit_btn.pack(side=tk.LEFT, padx=10)
    
    def show_registration_form(self):
        """
        Create Employee Registration Form with validation
        """
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create form frame
        form_frame = tk.Frame(self.main_frame, bg='#ffffff', relief=tk.RAISED, bd=2)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        title_frame = tk.Frame(form_frame, bg='#ffffff')
        title_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(title_frame, text="Employee Registration Form",
                font=('Arial', 20, 'bold'), bg='#ffffff', fg='#1a5276').pack()
        
        # Form fields
        fields_frame = tk.Frame(form_frame, bg='#ffffff')
        fields_frame.pack(pady=30, padx=50)
        
        # First Name
        tk.Label(fields_frame, text="First Name:", font=('Arial', 12, 'bold'), 
                bg='#ffffff', fg='#2c3e50').grid(row=0, column=0, pady=12, padx=10, sticky='e')
        self.first_name = tk.Entry(fields_frame, font=('Arial', 12), width=35,
                                  relief=tk.SUNKEN, bd=2)
        self.first_name.grid(row=0, column=1, pady=12, padx=10)
        
        # Last Name
        tk.Label(fields_frame, text="Last Name:", font=('Arial', 12, 'bold'),
                bg='#ffffff', fg='#2c3e50').grid(row=1, column=0, pady=12, padx=10, sticky='e')
        self.last_name = tk.Entry(fields_frame, font=('Arial', 12), width=35,
                                 relief=tk.SUNKEN, bd=2)
        self.last_name.grid(row=1, column=1, pady=12, padx=10)
        
        # Email
        tk.Label(fields_frame, text="Email Address:", font=('Arial', 12, 'bold'),
                bg='#ffffff', fg='#2c3e50').grid(row=2, column=0, pady=12, padx=10, sticky='e')
        self.email = tk.Entry(fields_frame, font=('Arial', 12), width=35,
                             relief=tk.SUNKEN, bd=2)
        self.email.grid(row=2, column=1, pady=12, padx=10)
        
        # Department
        tk.Label(fields_frame, text="Department:", font=('Arial', 12, 'bold'),
                bg='#ffffff', fg='#2c3e50').grid(row=3, column=0, pady=12, padx=10, sticky='e')
        self.department = ttk.Combobox(fields_frame, font=('Arial', 12), width=32)
        self.department['values'] = ('Select Department', 'Human Resources', 
                                     'Information Technology', 
                                     'Finance', 'Marketing', 'Sales', 'Operations')
        self.department.current(0)
        self.department.grid(row=3, column=1, pady=12, padx=10)
        
        # Status label for messages
        self.status_label = tk.Label(form_frame, text="", font=('Arial', 10),
                                    bg='#ffffff', fg='red', wraplength=600)
        self.status_label.pack(pady=10)
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='#ffffff')
        button_frame.pack(pady=20)
        
        submit_btn = tk.Button(button_frame, text="Submit", 
                              command=self.validate_registration,
                              bg='#27ae60', fg='white', 
                              font=('Arial', 11, 'bold'),
                              padx=20, pady=8,
                              cursor='hand2',
                              relief=tk.RAISED,
                              bd=2,
                              width=12)
        submit_btn.pack(side=tk.LEFT, padx=8)
        
        clear_btn = tk.Button(button_frame, text="Clear",
                             command=self.clear_registration_form,
                             bg='#e74c3c', fg='white',
                             font=('Arial', 11, 'bold'),
                             padx=20, pady=8,
                             cursor='hand2',
                             relief=tk.RAISED,
                             bd=2,
                             width=12)
        clear_btn.pack(side=tk.LEFT, padx=8)
        
        reset_btn = tk.Button(button_frame, text="Reset",
                             command=self.reset_registration_form,
                             bg='#f39c12', fg='white',
                             font=('Arial', 11, 'bold'),
                             padx=20, pady=8,
                             cursor='hand2',
                             relief=tk.RAISED,
                             bd=2,
                             width=12)
        reset_btn.pack(side=tk.LEFT, padx=8)
        
        back_btn = tk.Button(button_frame, text="Back to Menu",
                            command=self.show_welcome_notice,
                            bg='#3498db', fg='white',
                            font=('Arial', 11, 'bold'),
                            padx=20, pady=8,
                            cursor='hand2',
                            relief=tk.RAISED,
                            bd=2,
                            width=12)
        back_btn.pack(side=tk.LEFT, padx=8)
    
    def validate_registration(self):
        """
        Validate all form fields before submission
        """
        first_name = self.first_name.get().strip()
        last_name = self.last_name.get().strip()
        email = self.email.get().strip()
        department = self.department.get()
        
        # Check if all fields are filled
        if not first_name:
            self.status_label.config(text="Error: First Name is required!", fg='red')
            messagebox.showwarning("Validation Error", "First Name is required!")
            return
        if not last_name:
            self.status_label.config(text="Error: Last Name is required!", fg='red')
            messagebox.showwarning("Validation Error", "Last Name is required!")
            return
        if not email:
            self.status_label.config(text="Error: Email Address is required!", fg='red')
            messagebox.showwarning("Validation Error", "Email Address is required!")
            return
        if department == 'Select Department':
            self.status_label.config(text="Error: Please select a Department!", fg='red')
            messagebox.showwarning("Validation Error", "Please select a Department!")
            return
        
        # Validate name fields (no numbers)
        if any(char.isdigit() for char in first_name):
            self.status_label.config(text="Error: First Name should not contain numbers!", fg='red')
            messagebox.showwarning("Validation Error", "First Name should not contain numbers!")
            return
        if any(char.isdigit() for char in last_name):
            self.status_label.config(text="Error: Last Name should not contain numbers!", fg='red')
            messagebox.showwarning("Validation Error", "Last Name should not contain numbers!")
            return
        
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            self.status_label.config(text="Error: Please enter a valid email address!", fg='red')
            messagebox.showwarning("Validation Error", "Please enter a valid email address!\nExample: name@company.com")
            return
        
        # If all validations pass
        self.status_label.config(text="Registration Successful!", fg='green', font=('Arial', 10, 'bold'))
        
        # Show success message box
        messagebox.showinfo("Success", 
                           f"Employee Registered Successfully!\n\n"
                           f"Name: {first_name} {last_name}\n"
                           f"Email: {email}\n"
                           f"Department: {department}")
    
    def clear_registration_form(self):
        """
        Clear all form fields
        """
        self.first_name.delete(0, tk.END)
        self.last_name.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.department.current(0)
        self.status_label.config(text="Form cleared. Ready for new entry.", fg='blue')
    
    def reset_registration_form(self):
        """
        Reset form to default values
        """
        self.clear_registration_form()
        self.status_label.config(text="Form has been reset.", fg='orange')
    
    def show_salary_calculator(self):
        """
        Salary Utility Calculator
        Calculates total salary based on daily wage and working days
        """
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create calculator frame
        calc_frame = tk.Frame(self.main_frame, bg='#ffffff', relief=tk.RAISED, bd=2)
        calc_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        title_frame = tk.Frame(calc_frame, bg='#ffffff')
        title_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(title_frame, text="Salary Utility Calculator",
                font=('Arial', 20, 'bold'), bg='#ffffff', fg='#1a5276').pack()
        
        # Input fields
        input_frame = tk.Frame(calc_frame, bg='#ffffff')
        input_frame.pack(pady=30, padx=50)
        
        # Daily Wage
        tk.Label(input_frame, text="Daily Wage ($):", font=('Arial', 12, 'bold'),
                bg='#ffffff', fg='#2c3e50').grid(row=0, column=0, pady=15, padx=10, sticky='e')
        self.daily_wage = tk.Entry(input_frame, font=('Arial', 12), width=25,
                                  relief=tk.SUNKEN, bd=2)
        self.daily_wage.grid(row=0, column=1, pady=15, padx=10)
        self.daily_wage.insert(0, "0.00")
        
        # Working Days
        tk.Label(input_frame, text="Working Days:", font=('Arial', 12, 'bold'),
                bg='#ffffff', fg='#2c3e50').grid(row=1, column=0, pady=15, padx=10, sticky='e')
        self.working_days = tk.Entry(input_frame, font=('Arial', 12), width=25,
                                    relief=tk.SUNKEN, bd=2)
        self.working_days.grid(row=1, column=1, pady=15, padx=10)
        self.working_days.insert(0, "0")
        
        # Result display with styling
        result_frame = tk.Frame(calc_frame, bg='#eaf2f8', relief=tk.GROOVE, bd=2)
        result_frame.pack(pady=20, padx=50, fill=tk.X)
        
        tk.Label(result_frame, text="Calculation Result:",
                font=('Arial', 14, 'bold'), bg='#eaf2f8', fg='#1a5276').pack(pady=10)
        
        self.salary_result = tk.Label(result_frame, text="$0.00",
                                      font=('Arial', 26, 'bold'), 
                                      bg='#eaf2f8', fg='#27ae60')
        self.salary_result.pack(pady=10)
        
        # Status message
        self.calc_status = tk.Label(calc_frame, text="", font=('Arial', 10),
                                   bg='#ffffff', fg='red')
        self.calc_status.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(calc_frame, bg='#ffffff')
        button_frame.pack(pady=20)
        
        calculate_btn = tk.Button(button_frame, text="Calculate", 
                                 command=self.calculate_salary,
                                 bg='#27ae60', fg='white', 
                                 font=('Arial', 11, 'bold'),
                                 padx=20, pady=8,
                                 cursor='hand2',
                                 relief=tk.RAISED,
                                 bd=2,
                                 width=12)
        calculate_btn.pack(side=tk.LEFT, padx=8)
        
        reset_btn = tk.Button(button_frame, text="Reset",
                             command=self.reset_calculator,
                             bg='#f39c12', fg='white',
                             font=('Arial', 11, 'bold'),
                             padx=20, pady=8,
                             cursor='hand2',
                             relief=tk.RAISED,
                             bd=2,
                             width=12)
        reset_btn.pack(side=tk.LEFT, padx=8)
        
        clear_btn = tk.Button(button_frame, text="Clear",
                             command=self.clear_calculator,
                             bg='#e74c3c', fg='white',
                             font=('Arial', 11, 'bold'),
                             padx=20, pady=8,
                             cursor='hand2',
                             relief=tk.RAISED,
                             bd=2,
                             width=12)
        clear_btn.pack(side=tk.LEFT, padx=8)
        
        back_btn = tk.Button(button_frame, text="Back to Menu",
                            command=self.show_welcome_notice,
                            bg='#3498db', fg='white',
                            font=('Arial', 11, 'bold'),
                            padx=20, pady=8,
                            cursor='hand2',
                            relief=tk.RAISED,
                            bd=2,
                            width=12)
        back_btn.pack(side=tk.LEFT, padx=8)
        
        # Additional info
        info_frame = tk.Frame(calc_frame, bg='#eaf2f8', relief=tk.GROOVE, bd=1)
        info_frame.pack(pady=15, padx=50, fill=tk.X)
        
        tk.Label(info_frame, text="Formula: Total Salary = Daily Wage x Working Days",
                font=('Arial', 10), bg='#eaf2f8', fg='#34495e').pack(pady=5)
        tk.Label(info_frame, text="Note: This calculation does not include bonuses or deductions.",
                font=('Arial', 9, 'italic'), bg='#eaf2f8', fg='#7f8c8d').pack(pady=5)
    
    def calculate_salary(self):
        """
        Calculate total salary with comprehensive exception handling
        Handles empty fields, invalid inputs, negative values, and edge cases
        """
        
        # Get values from entry fields
        daily_wage_str = self.daily_wage.get().strip()
        working_days_str = self.working_days.get().strip()
        
        # Exception handling for EMPTY FIELDS
        if not daily_wage_str:
            self.calc_status.config(text="Error: Daily Wage field is empty!", fg='red')
            messagebox.showerror("Input Error", "Daily Wage field cannot be empty!\nPlease enter a valid amount.")
            self.daily_wage.focus()
            return
        
        if not working_days_str:
            self.calc_status.config(text="Error: Working Days field is empty!", fg='red')
            messagebox.showerror("Input Error", "Working Days field cannot be empty!\nPlease enter the number of working days.")
            self.working_days.focus()
            return
        
        # Exception handling for INVALID CHARACTERS (non-numeric)
        try:
            # Try to convert to float
            daily_wage = float(daily_wage_str)
        except ValueError:
            self.calc_status.config(text="Error: Daily Wage must be a valid number!", fg='red')
            messagebox.showerror("Invalid Input", 
                               f"Invalid Daily Wage: '{daily_wage_str}'\n\n"
                               f"Please enter a valid numeric value.\n"
                               f"Examples: 100, 150.50, 200.75")
            self.daily_wage.delete(0, tk.END)
            self.daily_wage.focus()
            return
        
        try:
            working_days = float(working_days_str)
        except ValueError:
            self.calc_status.config(text="Error: Working Days must be a valid number!", fg='red')
            messagebox.showerror("Invalid Input", 
                               f"Invalid Working Days: '{working_days_str}'\n\n"
                               f"Please enter a valid numeric value.\n"
                               f"Examples: 20, 22, 25.5")
            self.working_days.delete(0, tk.END)
            self.working_days.focus()
            return
        
        # Exception handling for NEGATIVE VALUES
        if daily_wage < 0:
            self.calc_status.config(text="Error: Daily Wage cannot be negative!", fg='red')
            messagebox.showerror("Invalid Input", 
                               f"Daily Wage cannot be negative!\n\n"
                               f"Entered value: ${daily_wage:.2f}\n"
                               f"Please enter a positive value.")
            self.daily_wage.delete(0, tk.END)
            self.daily_wage.insert(0, "0.00")
            self.daily_wage.focus()
            return
        
        if working_days < 0:
            self.calc_status.config(text="Error: Working Days cannot be negative!", fg='red')
            messagebox.showerror("Invalid Input", 
                               f"Working Days cannot be negative!\n\n"
                               f"Entered value: {working_days:.0f}\n"
                               f"Please enter a positive value.")
            self.working_days.delete(0, tk.END)
            self.working_days.insert(0, "0")
            self.working_days.focus()
            return
        
        # Exception handling for ZERO VALUES (warning but not error)
        if daily_wage == 0:
            self.calc_status.config(text="Warning: Daily Wage is zero. Salary will be $0.", fg='orange')
        
        if working_days == 0:
            self.calc_status.config(text="Warning: Working Days is zero. Salary will be $0.", fg='orange')
        
        # Exception handling for EXCESSIVE VALUES
        if working_days > 365:
            self.calc_status.config(text="Error: Working Days cannot exceed 365 days per year!", fg='red')
            messagebox.showerror("Invalid Input", 
                               f"Working Days cannot exceed 365!\n\n"
                               f"Entered value: {working_days:.0f} days\n"
                               f"Maximum allowed: 365 days")
            self.working_days.delete(0, tk.END)
            self.working_days.insert(0, "0")
            self.working_days.focus()
            return
        
        if daily_wage > 10000:
            result = messagebox.askyesno("High Wage Warning", 
                                        f"Daily Wage is very high: ${daily_wage:,.2f}\n\n"
                                        f"This will result in a salary of ${daily_wage * working_days:,.2f}\n"
                                        f"Are you sure this is correct?")
            if not result:
                self.daily_wage.focus()
                return
        
        # Calculate total salary
        total_salary = daily_wage * working_days
        
        # Format with thousand separators and 2 decimal places
        self.salary_result.config(text=f"${total_salary:,.2f}", fg='#27ae60')
        
        # Success message
        if daily_wage > 0 and working_days > 0:
            self.calc_status.config(text="Calculation completed successfully!", fg='green')
        else:
            self.calc_status.config(text="Calculation completed (zero values detected).", fg='orange')
        
        # Show detailed breakdown in message box
        messagebox.showinfo("Salary Calculation Result",
                           f"SALARY CALCULATION BREAKDOWN\n\n"
                           f"{'=' * 35}\n"
                           f"Daily Wage:        ${daily_wage:,.2f}\n"
                           f"Working Days:      {working_days:,.0f}\n"
                           f"{'=' * 35}\n"
                           f"Total Salary:      ${total_salary:,.2f}\n"
                           f"{'=' * 35}\n\n"
                           f"Calculation: ${daily_wage:,.2f} x {working_days:,.0f} = ${total_salary:,.2f}")
    
    def reset_calculator(self):
        """
        Reset calculator fields to default values
        """
        self.daily_wage.delete(0, tk.END)
        self.working_days.delete(0, tk.END)
        self.daily_wage.insert(0, "0.00")
        self.working_days.insert(0, "0")
        self.salary_result.config(text="$0.00", fg='#27ae60')
        self.calc_status.config(text="Calculator reset to default values.", fg='blue')
        messagebox.showinfo("Reset", "Calculator has been reset to default values!")
    
    def clear_calculator(self):
        """
        Clear all calculator fields
        """
        self.daily_wage.delete(0, tk.END)
        self.working_days.delete(0, tk.END)
        self.salary_result.config(text="$0.00", fg='#27ae60')
        self.calc_status.config(text="All fields cleared. Enter new values.", fg='blue')
        messagebox.showinfo("Cleared", "All calculator fields have been cleared!")
    
    def show_about(self):
        """
        Display about information
        """
        about_text = """Employee Registration and Salary Utility System

Version: 2.0
Developer: Lab 09 - Tkinter Implementation
Framework: Python Tkinter

Features:
- Employee Registration with Validation
- Salary Calculator with Exception Handling
- Menu-based Navigation System
- Advanced Input Validation
- Professional UI Design
- Form Reset and Clear Options
- Cross-platform Compatibility

Exception Handling Includes:
- Empty field detection
- Invalid character validation
- Negative value prevention
- Range validation (0-365 days)
- High value warnings

Technical Details:
- Built with Python 3.x
- Uses Tkinter GUI Toolkit
- Regex for Email Validation
- Object-Oriented Design"""
        
        messagebox.showinfo("About System", about_text)
    
    def show_instructions(self):
        """
        Display usage instructions
        """
        instructions = """How to Use This System:

EMPLOYEE REGISTRATION:
- Fill in all employee details
- Names should not contain numbers
- Enter a valid email address (name@domain.com)
- Select department from dropdown menu
- Click 'Submit' to register employee
- Use 'Clear' to remove all entries
- Use 'Reset' to restore default values

SALARY CALCULATOR:
- Enter Daily Wage amount (USD)
- Enter Number of Working Days
- Click 'Calculate' to see total salary
- Use 'Reset' to set default values
- Use 'Clear' to empty all fields

SALARY CALCULATOR VALIDATION RULES:
- Fields cannot be empty
- Only numeric values allowed (0-9 and decimal point)
- Negative values are not allowed
- Working days cannot exceed 365
- Daily wage cannot exceed $10,000 (warning shown)
- Zero values are allowed but show warning

NAVIGATION:
- Use menu bar at top of window
- Click 'Back to Menu' to return to home
- Use File menu to switch features
- Click 'Exit' to close application

ERROR MESSAGES:
- Empty field: Shows specific error for each field
- Invalid input: Shows what was entered and correct format
- Negative values: Prevents calculation and shows error
- Excessive values: Shows warning or error as appropriate"""

        messagebox.showinfo("User Instructions", instructions)


# Main execution
if __name__ == "__main__":
    try:
        # Create main window
        root = tk.Tk()
        
        # Create application instance
        app = EmployeeSystem(root)
        
        # Start the application
        print("Starting Employee Registration and Salary Utility System...")
        print("Application loaded successfully!")
        print("Use the menu bar to navigate between features")
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\nApplication closed by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")
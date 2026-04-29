"""
Lab 10 - SMART Billing System with Multi-Item Support
FIXED: Proper layout with all elements visible
"""

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from datetime import datetime
import random
import json
import os


# ================================================================
# DATA SETUP
# ================================================================

PRODUCTS = {
    "Tea": {"price": 80, "category": "beverage", "tax": 5},
    "Coffee": {"price": 150, "category": "beverage", "tax": 5},
    "Sandwich": {"price": 250, "category": "food", "tax": 12},
    "Burger": {"price": 450, "category": "food", "tax": 12},
    "Fries": {"price": 200, "category": "snack", "tax": 8},
    "Juice": {"price": 180, "category": "beverage", "tax": 5},
    "Pizza Slice": {"price": 350, "category": "food", "tax": 12},
    "Ice Cream": {"price": 120, "category": "dessert", "tax": 8},
}

# File storage
BILL_HISTORY_FILE = "bill_history.json"
LOYALTY_POINTS_FILE = "loyalty_points.json"


def load_bill_history():
    if os.path.exists(BILL_HISTORY_FILE):
        with open(BILL_HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []


def save_bill_to_history(bill_data):
    history = load_bill_history()
    history.append(bill_data)
    with open(BILL_HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)


def load_loyalty_points():
    if os.path.exists(LOYALTY_POINTS_FILE):
        with open(LOYALTY_POINTS_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_loyalty_points(points_data):
    with open(LOYALTY_POINTS_FILE, 'w') as f:
        json.dump(points_data, f, indent=2)


def apply_smart_discount(subtotal, quantity, is_member=False, loyalty_points=0):
    discount_percent = 0
    reasons = []
    
    if quantity >= 5:
        discount_percent += 10
        reasons.append("Bulk Purchase (10%)")
    
    if subtotal >= 1000:
        discount_percent += 15
        reasons.append("High Value Order (15%)")
    
    if is_member:
        discount_percent += 5
        reasons.append("Member Discount (5%)")
    
    points_discount = min(loyalty_points // 100, 10)
    if points_discount > 0:
        discount_percent += points_discount
        reasons.append(f"Loyalty Points ({points_discount}%)")
    
    discount_percent = min(discount_percent, 35)
    
    if discount_percent == 0 and subtotal >= 300:
        discount_percent = 3
        reasons.append("Loyalty Discount (3%)")
    
    return discount_percent, reasons


def suggest_related_items(selected_item):
    related = {
        "Tea": ["Biscuits", "Sandwich"],
        "Coffee": ["Biscuits", "Burger"],
        "Sandwich": ["Juice", "Fries"],
        "Burger": ["Fries", "Juice"],
        "Fries": ["Burger", "Juice"],
        "Juice": ["Sandwich", "Fries"],
        "Pizza Slice": ["Juice", "Fries"],
        "Ice Cream": ["Juice", "Coffee"]
    }
    suggestions = related.get(selected_item, ["Tea", "Coffee"])
    return random.sample(suggestions, min(2, len(suggestions)))


def calculate_tax(subtotal, item_name):
    tax_rate = PRODUCTS.get(item_name, {}).get("tax", 8)
    tax_amount = subtotal * (tax_rate / 100)
    return tax_amount, tax_rate


def validate_name(name):
    if not name:
        return False, "Name is required!"
    if any(char.isdigit() for char in name):
        return False, "Name cannot contain numbers!"
    return True, ""


# ================================================================
# MAIN APPLICATION CLASS
# ================================================================

class SmartBillingSystem:
    def __init__(self, root):
        self.root = root
        self.shopping_cart = []
        self.bill_history = load_bill_history()
        self.loyalty_points = load_loyalty_points()
        self.setup_window()
        self.create_menubar()
        self.create_widgets()
        self.update_clock()
        
    def setup_window(self):
        """Configure the main window - LARGER SIZE"""
        self.root.title("SMART Billing System - Multi-Item Support")
        
        # Set a large window size
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        self.root.configure(bg="#f0f0f0")
        
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def create_menubar(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save Receipt", command=self.save_receipt_to_file)
        file_menu.add_command(label="Print Receipt", command=self.print_receipt)
        file_menu.add_separator()
        file_menu.add_command(label="Export to CSV", command=self.export_to_csv)
        file_menu.add_command(label="Bill History", command=self.view_bill_history)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        menubar.add_cascade(label="File", menu=file_menu)
        
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Loyalty Points", command=self.manage_loyalty_points)
        tools_menu.add_command(label="Search Customer", command=self.search_customer)
        tools_menu.add_command(label="Dashboard", command=self.show_dashboard)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="User Guide", command=self.show_user_guide)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_widgets(self):
        """Create all GUI widgets with proper spacing"""
        
        # Main container with padding
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # ===== TOP BAR =====
        top_bar = tk.Frame(main_frame, bg="#1a237e", height=50)
        top_bar.pack(fill="x", pady=(0, 15))
        top_bar.pack_propagate(False)
        
        title_label = tk.Label(top_bar, text="🤖 SMART BILLING SYSTEM", 
                               font=("Arial", 18, "bold"), bg="#1a237e", fg="white")
        title_label.pack(side="left", padx=20, pady=10)
        
        self.clock_label = tk.Label(top_bar, font=("Arial", 12), bg="#1a237e", fg="white")
        self.clock_label.pack(side="right", padx=20, pady=10)
        
        # ===== STATISTICS BAR =====
        stats_frame = tk.Frame(main_frame, bg="#4caf50", height=40)
        stats_frame.pack(fill="x", pady=(0, 15))
        stats_frame.pack_propagate(False)
        
        self.total_sales_label = tk.Label(stats_frame, text="💰 Today's Sales: Rs. 0", 
                                          font=("Arial", 11, "bold"), bg="#4caf50", fg="white")
        self.total_sales_label.pack(side="left", padx=20, pady=8)
        
        self.loyalty_points_label = tk.Label(stats_frame, text="⭐ Loyalty Points: 0", 
                                              font=("Arial", 11, "bold"), bg="#4caf50", fg="white")
        self.loyalty_points_label.pack(side="left", padx=20, pady=8)
        
        # ===== MAIN CONTENT - 3 COLUMNS =====
        content_frame = tk.Frame(main_frame, bg="#f0f0f0")
        content_frame.pack(fill="both", expand=True)
        
        # Column widths: 30% - 30% - 40%
        content_frame.grid_columnconfigure(0, weight=3)
        content_frame.grid_columnconfigure(1, weight=3)
        content_frame.grid_columnconfigure(2, weight=4)
        
        # ========== COLUMN 1: CUSTOMER INFORMATION ==========
        col1 = tk.Frame(content_frame, bg="#f0f0f0")
        col1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        customer_frame = tk.LabelFrame(col1, text="👤 CUSTOMER INFORMATION", 
                                        font=("Arial", 12, "bold"), bg="white",
                                        padx=15, pady=15, relief=tk.RIDGE)
        customer_frame.pack(fill="both", expand=True)
        
        # Name
        tk.Label(customer_frame, text="Customer Name *", font=("Arial", 10, "bold"), 
                bg="white").pack(anchor="w", pady=(5, 0))
        self.name_entry = tk.Entry(customer_frame, font=("Arial", 11), relief=tk.SOLID, borderwidth=1)
        self.name_entry.pack(fill="x", pady=5)
        
        # Contact
        tk.Label(customer_frame, text="Contact Number *", font=("Arial", 10, "bold"), 
                bg="white").pack(anchor="w", pady=(10, 0))
        self.contact_entry = tk.Entry(customer_frame, font=("Arial", 11), relief=tk.SOLID, borderwidth=1)
        self.contact_entry.pack(fill="x", pady=5)
        self.contact_entry.bind('<KeyRelease>', self.update_loyalty_display)
        
        # Member Checkbox
        self.member_var = tk.BooleanVar()
        member_cb = tk.Checkbutton(customer_frame, text="✓ Premium Member (5% extra discount)", 
                                    variable=self.member_var, bg="white", font=("Arial", 10))
        member_cb.pack(anchor="w", pady=15)
        
        # Loyalty Points Display
        tk.Label(customer_frame, text="⭐ Loyalty Points", font=("Arial", 10, "bold"), 
                bg="white").pack(anchor="w", pady=(10, 0))
        self.loyalty_display = tk.Label(customer_frame, text="0 points available", 
                                         bg="white", fg="#4caf50", font=("Arial", 11, "bold"))
        self.loyalty_display.pack(anchor="w", pady=5)
        
        # ========== COLUMN 2: ADD ITEMS TO CART ==========
        col2 = tk.Frame(content_frame, bg="#f0f0f0")
        col2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        add_frame = tk.LabelFrame(col2, text="➕ ADD ITEMS TO CART", 
                                   font=("Arial", 12, "bold"), bg="white",
                                   padx=15, pady=15, relief=tk.RIDGE)
        add_frame.pack(fill="both", expand=True)
        
        # Item Selection
        tk.Label(add_frame, text="Select Item", font=("Arial", 10, "bold"), 
                bg="white").pack(anchor="w", pady=(5, 0))
        self.item_var = tk.StringVar(value="Select Item")
        item_menu = tk.OptionMenu(add_frame, self.item_var, *PRODUCTS.keys())
        item_menu.config(font=("Arial", 10), width=25)
        item_menu.pack(fill="x", pady=5)
        self.item_var.trace_add("write", self.update_price_display)
        
        # Quantity
        tk.Label(add_frame, text="Quantity", font=("Arial", 10, "bold"), 
                bg="white").pack(anchor="w", pady=(10, 0))
        self.qty_entry = tk.Entry(add_frame, font=("Arial", 11), relief=tk.SOLID, borderwidth=1)
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack(fill="x", pady=5)
        
        # Price Display
        tk.Label(add_frame, text="Price per item", font=("Arial", 10, "bold"), 
                bg="white").pack(anchor="w", pady=(10, 0))
        self.price_display = tk.Label(add_frame, text="Rs. 0", 
                                       bg="white", fg="#1a237e", font=("Arial", 14, "bold"))
        self.price_display.pack(anchor="w", pady=5)
        
        # Tax Display
        self.tax_display = tk.Label(add_frame, text="GST: 5%", 
                                     bg="white", fg="#666", font=("Arial", 9))
        self.tax_display.pack(anchor="w", pady=2)
        
        # AI Suggestion
        self.suggestion_text = tk.StringVar(value="Select an item to see recommendations")
        suggestion_label = tk.Label(add_frame, textvariable=self.suggestion_text, 
                                     bg="#fff3e0", fg="#e65100", font=("Arial", 9, "italic"),
                                     padx=8, pady=8, relief=tk.SOLID)
        suggestion_label.pack(fill="x", pady=15)
        
        # Add to Cart Button
        add_btn = tk.Button(add_frame, text="➕ ADD TO CART", 
                            bg="#4caf50", fg="white", font=("Arial", 12, "bold"),
                            command=self.add_to_cart, cursor="hand2", pady=8)
        add_btn.pack(fill="x", pady=10)
        
        # ========== COLUMN 3: SHOPPING CART & RECEIPT ==========
        col3 = tk.Frame(content_frame, bg="#f0f0f0")
        col3.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        # Cart Frame
        cart_frame = tk.LabelFrame(col3, text="🛒 SHOPPING CART", 
                                    font=("Arial", 12, "bold"), bg="white",
                                    padx=15, pady=15, relief=tk.RIDGE)
        cart_frame.pack(fill="both", expand=True)
        
        # Cart Listbox
        cart_list_frame = tk.Frame(cart_frame, bg="white")
        cart_list_frame.pack(fill="both", expand=True, pady=5)
        
        scrollbar = tk.Scrollbar(cart_list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.cart_listbox = tk.Listbox(cart_list_frame, height=6, font=("Consolas", 10),
                                        yscrollcommand=scrollbar.set, relief=tk.SOLID, borderwidth=1)
        self.cart_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.cart_listbox.yview)
        
        # Cart Buttons
        cart_btn_frame = tk.Frame(cart_frame, bg="white")
        cart_btn_frame.pack(fill="x", pady=10)
        
        remove_btn = tk.Button(cart_btn_frame, text="❌ Remove Selected", 
                               bg="#f44336", fg="white", font=("Arial", 9, "bold"),
                               command=self.remove_from_cart, cursor="hand2")
        remove_btn.pack(side="left", padx=5)
        
        clear_cart_btn = tk.Button(cart_btn_frame, text="🗑️ Clear Cart", 
                                    bg="#9e9e9e", fg="white", font=("Arial", 9, "bold"),
                                    command=self.clear_cart, cursor="hand2")
        clear_cart_btn.pack(side="left", padx=5)
        
        # Cart Total
        self.cart_total_label = tk.Label(cart_frame, text="Cart Total: Rs. 0", 
                                          bg="white", fg="#1a237e", font=("Arial", 13, "bold"))
        self.cart_total_label.pack(pady=10)
        
        # Discount Section
        discount_frame = tk.Frame(cart_frame, bg="white")
        discount_frame.pack(fill="x", pady=5)
        
        tk.Label(discount_frame, text="Discount (%):", font=("Arial", 10, "bold"), 
                bg="white").pack(side="left")
        self.discount_entry = tk.Entry(discount_frame, width=10, font=("Arial", 11), 
                                        relief=tk.SOLID, borderwidth=1)
        self.discount_entry.insert(0, "0")
        self.discount_entry.pack(side="left", padx=5)
        
        # ===== ACTION BUTTONS =====
        action_frame = tk.Frame(cart_frame, bg="white")
        action_frame.pack(fill="x", pady=15)
        
        # AI Discount Button - PROMINENT
        ai_btn = tk.Button(action_frame, text="🤖 APPLY AI DISCOUNT", 
                          bg="#2196f3", fg="white", font=("Arial", 11, "bold"),
                          command=self.apply_ai_discount, cursor="hand2",
                          pady=8, relief=tk.RAISED)
        ai_btn.pack(fill="x", pady=4)
        
        # Generate Receipt Button - PROMINENT
        generate_btn = tk.Button(action_frame, text="📄 GENERATE RECEIPT", 
                                bg="#4caf50", fg="white", font=("Arial", 11, "bold"),
                                command=self.generate_bill, cursor="hand2",
                                pady=8, relief=tk.RAISED)
        generate_btn.pack(fill="x", pady=4)
        
        # Clear All Button
        clear_btn = tk.Button(action_frame, text="🗑️ CLEAR ALL", 
                             bg="#ff9800", fg="white", font=("Arial", 11, "bold"),
                             command=self.clear_all, cursor="hand2",
                             pady=8, relief=tk.RAISED)
        clear_btn.pack(fill="x", pady=4)
        
        # Exit Button
        exit_btn = tk.Button(action_frame, text="🚪 EXIT", 
                            bg="#f44336", fg="white", font=("Arial", 11, "bold"),
                            command=self.exit_app, cursor="hand2",
                            pady=8, relief=tk.RAISED)
        exit_btn.pack(fill="x", pady=4)
        
        # Receipt Preview
        tk.Label(cart_frame, text="📋 RECEIPT PREVIEW", font=("Arial", 10, "bold"), 
                bg="white", fg="#666").pack(pady=(10, 5))
        
        receipt_text_frame = tk.Frame(cart_frame, bg="white")
        receipt_text_frame.pack(fill="both", expand=True, pady=5)
        
        receipt_scroll = tk.Scrollbar(receipt_text_frame)
        receipt_scroll.pack(side="right", fill="y")
        
        self.receipt_box = tk.Text(receipt_text_frame, height=10, 
                                    font=("Consolas", 9), bg="#fafafa", 
                                    fg="#333", wrap="word",
                                    yscrollcommand=receipt_scroll.set)
        self.receipt_box.pack(side="left", fill="both", expand=True)
        receipt_scroll.config(command=self.receipt_box.yview)
        
        # Status Bar
        self.status_bar = tk.Label(main_frame, text="System Ready | Add items to cart | Name cannot contain numbers", 
                                    bg="#333", fg="white", font=("Arial", 9), pady=6)
        self.status_bar.pack(side="bottom", fill="x", pady=(10, 0))
    
    def update_loyalty_display(self, event=None):
        contact = self.contact_entry.get().strip()
        points = self.loyalty_points.get(contact, 0)
        self.loyalty_display.config(text=f"{points} points available")
        return points
    
    def update_price_display(self, *args):
        selected = self.item_var.get()
        if selected in PRODUCTS:
            price = PRODUCTS[selected]["price"]
            tax_rate = PRODUCTS[selected]["tax"]
            self.price_display.config(text=f"Rs. {price}")
            self.tax_display.config(text=f"GST: {tax_rate}%")
            suggestions = suggest_related_items(selected)
            self.suggestion_text.set(f" Try {', '.join(suggestions)} with {selected}!")
        else:
            self.price_display.config(text="Rs. 0")
            self.tax_display.config(text="GST: 5%")
    
    def add_to_cart(self):
        item = self.item_var.get()
        if item == "Select Item":
            messagebox.showwarning("No Item", "Please select an item first!")
            return
        
        try:
            quantity = int(self.qty_entry.get())
            if quantity <= 0:
                messagebox.showwarning("Invalid Quantity", "Quantity must be greater than 0!")
                return
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid quantity!")
            return
        
        price = PRODUCTS[item]["price"]
        tax_rate = PRODUCTS[item]["tax"]
        subtotal = price * quantity
        tax = subtotal * (tax_rate / 100)
        total = subtotal + tax
        
        cart_item = {
            "item": item,
            "quantity": quantity,
            "price": price,
            "subtotal": subtotal,
            "tax_rate": tax_rate,
            "tax": tax,
            "total": total
        }
        
        self.shopping_cart.append(cart_item)
        self.update_cart_display()
        
        self.item_var.set("Select Item")
        self.qty_entry.delete(0, tk.END)
        self.qty_entry.insert(0, "1")
        
        self.status_bar.config(text=f"Added {quantity}x {item} to cart!")
    
    def update_cart_display(self):
        self.cart_listbox.delete(0, tk.END)
        cart_total = 0
        for i, item in enumerate(self.shopping_cart):
            display_text = f"{item['quantity']}x {item['item']:<12} - Rs. {item['total']:.2f}"
            self.cart_listbox.insert(tk.END, display_text)
            cart_total += item['total']
        self.cart_total_label.config(text=f"Cart Total: Rs. {cart_total:.2f}")
        return cart_total
    
    def remove_from_cart(self):
        selection = self.cart_listbox.curselection()
        if selection:
            index = selection[0]
            removed = self.shopping_cart.pop(index)
            self.update_cart_display()
            self.status_bar.config(text=f" Removed {removed['quantity']}x {removed['item']}")
        else:
            messagebox.showwarning("No Selection", "Please select an item to remove!")
    
    def clear_cart(self):
        if self.shopping_cart:
            self.shopping_cart = []
            self.update_cart_display()
            self.status_bar.config(text="🗑️ Cart cleared!")
    
    def apply_ai_discount(self):
        if not self.shopping_cart:
            messagebox.showwarning("Empty Cart", "Please add items to cart first!")
            return
        
        cart_total = sum(item['total'] for item in self.shopping_cart)
        total_quantity = sum(item['quantity'] for item in self.shopping_cart)
        is_member = self.member_var.get()
        
        contact = self.contact_entry.get().strip()
        points = self.loyalty_points.get(contact, 0)
        
        discount, reasons = apply_smart_discount(cart_total, total_quantity, is_member, points)
        
        self.discount_entry.delete(0, tk.END)
        self.discount_entry.insert(0, str(discount))
        
        if discount > 0:
            savings = cart_total * discount / 100
            messagebox.showinfo("AI Discount Applied", 
                               f"{discount}% discount applied!\n\n"
                               f"Original: Rs. {cart_total:.2f}\n"
                               f"Discount: {discount}%\n"
                               f"You Save: Rs. {savings:.2f}\n\n"
                               f"Reasons:\n• " + "\n• ".join(reasons))
        else:
            messagebox.showinfo("No Discount", "No automatic discount available.\n\nTry adding more items or becoming a member!")
    
    def generate_bill(self):
        if not self.shopping_cart:
            messagebox.showwarning("Empty Cart", "Please add items to cart first!")
            return
        
        name = self.name_entry.get().strip()
        contact = self.contact_entry.get().strip()
        discount_text = self.discount_entry.get().strip()
        is_member = self.member_var.get()
        
        # Validation
        name_valid, name_error = validate_name(name)
        if not name_valid:
            messagebox.showerror("Error", name_error)
            self.name_entry.focus()
            return
        
        if not contact:
            messagebox.showerror("Error", "Contact number is required!")
            self.contact_entry.focus()
            return
        
        if not contact.isdigit():
            messagebox.showerror("Error", "Contact number must contain only digits!")
            return
        
        if len(contact) < 10 or len(contact) > 13:
            messagebox.showerror("Error", "Contact number must be 10-13 digits!")
            return
        
        try:
            discount = float(discount_text) if discount_text else 0
        except ValueError:
            messagebox.showerror("Error", "Discount must be a number!")
            return
        
        if discount < 0 or discount > 100:
            messagebox.showerror("Error", "Discount must be between 0 and 100!")
            return
        
        # Calculate totals
        subtotal = sum(item['subtotal'] for item in self.shopping_cart)
        tax_total = sum(item['tax'] for item in self.shopping_cart)
        cart_total = sum(item['total'] for item in self.shopping_cart)
        
        discount_amount = cart_total * (discount / 100)
        final_total = cart_total - discount_amount
        
        # Loyalty points
        points_earned = int(final_total // 10)
        
        if contact in self.loyalty_points:
            self.loyalty_points[contact] += points_earned
        else:
            self.loyalty_points[contact] = points_earned
        save_loyalty_points(self.loyalty_points)
        
        # Receipt
        current_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")
        receipt_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
        self.receipt_box.delete("1.0", tk.END)
        
        self.receipt_box.insert(tk.END, "=" * 55 + "\n")
        self.receipt_box.insert(tk.END, " " * 15 + "SMART BILLING\n")
        self.receipt_box.insert(tk.END, "=" * 55 + "\n")
        self.receipt_box.insert(tk.END, f"Date     : {current_time}\n")
        self.receipt_box.insert(tk.END, f"Receipt #: {receipt_id}\n")
        self.receipt_box.insert(tk.END, "-" * 55 + "\n")
        self.receipt_box.insert(tk.END, f"Customer : {name.title()}\n")
        self.receipt_box.insert(tk.END, f"Contact  : {contact}\n")
        self.receipt_box.insert(tk.END, f"Member   : {'Yes' if is_member else 'No'}\n")
        self.receipt_box.insert(tk.END, "-" * 55 + "\n")
        self.receipt_box.insert(tk.END, "ITEMS:\n")
        
        for item in self.shopping_cart:
            self.receipt_box.insert(tk.END, f"  {item['quantity']}x {item['item']:<12} @ Rs.{item['price']:.0f} = Rs.{item['subtotal']:.2f}\n")
        
        self.receipt_box.insert(tk.END, "-" * 55 + "\n")
        self.receipt_box.insert(tk.END, f"Subtotal    : Rs. {subtotal:.2f}\n")
        self.receipt_box.insert(tk.END, f"GST Total   : Rs. {tax_total:.2f}\n")
        self.receipt_box.insert(tk.END, f"Cart Total  : Rs. {cart_total:.2f}\n")
        self.receipt_box.insert(tk.END, f"Discount    : {discount:.0f}% (Rs. {discount_amount:.2f})\n")
        self.receipt_box.insert(tk.END, f"FINAL TOTAL : Rs. {final_total:.2f}\n")
        self.receipt_box.insert(tk.END, "-" * 55 + "\n")
        self.receipt_box.insert(tk.END, f"Points Earned: {points_earned}\n")
        self.receipt_box.insert(tk.END, "=" * 55 + "\n")
        self.receipt_box.insert(tk.END, "     Thank You! Visit Again!\n")
        
        # Save to history
        bill_data = {
            "receipt_id": receipt_id,
            "date": current_time,
            "customer": name,
            "contact": contact,
            "items": len(self.shopping_cart),
            "total": final_total
        }
        save_bill_to_history(bill_data)
        
        # Update stats
        current_total = 0
        try:
            text = self.total_sales_label.cget("text")
            if "Rs." in text:
                current_total = float(text.split("Rs.")[1].strip())
        except:
            pass
        self.total_sales_label.config(text=f" Today's Sales: Rs. {current_total + final_total:.2f}")
        self.loyalty_points_label.config(text=f"Loyalty Points: {points_earned} earned")
        
        # Clear cart
        self.shopping_cart = []
        self.update_cart_display()
        
        messagebox.showinfo("Success", f"Bill generated!\n\nCustomer: {name}\nTotal: Rs. {final_total:.2f}\nPoints Earned: {points_earned}")
    
    def save_receipt_to_file(self):
        content = self.receipt_box.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("No Receipt", "Generate a receipt first!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Success", f"Saved to {file_path}")
    
    def print_receipt(self):
        if not self.receipt_box.get("1.0", tk.END).strip():
            messagebox.showwarning("No Receipt", "Generate a receipt first!")
            return
        messagebox.showinfo("Print", "Receipt sent to printer!")
    
    def export_to_csv(self):
        history = load_bill_history()
        if not history:
            messagebox.showwarning("No Data", "No bill history!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            import csv
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=history[0].keys())
                writer.writeheader()
                writer.writerows(history)
            messagebox.showinfo("Success", f"Exported {len(history)} bills!")
    
    def view_bill_history(self):
        history = load_bill_history()
        if not history:
            messagebox.showinfo("No History", "No bills yet!")
            return
        win = tk.Toplevel(self.root)
        win.title("Bill History")
        win.geometry("800x500")
        tree = ttk.Treeview(win, columns=("Date", "Customer", "Items", "Total"), show="headings")
        for col in ("Date", "Customer", "Items", "Total"):
            tree.heading(col, text=col)
            tree.column(col, width=180)
        for bill in history[-50:]:
            tree.insert("", "end", values=(bill.get("date", ""), bill.get("customer", ""), bill.get("items", 0), f"Rs. {bill.get('total', 0):.2f}"))
        tree.pack(fill="both", expand=True, padx=10, pady=10)
    
    def manage_loyalty_points(self):
        win = tk.Toplevel(self.root)
        win.title("Loyalty Points")
        win.geometry("500x400")
        tk.Label(win, text="Loyalty Points", font=("Arial", 16, "bold")).pack(pady=10)
        text = tk.Text(win, font=("Consolas", 10))
        text.pack(fill="both", expand=True, padx=10, pady=10)
        for contact, points in self.loyalty_points.items():
            text.insert(tk.END, f"{contact}: {points} points\n")
        text.config(state="disabled")
    
    def search_customer(self):
        win = tk.Toplevel(self.root)
        win.title("Search Customer")
        win.geometry("600x500")
        tk.Label(win, text="Enter Contact Number:", font=("Arial", 12)).pack(pady=10)
        entry = tk.Entry(win, font=("Arial", 12), width=20)
        entry.pack(pady=5)
        text = tk.Text(win, font=("Consolas", 10))
        text.pack(fill="both", expand=True, padx=10, pady=10)
        def search():
            contact = entry.get()
            history = load_bill_history()
            bills = [b for b in history if b.get("contact") == contact]
            text.delete("1.0", tk.END)
            if bills:
                total = sum(b.get("total", 0) for b in bills)
                text.insert(tk.END, f"Found {len(bills)} bills\nTotal Spent: Rs. {total:.2f}\nPoints: {self.loyalty_points.get(contact, 0)}\n\n")
                for b in bills[-10:]:
                    text.insert(tk.END, f"{b.get('date')} - Rs. {b.get('total', 0):.2f}\n")
            else:
                text.insert(tk.END, "No customer found!")
        tk.Button(win, text="Search", command=search, bg="#2196f3", fg="white", font=("Arial", 10, "bold")).pack()
    
    def show_dashboard(self):
        history = load_bill_history()
        total = sum(b.get("total", 0) for b in history)
        customers = len(set(b.get("contact", "") for b in history))
        win = tk.Toplevel(self.root)
        win.title("Dashboard")
        win.geometry("400x300")
        tk.Label(win, text="Dashboard", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(win, text=f"Total Sales: Rs. {total:,.2f}", font=("Arial", 12)).pack(pady=5)
        tk.Label(win, text=f"Total Customers: {customers}", font=("Arial", 12)).pack(pady=5)
        tk.Label(win, text=f"Total Bills: {len(history)}", font=("Arial", 12)).pack(pady=5)
    
    def show_user_guide(self):
        win = tk.Toplevel(self.root)
        win.title("User Guide")
        win.geometry("600x500")
        text = tk.Text(win, wrap="word", font=("Arial", 10))
        text.pack(fill="both", expand=True, padx=10, pady=10)
        guide = """
        USER GUIDE - SMART BILLING SYSTEM
        
        1. Enter customer name (no numbers allowed)
        2. Enter contact number (10-13 digits)
        3. Check "Premium Member" if applicable
        4. Add items to cart:
           - Select item
           - Enter quantity
           - Click "ADD TO CART"
           - Repeat for multiple items
        5. Click "APPLY AI DISCOUNT" for automatic discounts
        6. Click "GENERATE RECEIPT" to complete bill
        
        AI DISCOUNTS:
        - 10% off for 5+ items
        - 15% off for Rs. 1000+ orders
        - 5% off for Premium Members
        - Up to 10% off with loyalty points
        
        TIPS:
        - Use "Remove Selected" to delete items from cart
        - Use "Clear Cart" to start over
        - Save receipts for records
        """
        text.insert("1.0", guide)
        text.config(state="disabled")
    
    def show_about(self):
        messagebox.showinfo("About", "SMART Billing System v3.0\nMulti-Item Support\nAI Discounts\nLoyalty Points\n\nLab 10 Project")
    
    def update_clock(self):
        current_time = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        self.clock_label.config(text=f" {current_time}")
        self.root.after(1000, self.update_clock)
    
    def clear_all(self):
        self.name_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.member_var.set(False)
        self.discount_entry.delete(0, tk.END)
        self.discount_entry.insert(0, "0")
        self.shopping_cart = []
        self.update_cart_display()
        self.receipt_box.delete("1.0", tk.END)
        self.item_var.set("Select Item")
        self.qty_entry.delete(0, tk.END)
        self.qty_entry.insert(0, "1")
        self.loyalty_display.config(text="0 points available")
        self.name_entry.focus()
        self.status_bar.config(text="All fields cleared!")
    
    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()


# ================================================================
# MAIN ENTRY POINT
# ================================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartBillingSystem(root)
    root.mainloop()
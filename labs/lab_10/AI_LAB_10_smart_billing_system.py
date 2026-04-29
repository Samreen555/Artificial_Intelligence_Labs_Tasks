"""
Lab 10 - Smart Billing System with AI-Based Decision Rules
Fixed: Screen size optimized + Name cannot contain digits
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import random


# ================================================================
# DATA SETUP
# ================================================================

# Product database with prices and categories
PRODUCTS = {
    "Tea": {"price": 80, "category": "beverage"},
    "Coffee": {"price": 150, "category": "beverage"},
    "Sandwich": {"price": 250, "category": "food"},
    "Burger": {"price": 450, "category": "food"},
    "Fries": {"price": 200, "category": "snack"},
    "Juice": {"price": 180, "category": "beverage"},
    "Pizza Slice": {"price": 350, "category": "food"},
    "Ice Cream": {"price": 120, "category": "dessert"}
}

# AI Rule: Related items suggestions
RELATED_ITEMS = {
    "Tea": ["Biscuits", "Sandwich"],
    "Coffee": ["Biscuits", "Burger"],
    "Sandwich": ["Juice", "Fries"],
    "Burger": ["Fries", "Juice"],
    "Fries": ["Burger", "Juice"],
    "Juice": ["Sandwich", "Fries"],
    "Pizza Slice": ["Juice", "Fries"],
    "Ice Cream": ["Juice", "Coffee"]
}


# ================================================================
# AI RULE FUNCTIONS
# ================================================================

def apply_smart_discount(subtotal, quantity, is_member=False):
    """Apply automatic discount based on rules"""
    discount_percent = 0
    reasons = []
    
    # Rule 1: Bulk purchase (5+ items) → 10% off
    if quantity >= 5:
        discount_percent += 10
        reasons.append("Bulk Purchase (10%)")
    
    # Rule 2: High value order (Rs. 1000+) → 15% off
    if subtotal >= 1000:
        discount_percent += 15
        reasons.append("High Value Order (15%)")
    
    # Rule 3: Member discount → extra 5%
    if is_member:
        discount_percent += 5
        reasons.append("Member Discount (5%)")
    
    # Cap at 30%
    discount_percent = min(discount_percent, 30)
    
    # Small loyalty discount for regular orders
    if discount_percent == 0 and subtotal >= 300:
        discount_percent = 3
        reasons.append("Loyalty Discount (3%)")
    
    return discount_percent, reasons


def suggest_related_items(selected_item):
    """AI: Suggest items that go well together"""
    if selected_item in RELATED_ITEMS:
        suggestions = RELATED_ITEMS[selected_item]
        return random.sample(suggestions, min(2, len(suggestions)))
    return ["Tea", "Coffee"]


def get_bundle_offer(item_name, quantity):
    """Check for special bundle deals"""
    category = PRODUCTS.get(item_name, {}).get("category", "")
    offers = {
        "beverage": "Buy 3 beverages, get 1 FREE!",
        "snack": "Buy 2 snacks, get 10% OFF!",
        "food": "Burger + Fries combo: Save Rs. 50!"
    }
    return offers.get(category, "")


def validate_name(name):
    """Check if name contains only letters and spaces"""
    if not name:
        return False, "Name is required!"
    
    # Check if name contains any digits
    if any(char.isdigit() for char in name):
        return False, "Name cannot contain numbers!"
    
    # Check if name contains only valid characters (letters, spaces, dots)
    valid_chars = all(char.isalpha() or char.isspace() or char in ".-'" for char in name)
    if not valid_chars:
        return False, "Name can only contain letters, spaces, dots, and hyphens!"
    
    return True, ""


# ================================================================
# MAIN APPLICATION CLASS
# ================================================================

class SmartBillingSystem:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()
        self.setup_bindings()
        
    def setup_window(self):
        """Configure the main window - OPTIMIZED SCREEN SIZE"""
        self.root.title("Smart Billing System - AI Powered")
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set window size (1000x800 is good for most screens)
        window_width = 1000
        window_height = 800
        
        # Calculate position to center the window
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        
        # Set window geometry: width x height + x + y
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        
        # Make window resizable but with minimum size
        self.root.minsize(900, 700)
        self.root.configure(bg="#E8F0FE")
    
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # ===== MAIN CONTAINER WITH SCROLLING =====
        main_container = tk.Frame(self.root, bg="#E8F0FE")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # ===== TITLE SECTION =====
        title_frame = tk.Frame(main_container, bg="#E8F0FE")
        title_frame.pack(fill="x", pady=(0, 10))
        
        title = tk.Label(title_frame, text="Smart Billing System", 
                        font=("Arial", 26, "bold"), bg="#E8F0FE", fg="#1E3A8A")
        title.pack()
        
        subtitle = tk.Label(title_frame, text="AI-Powered Retail with Smart Discounts & Recommendations | Real-Time Billing Solution",
                           font=("Arial", 10), bg="#E8F0FE", fg="#4B5563")
        subtitle.pack()
        
        # ===== CONTENT AREA (Two Columns) =====
        content_frame = tk.Frame(main_container, bg="#E8F0FE")
        content_frame.pack(fill="both", expand=True, pady=10)
        
        # Left Column - Input Form
        left_column = tk.Frame(content_frame, bg="#E8F0FE")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Right Column - Receipt Display
        right_column = tk.Frame(content_frame, bg="#E8F0FE")
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # ===== FORM FRAME (Left Column) =====
        form_frame = tk.Frame(left_column, bg="white", padx=30, pady=25, 
                               relief=tk.RIDGE, borderwidth=2)
        form_frame.pack(fill="both", expand=True)
        
        # Form Title
        form_title = tk.Label(form_frame, text="📝 Order Details", 
                              font=("Arial", 16, "bold"), bg="white", fg="#1E3A8A")
        form_title.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="w")
        
        # Row 1: Customer Name
        tk.Label(form_frame, text="Customer Name *", bg="white", 
                font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="w", pady=8)
        self.name_entry = tk.Entry(form_frame, width=35, font=("Arial", 11), 
                                    relief=tk.SOLID, borderwidth=1)
        self.name_entry.grid(row=1, column=1, padx=15, pady=8)
        
        # Row 2: Contact Number
        tk.Label(form_frame, text="Contact Number *", bg="white", 
                font=("Arial", 11, "bold")).grid(row=2, column=0, sticky="w", pady=8)
        self.contact_entry = tk.Entry(form_frame, width=35, font=("Arial", 11),
                                       relief=tk.SOLID, borderwidth=1)
        self.contact_entry.grid(row=2, column=1, padx=15, pady=8)
        
        # Row 3: Member Status (AI Feature)
        tk.Label(form_frame, text="Member Status", bg="white", 
                font=("Arial", 11, "bold")).grid(row=3, column=0, sticky="w", pady=8)
        self.member_var = tk.BooleanVar()
        member_check = tk.Checkbutton(form_frame, text="Premium Member (5% extra discount)", 
                                       variable=self.member_var, bg="white", 
                                       font=("Arial", 10), fg="#10B981")
        member_check.grid(row=3, column=1, padx=15, pady=8, sticky="w")
        
        # Row 4: Item Selection
        tk.Label(form_frame, text="Select Item *", bg="white", 
                font=("Arial", 11, "bold")).grid(row=4, column=0, sticky="w", pady=8)
        self.item_var = tk.StringVar(value="Select Item")
        self.item_var.trace_add("write", self.update_price)
        item_menu = tk.OptionMenu(form_frame, self.item_var, *PRODUCTS.keys())
        item_menu.config(width=30, font=("Arial", 11), bg="white", relief=tk.SOLID)
        item_menu.grid(row=4, column=1, padx=15, pady=8)
        
        # Row 5: Price
        tk.Label(form_frame, text="Item Price *", bg="white", 
                font=("Arial", 11, "bold")).grid(row=5, column=0, sticky="w", pady=8)
        self.price_entry = tk.Entry(form_frame, width=35, font=("Arial", 11),
                                     relief=tk.SOLID, borderwidth=1)
        self.price_entry.grid(row=5, column=1, padx=15, pady=8)
        
        # Row 6: Quantity
        tk.Label(form_frame, text="Quantity *", bg="white", 
                font=("Arial", 11, "bold")).grid(row=6, column=0, sticky="w", pady=8)
        self.quantity_entry = tk.Entry(form_frame, width=35, font=("Arial", 11),
                                        relief=tk.SOLID, borderwidth=1)
        self.quantity_entry.grid(row=6, column=1, padx=15, pady=8)
        
        # Row 7: Discount (Manual)
        tk.Label(form_frame, text="Discount (%)", bg="white", 
                font=("Arial", 11, "bold")).grid(row=7, column=0, sticky="w", pady=8)
        discount_frame = tk.Frame(form_frame, bg="white")
        discount_frame.grid(row=7, column=1, padx=15, pady=8, sticky="w")
        
        self.discount_entry = tk.Entry(discount_frame, width=20, font=("Arial", 11),
                                        relief=tk.SOLID, borderwidth=1)
        self.discount_entry.pack(side="left")
        
        tk.Label(discount_frame, text="% (0-100)", bg="white", 
                font=("Arial", 9), fg="#6B7280").pack(side="left", padx=(5, 0))
        
        # AI Suggestion Label
        self.suggestion_text = tk.StringVar(value="💡 AI Suggestion: Select an item to see recommendations")
        suggestion_label = tk.Label(form_frame, textvariable=self.suggestion_text, 
                                     bg="#FEF3C7", fg="#92400E", font=("Arial", 9, "italic"),
                                     padx=12, pady=8, relief=tk.SOLID, borderwidth=1)
        suggestion_label.grid(row=8, column=0, columnspan=2, pady=(15, 5), sticky="ew")
        
        # ===== BUTTON FRAME =====
        button_frame = tk.Frame(left_column, bg="#E8F0FE")
        button_frame.pack(fill="x", pady=(15, 0))
        
        # Create a stylish button container
        btn_container = tk.Frame(button_frame, bg="#E8F0FE")
        btn_container.pack()
        
        # AI Discount Button
        ai_btn = tk.Button(btn_container, text="🤖 Apply AI Discount", width=18,
                           bg="#10B981", fg="white", font=("Arial", 11, "bold"),
                           command=self.apply_ai_discount,
                           cursor="hand2", relief=tk.RAISED, borderwidth=2)
        ai_btn.grid(row=0, column=0, padx=6, pady=5)
        
        # Generate Receipt Button
        generate_btn = tk.Button(btn_container, text="📄 Generate Receipt", width=18,
                                  bg="#2563EB", fg="white", font=("Arial", 11, "bold"),
                                  command=self.generate_bill,
                                  cursor="hand2", relief=tk.RAISED, borderwidth=2)
        generate_btn.grid(row=0, column=1, padx=6, pady=5)
        
        # Clear Button
        clear_btn = tk.Button(btn_container, text="🗑️ Clear All", width=14,
                               bg="#6B7280", fg="white", font=("Arial", 11, "bold"),
                               command=self.clear_all,
                               cursor="hand2", relief=tk.RAISED, borderwidth=2)
        clear_btn.grid(row=0, column=2, padx=6, pady=5)
        
        # Exit Button
        exit_btn = tk.Button(btn_container, text="🚪 Exit", width=14,
                              bg="#DC2626", fg="white", font=("Arial", 11, "bold"),
                              command=self.exit_app,
                              cursor="hand2", relief=tk.RAISED, borderwidth=2)
        exit_btn.grid(row=0, column=3, padx=6, pady=5)
        
        # ===== RECEIPT AREA (Right Column) =====
        receipt_frame = tk.Frame(right_column, bg="white", relief=tk.RIDGE, borderwidth=2)
        receipt_frame.pack(fill="both", expand=True)
        
        receipt_title = tk.Label(receipt_frame, text="📋 Generated Receipt", 
                                  font=("Arial", 14, "bold"), bg="#1E3A8A", 
                                  fg="white", pady=8)
        receipt_title.pack(fill="x")
        
        # Receipt text box with scrollbar
        receipt_text_frame = tk.Frame(receipt_frame, bg="white")
        receipt_text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(receipt_text_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.receipt_box = tk.Text(receipt_text_frame, width=50, height=25, 
                                    font=("Consolas", 9), bg="#FAFAFA", 
                                    fg="#111827", wrap="word",
                                    yscrollcommand=scrollbar.set)
        self.receipt_box.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.receipt_box.yview)
        
        # ===== STATUS BAR =====
        status_bar = tk.Label(self.root, text="System Ready | AI Rules Active | Smart Discounts Enabled | Name cannot contain numbers", 
                               bg="#1E3A8A", fg="white", font=("Arial", 9), pady=5)
        status_bar.pack(side="bottom", fill="x")
    
    def setup_bindings(self):
        """Setup keyboard shortcuts"""
        self.name_entry.focus()
        self.root.bind('<Return>', lambda e: self.generate_bill())
        self.root.bind('<Escape>', lambda e: self.clear_all())
        self.root.bind('<Control-d>', lambda e: self.apply_ai_discount())
    
    def update_price(self, *args):
        """Auto-fill price when item is selected"""
        selected = self.item_var.get()
        if selected in PRODUCTS:
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, str(PRODUCTS[selected]["price"]))
            # Show AI suggestion
            suggestions = suggest_related_items(selected)
            self.suggestion_text.set(f"💡 AI Suggestion: Try {', '.join(suggestions)} with your {selected}!")
    
    def apply_ai_discount(self):
        """Apply automatic AI-based discount"""
        try:
            if not self.price_entry.get() or not self.quantity_entry.get():
                messagebox.showwarning("Cannot Apply", "Please enter price and quantity first!")
                return
                
            price = float(self.price_entry.get())
            quantity = int(self.quantity_entry.get())
            subtotal = price * quantity
            is_member = self.member_var.get()
            
            discount, reasons = apply_smart_discount(subtotal, quantity, is_member)
            self.discount_entry.delete(0, tk.END)
            self.discount_entry.insert(0, str(discount))
            
            if discount > 0:
                messagebox.showinfo("AI Discount Applied", 
                                   f"{discount}% discount applied!\n\nReasons:\n• " + "\n• ".join(reasons))
            else:
                messagebox.showinfo("No Discount", "No automatic discount available for this order.")
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter valid price and quantity first!")
    
    def generate_bill(self):
        """Generate complete bill with validation"""
        
        # Get values
        name = self.name_entry.get().strip()
        contact = self.contact_entry.get().strip()
        item = self.item_var.get()
        price_text = self.price_entry.get().strip()
        qty_text = self.quantity_entry.get().strip()
        discount_text = self.discount_entry.get().strip()
        is_member = self.member_var.get()
        
        # ===== VALIDATION =====
        
        # Name validation (NEW - No digits allowed)
        name_valid, name_error = validate_name(name)
        if not name_valid:
            messagebox.showerror("Validation Error", f" {name_error}")
            self.name_entry.focus()
            return
        
        # Contact validation
        if not contact:
            messagebox.showerror("Validation Error", "Contact number is required!")
            self.contact_entry.focus()
            return
        
        if not contact.isdigit():
            messagebox.showerror("Validation Error", "Contact number must contain only digits!")
            return
        
        if len(contact) < 10 or len(contact) > 13:
            messagebox.showerror("Validation Error", "Contact number must be 10-13 digits!")
            return
        
        # Item validation
        if item == "Select Item":
            messagebox.showerror("Validation Error", "Please select an item!")
            return
        
        # Price validation
        if not price_text:
            messagebox.showerror("Validation Error", "Price is required!")
            return
        
        # Quantity validation
        if not qty_text:
            messagebox.showerror("Validation Error", "Quantity is required!")
            return
        
        # Numeric validation
        try:
            price = float(price_text)
            quantity = int(qty_text)
            discount = float(discount_text) if discount_text else 0
        except ValueError:
            messagebox.showerror("Validation Error", "Price and quantity must be numbers!")
            return
        
        if price <= 0:
            messagebox.showerror("Validation Error", "Price must be greater than 0!")
            return
        
        if quantity <= 0:
            messagebox.showerror("Validation Error", "Quantity must be greater than 0!")
            return
        
        if discount < 0 or discount > 100:
            messagebox.showerror("Validation Error", "Discount must be between 0 and 100!")
            return
        
        # ===== CALCULATIONS =====
        subtotal = price * quantity
        discount_amount = subtotal * (discount / 100)
        final_total = subtotal - discount_amount
        
        # AI: Check bundle offer
        bundle_offer = get_bundle_offer(item, quantity)
        
        # ===== GENERATE RECEIPT =====
        current_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")
        receipt_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
        self.receipt_box.delete("1.0", tk.END)
        
        # Header
        self.receipt_box.insert(tk.END, "=" * 58 + "\n")
        self.receipt_box.insert(tk.END, " " * 15 + "🏪 SMART BILLING SYSTEM\n")
        self.receipt_box.insert(tk.END, " " * 12 + "AI-Powered Retail Solution\n")
        self.receipt_box.insert(tk.END, "=" * 58 + "\n")
        self.receipt_box.insert(tk.END, f"Date         : {current_time}\n")
        self.receipt_box.insert(tk.END, f"Receipt #    : {receipt_id}\n")
        self.receipt_box.insert(tk.END, "-" * 58 + "\n")
        
        # Customer Details
        self.receipt_box.insert(tk.END, f"Customer     : {name.title()}\n")
        self.receipt_box.insert(tk.END, f"Contact      : {contact}\n")
        member_status = "⭐ Premium Member ⭐" if is_member else "Regular Customer"
        self.receipt_box.insert(tk.END, f"Status       : {member_status}\n")
        self.receipt_box.insert(tk.END, "-" * 58 + "\n")
        
        # Order Details
        self.receipt_box.insert(tk.END, f"Item         : {item}\n")
        self.receipt_box.insert(tk.END, f"Category     : {PRODUCTS[item]['category'].upper()}\n")
        self.receipt_box.insert(tk.END, f"Unit Price   : Rs. {price:.2f}\n")
        self.receipt_box.insert(tk.END, f"Quantity     : {quantity}\n")
        self.receipt_box.insert(tk.END, "-" * 58 + "\n")
        
        # Financials
        self.receipt_box.insert(tk.END, f"Subtotal     : Rs. {subtotal:.2f}\n")
        self.receipt_box.insert(tk.END, f"Discount     : {discount:.0f}% (Rs. {discount_amount:.2f})\n")
        self.receipt_box.insert(tk.END, f"FINAL TOTAL  : Rs. {final_total:.2f}\n")
        self.receipt_box.insert(tk.END, "-" * 58 + "\n")
        
        # AI Offers
        if bundle_offer:
            self.receipt_box.insert(tk.END, f"🎁 {bundle_offer}\n")
            self.receipt_box.insert(tk.END, "-" * 58 + "\n")
        
        # Footer
        self.receipt_box.insert(tk.END, "\n" + " " * 18 + "Thank You! Visit Again!\n")
        self.receipt_box.insert(tk.END, " " * 12 + "Rate us 5 stars on Google\n")
        self.receipt_box.insert(tk.END, "=" * 58 + "\n")
        
        # Show success message
        messagebox.showinfo("Success", f"Bill generated successfully!\n\nCustomer: {name}\nTotal Amount: Rs. {final_total:.2f}")
    
    def clear_all(self):
        """Clear all fields"""
        self.name_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.item_var.set("Select Item")
        self.price_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.discount_entry.delete(0, tk.END)
        self.member_var.set(False)
        self.suggestion_text.set("💡 AI Suggestion: Select an item to see recommendations")
        self.receipt_box.delete("1.0", tk.END)
        self.name_entry.focus()
    
    def exit_app(self):
        """Exit with confirmation"""
        if messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit the Smart Billing System?"):
            self.root.destroy()


# ================================================================
# MAIN ENTRY POINT
# ================================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartBillingSystem(root)
    root.mainloop()
import math

class Shape:
    """Base class with abstract method calculate_area()"""
    def __init__(self):
        """Constructor for base class"""
        print("Shape constructor called")
    
    def calculate_area(self):
        """Abstract method to be implemented by subclasses"""
        raise NotImplementedError("Subclass must implement abstract method")

class Rectangle(Shape):
    def __init__(self, length, width):
        # Using super() to call parent class constructor
        super().__init__()
        self.length = length
        self.width = width
        print(f"Rectangle constructor called with length={length}, width={width}")
    
    def calculate_area(self):
        return self.length * self.width

class Square(Shape):
    def __init__(self, side):
        # Using super() to call parent class constructor
        super().__init__()
        self.side = side
        print(f"Square constructor called with side={side}")
    
    def calculate_area(self):
        return self.side ** 2

class Circle(Shape):
    def __init__(self, radius):
        # Using super() to call parent class constructor
        super().__init__()
        self.radius = radius
        print(f"Circle constructor called with radius={radius}")
    
    def calculate_area(self):
        return math.pi * (self.radius ** 2)

class Cylinder(Shape):
    def __init__(self, radius, height):
        # Using super() to call parent class constructor
        super().__init__()
        self.radius = radius
        self.height = height
        print(f"Cylinder constructor called with radius={radius}, height={height}")
    
    def calculate_area(self):
        # Surface area of cylinder: 2πr(r + h)
        return 2 * math.pi * self.radius * (self.radius + self.height)

def get_float_input(prompt):
    """Helper function to get valid float input from user"""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

# Test the classes with user input
if __name__ == "__main__":
    print("===== SHAPE AREA CALCULATOR (using super()) =====")
    print("This program calculates areas of different shapes.\n")
    print("Note: Constructor messages show inheritance using super()\n")
    
    # Menu for shape selection
    while True:
        print("\nSelect a shape to calculate area:")
        print("1. Rectangle")
        print("2. Square")
        print("3. Circle")
        print("4. Cylinder")
        print("5. Calculate all shapes")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            # Rectangle
            print("\n--- RECTANGLE ---")
            length = get_float_input("Enter length: ")
            width = get_float_input("Enter width: ")
            rectangle = Rectangle(length, width)
            print(f"\nRectangle Area ({length} × {width}): {rectangle.calculate_area():.2f}")
        
        elif choice == '2':
            # Square
            print("\n--- SQUARE ---")
            side = get_float_input("Enter side length: ")
            square = Square(side)
            print(f"\nSquare Area ({side}²): {square.calculate_area():.2f}")
        
        elif choice == '3':
            # Circle
            print("\n--- CIRCLE ---")
            radius = get_float_input("Enter radius: ")
            circle = Circle(radius)
            print(f"\nCircle Area (π × {radius}²): {circle.calculate_area():.2f}")
        
        elif choice == '4':
            # Cylinder
            print("\n--- CYLINDER ---")
            radius = get_float_input("Enter radius: ")
            height = get_float_input("Enter height: ")
            cylinder = Cylinder(radius, height)
            print(f"\nCylinder Surface Area (2π×{radius}×({radius}+{height})): {cylinder.calculate_area():.2f}")
        
        elif choice == '5':
            # Calculate all shapes
            print("\n--- CALCULATE ALL SHAPES ---")
            
            # Get inputs for all shapes
            print("\nEnter dimensions for each shape:")
            
            # Rectangle
            length = get_float_input("Rectangle - Enter length: ")
            width = get_float_input("Rectangle - Enter width: ")
            rectangle = Rectangle(length, width)
            
            # Square
            side = get_float_input("Square - Enter side length: ")
            square = Square(side)
            
            # Circle
            radius_circle = get_float_input("Circle - Enter radius: ")
            circle = Circle(radius_circle)
            
            # Cylinder
            radius_cylinder = get_float_input("Cylinder - Enter radius: ")
            height_cylinder = get_float_input("Cylinder - Enter height: ")
            cylinder = Cylinder(radius_cylinder, height_cylinder)
            
            # Display all results
            print("\n" + "="*40)
            print("ALL SHAPE AREAS:")
            print("="*40)
            print(f"Rectangle ({length} × {width}): {rectangle.calculate_area():.2f}")
            print(f"Square ({side}²): {square.calculate_area():.2f}")
            print(f"Circle (π × {radius_circle}²): {circle.calculate_area():.2f}")
            print(f"Cylinder (2π×{radius_cylinder}×({radius_cylinder}+{height_cylinder})): {cylinder.calculate_area():.2f}")
            print("="*40)
        
        elif choice == '6':
            print("\nThank you for using the Shape Area Calculator. Goodbye!")
            break
        
        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.")
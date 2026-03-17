# Lambda expression to calculate square of a given number
square = lambda x: x ** 2

if __name__ == "__main__":
    print("===== SQUARE CALCULATOR =====")
    
    try:
        num = float(input("Enter a number: "))
        print(f"Square of {num} = {square(num)}")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

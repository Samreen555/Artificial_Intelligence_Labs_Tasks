def fibonacci_generator(n):
    """
    Generator function that returns Fibonacci sequence up to a given limit n
    Args:
        n: The limit (generate Fibonacci numbers less than or equal to n)
    """
    a, b = 0, 1
    while a <= n:
        yield a
        a, b = b, a + b

# Simple user input
if __name__ == "__main__":
    print("===== FIBONACCI SEQUENCE GENERATOR =====")
    
    # Get limit from user
    try:
        limit = int(input("Enter the limit for Fibonacci sequence: "))
        
        if limit < 0:
            print("Please enter a non-negative number.")
        else:
            print(f"\nFibonacci sequence up to {limit}:")
            
            # Generate and print the sequence
            fib_numbers = []
            for num in fibonacci_generator(limit):
                fib_numbers.append(num)
                print(num, end=" ")
            
            print(f"\n\nTotal numbers generated: {len(fib_numbers)}")
            
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

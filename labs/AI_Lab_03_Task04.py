import random

def random_number_generator():
    """Generator function that yields 5 random numbers between 1 and 100"""
    for i in range(5):
        yield random.randint(1, 100)

# Test the generator function with a for loop
if __name__ == "__main__":
    print("5 Random Numbers between 1 and 100:")
    
    # Using for loop to get values from generator
    for i, num in enumerate(random_number_generator(), 1):
        print(f"Random number {i}: {num}")
    
    # Alternative demonstration showing generator can be used again
    print("\nAnother set of random numbers:")
    for i, num in enumerate(random_number_generator(), 1):
        print(f"Random number {i}: {num}")
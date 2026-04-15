"""
Lab 08: File Handling - Reading Text Files
This program demonstrates how to read a text file in Python
"""

print("="*60)
print("READING TEXT FILE DEMONSTRATION")
print("="*60)

file_name = "sample.txt"

try:
    # Method 1: Read entire file at once
    with open(file_name, 'r') as file:
        content = file.read()
        print("\nMethod 1 - Read entire file:")
        print("-"*40)
        print(content)
    
    # Method 2: Read line by line
    with open(file_name, 'r') as file:
        print("\nMethod 2 - Read line by line:")
        print("-"*40)
        for line_num, line in enumerate(file, 1):
            print(f"Line {line_num}: {line.strip()}")
    
    # Method 3: Read all lines into a list
    with open(file_name, 'r') as file:
        lines = file.readlines()
        print(f"\nMethod 3 - Read all lines as list:")
        print("-"*40)
        print(f"Total lines: {len(lines)}")
        print(f"Lines as list: {lines}")
        
except FileNotFoundError:
    print(f"\n Error: '{file_name}' not found!")
    print("Creating sample.txt file...")
    
    # Create sample file
    with open(file_name, 'w') as file:
        file.write("Hello World!\n")
        file.write("This is a sample text file.\n")
        file.write("Python file handling is easy to learn.\n")
        file.write("This is line 4.\n")
        file.write("End of file.")
    
    print(f"✓ '{file_name}' has been created. Run the program again!")

print("\n" + "="*60)
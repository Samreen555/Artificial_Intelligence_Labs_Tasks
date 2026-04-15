"""
Lab 08: File Handling - Writing to Text Files
This program demonstrates different modes of writing to files
"""

print("="*60)
print("WRITING TO TEXT FILES DEMONSTRATION")
print("="*60)

# Example 1: Write mode ('w') - Overwrites existing content
print("\n1. WRITE MODE ('w') - Overwrites file")
print("-"*40)
with open('output_write.txt', 'w') as file:
    file.write("This is line 1\n")
    file.write("This is line 2\n")
    file.write("This file was created using 'w' mode\n")
print(" Written to 'output_write.txt'")

# Example 2: Append mode ('a') - Adds to existing content
print("\n2. APPEND MODE ('a') - Adds to file")
print("-"*40)
with open('output_append.txt', 'a') as file:
    file.write("First entry\n")
    file.write("Second entry\n")
print(" Appended to 'output_append.txt'")

# Add more content to the same file
with open('output_append.txt', 'a') as file:
    file.write("Third entry - added later\n")
print(" Appended more content to 'output_append.txt'")

# Example 3: Create mode ('x') - Creates new file, errors if exists
print("\n3. CREATE MODE ('x') - Creates new file only")
print("-"*40)
try:
    with open('new_file.txt', 'x') as file:
        file.write("This is a brand new file!\n")
    print(" Created 'new_file.txt'")
except FileExistsError:
    print(" 'new_file.txt' already exists!")

# Example 4: Writing multiple lines
print("\n4. WRITING MULTIPLE LINES")
print("-"*40)
lines = ["Line 1: Student Name\n", "Line 2: Student ID\n", "Line 3: Course\n"]
with open('multiple_lines.txt', 'w') as file:
    file.writelines(lines)
print(" Written multiple lines to 'multiple_lines.txt'")

# Read and display the files
print("\n5. VERIFYING FILE CONTENTS")
print("-"*40)
for filename in ['output_write.txt', 'output_append.txt', 'multiple_lines.txt']:
    print(f"\nContents of '{filename}':")
    try:
        with open(filename, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print("File not found")

print("\n" + "="*60)
"""
Lab 08: Reading CSV Files using built-in csv module
"""

import csv

print("="*60)
print("READING CSV FILES WITH BUILT-IN CSV MODULE")
print("="*60)

filename = 'students.csv'

try:
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        
        # Read header
        header = next(csv_reader)
        print(f"\nHeaders: {header}")
        print("-"*60)
        
        # Read and display data
        print(f"{'Name':<25} {'Marks':<10} {'Email':<30}")
        print("-"*60)
        
        for row in csv_reader:
            if len(row) >= 3:
                print(f"{row[0]:<25} {row[1]:<10} {row[2]:<30}")
                
except FileNotFoundError:
    print(f" '{filename}' not found!")
    print("Please run the main program to generate sample data.")

print("\n" + "="*60)
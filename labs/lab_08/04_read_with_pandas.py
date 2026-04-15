"""
Lab 08: Reading Files with Pandas
This program demonstrates reading text and CSV files using pandas
"""

import pandas as pd

print("="*70)
print("READING FILES WITH PANDAS")
print("="*70)

# Part 1: Read text file with pandas
print("\n1. READING TEXT FILE WITH PANDAS:")
print("-"*70)

try:
    # Read text file as CSV with a single column
    text_df = pd.read_csv('sample.txt', header=None, names=['Content'])
    print("Text file contents:")
    print(text_df)
    print(f"\nNumber of lines: {len(text_df)}")
    
except FileNotFoundError:
    print(" sample.txt not found!")
    print("Creating sample.txt...")
    with open('sample.txt', 'w') as f:
        f.write("Line 1: Hello World\n")
        f.write("Line 2: Python is awesome\n")
        f.write("Line 3: Pandas makes data easy\n")
    print(" sample.txt created. Run again!")

# Part 2: Read CSV file with pandas
print("\n2. READING CSV FILE WITH PANDAS:")
print("-"*70)

try:
    # Read CSV file
    df = pd.read_csv('students.csv')
    
    print("First 5 rows of the dataset:")
    print(df.head())
    
    print("\nDataFrame Information:")
    print("-"*40)
    print(f"Shape: {df.shape} (rows, columns)")
    print(f"Columns: {list(df.columns)}")
    
    print("\nBasic Statistics:")
    print("-"*40)
    print(df['Marks'].describe())
    
    print("\nData Types:")
    print("-"*40)
    print(df.dtypes)
    
    print("\nStudents with marks > 12:")
    print("-"*40)
    high_performers = df[df['Marks'] > 12]
    print(high_performers[['Name', 'Marks']])
    
    print("\nSort by marks (descending):")
    print("-"*40)
    sorted_df = df.sort_values('Marks', ascending=False)
    print(sorted_df[['Name', 'Marks']])
    
except FileNotFoundError:
    print(" students.csv not found!")
    print("Please run the main program first.")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*70)
print("Pandas file reading complete!")
print("="*70)
"""
Lab 08: File Handling & Regular Expressions - Case Study
Student Performance Analyzer with Email Validation
Author: [Your Name]
Date: [Current Date]

This program reads student data, identifies underperforming students,
validates emails using regex, and generates a comprehensive report.
"""

import csv
import re
import pandas as pd
from datetime import datetime

def validate_email(email):
    """
    Validate email format using regular expressions
    
    Pattern explanation:
    ^[a-zA-Z0-9._%+-]+  - Username (letters, numbers, dots, underscores, etc.)
    @                    - Required @ symbol
    [a-zA-Z0-9.-]+      - Domain name
    \.                  - Required dot
    [a-zA-Z]{2,}$       - Top-level domain (minimum 2 letters)
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, str(email).strip()))

def create_sample_data():
    """Create sample student data CSV file"""
    sample_data = {
        'Name': [
            'Samreen', 'Smith', 'Umama', 'Tayyaba',
            'Zain', 'Rehan', 'Ali', 'ahmed',
            'Cen', 'Jack', 'Kevin', 'Lisa',
            'Mike', 'Nina', 'Oscar'
        ],
        'Marks': [
            15.5, 9.0, 14.0, 11.5, 16.5, 8.0, 13.5, 18.0,
            10.5, 12.5, 7.5, 14.5, 9.5, 17.0, 11.0
        ],
        'Email': [
            'Samreen@email.com', 'smith@invalid', 'Umama@university.edu',
            'Tayyaba@college.org', 'zain@domain', 'rehan@school.edu',
            'ali@wrong', 'ahmed@student.uni.edu', 'chen@academy.com',
            'jack@email.com', 'kevin.', 'lisa@valid.edu',
            'mike@boxing.com', 'nina@music.org', 'oscar@literature.edu'
        ]
    }
    
    df = pd.DataFrame(sample_data)
    df.to_csv('students.csv', index=False)
    print("Sample 'students.csv' created with 15 student records!")
    return df

def analyze_with_pandas(input_file='students.csv', passing_marks=12):
    """
    Analyze student data using pandas
    """
    print("\n" + "="*80)
    print(" "*25 + "STUDENT PERFORMANCE ANALYZER")
    print("="*80)
    
    try:
        # Read CSV using pandas
        print(f"\nReading data from '{input_file}'...")
        df = pd.read_csv(input_file)
        
        print(f"\nDataset Overview:")
        print("-"*80)
        print(f"Total students: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        print(f"\nFirst 5 records:")
        print(df.head())
        
        # Add validation columns
        print("\nAnalyzing data...")
        df['Email_Valid'] = df['Email'].apply(validate_email)
        df['Underperforming'] = df['Marks'] < passing_marks
        
        # Display analysis
        print("-"*80)
        print(f"{'Name':<20} {'Marks':<8} {'Performance':<18} {'Email Status':<15}")
        print("-"*80)
        
        for _, row in df.iterrows():
            perf_status = "UNDER" if row['Underperforming'] else "✓ OK"
            email_status = "Valid" if row['Email_Valid'] else "✗ Invalid"
            print(f"{row['Name']:<20} {row['Marks']:<8.1f} {perf_status:<18} {email_status:<15}")
        
        # Statistics
        underperforming = df[df['Underperforming']]
        invalid_emails = df[~df['Email_Valid']]
        
        print("\n" + "="*80)
        print("ANALYSIS SUMMARY")
        print("="*80)
        print(f"Total Students:                {len(df)}")
        print(f"Average Marks:                 {df['Marks'].mean():.2f}")
        print(f"Highest Marks:                 {df['Marks'].max():.2f}")
        print(f"Lowest Marks:                  {df['Marks'].min():.2f}")
        print(f"Underperforming Students:      {len(underperforming)} ({len(underperforming)/len(df)*100:.1f}%)")
        print(f"Invalid Email Addresses:       {len(invalid_emails)} ({len(invalid_emails)/len(df)*100:.1f}%)")
        
        # Generate Report
        generate_report(df, underperforming, invalid_emails, passing_marks)
        
        # Display underperforming students
        if len(underperforming) > 0:
            print("\nUNDERPERFORMING STUDENTS (Marks < 12):")
            print("-"*80)
            for _, student in underperforming.iterrows():
                print(f"  • {student['Name']:<20} Marks: {student['Marks']:.1f}")
        
        # Display invalid emails
        if len(invalid_emails) > 0:
            print("\nSTUDENTS WITH INVALID EMAILS:")
            print("-"*80)
            for _, student in invalid_emails.iterrows():
                print(f"  • {student['Name']:<20} Email: {student['Email']}")
        
        return df
        
    except FileNotFoundError:
        print(f"'{input_file}' not found!")
        print("Creating sample data...")
        df = create_sample_data()
        return analyze_with_pandas(input_file, passing_marks)
    except Exception as e:
        print(f" Error: {e}")
        return None

def generate_report(df, underperforming, invalid_emails, passing_marks):
    """Generate comprehensive report file"""
    
    report_file = 'report.txt'
    
    with open(report_file, 'w', encoding='utf-8') as report:
        # Header
        report.write("="*85 + "\n")
        report.write(" "*30 + "STUDENT ANALYSIS REPORT\n")
        report.write("="*85 + "\n")
        report.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.write(f"Passing Marks Threshold: {passing_marks}\n")
        report.write("="*85 + "\n\n")
        
        # Executive Summary
        report.write("EXECUTIVE SUMMARY\n")
        report.write("-"*85 + "\n")
        report.write(f"Total Students Analyzed:        {len(df)}\n")
        report.write(f"Average Marks:                  {df['Marks'].mean():.2f}\n")
        report.write(f"Highest Marks:                  {df['Marks'].max():.2f}\n")
        report.write(f"Lowest Marks:                   {df['Marks'].min():.2f}\n")
        report.write(f"Students Below Passing Marks:   {len(underperforming)} ({len(underperforming)/len(df)*100:.1f}%)\n")
        report.write(f"Students with Invalid Emails:   {len(invalid_emails)} ({len(invalid_emails)/len(df)*100:.1f}%)\n")
        report.write("\n")
        
        # Underperforming Students
        report.write("="*85 + "\n")
        report.write(f"UNDERPERFORMING STUDENTS (Marks < {passing_marks})\n")
        report.write("="*85 + "\n")
        report.write(f"{'Name':<25} {'Marks':<10} {'Email Valid?':<15} {'Email Address':<35}\n")
        report.write("-"*85 + "\n")
        
        if len(underperforming) > 0:
            for _, student in underperforming.iterrows():
                email_status = "Yes" if student['Email_Valid'] else "No"
                report.write(f"{student['Name']:<25} {student['Marks']:<10.1f} {email_status:<15} {student['Email']:<35}\n")
        else:
            report.write("✓ No underperforming students found.\n")
        report.write("\n")
        
        # Invalid Emails
        report.write("="*85 + "\n")
        report.write("STUDENTS WITH INVALID EMAIL ADDRESSES\n")
        report.write("="*85 + "\n")
        report.write(f"{'Name':<25} {'Marks':<10} {'Email Address':<50}\n")
        report.write("-"*85 + "\n")
        
        if len(invalid_emails) > 0:
            for _, student in invalid_emails.iterrows():
                report.write(f"{student['Name']:<25} {student['Marks']:<10.1f} {student['Email']:<50}\n")
        else:
            report.write("All email addresses are valid.\n")
        report.write("\n")
        
        # Complete Student List (Sorted by Marks)
        report.write("="*85 + "\n")
        report.write("COMPLETE STUDENT LIST (Sorted by Marks)\n")
        report.write("="*85 + "\n")
        report.write(f"{'Rank':<5} {'Name':<25} {'Marks':<10} {'Performance':<20} {'Email Status':<15}\n")
        report.write("-"*85 + "\n")
        
        sorted_df = df.sort_values('Marks', ascending=False)
        for rank, (_, student) in enumerate(sorted_df.iterrows(), 1):
            performance = "Underperforming" if student['Underperforming'] else "Satisfactory"
            email_status = "Valid" if student['Email_Valid'] else "Invalid"
            report.write(f"{rank:<5} {student['Name']:<25} {student['Marks']:<10.1f} {performance:<20} {email_status:<15}\n")
        
        report.write("\n")
        
        # Recommendations
        report.write("="*85 + "\n")
        report.write("RECOMMENDATIONS\n")
        report.write("="*85 + "\n")
        
        if len(underperforming) > 0:
            report.write(f"1. Provide academic support to {len(underperforming)} underperforming students\n")
            report.write("2. Schedule tutoring sessions for struggling students\n")
        else:
            report.write("1. All students are performing satisfactorily\n")
        
        if len(invalid_emails) > 0:
            report.write(f"3. Contact {len(invalid_emails)} students to update their email addresses\n")
            report.write("4. Verify email format before sending official communications\n")
        else:
            report.write("2. All email addresses are properly formatted\n")
        
        report.write("\n" + "="*85 + "\n")
        report.write("END OF REPORT\n")
        report.write("="*85 + "\n")
    
    print(f"\nReport generated successfully: '{report_file}'")

def main():
    """Main function to run the analysis"""
    print("\n" + "="*80)
    print(" "*20 + "UNIVERSITY STUDENT SUPPORT OFFICE")
    print(" "*20 + "Automated Student Record Analyzer")
    print("="*80)
    
    # Run analysis
    df = analyze_with_pandas('students.csv', passing_marks=12)
    
    if df is not None:
        print("\n" + "="*80)
        print("ANALYSIS COMPLETE!")
        print("="*80)
        print("\nFiles generated:")
        print("  • report.txt - Comprehensive analysis report")
        print("  • students.csv - Student data file")
        print("\nLogic Used:")
        print("  • File Handling: CSV reading/writing operations")
        print("  • Regex: Email validation pattern matching")
        print("  • Pandas: Data analysis and manipulation")
        print("="*80)

if __name__ == "__main__":
    main()
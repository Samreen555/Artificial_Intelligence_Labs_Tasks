def calculate_average_marks():
    # Input: Total number of students
    N = int(input("Enter total number of students: "))
    # Input: Column headers (convert to uppercase to avoid case issues)
    columns = input("Enter column names separated by space: ").upper().split()
    # Find index of MARKS column
    if "MARKS" not in columns:
        print("Error: MARKS column not found.")
        return
    marks_index = columns.index("MARKS")
    total_marks = 0.0

    # Input: Student records
    print("Enter student data:")
    for _ in range(N):
        data = input().split()
        total_marks += float(data[marks_index])
    # Calculate average
    average = total_marks / N
    # Output formatted to 2 decimal places
    print("Average Marks: {:.2f}".format(average))
# Run the function
calculate_average_marks()

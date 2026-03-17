print("Welcome to Bahria Grading System:..")
x=int(input("Enter The Marks To Calculate The Grades:"))

if x>=85 and x<=100:
 print("Grade is A")
elif x>=80 and x<=84:
 print("Grade is A-")
elif x>=75 and x<=79:
 print("Grade is B+")
elif x>=71 and x<=74:
 print("Grade is B")
elif x>=68 and x<=70:
 print("Grade is B-")
elif x>=64 and x<=67:
 print("Grade is C+")
elif x>=60 and x<=63:
 print("Grade is C")
elif x>=57 and x<=59:
 print("Grade is C-")
elif x>=53 and x<=56:
 print("Grade is D+")
elif x>=50 and x<=52:
 print("Grade is D")
elif x>=0 and x<=49:
 print("Grade is F")
else:
 print("Invalid marks....")

# Lambda expression to calculate the length of a passed string
string_length = lambda s: len(s)

# Simple user input
if __name__ == "__main__":
    print("===== STRING LENGTH CALCULATOR =====")
    
    # Get input from user
    user_input = input("Enter a string: ")
    
    # Calculate and display length
    print(f"Length of '{user_input}' = {string_length(user_input)}")

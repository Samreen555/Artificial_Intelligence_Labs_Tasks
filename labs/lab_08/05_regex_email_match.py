"""
Lab 08: Regular Expressions - Email Validation
"""

import re

def validate_email(email):
    """
    Validate email format using regex
    Pattern: username@domain.extension
    """
    # Comprehensive email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True, "Valid"
    else:
        return False, "Invalid"

print("="*70)
print("EMAIL VALIDATION USING REGULAR EXPRESSIONS")
print("="*70)

# Test cases
test_emails = [
    "john.doe@example.com",
    "invalid-email",
    "student@university.edu",
    "no@domain",
    "user@company.co.uk",
    "@missingusername.com",
    "missing@domain.",
    "spaces in@email.com",
    "valid_email123@test-domain.com",
    "user.name+tag@example.co.in"
]

print("\nTesting various email formats:")
print("-"*70)
print(f"{'Email Address':<40} {'Status':<10} {'Valid?':<10}")
print("-"*70)

valid_count = 0
for email in test_emails:
    is_valid, status = validate_email(email)
    if is_valid:
        valid_count += 1
        symbol = "✓"
    else:
        symbol = "✗"
    print(f"{email:<40} {status:<10} {symbol:<10}")

print("-"*70)
print(f"\nSummary: {valid_count}/{len(test_emails)} emails are valid")

# Interactive email validation
print("\n" + "="*70)
print("INTERACTIVE EMAIL VALIDATION")
print("="*70)

while True:
    email = input("\nEnter an email to validate (or 'quit' to exit): ").strip()
    
    if email.lower() == 'quit':
        break
    
    is_valid, status = validate_email(email)
    if is_valid:
        print(f"✓ '{email}' is a VALID email address")
        
        # Extract parts using regex
        match = re.match(r'^([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,})$', email)
        if match:
            username = match.group(1)
            domain = match.group(2)
            tld = match.group(3)
            print(f"  Username: {username}")
            print(f"  Domain: {domain}")
            print(f"  TLD: {tld}")
    else:
        print(f"✗ '{email}' is INVALID")

print("\nProgram ended.")
"""
Lab 08: Regular Expressions - Finding Patterns in Text
"""

import re

print("="*70)
print("PATTERN MATCHING WITH REGULAR EXPRESSIONS")
print("="*70)

# Sample text with names
text = """The students registered for the course are:
Alice Johnson, Bob Smith, and Charlie Brown.
Additional students include Diana Prince, Edward Norton,
and Fiona Gallagher. The instructor is Dr. Sarah Williams."""

print("\nOriginal Text:")
print("-"*70)
print(text)

# Pattern 1: Find all capitalized words (potential names)
print("\n1. FINDING ALL CAPITALIZED WORDS:")
print("-"*70)
pattern1 = r'[A-Z][a-z]+'
capitalized_words = re.findall(pattern1, text)
print(f"Found {len(capitalized_words)} capitalized words:")
print(capitalized_words)

# Pattern 2: Find full names (First Last)
print("\n2. FINDING FULL NAMES (First Last):")
print("-"*70)
pattern2 = r'[A-Z][a-z]+ [A-Z][a-z]+'
full_names = re.findall(pattern2, text)
print(f"Found {len(full_names)} full names:")
for name in full_names:
    print(f"  ✓ {name}")

# Pattern 3: Find names with titles (Dr., Mr., Mrs., etc.)
print("\n3. FINDING NAMES WITH TITLES:")
print("-"*70)
pattern3 = r'(Dr|Mr|Mrs|Ms|Prof)\. [A-Z][a-z]+ [A-Z][a-z]+'
titled_names = re.findall(pattern3, text)
if titled_names:
    for title, first, last in re.findall(r'(Dr|Mr|Mrs|Ms|Prof)\. ([A-Z][a-z]+) ([A-Z][a-z]+)', text):
        print(f"  ✓ {title}. {first} {last}")
else:
    print("  No titled names found in this text")

# Pattern 4: Search for specific name
print("\n4. SEARCHING FOR SPECIFIC NAMES:")
print("-"*70)
search_names = ["Alice", "John", "Sarah", "Michael"]
for name in search_names:
    if re.search(r'\b' + name + r'\b', text):
        print(f"  ✓ '{name}' found in text")
    else:
        print(f"  ✗ '{name}' not found in text")

# Pattern 5: Split text by punctuation
print("\n5. SPLITTING TEXT:")
print("-"*70)
sentences = re.split(r'[.,]', text)
for i, sentence in enumerate(sentences, 1):
    if sentence.strip():
        print(f"  Sentence {i}: {sentence.strip()}")

# Pattern 6: Replace patterns
print("\n6. REPLACING PATTERNS:")
print("-"*70)
# Replace all names with [STUDENT]
anonymized = re.sub(r'[A-Z][a-z]+ [A-Z][a-z]+', '[STUDENT NAME]', text)
print("Anonymized text:")
print(anonymized)

print("\n" + "="*70)
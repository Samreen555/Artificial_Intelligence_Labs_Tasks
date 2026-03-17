def count_characters():
    input_str = input("Enter the string: ")

    char_count = {}

    # Count occurrences
    for ch in input_str:
        if ch in char_count:
            char_count[ch] += 1
        else:
            char_count[ch] = 1

    # Print in required format
    output = []
    for ch in char_count:
        output.append(f"{ch}:{char_count[ch]}")

    print(", ".join(output))


count_characters()

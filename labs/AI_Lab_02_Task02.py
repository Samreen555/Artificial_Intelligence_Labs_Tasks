def count_substring_occurrences():
    string = input("Enter the main string: ")
    substring = input("Enter the substring: ")

    count = 0
    sub_len = len(substring)

    for i in range(len(string) - sub_len + 1):
        if string[i:i + sub_len] == substring:
            count += 1

    print("Total occurrences:", count)


count_substring_occurrences()

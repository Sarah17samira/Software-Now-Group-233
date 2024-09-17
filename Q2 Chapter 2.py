def process_string(s):
    numbers = ''.join([char for char in s if char.isdigit()])
    letters = ''.join([char for char in s if char.isalpha()])

    even_numbers_ascii = [ord(chr(int(num))) for num in numbers if int(num) % 2 == 0]
    uppercase_letters_ascii = [ord(letter) for letter in letters if letter.isupper()]

    print(f"Even numbers converted to ASCII: {even_numbers_ascii}")
    print(f"Uppercase letters converted to ASCII: {uppercase_letters_ascii}")

# Example usage
s = "56aAww1984sktr235270aYmn145ss785fsq31D0"
process_string(s)

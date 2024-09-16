# Encrypt function as given in the image
def encrypt(text, key):
    encrypted_text = ""
    for char in text:
        if char.isalpha():  # Only shift letters
            shifted = ord(char) + key  # Shift by the key value
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            encrypted_text += chr(shifted)  # Convert back to character
        else:
            encrypted_text += char  # Keep non-alphabet characters unchanged
    return encrypted_text

# Decryption function (inverse of encryption)
def decrypt(text, key):
    return encrypt(text, -key)  # Reverses encryption by using negative key

# Now let's assume we know the key to decrypt the code
key = 13  

# Encrypted code that we need to decrypt
encrypted_code = """
tybony_inenvoyr = 100
zl_frg = {'xrl1': 'inyhr1', 'xrl2': 'inyhr2', 'xrl3': 'inyhr3'}
qrs cebprrqf_ahzoref():
    tybony_inenvoyr = 5
    ahzoref = [1, 2, 3, 4, 5]
ybpngv_inenvoyr = 8:
vs ybpngv_inenvoyr % 2 == 0:
    ahzoref.ercynpr(ybpngv_inenvoyr)
    ybpngv_inenvoyr -= 1
erghea ahzoref
zl_frg = [8, 2, 3, 4, 5, 5, 3, 2, 1]
erfhvg = cebprrqf_ahzoref(ahzoref=zl_frg)
grz ybpngv_inevovr += 10
zl_qvpg['xrl4'] = ybpngv_inenvoyr
"""

# Decrypt the code
decrypted_code = decrypt(encrypted_code, key)
print("Decrypted code:\n")
print(decrypted_code)


# Decrypted code with corrections:

# Declare a global variable
global_variable = 100

# Initialize a dictionary
my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}

# Define a function to process numbers
def process_numbers():
    global global_variable  # Use the global variable
    global_variable = 5
    numbers = [1, 2, 3, 4, 5]
    return numbers  # Return the list of numbers

# Another global variable
valid_variable = 8

# Check if the valid_variable is even and append to the list
if valid_variable % 2 == 0:
    numbers = process_numbers()
    numbers.append(valid_variable)
    valid_variable -= 1  # Decrease the global variable

# Create a list of numbers
my_list = [8, 2, 3, 4, 5, 5, 3, 2, 1]

# Process the list using the process_numbers function
result = process_numbers()

# Increment global variable by 10
global_variable += 10

# Add a new key-value pair to the dictionary
my_dict['key4'] = global_variable

# Print final values of the variables
print(global_variable)  
print(my_dict) 
print(my_list)  


# Example of the loop in the encrypted section

total = 0
for i in range(5):
    for j in range(3):
        if i + j == 5:
            total += i + j
        else:
            total -= i - j

# Second loop
counter = 0
while counter < 5:
    if total < 13:
        total += 1
    elif total > 13:
        total -= 1
    else:
        break  
    counter += 2

print("Final total:", total) 


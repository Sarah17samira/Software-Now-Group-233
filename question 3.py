
def encrypt(text, key):
    encrypted_text = ""
    for char in text:
        if char.isalpha(): 
            shifted = ord(char) + key 
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
            encrypted_text += chr(shifted)  
        else:
            encrypted_text += char  
    return encrypted_text

def decrypt(text, key):
    return encrypt(text, -key)  

key = 13  

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

decrypted_code = decrypt(encrypted_code, key)
print("Decrypted code:\n")
print(decrypted_code)

global_variable = 100

my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}

def process_numbers():
    global global_variable 
    global_variable = 5
    numbers = [1, 2, 3, 4, 5]
    return numbers 
valid_variable = 8

if valid_variable % 2 == 0:
    numbers = process_numbers()
    numbers.append(valid_variable)
    valid_variable -= 1 

my_list = [8, 2, 3, 4, 5, 5, 3, 2, 1]

result = process_numbers()

global_variable += 10

my_dict['key4'] = global_variable

print(global_variable)  
print(my_dict) 
print(my_list)  



total = 0
for i in range(5):
    for j in range(3):
        if i + j == 5:
            total += i + j
        else:
            total -= i - j

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


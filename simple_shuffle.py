import random
import string

char_list = list(" " + string.ascii_letters + string.digits)
key_list = char_list.copy()
random.shuffle(key_list)

orj_text = input("enter the text")
cipher_text = ""

#encrypting

for i in orj_text:
    index_val = char_list.index(i)
    cipher_text += key_list[index_val]
print(cipher_text)
#decrypting
decipher_text = ""
for i in cipher_text:
    index_val = key_list.index(i)
    decipher_text += char_list[index_val]
print(decipher_text)
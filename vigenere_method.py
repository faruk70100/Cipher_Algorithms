import string
import numpy as np

vigenere_list = list(
    " " + string.digits + string.ascii_letters + "Ü" + "ü" + "İ" + "ı" + "Ö" + "ö" + "Ş" + "ş" + "Ç" + "ç" + "Ğ" + "ğ")

# her satırda bir üst satırı kayıdırılmasını sağlar
vigenere_list1 = [vigenere_list[i:] + vigenere_list[:i] for i in range(len(vigenere_list))]

# bu listeyi matrix haline getirdik
vigenere_matrix = np.array(vigenere_list1)


def key_word_maker(orj_key_word, orj_text):
    key_word = ""
    if len(orj_key_word) != len(orj_text):
        count = 0
        while count != len(orj_text):
            key_word = key_word + orj_key_word[count % len(orj_key_word)]
            count += 1
    return list(key_word)
def vigenere_encrption(orj_text, orj_key_word):
    global vigenere_matrix
    global vigenere_list
    # kilit kelimeyi metin ile aynı uzunluğa getirildi
    key_word = key_word_maker(orj_key_word, orj_text)

    # encryption
    encrypted_text = ""
    vigenere_list = list(vigenere_list)
    count = 0
    while count < len(orj_text):
        encrypted_text = encrypted_text + vigenere_matrix[
            vigenere_list.index(orj_text[count]), vigenere_list.index(key_word[count])]
        count += 1
    return encrypted_text

def vigenere_decryption(crypt_text, orj_key_word):
    global vigenere_matrix
    global vigenere_list
    count = 0
    decrypted_text = ""

    key_word = key_word_maker(orj_key_word, crypt_text)

    while count < len(key_word):
        crypted_row = list(vigenere_matrix[vigenere_list.index(key_word[count]), :])
        index_val = crypted_row.index(crypt_text[count])
        decrypted_text = decrypted_text + vigenere_list[index_val]
        count += 1
    return decrypted_text

if __name__ == "__main__":
    # encryption
    orj_text = input("enter the message")
    orj_text = list(orj_text)
    orj_key_word = input("enter the key word")
    orj_key_word = list(orj_key_word)
    vigenere_encrption(orj_text, orj_key_word)

    #decryption
    crypt_text = input("enter the cryted message")
    crypt_text = list(crypt_text)
    key_word = input("enter the keyword")
    vigenere_decryption(crypt_text, key_word)

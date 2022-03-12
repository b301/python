"""
__version__ = "3.9.6"
__author__ = "0xb301"
"""

import string


#Global Dictionary
ALPHABET_VALUES = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10,
    'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20,
    'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25
}

NUMERIC_TO_ALPHABET = {value: key for key, value in ALPHABET_VALUES.items()}
ROT13 = {
    'a': 'n', 'n': 'a', 'A': 'N', 'N': 'A', 'b': 'o', 'o': 'b', 'B': 'O', 'O': 'B', 'c': 'p',
    'p': 'c', 'C': 'P', '': 'C', 'd': 'q', 'q': 'd', 'D': 'Q', 'Q': 'D', 'e': 'r', 'r': 'e',
    'E': 'R', 'R': 'E', 'f': 's', 's': 'f', 'F': 'S', 'S': 'F', 'g': 't', 't': 'g', 'G': 'T',
    'T': 'G', 'h': 'u', 'u': 'h', 'H': 'U', 'U': 'H', 'i': 'v', 'v': 'i', 'I': 'V', 'V': 'I',
    'j': 'w', 'w': 'j', 'J': 'W', 'W': 'J', 'k': 'x', 'x': 'k', 'K': 'X', 'X': 'K', 'l': 'y',
    'y': 'l', 'L': 'Y', 'Y': 'L', 'm': 'z', 'z': 'm', 'M': 'Z', 'Z': 'M', '0': '5', '5': '0',
    '1': '6', '6': '1', '2': '7', '7': '2', '3': '8', '8': '3', '4': '9', '9': '4'
}

MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.",
    "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.",
    "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-",
    "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--..", "1": ".----",
    "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----.", "0": "-----", "&": ".-...", "@": ".--.-.",
    ":": "---...", ",": "--..--", ".": ".-.-.-", "'": ".----.", '"': ".-..-.",
    "?": "..--..", "/": "-..-.", "=": "-...-", "+": ".-.-.", "-": "-....-",
    "(": "-.--.", ")": "-.--.-", "!": "-.-.--", " ": "/"
}
REMORSE = {value: key for key, value in MORSE.items()}

BASE10NUMBERS = [0,1,2,3,4,5,6,7,8,9]

#Functions
def vigenere_encoder(message: str, key: str) -> str:
    """
    Encodes a plaintext into a Vigerene-encoded string given a key

    >> lib.cipher.vigenere_encoder("HELLO WORLD", "GOLD")

    `NSWOU KZURR`
    """
    key = key.upper()
    message = message.upper()

    ciphertext = ""
    j = 0
    #print(ALPHABET_VALUES.keys())
    for i in range(len(message)):
        #print(message[i], message[i] in ALPHABET_VALUES.keys())
        if message[i] in ALPHABET_VALUES.keys():
            letter = NUMERIC_TO_ALPHABET[(ALPHABET_VALUES[message[i]] + ALPHABET_VALUES[key[j % len(key)]]) % 26]
            #print(f"{message[i]}:{ALPHABET_VALUES[message[i]]}, {key[i % len(key)]}:{ALPHABET_VALUES[key[i % len(key)]]}, {letter}:{(ALPHABET_VALUES[message[i]] + ALPHABET_VALUES[key[i % 4]]) % 26}")
            ciphertext += f'{letter}'
            j += 1
        else:
            ciphertext += f'{message[i]}'

    return ciphertext

def vigenere_decoder(ciphertext: str, key:str) -> str:
    """
    Decodes a Vigenere-encoded ciphertext into plaintext given a key

    >> lib.cipher.vigenere_decoder("NSWOU KZURR", "GOLD")

    `HELLO WORLD`
    """
    key = key.upper()
    ciphertext = ciphertext.upper()
    
    plaintext = ""
    j = 0
    for i in range(len(ciphertext)):
        if ciphertext[i] in ALPHABET_VALUES.keys():
            val = ALPHABET_VALUES[ciphertext[i]] - ALPHABET_VALUES[key[j % len(key)]]
            letter = NUMERIC_TO_ALPHABET[val] if val >= 0 else NUMERIC_TO_ALPHABET[val + 26]
            plaintext += f'{letter}'
            j += 1
        else:
            plaintext += f'{ciphertext[i]}'

    return plaintext

def caesar_encoder(message: str, shift: int) -> str:
    """
    Encodes a plaintext into Caesar Cipher

    >> lib.cipher.caesar_encoder("HELLO WORLD", 3)
    
    `KHOOR ZRUOG`
    """
    message = message.upper()

    ciphertext = ""
    for i in message:
        if i in string.ascii_uppercase:
            val = ALPHABET_VALUES[i] + shift
            if val >= 0:
                ciphertext += NUMERIC_TO_ALPHABET[val] if val < 26 else NUMERIC_TO_ALPHABET[val - 26]
            
            else:
                ciphertext += NUMERIC_TO_ALPHABET[val + 26]
        else:
            ciphertext += f'{i}'

    return ciphertext

def caesar_decoder(message: str, shift: int) -> str:
    """
    Decodes Caesar's Cipher given a string and a shift
    
    >> lib.cipher.caesar_decoder("KHOOR ZRUOG", 3)

    `HELLO WORLD`
    """
    message = message.upper()

    plaintext = ""
    for i in message:
        if i in string.ascii_uppercase:
            val = ALPHABET_VALUES[i] - shift
            if val >= 0:
                plaintext += NUMERIC_TO_ALPHABET[val] if val < 26 else NUMERIC_TO_ALPHABET[val - 26]

            else:
                plaintext += NUMERIC_TO_ALPHABET[val + 26]
        else:
            plaintext += f'{i}'

    return plaintext

def caesar_brute(message: str):
    """
    Brute forces Caesar Cipher
    """
    for i in range(25):
        print(f"Key: {i + 1} >> {caesar_decoder(message, i + 1)}")
    
    return

def rot_13(message: str) -> str:
    """
    Returns a string rotated by 13

    >> lib.cipher.rot_13("HELLO WORLD")
    
    `URYYB JBEYQ`

    >> lib.cipher.to_13("URYYB JBEYQ")

    `HELLO WORLD`
    """
    output = ""
    for i in message:
        if i not in ROT13:
            output += f'{i}'
        else:
            output += ROT13[i]

    return output

def morse_encoder(plaintext: str) -> str:
    """
    Encodes a plaintext into morse code

    >> lib.cipher.morse_encoder("SOS")

    `... --- ...`
    """
    code = ""
    plaintext = plaintext.upper()
    for char in plaintext:
        if char in MORSE:
            code += MORSE[char] + ' '
        else:
            return f"Morse dictionary does not contain this character: {char}"

    return code

def morse_decoder(code: str) -> str:
    """
    Decodes morse code into plaintext

    >> lib.cipher.morse_decoder("... --- ...")

    `SOS`
    """
    plaintext = ""
    code = code.split()

    for char in code:
        if char in REMORSE:
            plaintext += REMORSE[char]
        else:
            return f"Morse dictionary does not contain this character: {char}"

    return plaintext.upper()

def client() -> None:
    #Cipher
    while True:
        cipher = input("Type? ").lower()
        if cipher == "exit":
            return
        elif cipher != "caesar" and cipher != "vigenere" and cipher != "morse" and cipher != "rot13":
            print("Options: Caesar, Vigenere, Morse, ROT13")
        else:
            break
        
    #Encode/Encrypt or Decode/Decrypt
    while True:
        if cipher == "rot13":
            eod = ''
            break
        eod = input("D/E? ").lower()
        if eod == "exit": 
            return
        elif len(eod) == 1 and eod == 'e' or eod == 'd':
            break
        else:
            print("Enter E/D")

    #Plaintext/Ciphertext
    text = input("Enter ciphertext: " if eod == "d" else "Enter plaintext: ")
    if text.lower() == "exit":
        return
    if cipher == "caesar":
        while True:
            shift = input("Shift? ").lower()
            if shift == "exit":
                return
            elif shift == 'b':
                eod = 'b'
                break
            elif shift != '':
                try:
                    shift = int(shift)
                    break
                except:
                    print("shift must be of int type")
        if eod == 'b':
            print(caesar_brute(text))
        elif eod == 'd':
            print(caesar_decoder(text, shift))
        elif eod == 'e':
            print(caesar_encoder(text, shift))
    
    if cipher == "vigenere":
        while True:
            key = input("Key? ").lower()
            flag = True
            for i in key:
                if i not in string.ascii_lowercase:
                    print("Key may only contain letters of the english alphabet")
                    flag = False
            if key != "" and flag:
                break
        if eod == 'd':
            print(vigenere_decoder(text, key))
        else:
            print(vigenere_encoder(text, key))

    if cipher == "morse":
        if eod == 'd':
            print(morse_decoder(text))
        else:
            print(morse_encoder(text))
    
    if cipher == "rot13":
        print(rot_13(text))

    return

def playfair(message: str, keyword: str = '', mode: str = "encode", verbose: bool = False, results: bool = True) -> str:
    """
    Args         ( message: str, keyword: str )
    Return value ( cipher: str )

    Note: If you enter an empty key, it is assumed to be the first 25 characters of the alphabet.
    Note: If double-letters will be seperated by the letter 'X'
    Note: The letter J is replaced with I as the cipher uses a 5x5 table
    """
    if not isinstance(message, str): print("[!] message has to be of type str"); return None
    if not isinstance(keyword, str): print("[!] keyword has to be of type str"); return None
    if not isinstance(mode, str): print("[!] mode has to be of type str"); return None
    if not isinstance(verbose, bool): print("[!] verbose has to be of type bool"); return None
    if not isinstance(results, bool): print("[!] results has to be of type bool"); return None

    if len(message) <= 1:
        print("[!] What am I supposed to do with that? Come back with more than {len(message)} letters...")
        return None
    if len(keyword) > 25:
        print("[!] Key should not be longer than 25 characters")
        return None
    if mode.upper() not in ["DECODE", "ENCODE"]:
        print("[!] Please enter mode=decode or mode=encode")
        return None
        
    keyword = keyword.upper()
    message = message.upper().replace('  ', ' ')
    mode = mode.upper()

    extrachr = r"<>{}[]().,:;/\ `|_=+-?!@#$%^&*" + string.digits
    varm: str = ''

    #Get rid of multiplicities
    temp: str = ''
    for i in keyword:
        if i not in temp:
            temp += i

    if verbose and keyword != temp: print(f"[*] Rid of multiplicities in the key: {temp}")
    keyword = temp

    #Fill the rest of the words
    for i in string.ascii_uppercase:
        if len(keyword) == 25:
            break
        if i not in keyword and i != 'J':
            keyword += i
    
    if verbose: print(f"[*] Alphabet created: {keyword} ({len(keyword)})")
    
    #Generate table
    alphabet: list = []
    counter: int = 0
    if verbose: print("[*] Table created")
    for i in range(5):
        temp: list = []
        for j in range(5):
            temp.append(keyword[counter])
            if verbose: print(keyword[counter], end=' ')
            counter += 1
        alphabet.append(temp)
        if verbose: print()

    temp: str = ''
    for i in message:
        if i in keyword or i == ' ' or i in extrachr:
            temp += i
    
    message = temp

    #If there is a double-letter, seperates them wtih the letter 'X' (i.e: heLLo => heLXLo)
    if mode == "ENCODE":
        for i in range(len(message) - 1):
            if message[i] == message[i + 1] and message[i] in string.ascii_uppercase:
                message = message[:i+1] + 'X' + message [i + 1:]

            i += 2
        
    if len(message) % 2 == 1:
        message += 'X'

    if mode == "DECODE":
        varm: str = message
        for i in range(len(varm) - 5):
            if varm[i] == varm[i + 2] and varm[i + 1] == 'X':
                varm = varm[:i + 1] + varm[i + 2:]

    placeholder: str = message
    if verbose: print(f"[*] Cleaned message: {message}")

    def __find__(letter: chr) -> tuple:
        for i in alphabet:
            if letter in i:
                return alphabet.index(i), i.index(letter)

        return -1, -1

    #Cipher logic [a=z, b=y, f stands for first, s stands for second, flag to get out of loop]
    def __logic__(m: str):
        c: str = ''
        temp: str = ''
        z: chr
        y: chr
        f: chr
        s: chr
        flag: bool = True
        while flag and m:
            while m[0] in extrachr:
                if len(m) <= 1:
                    flag = False
                    break
                c += m[0]
                m = m[1:]

            if len(m) <= 1:
                if len(m) == 1:
                    c += m
                break

            z = m[0]
            while m[1] in extrachr:
                temp += m[1]
                m = m[1:]
                if len(m) <= 1:
                    flag = False
                    c += z + temp
                    break

            if len(m) <= 1:
                break

            y = m[1]

            if verbose: print(m)
            a = __find__(z)
            b = __find__(y)

            #Case: not the same row and not the same column
            if a[0] != b[0] and a[1] != b[1]:
                f = alphabet[a[0]][b[1]]
                s = alphabet[b[0]][a[1]]

            #Case: same row
            elif a[0] == b[0]:
                if mode == "ENCODE":
                    f = alphabet[a[0]][0 if a[1] == 4 else a[1] + 1]
                    s = alphabet[b[0]][0 if b[1] == 4 else b[1] + 1]
                else:
                    f = alphabet[a[0]][4 if a[1] == 0 else a[1] - 1]
                    s = alphabet[b[0]][4 if b[1] == 0 else b[1] - 1]

            #Case: same column
            elif a[1] == b[1]:
                if mode == "ENCODE":
                    f = alphabet[0 if a[0] == 4 else a[0] + 1][a[1]]
                    s = alphabet[0 if b[0] == 4 else b[0] + 1][b[1]]
                else:
                    f = alphabet[4 if a[0] == 0 else a[0] - 1][a[1]]
                    s = alphabet[4 if b[0] == 0 else b[0] - 1][b[1]]

            c += f + temp + s
            temp = ''
            if verbose: print(a, b, ">>", c)
            m = m[2:]

        return c

    cipher = __logic__(message)
    variation = __logic__(varm)

    if mode == "DECODE" and results or verbose:
        for i in range(len(variation) - 4):
            if variation[i - 1] == variation[i + 1] and variation[i] == 'X':
                variation = variation[:i] + variation[i + 1:]
        
        variation = variation[:-1] if variation[-1] == 'X' else variation

    if results and verbose: print(f"[{'Plaintext' if mode == 'ENCODE' else 'Ciphertxt'}]: {placeholder}")
    if results or verbose: print(f"[{'Ciphertxt' if mode == 'ENCODE' else 'Plaintext'}]: {cipher}")
    if results or verbose: print(f"[Variation]: {variation}") if mode == "DECODE" else ''

    return cipher

if __name__ == "__main__":
    print("[*] FeelsWeirdMan")

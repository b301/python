import string

"""
__author__ == b301
__date__ == 27.02.2022
"""

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
    message: str = r"HELLO WORLD THIS IS A TEST"
    keyword: str = "QWERTYUIOPASDFGHKLZXCVBNM"
    print(f"[Message]:   {message}")
    ciphertext = playfair(message=message, keyword=keyword, mode="encode", verbose=False, results=True)
    plaintext = playfair(ciphertext, keyword=keyword, mode="decode", verbose=False, results=True)

"""
PS C:\Users\User\Desktop\Challenges> python .\playfair.py
[Message]:   HELLO WORLD THIS IS A TEST
[Ciphertxt]: LQZHZI RUEZG ELYD UD S QRGWX
[Plaintext]: HELXLO WORLD THIS IS A TESTX
[Variation]: HELLO WORLD THIS IS A TEST
"""

# BabyEncryption.py
# ~/hackthebox/crypto

def dictionary(msg):
    ct = []
    decryption_dict = {}
    for char in msg:
        decryption_dict[(123 * (char) + 18) % 256] = chr(char)

    return decryption_dict
    
def encryption(msg):
    ct = []
    for char in msg:
        ct.append((123 * char + 18) % 256)
        print(char, ct)
    return bytes(ct)

def decryption(msg):
    decdict = dictionary(''.join(chr(i) for i in range(128)).encode())
    values = [msg[i:i+2] for i in range(0, len(msg), 2)]
    original = ''
    print(decdict)
    for i in values:
        print(original, i)
        original += decdict[int(i, 16)]
    return original

    
message = "6e0a9372ec49a3f6930ed8723f9df6f6720ed8d89dc4937222ec7214d89d1e0e352ce0aa6ec82bf622227bb70e7fb7352249b7d893c493d8539dec8fb7935d490e7f9d22ec89b7a322ec8fd80e7f8921"
original = decryption(message)

print(original)

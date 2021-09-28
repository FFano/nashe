import random

def EncryptText(texto):
    textoCifrado = ""
    ay_or = False

    for ch in texto:
        textoCifrado += chr(ord(ch)+1)
        textoCifrado += chr(random.randint(32, 254))
        textoCifrado += chr(random.randint(32, 254))

    return textoCifrado

def DecryptText(texto):
    textoDescifrado = ""
    i = 0

    while i < len(texto):
        textoDescifrado += chr(ord(texto[i])-1)
        if(i >= len(texto)):
            break
        i += 3
        
    return textoDescifrado

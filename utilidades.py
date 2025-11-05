import unicodedata

def normalizar_caracteres(texto):
    texto_nfd = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto_nfd if unicodedata.category(c) != "Mn")

def normalizar_texto(texto):
    texto = texto.strip()
    texto = texto.lower()
    texto = normalizar_caracteres(texto)
    return texto
import random
import unicodedata
import nltk
from nltk.corpus import words

nltk.download('words')

palabras = words.words()

template = 'public void {method_name}() {{ System.out.println("{word}"); }}'

def generar_nombre_metodo(palabra):
    palabra_sin_tilde = ''.join(
        c for c in unicodedata.normalize('NFD', palabra) if unicodedata.category(c) != 'Mn'
    )
    return ''.join(c for c in palabra_sin_tilde if c.isalnum()).lower()

output_file = "mock_data.jsonl"
num_samples = 10000

with open(output_file, "w", encoding="utf-8") as file:
    for _ in range(num_samples):
        palabra = random.choice(palabras)
        prob = random.random()
        if prob > 0.8:
            len_palabras = random.randint(2, 5)
            palabras_seleccionadas = random.sample(palabras, len_palabras)
            palabra = " ".join(palabras_seleccionadas)

        metodo = generar_nombre_metodo(palabra)
        linea = template.format(word=palabra, method_name=metodo)
        file.write(linea + "\n")

print(f"Archivo '{output_file}' generado con {num_samples} muestras.")

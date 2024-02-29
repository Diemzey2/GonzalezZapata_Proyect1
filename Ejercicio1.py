from Crypto.Util import number
import hashlib

# Función para cifrar con RSA
def rsa_encrypt(public_key, message):
    n, e = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message

# Función para descifrar con RSA
def rsa_decrypt(private_key, encrypted_message):
    n, d = private_key
    decrypted_message = ''.join([chr(pow(char, d, n)) for char in encrypted_message])
    return decrypted_message

# Función para generar hash del mensaje
def generate_hash(message):
    return hashlib.sha256(message.encode()).hexdigest()

# Generar claves RSA
def generate_rsa_keys():
    p = number.getPrime(512)
    q = number.getPrime(512)
    n = p * q
    phi = (p-1) * (q-1)
    e = 65537
    d = number.inverse(e, phi)
    return (n, e), (n, d)  # Clave pública, clave privada

# Dividir mensaje en bloques de 128 caracteres
def divide_message(message, block_size=128):
    return [message[i:i+block_size] for i in range(0, len(message), block_size)]

# Generar las claves RSA
public_key, private_key = generate_rsa_keys()
print("Clave pública de Bob:", public_key)
print("Clave privada de Bob:", private_key)

# Mensaje de Alice
original_message = "Hola, este es un mensaje largo de Alice para Bob." * 20  # Mensaje de ejemplo
print("\nMensaje original de Alice:", original_message)

# Dividir el mensaje en partes
message_parts = divide_message(original_message)
print(f"\nMensaje dividido en {len(message_parts)} partes.")

# Alice cifra el mensaje
print("\nCifrando cada parte del mensaje con la clave pública de Bob...")
encrypted_parts = [rsa_encrypt(public_key, part) for part in message_parts]

# Bob descifra el mensaje
print("\nDescifrando cada parte del mensaje con la clave privada de Bob...")
decrypted_parts = [rsa_decrypt(private_key, part) for part in encrypted_parts]
reconstructed_message = ''.join(decrypted_parts)
print("\nMensaje reconstruido por Bob:", reconstructed_message)

# Generar hash del mensaje original y del reconstruido
original_hash = generate_hash(original_message)
reconstructed_hash = generate_hash(reconstructed_message)

# Comparar los hash
hash_comparison = original_hash == reconstructed_hash
print(f"\nHash del mensaje original: {original_hash}")
print(f"Hash del mensaje reconstruido: {reconstructed_hash}")
print(f"¿Son iguales los hash? {hash_comparison}")

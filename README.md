# Cifrado RSA y Firma de PDF

Este script facilita el cifrado y descifrado RSA para la transmisión segura de mensajes y demuestra cómo añadir firmas digitales a documentos PDF. Incluye generación de claves RSA, cifrado y descifrado de mensajes, hashing de mensajes, división de mensajes en bloques para su cifrado, y la inclusión de firmas digitales en documentos PDF.

## Características Principales

- **Generación de claves RSA**: Crea pares de claves (pública y privada) para el cifrado y descifrado.
- **Cifrado y descifrado RSA**: Permite cifrar mensajes usando la clave pública y descifrarlos con la privada.
- **Hashing de mensajes**: Emplea SHA-256 para crear hashes únicos de los mensajes.
- **División de mensajes en bloques**: Facilita el cifrado de mensajes largos dividiéndolos en partes manejables.
- **Firma digital de documentos PDF**: Añade firmas digitales a documentos PDF para autenticar su origen.
- **Verificación de firmas digitales**: Comprueba la autenticidad de las firmas en los documentos PDF.

## Dependencias

Este script requiere de las siguientes librerías para su funcionamiento:

- `PyCryptoDome` para las operaciones de cifrado RSA.
- `hashlib` para la generación de hashes.
- `PyPDF2` para la manipulación de archivos PDF.
- `reportlab` para la creación de contenido PDF que se usará en las firmas.


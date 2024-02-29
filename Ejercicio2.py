import hashlib
from Crypto.Util.number import getPrime, inverse
import PyPDF2
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_keys(bit_length=1024):
    p = getPrime(bit_length)
    q = getPrime(bit_length)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = inverse(e, phi)
    return ((n, e), (n, d))


def rsa_encrypt(message, key):
    n, key_part = key
    message_int = int.from_bytes(message.encode('utf-8'), 'big')
    encrypted_int = pow(message_int, key_part, n)
    return encrypted_int.to_bytes((encrypted_int.bit_length() + 7) // 8, 'big')


def rsa_decrypt(encrypted_message, key):
    n, key_part = key
    encrypted_int = int.from_bytes(encrypted_message, 'big')
    decrypted_int = pow(encrypted_int, key_part, n)
    return decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'big').decode('utf-8')


def hash_file(filename):
    BUF_SIZE = 65536
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


def add_signature_to_pdf(pdf_path, signature_text, output_pdf_path, y_position):
    existing_pdf = PyPDF2.PdfReader(open(pdf_path, "rb"))
    output = PyPDF2.PdfWriter()

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(100, y_position, signature_text)
    can.save()

    packet.seek(0)
    new_pdf = PyPDF2.PdfReader(packet)
    signature_page = new_pdf.pages[0]

    for page in existing_pdf.pages:
        page.merge_page(signature_page)
        output.add_page(page)

    with open(output_pdf_path, "wb") as outputStream:
        output.write(outputStream)


alice_public, alice_private = generate_keys()
trusted_center_public, trusted_center_private = generate_keys()

contract_hash = hash_file("NDA.pdf")
signature_alice = rsa_encrypt(contract_hash, alice_private)

add_signature_to_pdf("NDA.pdf", f"Alice's Signature: {signature_alice.hex()}", "NDA_signed_by_Alice.pdf", 100)

alice_verification = rsa_decrypt(signature_alice, alice_public)
if alice_verification == contract_hash:
    signature_trusted_center = rsa_encrypt(contract_hash, trusted_center_private)
    add_signature_to_pdf("NDA_signed_by_Alice.pdf", f"Trusted Center's Signature: {signature_trusted_center.hex()}",
                         "NDA_signed_by_Trusted_Center.pdf", 50)


def bob_verifies_signature(signed_pdf_path, trusted_center_public_key):
    document_hash = hash_file(signed_pdf_path)
    signature_trusted_center = rsa_encrypt(document_hash, trusted_center_private)
    trusted_center_verification = rsa_decrypt(signature_trusted_center, trusted_center_public_key)

    if trusted_center_verification == document_hash:
        print("Bob has successfully verified the signature from the Trusted Center.")
        return True
    else:
        print("Bob's verification of the Trusted Center's signature has failed.")
        return False


signed_pdf_path = "NDA_signed_by_Trusted_Center.pdf"
bob_verification_result = bob_verifies_signature(signed_pdf_path, trusted_center_public)

if bob_verification_result:
    add_signature_to_pdf(signed_pdf_path, "Bob has verified the signatures.", "NDA_final.pdf", 20)

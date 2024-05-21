from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend

# Générer une clé privée RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Créer une liste de SANs appropriés
sans = [x509.DNSName("django")]

# Créer un certificat X.509 auto-signé avec les SANs
cert = x509.CertificateBuilder().subject_name(
    x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "BE"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Brussel"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Brussel"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "19 School"),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "mprofett's team"),
        x509.NameAttribute(NameOID.COMMON_NAME, "django"),
    ])
).issuer_name(
    x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "BE"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Brussel"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Brussel"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "19 School"),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "mprofett's team"),
        x509.NameAttribute(NameOID.COMMON_NAME, "django"),
    ])
).add_extension(
    x509.SubjectAlternativeName(sans),
    critical=False
).public_key(
    private_key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.utcnow()
).not_valid_after(
    datetime.utcnow() + timedelta(days=365)  # Certificat valable 1 an
).sign(
    private_key,
    hashes.SHA256(),
    default_backend()
)

# Exporter la clé privée et le certificat
private_key_pem = private_key.private_bytes(
    Encoding.PEM,
    PrivateFormat.TraditionalOpenSSL,
    NoEncryption()
)
cert_pem = cert.public_bytes(Encoding.PEM)

# Écrire la clé privée et le certificat dans des fichiers
with open("../../../certificates/key.pem", "wb") as key_file:
    key_file.write(private_key_pem)

with open("../../../certificates/cert.pem", "wb") as cert_file:
    cert_file.write(cert_pem)
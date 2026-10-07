from dataclasses import dataclass
import os, json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from .utils import sha256_bytes

@dataclass
class EncryptedBlob:
    nonce: bytes; ciphertext: bytes

def generate_aes_key(): return AESGCM.generate_key(bit_length=256)
def encrypt_aes_gcm(plaintext:bytes,key:bytes,aad:bytes=b""):
    nonce=os.urandom(12); return EncryptedBlob(nonce,AESGCM(key).encrypt(nonce,plaintext,aad))
def decrypt_aes_gcm(blob:EncryptedBlob,key:bytes,aad:bytes=b""):
    return AESGCM(key).decrypt(blob.nonce,blob.ciphertext,aad)
def generate_ec_keypair():
    private=ec.generate_private_key(ec.SECP256R1()); return private, private.public_key()
def serialize_public_key(pub):
    return pub.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo).decode()
def load_public_key(pem): return serialization.load_pem_public_key(pem.encode() if isinstance(pem,str) else pem)
def _kek(shared): return HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b"HealthBlockSecure-KeyWrap-v1").derive(shared)
def wrap_key(aes_key:bytes, recipient_public_key):
    eph=ec.generate_private_key(ec.SECP256R1()); shared=eph.exchange(ec.ECDH(),recipient_public_key); kek=_kek(shared)
    blob=encrypt_aes_gcm(aes_key,kek,b"session-key")
    eph_pub=eph.public_key().public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo)
    return {"ephemeral_public_key":eph_pub.hex(),"nonce":blob.nonce.hex(),"ciphertext":blob.ciphertext.hex()}
def unwrap_key(pkg,recipient_private_key):
    eph=serialization.load_der_public_key(bytes.fromhex(pkg['ephemeral_public_key'])); shared=recipient_private_key.exchange(ec.ECDH(),eph); kek=_kek(shared)
    return decrypt_aes_gcm(EncryptedBlob(bytes.fromhex(pkg['nonce']),bytes.fromhex(pkg['ciphertext'])),kek,b"session-key")
def sha256_record(data:bytes): return sha256_bytes(data)

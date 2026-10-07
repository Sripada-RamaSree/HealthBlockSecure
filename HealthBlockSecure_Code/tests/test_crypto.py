from healthblocksecure.crypto import *
def test_roundtrip():
    priv,pub=generate_ec_keypair(); k=generate_aes_key(); b=encrypt_aes_gcm(b'hello',k,b'x'); assert decrypt_aes_gcm(b,k,b'x')==b'hello'; pkg=wrap_key(k,pub); assert unwrap_key(pkg,priv)==k

from healthblocksecure.crypto import *
def test_tamper_detected_by_gcm():
    k=generate_aes_key(); b=encrypt_aes_gcm(b'abc',k); c=bytearray(b.ciphertext); c[-1]^=1
    import pytest
    with pytest.raises(Exception): decrypt_aes_gcm(EncryptedBlob(b.nonce,bytes(c)),k)

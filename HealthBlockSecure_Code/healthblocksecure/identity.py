import hashlib, base64
from dataclasses import dataclass
from .crypto import generate_ec_keypair, serialize_public_key

@dataclass
class Identity:
    did:str; role:str; organisation:str; private_key:object; public_key:object
    @property
    def document(self):
        pem=serialize_public_key(self.public_key); fp=hashlib.sha256(pem.encode()).hexdigest()
        return {"id":self.did,"role":self.role,"organisation":self.organisation,"publicKeyPem":pem,"fingerprint":fp,"status":"active"}

def create_identity(entity_id,role,organisation="HospitalOrg1"):
    priv,pub=generate_ec_keypair(); return Identity(f"did:hbs:{entity_id}",role,organisation,priv,pub)

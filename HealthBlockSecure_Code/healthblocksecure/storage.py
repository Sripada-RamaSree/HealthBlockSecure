from pathlib import Path
import uuid
class LocalEncryptedStorage:
    def __init__(self,root="data/storage"):
        self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
    def upload(self,data:bytes,record_id:str):
        name=f"{record_id}-{uuid.uuid4().hex}.bin"; p=self.root/name; p.write_bytes(data); return str(p)
    def download(self,pointer:str): return Path(pointer).read_bytes()
    def tamper(self,pointer:str,percent=1):
        p=Path(pointer); b=bytearray(p.read_bytes()); n=max(1,int(len(b)*percent/100));
        for i in range(min(n,len(b))): b[i]^=0x01
        p.write_bytes(bytes(b))

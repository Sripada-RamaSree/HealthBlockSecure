import os, time, hashlib, json, subprocess, tempfile
from dataclasses import dataclass

@dataclass
class ZKPResult:
    verified: bool; latency_ms: float; mode: str; public_digest: str

class ResearchZKPVerifier:
    """Self-contained deterministic research verifier used when a Groth16 toolchain is unavailable.
    It exposes only the conjunction outcome and a digest to the application layer. For cryptographic
    zero-knowledge guarantees use SnarkJSVerifier below.
    """
    mode='research'
    def prove_and_verify(self, claims):
        t=time.perf_counter(); ok=bool(claims.get('credential_valid') and claims.get('role_eligible') and claims.get('consent_eligible') and claims.get('not_expired'))
        digest=hashlib.sha256(json.dumps({'verified':ok,'nonce':claims.get('nonce','')},sort_keys=True).encode()).hexdigest()
        return ZKPResult(ok,(time.perf_counter()-t)*1000,self.mode,digest)

class SnarkJSVerifier:
    mode='snarkjs'
    def __init__(self, artifacts='circuits/build'): self.artifacts=artifacts
    def prove_and_verify(self, claims):
        # Expects generated access_auth.wasm/access_auth_final.zkey/verification_key.json.
        t=time.perf_counter()
        import pathlib
        b=pathlib.Path(self.artifacts)
        with tempfile.TemporaryDirectory() as td:
            inp=pathlib.Path(td)/'input.json'; proof=pathlib.Path(td)/'proof.json'; public=pathlib.Path(td)/'public.json'
            values={k:int(bool(claims[k])) for k in ['credential_valid','role_eligible','consent_eligible','not_expired']}
            inp.write_text(json.dumps(values))
            subprocess.run(['snarkjs','groth16','fullprove',str(inp),str(b/'access_auth.wasm'),str(b/'access_auth_final.zkey'),str(proof),str(public)],check=True,capture_output=True)
            r=subprocess.run(['snarkjs','groth16','verify',str(b/'verification_key.json'),str(public),str(proof)],check=False,capture_output=True,text=True)
            ok='OK!' in r.stdout
            digest=hashlib.sha256(public.read_bytes()+proof.read_bytes()).hexdigest()
        return ZKPResult(ok,(time.perf_counter()-t)*1000,self.mode,digest)

def make_verifier(mode=None):
    mode=(mode or os.getenv('HBS_ZKP_MODE','research')).lower(); return SnarkJSVerifier() if mode=='snarkjs' else ResearchZKPVerifier()

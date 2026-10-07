from __future__ import annotations
import json, time, uuid
from .utils import canonical_json
from .crypto import generate_aes_key,encrypt_aes_gcm,decrypt_aes_gcm,wrap_key,unwrap_key,sha256_record,EncryptedBlob
from .policy import evaluate_policy

class HealthBlockSecure:
    def __init__(self,ledger,storage,verifier,model,token_ttl=300):
        self.ledger=ledger; self.storage=storage; self.verifier=verifier; self.model=model; self.token_ttl=token_ttl
    def register_identity(self,identity): self.ledger.register_identity(identity.document)
    def upload_record(self,record,patient_identity,provider_identity,policy):
        t=time.perf_counter(); data=canonical_json(record); key=generate_aes_key(); blob=encrypt_aes_gcm(data,key,record['record_id'].encode())
        pointer=self.storage.upload(blob.nonce+blob.ciphertext,record['record_id']); wrapped=wrap_key(key,provider_identity.public_key); h=sha256_record(data)
        policy_id='POL-'+record['record_id']; self.ledger.set_policy(policy_id,policy)
        meta={'record_id':record['record_id'],'patient_did':patient_identity.did,'policy_id':policy_id,'storage_pointer':pointer,'record_hash':h,'wrapped_key':wrapped,'data_category':record.get('record_type'),'aad':record['record_id']}
        self.ledger.register_record(record['record_id'],meta); self.ledger.grant_consent(patient_identity.did,record['record_id'],provider_identity.did)
        return {'record_id':record['record_id'],'storage_pointer':pointer,'hash':h,'latency_ms':(time.perf_counter()-t)*1000}
    def request_access(self,request,provider_identity):
        t0=time.perf_counter(); meta=self.ledger.get_record(request['record_id'])
        if not meta: return {'granted':False,'reasons':['RECORD_NOT_FOUND']}
        consent=self.ledger.has_consent(meta['patient_did'],request['record_id'],provider_identity.did)
        claims={'credential_valid':request.get('credential_valid',True),'role_eligible':request.get('role_match',True),'consent_eligible':consent and request.get('consent_status',True),'not_expired':request.get('token_valid',True),'nonce':request.get('request_id','')}
        z=self.verifier.prove_and_verify(claims); score=self.model.predict_score(request); policy=self.ledger.get_policy(meta['policy_id'])
        granted,reasons=evaluate_policy(policy,request,consent,z.verified,score,self.model.threshold)
        event={'request_id':request.get('request_id'),'record_id':request['record_id'],'actor_did':provider_identity.did,'zkp_verified':z.verified,'zkp_latency_ms':z.latency_ms,'model_score':score,'threshold':self.model.threshold,'granted':granted,'reasons':reasons}
        self.ledger.audit('ACCESS_GRANTED' if granted else 'ACCESS_DENIED',event)
        if not granted:return dict(event,total_latency_ms=(time.perf_counter()-t0)*1000)
        tok=self.ledger.issue_token({'grantee_did':provider_identity.did,'record_id':request['record_id'],'request_id':request.get('request_id')},self.token_ttl)
        return dict(event,token=tok['token_id'],wrapped_key=meta['wrapped_key'],storage_pointer=meta['storage_pointer'],total_latency_ms=(time.perf_counter()-t0)*1000)
    def retrieve(self,token,record_id,provider_identity):
        t=time.perf_counter();
        if not self.ledger.consume_token(token,provider_identity.did,record_id): return {'ok':False,'reason':'TOKEN_REJECTED'}
        meta=self.ledger.get_record(record_id); package=self.storage.download(meta['storage_pointer']); nonce,cipher=package[:12],package[12:]
        try:
            key=unwrap_key(meta['wrapped_key'],provider_identity.private_key); plain=decrypt_aes_gcm(EncryptedBlob(nonce,cipher),key,record_id.encode()); integrity=(sha256_record(plain)==meta['record_hash'])
            self.ledger.audit('INTEGRITY_PASS' if integrity else 'INTEGRITY_FAILURE',{'record_id':record_id,'actor_did':provider_identity.did})
            return {'ok':integrity,'record':json.loads(plain.decode()) if integrity else None,'integrity':integrity,'latency_ms':(time.perf_counter()-t)*1000}
        except Exception as e:
            self.ledger.audit('INTEGRITY_FAILURE',{'record_id':record_id,'actor_did':provider_identity.did,'error':type(e).__name__}); return {'ok':False,'reason':'DECRYPT_OR_INTEGRITY_FAILURE','integrity':False,'latency_ms':(time.perf_counter()-t)*1000}

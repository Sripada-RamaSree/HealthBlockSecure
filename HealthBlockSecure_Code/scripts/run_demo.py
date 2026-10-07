import os, sys, json, shutil
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from healthblocksecure.config import load_config
from healthblocksecure.data import generate_ehrs,generate_access_requests
from healthblocksecure.model import PrivAccessNet
from healthblocksecure.ledger import SQLiteLedger
from healthblocksecure.storage import LocalEncryptedStorage
from healthblocksecure.zkp import ResearchZKPVerifier
from healthblocksecure.identity import create_identity
from healthblocksecure.workflow import HealthBlockSecure

cfg=load_config(); Path('data').mkdir(exist_ok=True)
if Path(cfg['runtime']['ledger_db']).exists(): Path(cfg['runtime']['ledger_db']).unlink()
records=generate_ehrs(1200,42); reqdf=generate_access_requests(records,3000,.70,42)
model=PrivAccessNet('auto',42); metrics,_=model.fit(reqdf,max_epochs=50)
patient=create_identity('patient001','patient'); provider=create_identity('provider001','doctor')
ledger=SQLiteLedger(cfg['runtime']['ledger_db']); storage=LocalEncryptedStorage(cfg['runtime']['storage_dir']); engine=HealthBlockSecure(ledger,storage,ResearchZKPVerifier(),model,300)
engine.register_identity(patient); engine.register_identity(provider)
policy={'allowed_roles':['doctor','nurse'],'allowed_actions':['read','audit','full_record'],'hours':[0,23]}
upload=engine.upload_record(records[0],patient,provider,policy)
req=generate_access_requests([records[0]],1,1.0,99).iloc[0].to_dict(); req['provider_role']='doctor'; req['record_id']=records[0]['record_id']; req['role_match']=True; req['policy_match']=True
access=engine.request_access(req,provider); retrieval=engine.retrieve(access['token'],records[0]['record_id'],provider) if access.get('granted') else None
print(json.dumps({'model_metrics':metrics,'upload':upload,'access':{k:v for k,v in access.items() if k not in ['wrapped_key']},'retrieval':retrieval,'audit_events':len(ledger.get_audits())},indent=2,default=str))

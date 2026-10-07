from pathlib import Path
from healthblocksecure.data import generate_ehrs,generate_access_requests
from healthblocksecure.model import PrivAccessNet
from healthblocksecure.ledger import SQLiteLedger
from healthblocksecure.storage import LocalEncryptedStorage
from healthblocksecure.zkp import ResearchZKPVerifier
from healthblocksecure.identity import create_identity
from healthblocksecure.workflow import HealthBlockSecure

def test_e2e(tmp_path):
    recs=generate_ehrs(500,7); df=generate_access_requests(recs,1200,.7,7); m=PrivAccessNet('sklearn',7); m.fit(df,max_epochs=25)
    p=create_identity('p','patient'); d=create_identity('d','doctor'); e=HealthBlockSecure(SQLiteLedger(tmp_path/'l.db'),LocalEncryptedStorage(tmp_path/'s'),ResearchZKPVerifier(),m)
    e.register_identity(p);e.register_identity(d);e.upload_record(recs[0],p,d,{'allowed_roles':['doctor'],'allowed_actions':['read','audit','full_record'],'hours':[0,23]})
    r=generate_access_requests([recs[0]],1,1,2).iloc[0].to_dict(); r.update({'record_id':recs[0]['record_id'],'provider_role':'doctor','role_match':True,'policy_match':True,'request_type':'read','request_hour':12})
    a=e.request_access(r,d); assert a['granted']; z=e.retrieve(a['token'],recs[0]['record_id'],d); assert z['ok']

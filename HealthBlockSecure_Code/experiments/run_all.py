import sys, json, argparse, shutil, time, statistics
from pathlib import Path
import pandas as pd, numpy as np
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from healthblocksecure.config import load_config
from healthblocksecure.data import generate_ehrs,generate_access_requests
from healthblocksecure.model import PrivAccessNet
from healthblocksecure.baselines import run_ml_baselines
from healthblocksecure.ledger import SQLiteLedger
from healthblocksecure.storage import LocalEncryptedStorage
from healthblocksecure.zkp import ResearchZKPVerifier
from healthblocksecure.identity import create_identity
from healthblocksecure.workflow import HealthBlockSecure

ap=argparse.ArgumentParser(); ap.add_argument('--config',default='config/base.yaml'); ap.add_argument('--backend',default='auto'); args=ap.parse_args(); cfg=load_config(args.config)
outdir=ROOT/'results'; (outdir/'raw').mkdir(parents=True,exist_ok=True); (outdir/'tables').mkdir(exist_ok=True); (outdir/'models').mkdir(exist_ok=True)
all_metrics=[]; baseline_rows=[]; security_rows=[]
for seed in cfg['project']['seeds']:
    recs=generate_ehrs(2500,seed); df=generate_access_requests(recs,cfg['data']['requests_per_dataset'],cfg['data']['compliant_fraction'],seed)
    model=PrivAccessNet(args.backend,seed); metrics,_=model.fit(df,cfg['privaccessnet']['max_epochs'],cfg['privaccessnet']['batch_size'],cfg['privaccessnet']['patience']); metrics['seed']=seed; all_metrics.append(metrics)
    for r in run_ml_baselines(df,seed): r['seed']=seed; baseline_rows.append(r)
    # clean standalone state per seed
    db=ROOT/f"results/raw/ledger_{seed}.db"; store=ROOT/f"results/raw/storage_{seed}"; shutil.rmtree(store,ignore_errors=True)
    ledger=SQLiteLedger(db); storage=LocalEncryptedStorage(store); verifier=ResearchZKPVerifier(); engine=HealthBlockSecure(ledger,storage,verifier,model,cfg['security']['token_ttl_seconds'])
    patient=create_identity(f'patient-{seed}','patient'); provider=create_identity(f'provider-{seed}','doctor'); engine.register_identity(patient); engine.register_identity(provider)
    policy={'allowed_roles':['doctor','nurse'],'allowed_actions':['read','audit','full_record'],'hours':[0,23]}; engine.upload_record(recs[0],patient,provider,policy)
    testdf=generate_access_requests([recs[0]],300,.70,seed+999); outcomes=[]
    for _,row in testdf.iterrows():
        req=row.to_dict(); req['record_id']=recs[0]['record_id']; req['provider_role']='doctor' if req['scenario']=='legitimate' else req['provider_role']
        if req['scenario']=='legitimate': req['role_match']=True; req['policy_match']=True
        res=engine.request_access(req,provider); outcomes.append((int(row['label']),int(bool(res.get('granted'))),res.get('total_latency_ms',0),res.get('zkp_latency_ms',0),row['scenario']))
    una=[x for x in outcomes if x[0]==0]; violation=sum(1 for x in una if x[1]==0)/len(una)
    acc=sum(1 for x in outcomes if x[0]==x[1])/len(outcomes)
    security_rows.append({'seed':seed,'access_decision_accuracy':acc,'violation_prevention_rate':violation,'mean_secure_access_validation_ms':statistics.mean(x[2] for x in outcomes),'mean_zkp_latency_ms':statistics.mean(x[3] for x in outcomes)})

pd.DataFrame(all_metrics).to_csv(outdir/'tables/privaccessnet_metrics.csv',index=False)
pd.DataFrame(baseline_rows).to_csv(outdir/'tables/ml_baselines.csv',index=False)
pd.DataFrame(security_rows).to_csv(outdir/'tables/security_metrics.csv',index=False)
summary={'privaccessnet':pd.DataFrame(all_metrics).mean(numeric_only=True).to_dict(),'security':pd.DataFrame(security_rows).mean(numeric_only=True).to_dict()}
(outdir/'summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))

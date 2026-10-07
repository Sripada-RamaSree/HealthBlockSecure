from __future__ import annotations
import random, uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
import pandas as pd
import numpy as np

RECORD_TYPES=["lab","prescription","diagnosis","procedure","note"]
ROLES=["doctor","nurse","researcher"]
REQUEST_TYPES=["read","audit","full_record"]
SCENARIOS=["legitimate","role_violation","consent_violation","expired_token","out_of_hours","privilege_escalation","replay","frequency_anomaly"]

FEATURE_COLUMNS=[
 "role_doctor","role_nurse","role_researcher","request_hour_norm","request_read","request_audit","request_full_record",
 "consent_status","token_valid","previous_access_frequency_norm","policy_match","credential_valid","role_match",
 "time_window_valid","replay_indicator","frequency_anomaly","privilege_escalation"
]

def generate_ehrs(n=1000, seed=42, prefix="SYN"):
    rng=random.Random(seed); rows=[]
    for i in range(n):
        age=rng.randint(18,90); sex=rng.choice(["F","M"]); rt=rng.choice(RECORD_TYPES)
        rows.append({
            "record_id":f"{prefix}-R{i:06d}", "patient_id":f"{prefix}-P{i:06d}",
            "encounter_id":f"{prefix}-E{i:06d}", "record_type":rt,
            "timestamp":(datetime(2026,1,1,tzinfo=timezone.utc)+timedelta(minutes=i)).isoformat(),
            "provider_id":f"PRV-{rng.randint(1,200):04d}", "demographics":{"age":age,"sex":sex},
            "diagnoses":[f"DX{rng.randint(1,50):03d}"], "medications":[f"MED{rng.randint(1,40):03d}"],
            "observations":{"heart_rate":rng.randint(55,115),"spo2":rng.randint(90,100)},
            "procedures":[f"PROC{rng.randint(1,25):03d}"]
        })
    return rows

def load_mimic_iv(folder, limit=5000):
    p=Path(folder)
    if not p.exists(): return []
    patients=p/'patients.csv'; admissions=p/'admissions.csv'
    if not patients.exists(): return []
    pat=pd.read_csv(patients, nrows=limit)
    adm=pd.read_csv(admissions, nrows=limit) if admissions.exists() else pd.DataFrame()
    rows=[]
    for i,r in pat.head(limit).iterrows():
        sid=str(r.get('subject_id', i));
        rows.append({"record_id":f"MIMIC-R{sid}","patient_id":f"MIMIC-P{sid}","encounter_id":f"MIMIC-E{i}",
                     "record_type":"clinical","timestamp":datetime.now(timezone.utc).isoformat(),"provider_id":"MIMIC-DEID",
                     "demographics":{"gender":str(r.get('gender','')),"anchor_age":int(r.get('anchor_age',0) or 0)},
                     "diagnoses":[],"medications":[],"observations":{},"procedures":[]})
    return rows

def _features(req):
    role=req['provider_role']; typ=req['request_type']
    return {
        "role_doctor":int(role=='doctor'),"role_nurse":int(role=='nurse'),"role_researcher":int(role=='researcher'),
        "request_hour_norm":req['request_hour']/23.0,"request_read":int(typ=='read'),"request_audit":int(typ=='audit'),
        "request_full_record":int(typ=='full_record'),"consent_status":int(req['consent_status']),"token_valid":int(req['token_valid']),
        "previous_access_frequency_norm":min(req['previous_access_frequency']/20.0,1.0),"policy_match":int(req['policy_match']),
        "credential_valid":int(req['credential_valid']),"role_match":int(req['role_match']),"time_window_valid":int(req['time_window_valid']),
        "replay_indicator":int(req['replay_indicator']),"frequency_anomaly":int(req['frequency_anomaly']),
        "privilege_escalation":int(req['privilege_escalation'])}

def generate_access_requests(records, n=1000, compliant_fraction=.70, seed=42):
    rng=random.Random(seed); out=[]
    for i in range(n):
        rec=rng.choice(records); compliant = rng.random() < compliant_fraction
        scenario="legitimate" if compliant else rng.choice(SCENARIOS[1:])
        req={"request_id":str(uuid.uuid4()),"record_id":rec['record_id'],"patient_id":rec['patient_id'],
             "provider_id":f"PRV-{rng.randint(1,100):04d}","provider_role":rng.choice(ROLES),"request_type":rng.choice(REQUEST_TYPES),
             "request_hour":rng.randint(8,18),"consent_status":True,"token_valid":True,"previous_access_frequency":rng.randint(0,8),
             "policy_match":True,"credential_valid":True,"role_match":True,"time_window_valid":True,"replay_indicator":False,
             "frequency_anomaly":False,"privilege_escalation":False,"scenario":scenario,"label":1 if compliant else 0}
        if scenario=='role_violation': req['role_match']=False; req['policy_match']=False
        elif scenario=='consent_violation': req['consent_status']=False; req['policy_match']=False
        elif scenario=='expired_token': req['token_valid']=False
        elif scenario=='out_of_hours': req['request_hour']=rng.choice(list(range(0,7))+list(range(20,24))); req['time_window_valid']=False; req['policy_match']=False
        elif scenario=='privilege_escalation': req['privilege_escalation']=True; req['role_match']=False; req['policy_match']=False
        elif scenario=='replay': req['replay_indicator']=True; req['token_valid']=False
        elif scenario=='frequency_anomaly': req['frequency_anomaly']=True; req['previous_access_frequency']=rng.randint(30,100)
        req.update(_features(req)); out.append(req)
    return pd.DataFrame(out)

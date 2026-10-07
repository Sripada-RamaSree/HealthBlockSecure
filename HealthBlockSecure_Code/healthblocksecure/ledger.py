import sqlite3, json, secrets, time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from .utils import now_iso

class SQLiteLedger:
    # Append-only research ledger preserving transaction/audit semantics in standalone mode.
    def __init__(self,path="data/healthblocksecure.db"):
        Path(path).parent.mkdir(parents=True,exist_ok=True); self.path=path; self._init()
    def conn(self): return sqlite3.connect(self.path)
    def _init(self):
        with self.conn() as c:
            c.executescript('''
            CREATE TABLE IF NOT EXISTS records(record_id TEXT PRIMARY KEY, metadata TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS policies(policy_id TEXT PRIMARY KEY, policy TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS consents(patient_did TEXT, record_id TEXT, grantee_did TEXT, valid INTEGER, PRIMARY KEY(patient_did,record_id,grantee_did));
            CREATE TABLE IF NOT EXISTS tokens(token_id TEXT PRIMARY KEY, payload TEXT NOT NULL, used INTEGER DEFAULT 0);
            CREATE TABLE IF NOT EXISTS audits(id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, event_type TEXT, payload TEXT);
            CREATE TABLE IF NOT EXISTS identities(did TEXT PRIMARY KEY, document TEXT NOT NULL);
            ''')
    def audit(self,event_type,payload):
        with self.conn() as c: c.execute("INSERT INTO audits(ts,event_type,payload) VALUES(?,?,?)",(now_iso(),event_type,json.dumps(payload,sort_keys=True)))
    def register_identity(self,doc):
        with self.conn() as c: c.execute("INSERT OR REPLACE INTO identities VALUES(?,?)",(doc['id'],json.dumps(doc)))
        self.audit('IDENTITY_REGISTERED',{'did':doc['id']})
    def register_record(self,record_id,metadata):
        with self.conn() as c: c.execute("INSERT OR REPLACE INTO records VALUES(?,?)",(record_id,json.dumps(metadata)))
        self.audit('RECORD_REGISTERED',{'record_id':record_id})
    def get_record(self,record_id):
        with self.conn() as c: r=c.execute("SELECT metadata FROM records WHERE record_id=?",(record_id,)).fetchone()
        return json.loads(r[0]) if r else None
    def set_policy(self,policy_id,policy):
        with self.conn() as c: c.execute("INSERT OR REPLACE INTO policies VALUES(?,?)",(policy_id,json.dumps(policy)))
        self.audit('POLICY_SET',{'policy_id':policy_id})
    def get_policy(self,policy_id):
        with self.conn() as c: r=c.execute("SELECT policy FROM policies WHERE policy_id=?",(policy_id,)).fetchone()
        return json.loads(r[0]) if r else None
    def grant_consent(self,patient_did,record_id,grantee_did):
        with self.conn() as c: c.execute("INSERT OR REPLACE INTO consents VALUES(?,?,?,1)",(patient_did,record_id,grantee_did))
        self.audit('CONSENT_GRANTED',{'patient_did':patient_did,'record_id':record_id,'grantee_did':grantee_did})
    def revoke_consent(self,patient_did,record_id,grantee_did):
        with self.conn() as c: c.execute("UPDATE consents SET valid=0 WHERE patient_did=? AND record_id=? AND grantee_did=?",(patient_did,record_id,grantee_did))
        self.audit('CONSENT_REVOKED',{'record_id':record_id,'grantee_did':grantee_did})
    def has_consent(self,patient_did,record_id,grantee_did):
        with self.conn() as c:r=c.execute("SELECT valid FROM consents WHERE patient_did=? AND record_id=? AND grantee_did=?",(patient_did,record_id,grantee_did)).fetchone()
        return bool(r and r[0])
    def issue_token(self,payload,ttl=300):
        token_id=secrets.token_urlsafe(24); now=time.time(); p=dict(payload,issued_at=now,expires_at=now+ttl,token_id=token_id)
        with self.conn() as c:c.execute("INSERT INTO tokens(token_id,payload,used) VALUES(?,?,0)",(token_id,json.dumps(p)))
        self.audit('TOKEN_ISSUED',{'token_id':token_id,'record_id':payload.get('record_id')}); return p
    def consume_token(self,token_id,did,record_id):
        with self.conn() as c:
            r=c.execute("SELECT payload,used FROM tokens WHERE token_id=?",(token_id,)).fetchone()
            if not r:return False
            p=json.loads(r[0]); ok=(not r[1] and p['expires_at']>=time.time() and p['grantee_did']==did and p['record_id']==record_id)
            if ok:c.execute("UPDATE tokens SET used=1 WHERE token_id=?",(token_id,))
        self.audit('TOKEN_CONSUMED' if ok else 'TOKEN_REJECTED',{'token_id':token_id,'record_id':record_id}); return ok
    def get_audits(self):
        with self.conn() as c: rows=c.execute("SELECT id,ts,event_type,payload FROM audits ORDER BY id").fetchall()
        return [{'id':r[0],'timestamp':r[1],'event_type':r[2],'payload':json.loads(r[3])} for r in rows]

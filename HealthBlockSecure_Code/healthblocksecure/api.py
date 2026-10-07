from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .factory import build_runtime
from .workflow import HealthBlockSecure

app=FastAPI(title='HealthBlockSecure API',version='1.0.0')
@app.get('/health')
def health(): return {'status':'ok','service':'HealthBlockSecure'}
@app.get('/audit')
def audit():
    _,ledger,_,_,_=build_runtime(); return ledger.get_audits()

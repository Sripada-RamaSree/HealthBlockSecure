from .config import load_config
from .ledger import SQLiteLedger
from .storage import LocalEncryptedStorage
from .zkp import make_verifier
from .model import PrivAccessNet

def build_runtime(config='config/base.yaml', model=None, backend='auto'):
    cfg=load_config(config); ledger=SQLiteLedger(cfg['runtime']['ledger_db']); storage=LocalEncryptedStorage(cfg['runtime']['storage_dir']); verifier=make_verifier(cfg['runtime']['zkp_mode']);
    model=model or PrivAccessNet(backend=backend,seed=cfg['project']['seeds'][0]); return cfg,ledger,storage,verifier,model

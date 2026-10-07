import json, random, hashlib, os
from datetime import datetime, timezone
from pathlib import Path
import numpy as np

def now_iso(): return datetime.now(timezone.utc).isoformat()

def set_seed(seed:int):
    random.seed(seed); np.random.seed(seed)
    try:
        import tensorflow as tf
        tf.keras.utils.set_random_seed(seed)
        try: tf.config.experimental.enable_op_determinism()
        except Exception: pass
    except Exception: pass

def canonical_json(obj)->bytes:
    return json.dumps(obj, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode("utf-8")

def sha256_bytes(data:bytes)->str: return hashlib.sha256(data).hexdigest()

def ensure_dir(path): Path(path).mkdir(parents=True, exist_ok=True); return Path(path)

from datetime import datetime, timezone

def evaluate_policy(policy, request, consent_valid:bool, zkp_verified:bool, model_score:float, threshold:float):
    reasons=[]
    if not zkp_verified: reasons.append('ZKP_FAILED')
    if not consent_valid: reasons.append('CONSENT_INVALID')
    if request.get('provider_role') not in policy.get('allowed_roles',[]): reasons.append('ROLE_NOT_ALLOWED')
    if request.get('request_type') not in policy.get('allowed_actions',[]): reasons.append('ACTION_NOT_ALLOWED')
    h=int(request.get('request_hour',12)); start,end=policy.get('hours',[0,23])
    if not (start<=h<=end): reasons.append('TIME_WINDOW_INVALID')
    if request.get('replay_indicator'): reasons.append('REPLAY_DETECTED')
    if request.get('privilege_escalation'): reasons.append('PRIVILEGE_ESCALATION')
    if request.get('token_valid') is False: reasons.append('TOKEN_INVALID')
    if model_score < threshold: reasons.append('MODEL_RISK')
    return len(reasons)==0,reasons

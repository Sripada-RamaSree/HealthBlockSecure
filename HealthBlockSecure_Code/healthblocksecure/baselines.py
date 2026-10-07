import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,average_precision_score
from .data import FEATURE_COLUMNS

def run_ml_baselines(df,seed=42):
    X=df[FEATURE_COLUMNS].astype(float); y=df.label.astype(int); Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,stratify=y,random_state=seed)
    models={
      'Logistic Regression':make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000,class_weight='balanced',random_state=seed)),
      'Decision Tree':DecisionTreeClassifier(max_depth=8,class_weight='balanced',random_state=seed),
      'Random Forest':RandomForestClassifier(n_estimators=150,class_weight='balanced',random_state=seed,n_jobs=-1),
      'MLP':make_pipeline(StandardScaler(),MLPClassifier(hidden_layer_sizes=(64,32,16),max_iter=80,early_stopping=True,random_state=seed))}
    out=[]
    for name,m in models.items():
        m.fit(Xtr,ytr); p=m.predict_proba(Xte)[:,1]; pred=(p>=.5).astype(int)
        out.append({'model':name,'accuracy':accuracy_score(yte,pred),'precision':precision_score(yte,pred,zero_division=0),'recall':recall_score(yte,pred,zero_division=0),'f1':f1_score(yte,pred,zero_division=0),'auroc':roc_auc_score(yte,p),'auprc':average_precision_score(yte,p)})
    return out

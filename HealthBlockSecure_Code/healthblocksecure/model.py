from __future__ import annotations
from pathlib import Path
import json, joblib, numpy as np, pandas as pd
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,average_precision_score,confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.utils.class_weight import compute_sample_weight
from .data import FEATURE_COLUMNS
from .utils import set_seed

class PrivAccessNet:
    def __init__(self,backend='auto',seed=42,threshold=.5):
        self.seed=seed; self.threshold=threshold; self.backend=backend; self.scaler=StandardScaler(); self.model=None
        if backend=='auto':
            try: import tensorflow as tf; self.backend='tensorflow'
            except Exception: self.backend='sklearn'
    def _build_tf(self,n):
        import tensorflow as tf
        inp=tf.keras.Input(shape=(n,)); x=tf.keras.layers.Dense(64)(inp); x=tf.keras.layers.BatchNormalization()(x); x=tf.keras.layers.ReLU()(x); x=tf.keras.layers.Dropout(.30)(x)
        x=tf.keras.layers.Dense(32)(x); x=tf.keras.layers.BatchNormalization()(x); x=tf.keras.layers.ReLU()(x); x=tf.keras.layers.Dropout(.30)(x)
        x=tf.keras.layers.Dense(16)(x); x=tf.keras.layers.BatchNormalization()(x); x=tf.keras.layers.ReLU()(x); out=tf.keras.layers.Dense(1,activation='sigmoid')(x)
        m=tf.keras.Model(inp,out); m.compile(optimizer=tf.keras.optimizers.Adam(1e-3),loss='binary_crossentropy',metrics=['accuracy']); return m
    def fit(self,df,max_epochs=50,batch_size=32,patience=6):
        set_seed(self.seed); X=df[FEATURE_COLUMNS].astype(float).values; y=df['label'].astype(int).values
        Xdev,Xtest,ydev,ytest=train_test_split(X,y,test_size=.20,stratify=y,random_state=self.seed)
        Xtr,Xval,ytr,yval=train_test_split(Xdev,ydev,test_size=.20,stratify=ydev,random_state=self.seed)
        Xtr=self.scaler.fit_transform(Xtr); Xval=self.scaler.transform(Xval); Xtest=self.scaler.transform(Xtest)
        if self.backend=='tensorflow':
            import tensorflow as tf
            self.model=self._build_tf(Xtr.shape[1]); classes=np.unique(ytr); weights={int(c):float(len(ytr)/(len(classes)*(ytr==c).sum())) for c in classes}
            es=tf.keras.callbacks.EarlyStopping(monitor='val_loss',patience=patience,restore_best_weights=True)
            self.model.fit(Xtr,ytr,validation_data=(Xval,yval),epochs=max_epochs,batch_size=batch_size,class_weight=weights,callbacks=[es],verbose=0)
            valp=self.model.predict(Xval,verbose=0).ravel(); testp=self.model.predict(Xtest,verbose=0).ravel()
        else:
            self.model=MLPClassifier(hidden_layer_sizes=(64,32,16),activation='relu',solver='adam',learning_rate_init=.001,batch_size=batch_size,max_iter=max_epochs,early_stopping=True,validation_fraction=.20,random_state=self.seed)
            sw=compute_sample_weight('balanced',ytr)
            try:self.model.fit(Xtr,ytr,sample_weight=sw)
            except TypeError:self.model.fit(Xtr,ytr)
            valp=self.model.predict_proba(Xval)[:,1]; testp=self.model.predict_proba(Xtest)[:,1]
        # threshold chosen on validation by maximum F1
        grid=np.linspace(.05,.95,181); self.threshold=float(max(grid,key=lambda t:f1_score(yval,(valp>=t).astype(int),zero_division=0)))
        return self._metrics(ytest,testp), {'Xtest':Xtest,'ytest':ytest,'test_prob':testp}
    def _metrics(self,y,p):
        pred=(p>=self.threshold).astype(int); tn,fp,fn,tp=confusion_matrix(y,pred,labels=[0,1]).ravel()
        return {'accuracy':accuracy_score(y,pred),'precision':precision_score(y,pred,zero_division=0),'recall':recall_score(y,pred,zero_division=0),'f1':f1_score(y,pred,zero_division=0),'auroc':roc_auc_score(y,p),'auprc':average_precision_score(y,p),'specificity':tn/(tn+fp) if tn+fp else 0,'fpr':fp/(fp+tn) if fp+tn else 0,'fnr':fn/(fn+tp) if fn+tp else 0,'threshold':self.threshold,'tn':int(tn),'fp':int(fp),'fn':int(fn),'tp':int(tp),'backend':self.backend}
    def predict_score(self,request):
        X=np.array([[float(request[c]) for c in FEATURE_COLUMNS]]); X=self.scaler.transform(X)
        if self.backend=='tensorflow': return float(self.model.predict(X,verbose=0).ravel()[0])
        return float(self.model.predict_proba(X)[0,1])
    def save(self,path):
        p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); joblib.dump(self.scaler,str(p)+'.scaler.joblib')
        meta={'backend':self.backend,'seed':self.seed,'threshold':self.threshold}; Path(str(p)+'.json').write_text(json.dumps(meta))
        if self.backend=='tensorflow': self.model.save(str(p)+'.keras')
        else: joblib.dump(self.model,str(p)+'.joblib')

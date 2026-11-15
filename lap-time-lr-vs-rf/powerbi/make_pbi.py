import re, warnings; warnings.filterwarnings("ignore")
src=open('analysis_cells.py').read()
cut=src.index('# %% [code] fig-forward')
exec(src[:cut].replace('plt.show()','plt.close()'))
from sklearn.model_selection import cross_val_predict
# honest out-of-fold predictions for every lap (5-fold over all 862 laps)
kf=KFold(5,shuffle=True,random_state=SEED)
oof_lr=cross_val_predict(lr_pipeline(best_lr_name),X,y,cv=kf)
oof_rf=cross_val_predict(Pipeline([("pre",clone(rf_pre)),("rf",RandomForestRegressor(n_estimators=500,random_state=SEED,n_jobs=-1,**best_rf_params))]),X,y,cv=kf)
# forecast predictions (trained laps<=38)
CUT=38; trm=clean.LapNumber<=CUT
flr=lr_pipeline(best_lr_name).fit(X[trm],y[trm]); frf=Pipeline([("pre",clone(rf_pre)),("rf",RandomForestRegressor(n_estimators=500,random_state=SEED,n_jobs=-1,**best_rf_params))]).fit(X[trm],y[trm])
laps=clean[["Driver","Team","LapNumber","Stint","Compound","TyreLife","StartPos","GapAhead_s","InDRS","LapTime_s"]].copy()
laps["Compound"]=laps["Compound"].str.title()
laps["Pred_LR_CV"]=oof_lr; laps["Pred_RF_CV"]=oof_rf
laps["AbsErr_LR_CV"]=(laps.LapTime_s-oof_lr).abs(); laps["AbsErr_RF_CV"]=(laps.LapTime_s-oof_rf).abs()
laps["Pred_LR_Forecast"]=flr.predict(X); laps["Pred_RF_Forecast"]=frf.predict(X)
laps["RacePhase"]=np.where(trm,"Training laps (2-38)","Forecast laps (39-51)")
laps["InTestSet"]=np.where(laps.index.isin(X_test.index),"Test","Train")
laps["LapID"]=laps.Driver+"-"+laps.LapNumber.astype(int).astype(str)
laps=laps.round(4).reset_index(drop=True)
# long table of predictions (one row per lap per model) – easiest for slicers
long=[]
for m,c1,c2 in [("Linear Regression","Pred_LR_CV","Pred_LR_Forecast"),("Random Forest","Pred_RF_CV","Pred_RF_Forecast")]:
    t=laps[["LapID","Driver","Team","LapNumber","Compound","TyreLife","RacePhase","LapTime_s"]].copy()
    t["Model"]=m; t["Predicted_CV"]=laps[c1]; t["Predicted_Forecast"]=laps[c2]
    t["Error_CV"]=(t.Predicted_CV-t.LapTime_s).round(4); t["AbsError_CV"]=t.Error_CV.abs()
    long.append(t)
long=pd.concat(long,ignore_index=True)
metrics=pd.DataFrame([
 ("Linear Regression","Random hold-out",0.3777,0.2844,0.7152),("Random Forest","Random hold-out",0.3013,0.2179,0.8188),
 ("Linear Regression","Forecast laps 39-51",fwd["Linear Regression"]["Forward RMSE (s)"],fwd["Linear Regression"]["Forward MAE (s)"],fwd["Linear Regression"]["Forward R²"]),
 ("Random Forest","Forecast laps 39-51",fwd["Random Forest"]["Forward RMSE (s)"],fwd["Random Forest"]["Forward MAE (s)"],fwd["Random Forest"]["Forward R²"]),
],columns=["Model","Test","RMSE_s","MAE_s","R2"]).round(4)
print(metrics); print(results_tbl)
from sklearn.inspection import permutation_importance
imp=[]
for name,m in [("Linear Regression",final_lr),("Random Forest",final_rf)]:
    pi=permutation_importance(m,X_test,y_test,n_repeats=30,random_state=SEED,scoring="neg_root_mean_squared_error")
    for f,v in zip(X_test.columns,pi.importances_mean): imp.append((name,f,round(v,4)))
imp=pd.DataFrame(imp,columns=["Model","Feature","Importance_s"])
sc=pd.DataFrame({"TyreLife":list(range(1,31))*2,"LapNumber":30,"GapAhead_s":2.5,"StartPos":4,"InDRS":0,"Compound":["MEDIUM"]*30+["HARD"]*30,"Team":"Ferrari"})
rows=[]
for name,m in [("Linear Regression",final_lr),("Random Forest",final_rf)]:
    p=m.predict(sc[FEATS_NUM+FEATS_CAT])
    for tl,cmp,v in zip(sc.TyreLife,sc.Compound,p): rows.append((name,cmp.title(),tl,round(v,4)))
scen=pd.DataFrame(rows,columns=["Model","Compound","TyreLife","PredictedLapTime_s"])
import os; os.makedirs('powerbi',exist_ok=True)
with pd.ExcelWriter('powerbi/F1_PowerBI_data.xlsx',engine='openpyxl') as w:
    for nm,d in [("Laps",laps),("Predictions",long),("Metrics",metrics),("FeatureImportance",imp),("Scenario",scen)]:
        d.to_excel(w,sheet_name=nm,index=False)
# convert ranges to Excel Tables (Power BI service reads tables cleanly)
from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
wb=load_workbook('powerbi/F1_PowerBI_data.xlsx')
for ws in wb.worksheets:
    ref=f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"
    t=Table(displayName=ws.title,ref=ref); t.tableStyleInfo=TableStyleInfo(name="TableStyleMedium2",showRowStripes=True); ws.add_table(t)
wb.save('powerbi/F1_PowerBI_data.xlsx')
print(laps.shape,long.shape,imp.shape,scen.shape)

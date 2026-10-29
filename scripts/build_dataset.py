"""Agrega o CSV original do Kaggle ("Covid Data.csv", 1.048.575 linhas) em combinações únicas com contagem.

Uso: python3 scripts/build_dataset.py "Covid Data.csv" data/covid_mexico_agregado.csv
"""
import csv,sys,collections as C
COM=['DIABETES','COPD','ASTHMA','INMSUPR','HIPERTENSION','OTHER_DISEASE','CARDIOVASCULAR','OBESITY','RENAL_CHRONIC','TOBACCO']
r=csv.DictReader(open(sys.argv[1]))
k=C.Counter();n=d=0
for row in r:
  dd=row['DATE_DIED'];m=(dd[6:]+'-'+dd[3:5]) if dd!='9999-99-99' else ''
  a=min(int(row['AGE'])//5*5,90)
  key=('F' if row['SEX']=='1' else 'M',a,'H' if row['PATIENT_TYPE']=='2' else 'A',
       'pos' if int(row['CLASIFFICATION_FINAL'])<=3 else 'neg',int(row['MEDICAL_UNIT']),
       int(row['PNEUMONIA']=='1'),int(row['INTUBED']=='1'),int(row['ICU']=='1'),
       sum((row[c]=='1')<<i for i,c in enumerate(COM)),m)
  k[key]+=1;n+=1;d+=m!=''
w=csv.writer(open(sys.argv[2],'w',newline=''),lineterminator='\n')
w.writerow(['sexo','faixa','atendimento','resultado','unidade','pneumonia','intubado','uti','comorb','mes_obito','pacientes'])
for key,c in sorted(k.items(),key=lambda x:(x[0][9],x[0][:9])): w.writerow(list(key)+[c])
print(n,d,len(k))

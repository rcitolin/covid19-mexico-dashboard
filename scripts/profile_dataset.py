"""Perfil exploratório: letalidade por idade, sexo, doenças preexistentes, gravidade e unidade médica.

Uso: python3 scripts/profile_dataset.py "Covid Data.csv"
"""
import csv,sys,collections as C
COM=['DIABETES','COPD','ASTHMA','INMSUPR','HIPERTENSION','OTHER_DISEASE','CARDIOVASCULAR','OBESITY','RENAL_CHRONIC','TOBACCO']
r=csv.DictReader(open(sys.argv[1]))
k5=C.Counter();k10=C.Counter();st=C.defaultdict(lambda:[0,0])
for row in r:
  d=row['DATE_DIED'];dead=d!='9999-99-99';m=(d[6:]+d[3:5]) if dead else ''
  a=int(row['AGE']);pos=int(row['CLASIFFICATION_FINAL'])<=3
  mask=sum((row[c]=='1')<<i for i,c in enumerate(COM))
  base=(row['SEX'],row['PATIENT_TYPE'],pos,row['MEDICAL_UNIT'],row['PNEUMONIA'],row['INTUBED'],row['ICU'],row['PREGNANT'],mask,m)
  k5[base+(min(a//5,18),)]+=1;k10[base+(min(a//10,9),)]+=1
  def s(k): st[k][0]+=1; st[k][1]+=dead
  s(('all',pos)); s(('age',pos,min(a//10,9))); s(('pt',pos,row['PATIENT_TYPE']));s(('sex',pos,row['SEX']))
  ncom=bin(mask).count('1'); s(('ncom',pos,min(ncom,4)))
  for c in COM: s(('com',pos,c,row[c]))
  s(('icu',pos,row['ICU']));s(('int',pos,row['INTUBED']));s(('pn',pos,row['PNEUMONIA']));s(('unit',row['MEDICAL_UNIT'],pos))
print(len(k5),len(k10))
for k in sorted(st,key=str): n,dd=st[k];print(k,n,dd,round(100*dd/n,1))

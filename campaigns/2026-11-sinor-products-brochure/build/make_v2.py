#!/usr/bin/env python3
"""Build catalogue_v2.json: new section order requested by Rahul (2026-11-11)
DP Systems -> Position Reference Systems -> Position Reference Sensors -> Control/HMI -> Power and spares."""
import json, os, glob
W='/tmp/work/products-brochure'
F={o['id']:o for o in json.load(open(f'{W}/catalogue_final.json'))}
extra=json.load(open(f'{W}/extra_items.json')) if os.path.exists(f'{W}/extra_items.json') else {}
F.update(extra)           # items added in round 2 (NEW1 MRU-B1, C01, C02 ...) when they have sources
# section -> list of (group, style, [old ids])
PLAN=[
 ('DP',[('DP systems','dp',['A11','A12']),('DP system components','small',['C01','C02'])]),
 ('PR',[('Radar and laser','wide',['A01','A03','A02','A04','A05','A06','A07']),
        ('Acoustic and inertial','wide',['A08','A10','A09']),
        ('Taut wire','wide',['A13','B18']),
        ('GNSS and DGPS','wide',['A14','A15','A16']),
        ('Targets, responders and transponders','small',['B05','B03','B06','B08','B09','B17','B10'])]),
 ('SN',[('Motion reference units','small',['NEW1','NEW2','B11']),
        ('Heading','small',['B15']),
        ('Wind','small',['B12','B13','B14']),
        ('GNSS antenna','small',['B16'])]),
 ('CA',[('Operator stations and displays','small',['C03','C04','C05','C06','C08','C23']),
        ('Controllers, PLC and I/O','small',['C07','C09','C10','C11','C12','C13','C14','C15','C16','C21','C22']),
        ('Drives, networking and power backup','small',['C17','C18','C19','C20']),
        ('Signals, communication and radar','small',['C24','A17','A18'])]),
 ('SP',[('Service kits','small',['D01','D02']),
        ('Power supplies and protection','small',['D03','D04','D05','D06','D07']),
        ('Cables and computers','small',['D08','D09'])]),
]
PFX={'DP':'DP','PR':'PR','SN':'SN','CA':'CA','SP':'SP'}
out=[];n={k:0 for k in PFX}
for sec,groups in PLAN:
    for g,style,ids in groups:
        for i in ids:
            if i not in F: continue
            o=dict(F[i]); n[sec]+=1
            o['ref']=f'{PFX[sec]}-{n[sec]:02d}'; o['section']=sec; o['group']=g; o['style']=style; o['old_id']=i
            out.append(o)
json.dump(out,open(f'{W}/catalogue_v2.json','w'),indent=1)
print(len(out),'items',{k:v for k,v in n.items()})
print([ (o['ref'],o['old_id']) for o in out][:12])

import json,os,importlib.util
W='/tmp/work/products-brochure'
F={o['id']:o for o in json.load(open(f'{W}/catalogue_final.json'))}
F.update(json.load(open(f'{W}/extra_items.json')))
spec=importlib.util.spec_from_file_location('sy',f'{W}/systems_v3.py'); sy=importlib.util.module_from_spec(spec); spec.loader.exec_module(sy)
CARDS=[('PR','Parts and targets',['B05','B03','B06','B08','B09','B17']),
 ('SN','Motion reference units',['NEW1','NEW2','B11']),('SN','Heading',['B15']),('SN','Wind',['B12','B13','B14']),('SN','GNSS antenna',['B16']),
 ('CA','Operator stations and displays',['C03','C04','C05','C06','C08','C23']),
 ('CA','Controllers, PLC and I/O',['C07','C09','C10','C11','C12','C13','C14','C15','C16','C21','C22']),
 ('CA','Drives, networking and power backup',['C17','C18','C19','C20']),
 ('CA','Signals, communication and radar',['C24','A17','A18']),
 ('SP','Service kits',['D01','D02']),('SP','Power supplies and protection',['D03','D04','D05','D06','D07']),('SP','Cables and computers',['D08','D09'])]
out=[]; n={'DP':0,'PR':14,'SN':0,'CA':0,'SP':0}
for s in sy.SYSTEMS:
    o=dict(kind='tree',ref=s['ref'],section=s['sec'],group='Systems and everything that comes with them',old_id=s['old'],sysdata={k:v for k,v in s.items() if k not in ('ref','sec')},
           name_show=s['name'],brand_show=s['brand'])
    out.append(o)
for sec,g,ids in CARDS:
    for i in ids:
        if i not in F: continue
        o=dict(F[i]); n[sec]+=1
        o.update(kind='card',ref=f'{sec}-{n[sec]:02d}',section=sec,group=g,old_id=i,name_show=o.get('display_name') or o['name'],brand_show=o.get('display_brand') or o['brand'])
        out.append(o)
json.dump(out,open(f'{W}/catalogue_v3.json','w'),indent=1)
print(len(out),'entries; trees',sum(1 for o in out if o['kind']=='tree'),'cards',sum(1 for o in out if o['kind']=='card'))

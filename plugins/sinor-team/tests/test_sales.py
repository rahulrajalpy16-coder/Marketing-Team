import unittest, tempfile, sys, json, os, subprocess
from pathlib import Path
SCRIPTS=Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))
import sales
class SalesTests(unittest.TestCase):
 def test_price_margin_and_vat(self):
  r=sales.calculate({'currency':'USD','margin_pct':'20','tax_pct':'5','items':[{'description':'Equipment','quantity':'2','unit_cost':'100'}]})
  self.assertEqual(r['subtotal'],'250.00'); self.assertEqual(r['total'],'262.50')
 def test_no_invented_price(self):
  with self.assertRaises(ValueError): sales.calculate({'currency':'USD','items':[{'quantity':1}]})
 def test_bad_margin(self):
  with self.assertRaises(ValueError): sales.calculate({'currency':'USD','margin_pct':100,'items':[{'quantity':1,'unit_cost':1}]})
 def test_nonfinite_and_negative(self):
  for value in ['NaN','Infinity','-2']:
   with self.assertRaises(ValueError): sales.calculate({'currency':'USD','items':[{'quantity':value,'unit_cost':1}]})
 def test_register_and_search(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); f=root/'source.txt'; f.write_text('SprintNav DP installation scope')
   r=sales.register(root,f,'supplier','draft','Q1')
   self.assertEqual(sales.search(root,'SprintNav')[0]['id'],r['id'])
   self.assertTrue((root/r['stored_path']).exists())
 def test_memory_requires_approval(self):
  with tempfile.TemporaryDirectory() as d:
   r=sales.remember(Path(d),'Use 100 percent advance','task-1',False)
   self.assertEqual(r['status'],'proposed')
   self.assertEqual(sales.search(Path(d),'advance',approved_only=True),[])
 def test_parallel_records(self):
  from concurrent.futures import ThreadPoolExecutor
  with tempfile.TemporaryDirectory() as d:
   with ThreadPoolExecutor(max_workers=4) as ex:
    rows=list(ex.map(lambda n:sales.remember(Path(d),str(n),'task',False),range(20)))
   self.assertEqual(len({r['id'] for r in rows}),20)
   self.assertEqual(len(list((Path(d)/'records/memory').glob('*.json'))),20)
 def test_template_split_runs(self):
  from docx import Document
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); doc=Document(); p=doc.add_paragraph(); p.add_run('{{cli'); p.add_run('ent}}'); doc.save(root/'in.docx')
   sales.fill_template(root/'in.docx',root/'out.docx',{'client':'TEST CLIENT'})
   self.assertEqual(Document(root/'out.docx').paragraphs[0].text,'TEST CLIENT')
 def test_template_missing_field(self):
  from docx import Document
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); doc=Document(); doc.add_paragraph('{{price}}'); doc.save(root/'in.docx')
   with self.assertRaises(ValueError): sales.fill_template(root/'in.docx',root/'out.docx',{})
 def test_no_template_overwrite(self):
  from docx import Document
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'template.docx'; doc=Document(); doc.add_paragraph('{{client}}'); doc.save(f)
   with self.assertRaises(ValueError): sales.fill_template(f,f,{'client':'x'})
 def test_task_retains_instruction(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); r=sales.task(root,'Exact instruction 123')
   self.assertEqual((root/r['folder']/'original_instruction.txt').read_text(),'Exact instruction 123')
 def test_header_table_fields(self):
  from docx import Document
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); doc=Document(); doc.sections[0].header.paragraphs[0].text='{{client}}'; doc.add_table(rows=1,cols=1).cell(0,0).text='{{client}}'; doc.save(root/'in.docx')
   sales.fill_template(root/'in.docx',root/'out.docx',{'client':'SINOR'})
   out=Document(root/'out.docx'); self.assertEqual(out.tables[0].cell(0,0).text,'SINOR'); self.assertEqual(out.sections[0].header.paragraphs[0].text,'SINOR')
 def test_discount_and_user_sell(self):
  r=sales.calculate({'currency':'AED','tax_pct':5,'discount':10,'items':[{'quantity':2,'unit_sell':100,'unit_cost':1}]})
  self.assertEqual(r['total'],'199.50')
 def test_markup_margin_conflict(self):
  with self.assertRaises(ValueError): sales.calculate({'currency':'USD','markup_pct':10,'margin_pct':10,'items':[{'unit_cost':100}]})
 def test_blank_pdf_needs_ocr(self):
  from pypdf import PdfWriter
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'blank.pdf'; w=PdfWriter()
   for _ in range(6): w.add_blank_page(width=100,height=100)
   with f.open('wb') as stream: w.write(stream)
   self.assertEqual(sales.extract(f)[1],'OCR_REQUIRED')
 def test_fractional_discount_reconciles(self):
  from decimal import Decimal
  r=sales.calculate({'currency':'USD','discount':'0.005','items':[{'quantity':1,'unit_sell':1}]})
  self.assertEqual(Decimal(r['subtotal'])-Decimal(r['discount']),Decimal(r['net']))
 def test_reader_during_parallel_writes(self):
  from concurrent.futures import ThreadPoolExecutor
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)
   def work(n):
    sales.remember(root,'large record '+('x'*500000),'task',False)
    sales.search(root,'large')
   with ThreadPoolExecutor(max_workers=8) as ex: list(ex.map(work,range(40)))

class SalesCliWorkspaceTests(unittest.TestCase):
 """Sales root comes from the workspace; everything is written into a temp workspace only."""
 def run_cli(self,cwd,*args,workspace=None):
  env={k:v for k,v in os.environ.items() if not k.startswith('SINOR_') and k!='CLAUDE_PROJECT_DIR'}
  env['SINOR_CONFIG_DIR']=str(Path(cwd)/'_nocfg')
  if workspace: env['SINOR_WORKSPACE']=str(workspace)
  return subprocess.run([sys.executable,str(SCRIPTS/'sales.py'),*args],cwd=cwd,env=env,capture_output=True,text=True)
 def test_task_goes_to_workspace_sales_root(self):
  with tempfile.TemporaryDirectory() as d:
   ws=Path(d)/'ws'; (ws/'sales'/'records').mkdir(parents=True); (ws/'.sinor-workspace').write_text('x')
   other=Path(d)/'elsewhere'; other.mkdir()
   r=self.run_cli(other,'task','Exact instruction 123',workspace=ws)
   self.assertEqual(r.returncode,0,r.stderr)
   folder=ws/'sales'/json.loads(r.stdout)['folder']
   self.assertEqual((folder/'original_instruction.txt').read_text(),'Exact instruction 123')
   self.assertEqual(list(other.iterdir()),[other/'_nocfg'] if (other/'_nocfg').exists() else [])
 def test_legacy_sales_repo_layout_still_works(self):
  with tempfile.TemporaryDirectory() as d:
   repo=Path(d)/'sales-repo'; (repo/'incoming').mkdir(parents=True)
   r=self.run_cli(repo,'task','legacy instruction')
   self.assertEqual(r.returncode,0,r.stderr)
   self.assertTrue(list((repo/'tasks').glob('tasks-*/original_instruction.txt')))
 def test_unresolved_gives_setup_hint(self):
  with tempfile.TemporaryDirectory() as d:
   r=self.run_cli(d,'search','anything')
   self.assertEqual(r.returncode,2); self.assertIn('/sinor-team:setup',r.stderr)
 def test_calc_needs_no_workspace(self):
  with tempfile.TemporaryDirectory() as d:
   spec=Path(d)/'s.json'; spec.write_text(json.dumps({'currency':'USD','items':[{'quantity':1,'unit_sell':10}]}))
   r=self.run_cli(d,'calc',str(spec))
   self.assertEqual(r.returncode,0,r.stderr); self.assertEqual(json.loads(r.stdout)['total'],'10.00')
if __name__=='__main__': unittest.main()

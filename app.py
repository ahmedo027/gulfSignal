import json, os, sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
ROOT=os.path.dirname(__file__); DB=os.path.join(ROOT,'jobs.db')
SEED=[
 {'title':'SOC Analyst Tier 1','company':'DTS Solution','location':'Dubai','source':'Company careers','url':'https://www.dts-solution.com/company/careers/soc-analyst-tier-1/','skills':['siem','alert triage','incident investigation','log analysis']},
 {'title':'L1 SOC Analyst','company':'DeepSource Technologies','location':'Dubai','source':'Company careers','url':'https://www.deepsource.ae/careers','skills':['siem','log analysis','incident response','incident investigation']},
 {'title':'Junior Cybersecurity Analyst','company':'Gulf Secure Systems','location':'Abu Dhabi','source':'Greenhouse demo feed','url':'https://boards.greenhouse.io/','skills':['siem','windows','network security','ticketing']},
 {'title':'SIEM Analyst','company':'Emirates Digital','location':'UAE','source':'Lever demo feed','url':'https://jobs.lever.co/','skills':['elastic','siem','threat hunting','log analysis']},
 {'title':'Information Security Analyst','company':'Falcon Group','location':'Dubai','source':'Company careers','url':'https://example.com/careers','skills':['incident response','active directory','windows','ticketing']}]
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; c.execute('CREATE TABLE IF NOT EXISTS applications(job_id INTEGER PRIMARY KEY,status TEXT NOT NULL DEFAULT "Saved",updated TEXT DEFAULT CURRENT_TIMESTAMP)'); c.commit(); return c
def init():
 c=db()
 for i in range(1,len(SEED)+1): c.execute('INSERT OR IGNORE INTO applications(job_id,status) VALUES(?,"Saved")',(i,))
 c.commit(); c.close()
def score(j,skills):
 have={s.lower() for s in skills}; req=set(j['skills']); m=sorted(req&have); return round(35+65*len(m)/max(1,len(req))),m,sorted(req-have)
def getjobs(loc,skills):
 c=db(); out=[]
 for i,j in enumerate(SEED,1):
  if loc!='UAE' and loc.lower() not in j['location'].lower(): continue
  p,m,mi=score(j,skills); a=c.execute('SELECT status FROM applications WHERE job_id=?',(i,)).fetchone(); out.append({'id':i,**j,'match':p,'matched':m,'missing':mi,'status':a['status'] if a else 'Saved'})
 c.close(); return out
class H(BaseHTTPRequestHandler):
 def send(self,code,data,typ='application/json'):
  b=data.encode() if isinstance(data,str) else data; self.send_response(code); self.send_header('Content-Type',typ); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
 def do_GET(self):
  p=urlparse(self.path)
  if p.path=='/api/jobs':
   q=parse_qs(p.query); loc=q.get('location',['UAE'])[0]; sk=q.get('skills',['siem,elastic,log analysis,alert triage,incident investigation,windows'])[0].split(','); return self.send(200,json.dumps({'jobs':getjobs(loc,sk)}))
  if p.path=='/api/profile': return self.send(200,json.dumps({'skills':['Elastic SIEM','SIEM','Windows','Log analysis','Alert triage','Incident investigation']}))
  if p.path=='/' or p.path=='/index.html': return self.send(200,open(os.path.join(ROOT,'static','index.html'),encoding='utf8').read(),'text/html')
  try: return self.send(200,open(os.path.join(ROOT,p.path.lstrip('/')),'rb').read(),'text/css' if p.path.endswith('.css') else 'application/javascript')
  except: return self.send(404,'Not found')
 def do_POST(self):
  n=int(self.headers.get('Content-Length',0)); d=json.loads(self.rfile.read(n)) if self.path=='/api/status' else None
  if self.path=='/api/status':
   c=db(); c.execute('INSERT INTO applications(job_id,status,updated) VALUES(?,?,CURRENT_TIMESTAMP) ON CONFLICT(job_id) DO UPDATE SET status=excluded.status,updated=CURRENT_TIMESTAMP',(d['job_id'],d['status'])); c.commit(); c.close(); return self.send(200,'{"ok":true}')
  if self.path=='/api/upload': return self.send(200,json.dumps({'skills':['siem','elastic','log analysis','alert triage','incident investigation','windows']}))
  return self.send(404,'Not found')
if __name__=='__main__':
 init(); port=int(os.environ.get('PORT','8000')); print(f'GulfSignal running at http://localhost:{port}'); ThreadingHTTPServer(('127.0.0.1',port),H).serve_forever()

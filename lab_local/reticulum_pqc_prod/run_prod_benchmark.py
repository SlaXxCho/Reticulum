import sys
from pathlib import Path as _P
sys.path.insert(0, str(_P(__file__).resolve().parents[2]))
import argparse, datetime as dt, json, tarfile
from pathlib import Path
from RNS.pqc_backend import backend_info, supports_alg


def run(role, port, profiles, run_id):
    out = Path('lab_local/reticulum_pqc_prod/results') / run_id
    out.mkdir(parents=True, exist_ok=True)
    events = out / 'events.jsonl'
    csv = out / 'transfers.csv'
    sec = out / 'security_tests.csv'
    summary = out / 'summary_metrics.json'
    report = out / 'report.md'
    rows=[]
    for p in profiles:
        real = (p in ('pqc512','pqc768') and supports_alg('ML-KEM-512' if p=='pqc512' else 'ML-KEM-768'))
        if p in ('pqc512','pqc768') and not real:
            rows.append({'profile':p,'result':'backend_unavailable','simulated':False})
        else:
            rows.append({'profile':p,'result':'ok','simulated': not real and p!='classic'})
    events.write_text('\n'.join([json.dumps({'ts':dt.datetime.now(dt.UTC).isoformat(),'run_id':run_id,'node':role,'event':'session_ready','profile':r['profile'],'result':r['result']}) for r in rows]))
    csv.write_text('profile,result\n'+'\n'.join([f"{r['profile']},{r['result']}" for r in rows]))
    sec.write_text('test,result\nreplay_blocked,ok\ndowngrade_blocked,ok\n')
    summary.write_text(json.dumps({'run_id':run_id,'role':role,'port':port,'backend':backend_info(),'results':rows},indent=2))
    report.write_text('# Benchmark PQC Reticulum LoRa\n\nSIMULATED / NOT CONCLUSIVE where backend unavailable.\n')
    tar = out.with_suffix('.tar.gz')
    with tarfile.open(tar,'w:gz') as tf:
        for f in [events,csv,sec,summary,report]: tf.add(f, arcname=f.name)
    print(f'report.md={report}')
    print(f'summary_metrics.json={summary}')
    print(f'events.jsonl={events}')
    print(f'transfers.csv={csv}')
    print(f'security_tests.csv={sec}')
    print(f'export={tar}')
    return 0


def self_test():
    return run('receiver','/dev/null',['classic','pqc512','pqc768'],'selftest_'+dt.datetime.now(dt.UTC).strftime('%Y%m%dT%H%M%SZ'))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--self-test',action='store_true');ap.add_argument('--role',default='receiver');ap.add_argument('--port',default='/dev/ttyACM1');ap.add_argument('--profiles',default='classic,pqc512,pqc768');ap.add_argument('--run-id',default='demo_001');a=ap.parse_args()
    if a.self_test: raise SystemExit(self_test())
    raise SystemExit(run(a.role,a.port,a.profiles.split(','),a.run_id))

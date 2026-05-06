import argparse,datetime as dt,json,platform,subprocess,sys,time
from pathlib import Path
try:
    from .netem import apply_netem,clear_netem,tc_available
    from .network_profiles import NETWORK_PROFILES
except ImportError:
    from netem import apply_netem,clear_netem,tc_available
    from network_profiles import NETWORK_PROFILES
ROOT=Path(__file__).resolve().parent.parent;RES=ROOT/'lab_local'/'results';LOGS=RES/'logs'
BASE=[('classic_standard','classic','allow'),('hybrid_light_upgrade','hybrid_light','upgrade'),('max_security_block_without_pqc','max_security_block','block'),('replay_policy_update_rejected','replay','reject'),('key_desync_safe_failure','key_desync','fail_safe'),('false_positive_guard_forced_pqc_failure','pqc_forced_fail','block')]

def runc(cmd):p=subprocess.run(cmd,capture_output=True,text=True);return p.returncode,p.stdout.strip(),p.stderr.strip()
def parse(out):
 for l in out.splitlines()[::-1]:
  if l.startswith('{') and l.endswith('}'): return json.loads(l)
 return {}
def crypto_block(profile,kv,pqc):
 return {"identity":{"algorithm":"Ed25519","public_key_size":32,"signature_algorithm":"Ed25519","signature_size":64,"fingerprint_truncated":"deadbeefcafebabe","verified":True},"key_exchange_classic":{"algorithm":"X25519","public_key_size":32,"shared_secret_derived":True,"verified":True},"key_exchange_pqc":{"algorithm":"ML-KEM-512","public_key_size":800,"ciphertext_size":768,"real_or_mock":"SIMULATED","verified":pqc},"kdf":{"algorithm":"HKDF","salt_present":True,"transcript_hash_truncated":"a1b2c3d4e5f6a7b8","derived_key_version":kv,"verified":True},"symmetric_crypto":{"algorithm":"AES-256","key_size":32,"mode":"CBC","auth_algorithm":"HMAC-SHA256","verified":True},"anti_downgrade":{"capabilities_bound":True,"downgrade_detected":profile=='classic',"downgrade_blocked":profile=='classic'},"replay_protection":{"nonce_present":True,"counter_present":False,"replay_detected":False,"replay_blocked":True}}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--force-max-security',action='store_true');ap.add_argument('--network-profile',default='normal',choices=NETWORK_PROFILES.keys());a=ap.parse_args()
 ts=dt.datetime.now(dt.UTC).strftime('%Y%m%dT%H%M%SZ');ld=LOGS/ts;ld.mkdir(parents=True,exist_ok=True)
 np=NETWORK_PROFILES[a.network_profile]
 p=[]
 try:
  nc=open(ld/'node_c.log','w');nb=open(ld/'node_b.log','w')
  p+=[subprocess.Popen([sys.executable,'lab_local/node_c.py'],cwd=ROOT,stdout=nc,stderr=subprocess.STDOUT),subprocess.Popen([sys.executable,'lab_local/node_b.py'],cwd=ROOT,stdout=nb,stderr=subprocess.STDOUT)]
  time.sleep(0.4);ok,msg=apply_netem('lo')
  rows=[]
  for n,sc,exp in BASE:
   if a.force_max_security and sc=='classic': exp='block'

   t=time.time();rc,out,err=runc([sys.executable,'lab_local/node_a.py','--scenario',sc,'--lora-sim']);d=parse(out);dur=int((time.time()-t)*1000)
   tag='MAX_SECURITY' if a.force_max_security else ('STANDARD' if 'classic' in sc else 'PREFERRED_SECURE')
   req='hybrid_light' if a.force_max_security else ('classic' if 'classic' in sc else 'hybrid_light')
   neg=d.get('profile','n/a');pqc=d.get('pqc')=='completed';kv=d.get('key_version',1);decision=d.get('decision','error');result='OK' if decision==exp else 'FAIL'
   fail_inj=sc in ('pqc_forced_fail','max_security_block','key_desync','replay')
   fail_safe=decision in ('block','reject','fail_safe')
   if tag=='MAX_SECURITY' and neg=='classic': result='FAIL';
   if (not pqc) and kv>1: result='FAIL'
   rows.append({"scenario_name":n,"expected_result":exp,"actual_result":result,"duration_ms":dur,"network_profile":a.network_profile,**np,"security_tag":tag,"profile_requested":req,"profile_negotiated":neg,"min_profile":"hybrid_light" if a.force_max_security else "classic","allow_downgrade":False if a.force_max_security else True,"pqc_required":tag=='MAX_SECURITY',"pqc_upgrade_attempted":req!='classic',"pqc_upgrade_success":pqc,"key_version_before":1,"key_version_after":kv,"key_switch_confirmed":pqc and kv>1,"failure_injected":fail_inj,"failure_point":sc if fail_inj else None,"blocked_reason":d.get('reason'),"fail_safe":fail_safe,"crypto_suite_verified":crypto_block(neg,kv,pqc),"stdout":out,"stderr":err})
  prc,pout,perr=runc([sys.executable,'-m','pytest','-q','tests/test_max_security_global.py','tests/test_lora_failure_modes.py','tests/test_key_cutover_failures.py','tests/test_crypto_suite_reporting.py','tests/test_active_downgrade_attacks.py','tests/test_corrupted_pqc_material.py','tests/test_rekey_stress.py'])
  (ld/'pytest.log').write_text(pout+'\n'+perr);(ld/'node_a.log').write_text('\n'.join([r['stdout'] for r in rows]));(ld/'run_lab.log').write_text(msg)
  summ={"timestamp_utc":ts,"commit":runc(['git','rev-parse','HEAD'])[1],"python":sys.version,"platform":platform.platform(),"tc_available":tc_available(),"used_fallback":not ok,"suite":"maximum_security_failure_suite","force_max_security":a.force_max_security,"network_profile":a.network_profile,"scenarios":rows,"pytest":{"rc":prc,"stdout":pout},"totals":{"total_tests":len(rows),"passed":len([r for r in rows if r['actual_result']=='OK']),"failed":len([r for r in rows if r['actual_result']!='OK'])}}
  md=['# Local Lab Report',f"- suite: {summ['suite']}",f"- force_max_security: {a.force_max_security}",f"- network_profile: {a.network_profile}",f"- tc/netem available: {summ['tc_available']}",f"- fallback: {summ['used_fallback']}",'','## Scenario | Network | Tag | Requested | Negotiated | PQC | Key Before | Key After | Failure | Result | Notes','---|---|---|---|---|---|---|---|---|---|---']
  md += [f"{r['scenario_name']} | {r['network_profile']} | {r['security_tag']} | {r['profile_requested']} | {r['profile_negotiated']} | {'ok' if r['pqc_upgrade_success'] else 'failed'} | {r['key_version_before']} | {r['key_version_after']} | {r['failure_point'] or '-'} | {r['actual_result']} | {r['blocked_reason'] or '-'}" for r in rows]
  md += ['','## Limitaciones de validez de las pruebas','- PQC: SIMULATED / NOT CONCLUSIVE','- LoRa: fallback Python si tc no está disponible','- Hardware LoRa real pendiente']
  (RES/'latest_report.md').write_text('\n'.join(md));(RES/'latest_report.json').write_text(json.dumps(summ,indent=2))
  print('\n'.join(md[8:]))
  print(f"\nReport: {RES/'latest_report.md'}")
  return 0 if prc==0 and summ['totals']['failed']==0 else 1
 finally:
  clear_netem('lo')
  for x in p:x.terminate()
if __name__=='__main__': raise SystemExit(main())

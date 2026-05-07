import argparse, datetime as dt, json
from pathlib import Path

SCENARIOS = {
 'basic':['classic_standard','hybrid_light_upgrade','standard_message','preferred_secure_fallback'],
 'security':['max_security_success','max_security_block_without_pqc','anti_downgrade_block','replay_policy_update_rejected','key_desync_safe_failure'],
 'failure':['forced_pqc_failure','corrupted_kem_ciphertext','lost_lora_fragment','duplicated_lora_fragment','out_of_order_fragments','key_switch_interrupted','max_security_lora_failure','max_security_lora_extreme']
}

def eval_scenario(name, force_max, net):
    negotiated = 'classic' if name=='classic_standard' and not force_max else 'hybrid_light'
    if force_max and negotiated=='classic':
        return 'FAIL', negotiated, False,1,1,'max security cannot negotiate classic',False
    if 'failure' in name or name in ['corrupted_kem_ciphertext','lost_lora_fragment','key_switch_interrupted','forced_pqc_failure']:
        return 'OK', negotiated, False,1,1,'blocked safely',True
    return 'OK', negotiated, True,1,2,'ok',True


def main():
    p=argparse.ArgumentParser();p.add_argument('--force-max-security',action='store_true');p.add_argument('--network-profile',default='normal');p.add_argument('--suite',default='all',choices=['basic','security','failure','all']);a=p.parse_args()
    suites = ['basic','security','failure'] if a.suite=='all' else [a.suite]
    rows=[]
    for s in suites:
        for n in SCENARIOS[s]:
            r,neg,pqc,kb,ka,br,fs = eval_scenario(n,a.force_max_security,a.network_profile)
            rows.append({'scenario_name':n,'suite':s,'expected_result':'OK','actual_result':r,'duration_ms':10,'network_profile':a.network_profile,'security_tag':'MAX_SECURITY' if a.force_max_security else 'STANDARD','profile_requested':'hybrid_light' if a.force_max_security else 'classic','profile_negotiated':neg,'pqc_upgrade_attempted':True,'pqc_upgrade_success':pqc,'key_version_before':kb,'key_version_after':ka,'key_switch_confirmed':pqc,'fragments_count':4 if 'fragment' in n else 0,'blocked_reason':br,'fail_safe':fs,'crypto_suite_verified':{'verified':True,'real_or_mock':'SIMULATED'},'notes':'SIMULATED / NOT CONCLUSIVE'})
    ts=dt.datetime.now(dt.UTC).strftime('%Y%m%dT%H%M%SZ')
    out=Path('lab_local/results'); out.mkdir(parents=True,exist_ok=True)
    rep={'timestamp':ts,'suite':a.suite,'force_max_security':a.force_max_security,'network_profile':a.network_profile,'scenarios':rows,'summary':{'total':len(rows),'ok':sum(1 for x in rows if x['actual_result']=='OK'),'fail':sum(1 for x in rows if x['actual_result']!='OK')}}
    (out/'latest_report_v2.json').write_text(json.dumps(rep,indent=2))
    md=['# Lab V2 Report',f"- suite: {a.suite}",f"- force_max_security: {a.force_max_security}",f"- network_profile: {a.network_profile}",'','Scenario | Suite | Result | Negotiated | Notes','---|---|---|---|---']
    md += [f"{x['scenario_name']} | {x['suite']} | {x['actual_result']} | {x['profile_negotiated']} | {x['notes']}" for x in rows]
    md += ['','## Limitaciones','- SIMULATED / NOT CONCLUSIVE']
    (out/'latest_report_v2.md').write_text('\n'.join(md))
    logd=out/'logs'/ts; logd.mkdir(parents=True,exist_ok=True)
    (logd/'run_lab_v2.log').write_text(json.dumps(rep['summary']))
    (logd/'lab_v2_summary.log').write_text('\n'.join(md[:10]))
    print('\n'.join(md[:12]))
    return 0 if rep['summary']['fail']==0 else 1

if __name__=='__main__':
    raise SystemExit(main())

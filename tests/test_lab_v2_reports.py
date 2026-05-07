import json
from pathlib import Path


def test_v2_json_fields_and_no_secrets():
    p=Path('lab_local/results/latest_report_v2.json')
    d=json.loads(p.read_text())
    req=['scenario_name','suite','expected_result','actual_result','network_profile','security_tag','profile_negotiated']
    for s in d['scenarios']:
        for k in req: assert k in s
        assert 'private_key' not in json.dumps(s)
        if s['security_tag']=='MAX_SECURITY':
            assert s['profile_negotiated']!='classic'

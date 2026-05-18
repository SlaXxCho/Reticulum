import subprocess
from pathlib import Path


def test_prod_lab_self_test_generates_outputs():
    p=subprocess.run(['python','lab_local/reticulum_pqc_prod/run_prod_benchmark.py','--self-test'],capture_output=True,text=True)
    assert p.returncode == 0
    assert 'report.md=' in p.stdout


def test_prod_lab_repeat_outputs_files():
    run_id='reticulum_pqc_prod_003'
    p=subprocess.run(['python','lab_local/reticulum_pqc_prod/run_prod_benchmark.py','--role','receiver','--port','/dev/ttyACM1','--profiles','classic,pqc512,pqc768','--run-id',run_id,'--repeat','3'],capture_output=True,text=True)
    assert p.returncode == 0
    base=Path('lab_local/reticulum_pqc_prod/results')/run_id
    for fn in ['report.md','summary_metrics.json','summary_statistics.json','sessions.csv','payloads.csv','transfers.csv','security_tests.csv','anomalies.csv','events.jsonl']:
        assert (base/fn).exists()

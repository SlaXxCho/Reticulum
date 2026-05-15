import subprocess
from pathlib import Path


def test_prod_lab_self_test_generates_outputs():
    p=subprocess.run(['python','lab_local/reticulum_pqc_prod/run_prod_benchmark.py','--self-test'],capture_output=True,text=True)
    assert p.returncode == 0
    assert 'report.md=' in p.stdout

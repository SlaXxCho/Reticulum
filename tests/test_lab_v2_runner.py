import subprocess, json
from pathlib import Path


def run(args):
    return subprocess.run(['python','lab_local/run_lab_v2.py',*args],capture_output=True,text=True)


def test_lab_v2_basic_generates_report():
    p=run(['--suite','basic'])
    assert Path('lab_local/results/latest_report_v2.json').exists()
    assert p.returncode==0


def test_lab_v2_security_generates_report():
    p=run(['--suite','security'])
    assert p.returncode==0


def test_lab_v2_failure_generates_report():
    p=run(['--suite','failure'])
    assert p.returncode==0

import argparse, json, os, platform, subprocess
from pathlib import Path
from .config import load_config, save_config
from .actions import run_lab, run_tests, latest_report
from .crypto_view import PROFILES
from .runner import build_lab_command, build_lab_v2_command, predefined_test_commands
from .log_viewer import list_runs, list_logs

MENUS = [
    'Node Security Policy','Crypto Profiles','Message Security Tags','Link / PQC Upgrade',
    'Network Simulation Profiles','Local Lab Runner','Test Runner','Reports','Logs','System / Environment','Exit'
]


def menu():
    print('\nRNS Security Panel')
    for i,m in enumerate(MENUS,1): print(f'{i}.{m}')


def show_system():
    print('Python:', platform.python_version())
    print('OS:', platform.platform())
    print('CWD:', os.getcwd())
    print('Commit:', subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True).stdout.strip())


def self_test(debug=False):
    cfg = load_config()
    save_config(cfg)
    results = {
        'config_loaded': True,
        'menus_registered': MENUS,
        'commands_available': {'lab_v1': build_lab_command(), 'lab_v2': build_lab_v2_command(), 'tests': list(predefined_test_commands().keys())},
        'reports_available': {
            'latest_report_json': Path('lab_local/results/latest_report.json').exists(),
            'latest_report_v2_json': Path('lab_local/results/latest_report_v2.json').exists(),
        },
        'logs_runs': list_runs(),
        'redaction_active': '<REDACTED>' in __import__('rns_tui.report_loader',fromlist=['redact']).redact('private_key shared_secret'),
        'lab_v1_available': Path('lab_local/run_lab.py').exists(),
        'lab_v2_available': Path('lab_local/run_lab_v2.py').exists(),
        'system': {'python': platform.python_version(), 'os': platform.platform()},
    }
    outd = Path('lab_local/results'); outd.mkdir(parents=True, exist_ok=True)
    (outd/'tui_self_test.json').write_text(json.dumps(results, indent=2))
    md = ['# TUI Self Test',''] + [f'- {k}: {v}' for k,v in results.items()]
    (outd/'tui_self_test.md').write_text('\n'.join(md))
    if debug: print(json.dumps(results, indent=2))
    return 0


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--debug',action='store_true');ap.add_argument('--self-test',action='store_true');args=ap.parse_args()
    if args.self_test:
        raise SystemExit(self_test(args.debug))
    while True:
        menu(); c=input('> ').strip()
        if c=='1': print(json.dumps(load_config(),indent=2))
        elif c=='2':
            for r in PROFILES: print(r)
        elif c=='6':
            cmd,res=run_lab(load_config()); print('CMD:', ' '.join(cmd)); print(res['stdout']); print(res['stderr'])
        elif c=='7':
            g=input('group [basic|security|extended|negative]: ').strip() or 'basic'
            cmd,res=run_tests(g); print('CMD:', ' '.join(cmd)); print(res['stdout']); print(res['stderr'])
        elif c=='8': print(json.dumps(latest_report(),indent=2)[:4000])
        elif c=='9':
            runs=list_runs(); print('runs:',runs)
            if runs: print('logs:', list_logs(runs[-1]))
        elif c=='10': show_system()
        elif c=='11': break
        else: print('not implemented in CLI fallback')

if __name__=='__main__':
    main()

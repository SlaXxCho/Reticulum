import argparse, json, os, platform, subprocess
from .config import load_config
from .actions import run_lab, run_tests, latest_report
from .crypto_view import PROFILES


def menu():
    print('''\nRNS Security Panel\n1.Node Security Policy\n2.Crypto Profiles\n3.Local Lab Runner\n4.Test Runner\n5.Reports\n6.System\n7.Exit''')


def show_system():
    print('Python:', platform.python_version())
    print('OS:', platform.platform())
    print('CWD:', os.getcwd())
    print('Commit:', subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True).stdout.strip())


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--debug',action='store_true');args=ap.parse_args()
    while True:
        menu(); c=input('> ').strip()
        if c=='1': print(json.dumps(load_config(),indent=2))
        elif c=='2':
            for r in PROFILES: print(r)
        elif c=='3':
            cmd,res=run_lab(load_config()); print('CMD:', ' '.join(cmd)); print(res['stdout']); print(res['stderr'])
        elif c=='4':
            g=input('group [basic|security|extended|negative]: ').strip() or 'basic'
            cmd,res=run_tests(g); print('CMD:', ' '.join(cmd)); print(res['stdout']); print(res['stderr'])
        elif c=='5': print(json.dumps(latest_report(),indent=2)[:4000])
        elif c=='6': show_system()
        elif c=='7': break
        else: print('invalid')

if __name__=='__main__':
    main()

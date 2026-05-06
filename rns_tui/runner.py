import shlex
import subprocess

SAFE = {'python', 'pytest'}


def build_lab_command(force_max=False, network_profile=None):
    cmd = ['python', 'lab_local/run_lab.py']
    if force_max:
        cmd.append('--force-max-security')
    if network_profile:
        cmd += ['--network-profile', network_profile]
    return cmd


def predefined_test_commands():
    return {
        'basic': ['python', '-m', 'pytest', '-q', 'tests/test_crypto_profiles.py', 'tests/test_security_policy.py', 'tests/test_pqc_upgrade.py', 'tests/test_link_security_tags.py'],
        'security': ['python', '-m', 'pytest', '-q', 'tests/test_anti_downgrade.py', 'tests/test_replay_protection.py', 'tests/test_key_desync.py', 'tests/test_lora_fragmentation.py'],
        'extended': ['python', '-m', 'pytest', '-q', 'tests/test_policy_matrix.py', 'tests/test_key_versioning_extended.py', 'tests/test_security_policy_update.py', 'tests/test_lora_stress.py'],
        'negative': ['python', '-m', 'pytest', '-q', 'tests/test_max_security_global.py', 'tests/test_lora_failure_modes.py', 'tests/test_key_cutover_failures.py', 'tests/test_crypto_suite_reporting.py', 'tests/test_active_downgrade_attacks.py', 'tests/test_corrupted_pqc_material.py', 'tests/test_rekey_stress.py'],
    }


def run_command(cmd):
    if cmd[0] not in SAFE:
        raise ValueError('Unsafe command')
    p = subprocess.run(cmd, capture_output=True, text=True)
    return {'rc': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}

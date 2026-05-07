import pytest
from rns_tui.runner import build_lab_command, predefined_test_commands, run_command, build_lab_v2_command


def test_build_lab_command():
    cmd = build_lab_command(True, 'lora_failure')
    assert '--force-max-security' in cmd
    assert 'lora_failure' in cmd


def test_predefined_groups():
    groups = predefined_test_commands()
    assert set(['basic','security','extended','negative']).issubset(groups.keys())


def test_block_unsafe_command():
    with pytest.raises(ValueError):
        run_command(['rm', '-rf', '/'])


def test_invalid_profile_and_injection_rejected():
    with pytest.raises(ValueError): build_lab_command(False,'x;rm -rf')
    with pytest.raises(ValueError): build_lab_v2_command('all',False,'../etc')

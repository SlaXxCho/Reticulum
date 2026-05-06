from lab_local.network_profiles import NETWORK_PROFILES

def test_lora_profiles_defined():
    assert NETWORK_PROFILES["lora_failure"]["mtu"]==96
    assert NETWORK_PROFILES["lora_extreme"]["loss_percent"]==50

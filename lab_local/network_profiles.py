NETWORK_PROFILES = {
    "normal": {"mtu": 1500, "latency_ms": 0, "loss_percent": 0, "bandwidth_kbit": 0},
    "wifi_like": {"mtu": 1200, "latency_ms": 20, "loss_percent": 1, "bandwidth_kbit": 10000},
    "ethernet_like": {"mtu": 1500, "latency_ms": 1, "loss_percent": 0, "bandwidth_kbit": 100000},
    "lora_basic": {"mtu": 200, "latency_ms": 500, "loss_percent": 5, "bandwidth_kbit": 10},
    "lora_degraded": {"mtu": 128, "latency_ms": 1000, "loss_percent": 20, "bandwidth_kbit": 5},
    "lora_failure": {"mtu": 96, "latency_ms": 2000, "loss_percent": 30, "bandwidth_kbit": 2},
    "lora_extreme": {"mtu": 64, "latency_ms": 3000, "loss_percent": 50, "bandwidth_kbit": 1},
}

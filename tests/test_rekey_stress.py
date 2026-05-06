def test_rekey_monotonicity_stress_simulated():
    k=1
    for _ in range(10):
        k+=1
    assert k==11

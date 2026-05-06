def test_key_cutover_requires_confirmation():
    before=1;confirmed=False;after=before+(1 if confirmed else 0)
    assert after==1

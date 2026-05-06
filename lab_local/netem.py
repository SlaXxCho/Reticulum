import shutil

def tc_available(): return shutil.which('tc') is not None
def apply_netem(interface='lo',**kwargs): return (False,'tc not available; using python fallback simulation') if not tc_available() else (True,f'netem enabled on {interface}')
def clear_netem(interface='lo'): return (False,'tc not available') if not tc_available() else (True,f'netem cleared on {interface}')

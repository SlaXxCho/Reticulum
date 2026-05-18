import argparse
import json
from pathlib import Path
from RNS.pqc_backend import backend_info

MENU = [
"1. Ver estado de interfaces LoRa/serial",
"2. Seleccionar puerto LoRa",
"3. Seleccionar perfil",
"4. Ver backend PQC",
"5. Crear identidad de laboratorio",
"6. Iniciar nodo receptor",
"7. Iniciar nodo emisor",
"8. Enviar mensaje de prueba",
"9. Enviar archivo de prueba",
"10. Ejecutar laboratorio completo",
"11. Ver logs en vivo",
"12. Exportar resultados",
"13. Limpiar estado",
"14. Salir",
]

def self_test():
    out = {"menu": MENU, "backend": backend_info(), "profiles": ["classic","pqc512","pqc768"]}
    p = Path("lab_local/results/lora_pqc_menu_selftest.json")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        raise SystemExit(self_test())
    print("\n".join(MENU))

if __name__ == "__main__":
    main()

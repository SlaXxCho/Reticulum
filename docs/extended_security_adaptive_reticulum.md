# Seguridad Adaptativa en Reticulum (Documento principal)

## A. Resumen ejecutivo
Este fork añade una capa de seguridad adaptativa para laboratorio sobre Reticulum, con:
- perfiles criptográficos configurables,
- `security_tag` por mensaje,
- Policy Engine,
- upgrade PQC/híbrido dentro de `Link`,
- `key_versioning`,
- controles anti-downgrade y replay,
- pruebas locales y simulación de entornos degradados tipo LoRa.

> **Estado**: laboratorio/investigación. No producción.

---

## B. Objetivo de la modificación
Problemas a resolver:
1. Reticulum base usa criptografía clásica (muy sólida hoy, pero no PQC por defecto).
2. LoRa impone límites fuertes de MTU, latencia y ancho de banda.
3. No todos los mensajes requieren el mismo nivel de seguridad.
4. Se necesita seguridad máxima bajo demanda, evitando downgrade silencioso.
5. Se quiere una ruta progresiva hacia PQC (Post-Quantum Cryptography).

---

## C. Enfoque elegido
### Alternativas evaluadas
1. **Modificar wire format base**
   - Ventaja: integración profunda.
   - Desventaja: alto riesgo de compatibilidad y fragmentación.
2. **Modificar handshake inicial del Link**
   - Ventaja: seguridad temprana.
   - Desventaja: impacto en nodos legacy y costo en enlaces estrechos.
3. **Upgrade dentro del Link (elegido)**
   - Ventaja: menor ruptura, adopción incremental.
   - Desventaja: fase inicial clásica antes del upgrade.

### Por qué se eligió la opción 3
- Minimiza ruptura con flujo base de Reticulum.
- Permite control por política (nodo+link+mensaje).
- Facilita pruebas progresivas en LoRa-like sin romper routing base.

---

## Mapa de cambios en el código
| Archivo | Clase/Función | Cambio realizado | Motivo | Riesgo | Estado |
|---|---|---|---|---|---|
| `RNS/crypto_profiles.py` | `CryptoProfileManager` | Perfiles/ranking/capabilities | negociación adaptable | selección subóptima | VALIDATED (funcional) |
| `RNS/security_policy.py` | `SecurityPolicyEngine` | allow/block/upgrade por tag | política por mensaje | complejidad de decisión | VALIDATED (funcional) |
| `RNS/pqc_upgrade.py` | `PQCUpgradeManager` | control messages, replay nonce, derive helper | upgrade y control | replay/desync/DoS | VALIDATED + SIMULATED(PQC) |
| `RNS/Link.py` | integración de política/upgrade | estados y APIs de seguridad adaptativa | enforcement por link | estado complejo | VALIDATED (parcial) |
| `lab_local/run_lab.py` | runner | escenarios, métricas, reportes | reproducibilidad | falsos positivos si mock pobre | VALIDATED (harness) |
| `lab_local/netem.py` | helper netem | fallback si `tc` no existe | portabilidad | no equivalente kernel/RF | SIMULATED |
| `tests/*` | múltiples | pruebas policy/replay/downgrade/desync | evidencia funcional | cobertura no cripto-concluyente | VALIDATED |

### Nota sobre Identity/Packet
En esta iteración la modificación principal documentada está concentrada en política, link y harness; cualquier impacto colateral en flujo de paquete debe verificarse en próximas auditorías trazables.

---

## Clases nuevas
### CryptoProfileManager
Responsabilidad: catálogo/ranking de perfiles y selección común con capacidades remotas.

### SecurityPolicyEngine
Inputs: `security_tag`, perfil actual, mínimo de nodo, capacidades remotas, medio.  
Outputs: `allow_send`, `block`, `require_pqc_upgrade`, `target_profile`, `reason`.

Pseudocódigo:
```text
required = tag_to_profile(tag)
best = choose_best_common(caps)
if best is None: block
elif rank(best) < rank(required):
    block for MAX_SECURITY
    else fallback policy
else:
    allow
    if current < required: require upgrade
```

### PQCUpgradeManager
Responsabilidad: construir/parsear mensajes de control (`CAPS`, `SECURITY_POLICY_UPDATE`, `PQC_KEM`), protección replay por nonce, helper de derivación híbrida HKDF.

### Modificaciones sobre Link
- Enforce por política antes de enviar.
- Ruta de negociación/upgrade y `key_version`.
- Bloqueo cuando el perfil negociado no cumple política crítica.

---

## Flujo completo (ASCII)
### STANDARD
```text
App -> security_tag=STANDARD -> PolicyEngine -> Link -> send
```

### MAX_SECURITY
```text
App -> MAX_SECURITY -> PolicyEngine(require PQC)
    -> if insufficient Link profile: start PQC upgrade
    -> PQCUpgradeManager negotiation
    -> HKDF(old_key || pqc_secret)
    -> key_version++
    -> send
```

### Bloqueo
```text
App -> MAX_SECURITY -> remote lacks PQC -> allow_downgrade=false
    -> block + blocked_reason
```

### Fallo seguro
```text
Upgrade incompleto -> no key switch confirm
-> key_version no sube
-> no SECURE
-> mensaje crítico bloqueado
```

---

## Perfiles criptográficos
| Perfil | Identidad | Intercambio | PQC | Uso recomendado | LoRa | Estado |
|---|---|---|---|---|---|---|
| classic | Ed25519 | X25519 | no | compatibilidad base | alto | VALIDATED |
| hybrid_light | Ed25519 | X25519 + ML-KEM-512 | sí | enlaces restringidos con seguridad elevada | medio | SIMULATED / NOT CONCLUSIVE |
| hybrid_strong | Ed25519 + ML-DSA | X25519 + ML-KEM-768 | sí | redes privadas de mayor capacidad | bajo en LoRa | SIMULATED / NOT CONCLUSIVE |
| pqc_experimental | ML-DSA | ML-KEM | sí | investigación | no recomendado | SIMULATED / NOT CONCLUSIVE |

---

## Security Tags
| Tag | Objetivo | Requiere PQC | Downgrade | Acción si no cumple | Ejemplo |
|---|---|---|---|---|---|
| STANDARD | normal | no | controlado | envío normal | telemetría común |
| PREFERRED_SECURE | preferir alto | preferido | sí (policy) | fallback o block | datos sensibles no críticos |
| MUST_DELIVER | priorizar entrega | depende del mínimo | sí (policy) | entrega con mejor disponible | alarmas operativas |
| MAX_SECURITY | máximo estricto | sí | no | bloqueo | secretos críticos |

---

## Riesgos introducidos
- complejidad de estado en Link,
- riesgo de desincronización de clave,
- superficie DoS en intentos de upgrade,
- errores de validación por simulación,
- falsa sensación de seguridad si PQC sigue mock.

## Qué falta por mejorar
- ML-KEM/ML-DSA reales,
- pruebas con `tc/netem` real,
- campañas LoRa hardware,
- auditoría externa criptográfica.

---

## Siglas
- PQC: Post-Quantum Cryptography
- KEM: Key Encapsulation Mechanism
- ML-KEM: Module-Lattice-Based Key Encapsulation Mechanism
- ML-DSA: Module-Lattice-Based Digital Signature Algorithm
- HKDF: HMAC-based Key Derivation Function
- KDF: Key Derivation Function
- ECDH: Elliptic Curve Diffie-Hellman
- MITM: Man-in-the-Middle
- DoS: Denial of Service
- MTU: Maximum Transmission Unit

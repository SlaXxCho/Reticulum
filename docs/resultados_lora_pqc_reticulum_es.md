# Resultados LoRa + PQC en Reticulum (ES)

## A) Establecimiento de sesión
| Modo | Pública | Setup | Bytes sesión | Tiempo pública | Tiempo setup | Tiempo sesión | Diferencia vs standard |
|---|---:|---:|---:|---:|---:|---:|---:|
| standard | 247 B | 382 B | 629 B | 18.012 s | 43.520 s | 61.532 s | base |
| pqc512 | 1.166 B | 1.450 B | 2.616 B | 54.026 s | 64.029 s | 118.055 s | +56.523 s |
| pqc768 | 1.686 B | 1.878 B | 3.564 B | 39.521 s | 82.535 s | 122.056 s | +60.524 s |

Interpretación:
- El coste PQC se concentra en el establecimiento de sesión.
- `pqc512` y `pqc768` ~ duplican sesión inicial frente a `standard`.
- `pqc768` fue solo +4-5 s frente a `pqc512` en esta corrida.

## B) Anomalía pública ML-KEM-512
| Pública enviada | Tamaño | Chunks reales | Chunks enviados | Tiempo | Throughput | Incidencias |
|---|---:|---:|---:|---:|---:|---|
| ML-KEM-512 | 1.166 B | 13 | 20 | ~54 s | ~630.6 bps | status_none=2 |
| ML-KEM-768 | 1.686 B | 18 | 32 | ~39.5 s | ~1187.5 bps | status_none=0 |

Conclusión: variabilidad de enlace LoRa (ACK/STATUS), no evidencia de coste algorítmico intrínseco de ML-KEM-512 mayor que ML-KEM-768.

## C) Estimación corregida
| Fase | Tiempo real | Tiempo esperado razonable |
|---|---:|---:|
| Pública ML-KEM-512 | 54.0 s | 28-35 s |
| Setup ML-KEM-512 | 64.0 s | 60-70 s |
| Sesión ML-KEM-512 total | 118.0 s | 90-105 s |
| Sesión ML-KEM-768 total | 122.0 s | 115-130 s |

## D) Payloads cifrados
| Modo | Payload | Tamaño cifrado | Overhead | Tiempo TX | Throughput aprox. | Chunks | Reintentos estimados |
|---|---:|---:|---:|---:|---:|---:|---:|
| standard | 1 KB | 1.622 B | +598 B | 48.024 s | 972.6 bps | 17 | 12 |
| standard | 5 KB | 5.718 B | +598 B | 157.059 s | 1176.6 bps | 60 | 62 |
| pqc512 | 1 KB | 1.617 B | +593 B | 47.524 s | 969.4 bps | 17 | 12 |
| pqc512 | 5 KB | 5.713 B | +593 B | 173.564 s | 1081.2 bps | 60 | 61 |
| pqc768 | 1 KB | 1.617 B | +593 B | 47.524 s | 969.4 bps | 17 | 12 |
| pqc768 | 5 KB | 5.713 B | +593 B | 174.564 s | 1107.3 bps | 60 | 66 |

Interpretación: coste por payload prácticamente igual entre modos; diferencia principal en sesión.

## E) Tiempo total por modo
| Modo | Tiempo sesión | Tiempo payloads | Total aproximado | Diferencia vs standard |
|---|---:|---:|---:|---:|
| standard | 61.532 s | 205.083 s | 266.615 s | base |
| pqc512 | 118.055 s | 221.088 s | 339.143 s | +72.528 s |
| pqc768 | 122.056 s | 222.088 s | 344.144 s | +77.529 s |

## F) Amortización estimada
| Mensajes por sesión | Sobrecoste pqc512 vs standard por mensaje | Sobrecoste pqc768 vs standard por mensaje |
|---:|---:|---:|
| 1 | +30-45 s estimado | +55-70 s estimado |
| 5 | +6-9 s | +11-14 s |
| 10 | +3-4.5 s | +5.5-7 s |
| 20 | +1.5-2.2 s | +2.8-3.5 s |
| 50 | <1 s | ~1-1.4 s |

## G) Seguridad
| Modo | Payload | Descifrado OK | Tamper bloqueado | Replay bloqueado |
|---|---|---:|---:|---:|
| standard | 1 KB | Sí | Sí | Sí |
| standard | 5 KB | Sí | Sí | Sí |
| pqc512 | 1 KB | Sí | Sí | Sí |
| pqc512 | 5 KB | Sí | Sí | Sí |
| pqc768 | 1 KB | Sí | Sí | Sí |
| pqc768 | 5 KB | Sí | Sí | Sí |

Conclusión técnica: AES-256-GCM + message_id anti-replay + TOFU/pinning cubren integridad y repetición en el flujo evaluado.

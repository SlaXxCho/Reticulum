# Decisión de funcionamiento Reticulum PQC LoRa (ES)

## Decisión de arquitectura
Se adopta **PQC solo para establecimiento de sesión** y **AES-256-GCM para contenido**.

### Motivos
1. LoRa es sensible a overhead por byte y retransmisión.
2. Repetir ML-KEM por mensaje/chunk multiplica latencia sin ganancia práctica.
3. HKDF permite derivar `session_key` robusta desde `shared_secret`.
4. Cifrar paquete completo antes de fragmentar minimiza sobrecosto y mantiene autenticación AEAD coherente.

## Por qué no PQC por chunk
- Cada chunk requeriría metadatos/nonce adicionales o nuevas encapsulaciones.
- Más superficie de fallo, retransmisión y desincronización.
- Coste muy alto en LoRa de bajo ancho de banda.

## Selección de perfiles
- `classic`: baseline/compatibilidad.
- `pqc512`: preferible en low-bandwidth.
- `pqc768`: recomendado para seguridad conservadora y sesiones reutilizadas.

## Riesgos
- Variabilidad LoRa (ACK/STATUS) puede distorsionar medidas de una sola ejecución.
- Sin backend ML-KEM real no hay validación criptográfica PQC concluyente.

## Pasos hacia producción
- Repeticiones con mediana/p95.
- Pinning/TOFU estricto.
- Auditoría externa de seguridad.
- Validación con hardware/entorno estable y métricas de canal.

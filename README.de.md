# Jellyfin-Nvidia-CUDA12 für Unraid

**🌐 [English Version](README.md)**

**⚠️ Hinweis: Dies ist ein nicht unterstütztes Community-Template. Nutzung auf eigene Gefahr. ⚠️**

Ein Docker-Image für Jellyfin Media Server mit voller NVIDIA GPU-Unterstützung (CUDA 12.9.1), optimiert für Hardware-Transcoding auf Unraid.

## Image-Varianten

| Tag | Beschreibung | Verwendung |
|-----|--------------|------------|
| `:main` / `:latest` | Produktions-Image, direkter Jellyfin-Start | Normaler Betrieb |
| `:debug` | Mit GPU-Diagnostik beim Start | Fehlerbehebung |
| `:mqtt` | Home Assistant Integration | Smart Home (geplant) |
| `:base` | Basis-Image (nicht direkt verwenden) | Nur für Builds |

## Unterstützte GPUs (CUDA 12.9.1)

| Generation | Jahre | Beispiele | Status |
|------------|-------|-----------|--------|
| Maxwell | 2014-2016 | GTX 960, GTX 980 Ti, Quadro K2200 | ✅ |
| Pascal | 2016-2017 | GTX 1050 Ti, GTX 1080 Ti, Quadro P4000 | ✅ |
| Volta | 2017-2018 | Titan V, Quadro GV100 | ✅ |
| Turing | 2018-2020 | GTX 1660, RTX 2080 Ti, Quadro RTX 5000 | ✅ |
| Ampere | 2020-2022 | RTX 3060, RTX 3090, A4000 | ✅ |
| Ada Lovelace | 2022+ | RTX 4060, RTX 4090 | ✅ |
| Hopper | 2022+ | H100, H200 | ❌ (benötigt CUDA 13+) |
| Blackwell | 2024+ | B100, B200 | ❌ (benötigt CUDA 13+) |

## Projektstruktur

```
jellyfin-nvidia-cuda12/
├── base/
│   └── Dockerfile         # Basis-Image: CUDA + Jellyfin + FFmpeg
├── main/
│   └── Dockerfile         # Produktions-Variante
├── debug/
│   ├── Dockerfile         # Debug-Variante mit Diagnostik
│   └── debug.sh           # GPU-Diagnostik-Script
├── mqtt/
│   └── (kommt bald)       # MQTT-Variante für Home Assistant
├── build.sh               # Build-Script für alle Varianten
├── Unraid/
│   └── template.xml       # Unraid Docker-Template
└── README.md
```

## Voraussetzungen

- Unraid 7.x
- NVIDIA GPU mit installierten Treibern (NVIDIA Driver Plugin)
- Docker mit NVIDIA Runtime-Unterstützung

## Schnellstart

### Fertiges Image verwenden (Docker Hub)

```bash
docker run -d \
  --name jellyfin \
  --gpus all \
  -p 8096:8096 \
  -v /pfad/zu/config:/config \
  -v /pfad/zu/medien:/media:ro \
  -e TZ=Europe/Berlin \
  drshyper/jellyfin-nvidia-cuda12:main
```

### Lokal bauen

```bash
# Auf Unraid - alle Images bauen
cd /mnt/cache/system/docker/Build1
./build.sh all

# Einzelne Variante bauen
./build.sh base    # Muss zuerst gebaut werden
./build.sh main    # Produktion
./build.sh debug   # Mit Diagnostik
```

## Installation in Unraid

### Ein-Klick-Methode

```bash
wget -O /boot/config/plugins/dockerMan/templates-user/my-Jellyfin-Nvidia-CUDA12.xml \
  https://github.com/rbxxswap/Jellyfin-Nvidia-CUDA12/raw/main/Unraid/template.xml
```

### Manuelle Installation

1. `template.xml` aus dem `Unraid/`-Ordner herunterladen
2. Nach `/boot/config/plugins/dockerMan/templates-user/` kopieren
3. Im Docker-Tab auf "Container hinzufügen" klicken und das Template auswählen

## Konfiguration

**Erforderliche Pfade:**
- **Config-Pfad**: `/mnt/user/appdata/jellyfin-nvidia`
- **Medien-Pfad**: `/mnt/user/media`

**GPU-Einstellungen:**

> ⚠️ **Wichtig:** Die folgenden Einstellungen sind bereits im Template vorkonfiguriert. Setze **NICHT** zusätzlich `runtime: nvidia` oder andere GPU-Runtime-Einstellungen - dies führt zu Konflikten mit dem Unraid NVIDIA Driver Plugin!

| Einstellung | Wert | Status |
|-------------|------|--------|
| `--gpus` | `all` | ✅ Vorkonfiguriert |
| `NVIDIA_VISIBLE_DEVICES` | `all` | ✅ Vorkonfiguriert |
| `NVIDIA_DRIVER_CAPABILITIES` | `all,compute,video,utility` | ✅ Vorkonfiguriert |

**NICHT setzen:**
- ❌ `runtime: nvidia`
- ❌ `NVIDIA_RUNTIME`
- ❌ Andere NVIDIA Runtime-Parameter

## Debug-Variante Ausgabe

Bei Verwendung von `:debug` erscheint diese Ausgabe beim Container-Start:

```
================================================
JELLYFIN NVIDIA GPU DIAGNOSTICS
Container Start: Wed Dec 18 07:00:00 UTC 2025
================================================
[GPU]
name, driver_version, temperature.gpu, utilization.gpu, memory.total, memory.used
Quadro K2200, 550.120, 45, 0 %, 4096 MiB, 100 MiB

[FFMPEG]
Version: ffmpeg version 6.1.1
NVENC encoders: 8
CUVID decoders: 12

[DEVICES]
NVIDIA devices found: 4
================================================
Starting Jellyfin...
================================================
```

## Lizenz

MIT-Lizenz - Siehe LICENSE-Datei für Details.

## Links

- [Docker Hub](https://hub.docker.com/r/drshyper/jellyfin-nvidia-cuda12)
- [GitHub](https://github.com/rbxxswap/Jellyfin-Nvidia-CUDA12)
- [Jellyfin Dokumentation](https://jellyfin.org/docs/)

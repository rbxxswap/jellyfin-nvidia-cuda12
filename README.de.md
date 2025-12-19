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

## Debug-Variante

Die `:debug`-Variante zeigt GPU-Diagnose beim Container-Start und speichert die Ausgabe in eine Datei für späteren Zugriff.

### Debug-Ausgabe anzeigen

**Methode 1: Unraid Container Console** (empfohlen)
1. Im Unraid Docker-Tab auf das Container-Icon klicken
2. **">_Console"** auswählen (öffnet eine Shell *im Container*)
3. Ausführen: `cat /config/debug-output.txt`

**Methode 2: Terminal/SSH**
```bash
docker exec jellyfin-debug cat /config/debug-output.txt
```

**Methode 3: Datei-Browser**
- Zum Config-Pfad navigieren (z.B. `/mnt/user/appdata/jellyfin-nvidia/`)
- `debug-output.txt` öffnen

### Beispiel-Ausgabe

```
================================================
JELLYFIN NVIDIA GPU DIAGNOSTICS
Container Start: Wed Dec 18 07:00:00 UTC 2025
================================================
[SYSTEM]
Image: "Ubuntu 24.04.2 LTS"

[GPU]
name, driver_version, temperature.gpu, utilization.gpu, memory.total, memory.used
Quadro P2000, 575.64.05, 33, 0 %, 5120 MiB, 0 MiB

[FFMPEG]
Version: ffmpeg version 6.1.1-3ubuntu5
NVENC encoders: 3
CUVID decoders: 10
Hardware acceleration methods:
vdpau
cuda
vaapi
qsv
drm
opencl
vulkan

[DEVICES]
NVIDIA devices found: 4
crw-rw-rw- 1 root root 195,   0 Dec 18 13:46 /dev/nvidia0
crw-rw-rw- 1 root root 195, 255 Dec 18 13:46 /dev/nvidiactl
...

================================================
Debug output saved to: /config/debug-output.txt
View anytime with: cat /config/debug-output.txt
================================================
Starting Jellyfin...
================================================
```

> **Hinweis:** Die Debug-Ausgabe wird bei jedem Container-Start neu generiert. Der Unraid Log-Viewer zeigt nur die neuesten Zeilen, daher die oben genannten Methoden für die vollständige Diagnose verwenden.

## Lizenz

MIT-Lizenz - Siehe LICENSE-Datei für Details.

## Links

- [Docker Hub](https://hub.docker.com/r/drshyper/jellyfin-nvidia-cuda12)
- [GitHub](https://github.com/rbxxswap/Jellyfin-Nvidia-CUDA12)
- [Jellyfin Dokumentation](https://jellyfin.org/docs/)

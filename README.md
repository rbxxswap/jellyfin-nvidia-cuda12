# Jellyfin-Nvidia-CUDA12 for Unraid

**⚠️ Disclaimer: This is an unsupported community template. Use at your own risk. No support will be provided. ⚠️**

A Docker image for Jellyfin Media Server with full NVIDIA GPU support (CUDA 12.9.1), optimized for hardware transcoding on Unraid.

## Image Variants

| Tag | Beschreibung | Use Case |
|-----|--------------|----------|
| `:main` / `:latest` | Produktions-Image, direkter Jellyfin-Start | Normaler Betrieb |
| `:debug` | Mit GPU-Diagnostik beim Start | Troubleshooting, Verifizierung |
| `:mqtt` | Mit MQTT-Integration für Home Assistant | Smart Home Integration |
| `:base` | Basis-Image (nicht direkt verwenden) | Nur für Builds |

## Supported GPUs (CUDA 12.9.1)

| Generation | Jahre | Beispiele | Status |
|------------|-------|-----------|--------|
| Maxwell | 2014-2016 | GTX 960, GTX 980 Ti, Quadro K2200 | ✅ |
| Pascal | 2016-2017 | GTX 1050 Ti, GTX 1080 Ti, Quadro P4000 | ✅ |
| Volta | 2017-2018 | Titan V, Quadro GV100 | ✅ |
| Turing | 2018-2020 | GTX 1660, RTX 2080 Ti, Quadro RTX 5000 | ✅ |
| Ampere | 2020-2022 | RTX 3060, RTX 3090, A4000 | ✅ |
| Ada Lovelace | 2022+ | RTX 4060, RTX 4090 | ✅ |
| Hopper | 2022+ | H100, H200 | ❌ (needs CUDA 13+) |
| Blackwell | 2024+ | B100, B200 | ❌ (needs CUDA 13+) |

## Project Structure

```
jellyfin-nvidia-cuda12/
├── base/
│   └── Dockerfile         # Base image: CUDA + Jellyfin + FFmpeg
├── main/
│   └── Dockerfile         # Production variant
├── debug/
│   ├── Dockerfile         # Debug variant with diagnostics
│   └── startup.sh         # GPU diagnostics script
├── mqtt/
│   └── (coming soon)      # MQTT variant for Home Assistant
├── build.sh               # Build script for all variants
├── Unraid/
│   └── template.xml       # Unraid Docker template
└── README.md
```

## Prerequisites

- Unraid 7.x
- NVIDIA GPU with drivers installed (NVIDIA Driver plugin)
- Docker with NVIDIA runtime support

## Quick Start

### Using Pre-built Image (Docker Hub)

```bash
docker run -d \
  --name jellyfin \
  --gpus all \
  -p 8096:8096 \
  -v /path/to/config:/config \
  -v /path/to/media:/media:ro \
  -e TZ=Europe/Berlin \
  drshyper/jellyfin-nvidia-cuda12:main
```

### Building Locally

```bash
# Auf Unraid - alle Images bauen
cd /mnt/cache/system/docker/Build1
./build.sh all

# Nur bestimmte Variante bauen
./build.sh base    # Muss zuerst gebaut werden
./build.sh main    # Produktion
./build.sh debug   # Mit Diagnostik
```

## Installation in Unraid

### One-Click Method

```bash
wget -O /boot/config/plugins/dockerMan/templates-user/my-Jellyfin-Nvidia-CUDA12.xml \
  https://github.com/rbxxswap/Jellyfin-Nvidia-CUDA12/raw/main/Unraid/template.xml
```

### Manual Installation

1. Download `template.xml` from the `Unraid/` folder
2. Copy to `/boot/config/plugins/dockerMan/templates-user/`
3. In Docker tab, click "Add Container" and select the template

## Configuration

**Required paths:**
- **Config Path**: `/mnt/user/appdata/jellyfin-nvidia`
- **Media Path**: `/mnt/user/media`

**GPU Settings:**
- Container uses `--gpus=all` by default
- `NVIDIA_VISIBLE_DEVICES=all`
- `NVIDIA_DRIVER_CAPABILITIES=all,compute,video,utility`

## Debug Variant Output

When using `:debug`, you'll see this output at container start:

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
Hardware acceleration methods:
cuda
vdpau
vaapi

[DEVICES]
NVIDIA devices found: 4
================================================
Starting Jellyfin...
================================================
```

## License

MIT License - See LICENSE file for details.

## Links

- [Docker Hub](https://hub.docker.com/r/drshyper/jellyfin-nvidia-cuda12)
- [GitHub](https://github.com/rbxxswap/Jellyfin-Nvidia-CUDA12)
- [Jellyfin Documentation](https://jellyfin.org/docs/)

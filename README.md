# Jellyfin-Nvidia-CUDA12 for Unraid

**🌐 [Deutsche Version](README.de.md)**

**⚠️ Disclaimer: This is an unsupported community template. Use at your own risk. ⚠️**

A Docker image for Jellyfin Media Server with full NVIDIA GPU support (CUDA 12.9.1), optimized for hardware transcoding on Unraid.

## Image Variants

| Tag | Description | Use Case |
|-----|-------------|----------|
| `:main` / `:latest` | Production image, direct Jellyfin start | Normal operation |
| `:debug` | With GPU diagnostics at startup | Troubleshooting |
| `:mqtt` | Home Assistant integration | Smart Home (planned) |
| `:base` | Base image (do not use directly) | Build only |

## Supported GPUs (CUDA 12.9.1)

| Generation | Years | Examples | Status |
|------------|-------|----------|--------|
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
│   └── debug.sh           # GPU diagnostics script
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
# On Unraid - build all images
cd /mnt/cache/system/docker/Build1
./build.sh all

# Build specific variant
./build.sh base    # Must be built first
./build.sh main    # Production
./build.sh debug   # With diagnostics
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

> ⚠️ **Important:** The following settings are already pre-configured in the template. Do **NOT** add `runtime: nvidia` or other GPU runtime settings - this will cause conflicts with Unraid's NVIDIA Driver plugin!

| Setting | Value | Status |
|---------|-------|--------|
| `--gpus` | `all` | ✅ Pre-configured |
| `NVIDIA_VISIBLE_DEVICES` | `all` | ✅ Pre-configured |
| `NVIDIA_DRIVER_CAPABILITIES` | `all,compute,video,utility` | ✅ Pre-configured |

**Do NOT set:**
- ❌ `runtime: nvidia`
- ❌ `NVIDIA_RUNTIME`
- ❌ Any other NVIDIA runtime parameters

## Debug Variant

The `:debug` variant shows GPU diagnostics at container start and saves the output to a file for later access.

### Viewing Debug Output

**Method 1: Unraid Container Console** (recommended)
1. In Unraid Docker tab, click the container icon
2. Select **">_Console"** (this opens a shell *inside* the container)
3. Run: `cat /config/debug-output.txt`

**Method 2: Terminal/SSH**
```bash
docker exec jellyfin-debug cat /config/debug-output.txt
```

**Method 3: File Browser**
- Navigate to your config path (e.g., `/mnt/user/appdata/jellyfin-nvidia/`)
- Open `debug-output.txt`

### Example Output

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

> **Note:** The debug output is regenerated each time the container starts. The Unraid log viewer only shows the most recent lines, so use the methods above to see the full diagnostics.

## Updating the Container (Unraid)

### Changing Settings

Container settings can be changed anytime via the Unraid GUI:
1. Docker tab → Click container icon → Edit
2. Change settings as needed
3. Apply → Container restarts with new settings

### Updating to a New Image Version

To pull a newer image version (e.g., after a Docker Hub update):

1. Docker tab → Click container icon → **Force Update**
2. Unraid pulls the latest image and recreates the container
3. ✅ Your data in `/config` is preserved

### After Local Rebuild

If you rebuilt the image locally (e.g., after Dockerfile changes):

```bash
# On Unraid
cd /mnt/cache/system/docker/Build1
./build.sh base    # Rebuild base first
./build.sh main    # Then rebuild main/latest
```

Then: Docker tab → Click container icon → **Force Update**

This recreates the container using your newly built local image. Your `/config` data remains intact.

## License

MIT License - See LICENSE file for details.

## Links

- [Docker Hub](https://hub.docker.com/r/drshyper/jellyfin-nvidia-cuda12)
- [GitHub](https://github.com/rbxxswap/Jellyfin-Nvidia-CUDA12)
- [Jellyfin Documentation](https://jellyfin.org/docs/)

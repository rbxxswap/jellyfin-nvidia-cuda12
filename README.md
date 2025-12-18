# Jellyfin-Nvidia-CUDA12 for Unraid

**⚠️ Disclaimer: This is an unsupported community template. Use at your own risk. No support will be provided. ⚠️**

A Docker template for Jellyfin Media Server with full NVIDIA GPU support (CUDA 12.9.1), optimized for hardware transcoding on Unraid.
-ffmpeg version 6.1.1

  SUPPORTED GPUs (CUDA 12.9.1):
    ✅ Maxwell (2014-2016): GTX 900 Series, Quadro M / K series
       Examples: GTX 960, GTX 980 Ti, Quadro K2200, Quadro M4000
    ✅ Pascal (2016-2017): GTX 1000 Series, Quadro P series  
       Examples: GTX 1050 Ti, GTX 1080 Ti, Quadro P2000, Quadro P4000
    ✅ Volta (2017-2018): Titan V, Quadro GV100
    ✅ Turing (2018-2020): GTX 1600/RTX 2000 Series, Quadro RTX 4000-8000
       Examples: GTX 1660, RTX 2060, RTX 2080 Ti, Quadro RTX 5000
    ✅ Ampere (2020-2022): RTX 3000 Series, A-Series
       Examples: RTX 3060, RTX 3090, A4000, A5000
    ✅ Ada Lovelace (2022+): RTX 4000 Series
       Examples: RTX 4060, RTX 4090, RTX 6000 Ada
    
    NOT SUPPORTED (requires CUDA 13+):
    ❌ Hopper (2022+): H100, H200 - needs CUDA 13.x
    ❌ Blackwell (2024+): B100, B200 - needs CUDA 13.x

## Prerequisites
- Unraid 7.2.2
- NVIDIA GPU with drivers installed (NVIDIA Driver plugin)
- Docker image built and published to your registry (or use the provided one if available)

## Installation in Unraid (One-Click Method)

1.  wget -O /boot/config/plugins/dockerMan/templates-user/my-Jellyfin-Nvidia-CUDA12.xml https://github.com/rbxxswap/Jellyfin-Nvidia-CUDA12/raw/main/Unraid/template.xml
3.  Paste the following **RAW GitHub URL** into the input field that appears:
    `https://github.com/rbxxswap/Jellyfin-Nvidia-CUDA12/raw/main/unraid/template.xml`
4.  Click **"OK"** or **"Install"**.
5.  The template will load. You **MUST** configure at least these two paths:
    - **Config Path**: Your preferred appdata path (e.g., `/mnt/user/appdata/jellyfin-nvidia`)
    - **Media Path**: Your main media library path (e.g., `/mnt/user/media`)
6.  Adjust other variables (like `TZ`) if needed.
7.  Click **"Apply"** to download the image and start the container.

## Manual / Alternative Installation
If the above method doesn't work, you can manually add the template:
1.  Download the `template.xml` file from the `unraid/` folder.
2.  Copy it to your Unraid flash drive at: `/boot/config/plugins/dockerMan/templates-user/`
3.  In the Docker tab, click "Add Container" and select "Jellyfin-Nvidia-CUDA12" from the Template dropdown.

## Configuration
- Ensure your NVIDIA GPU is passed through correctly (check the Unraid NVIDIA Driver plugin).
- The container runs in `host` network mode for best performance.
- For multiple media libraries, add additional paths after initial setup.

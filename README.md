# Jellyfin-Nvidia-CUDA12 for Unraid

**⚠️ Disclaimer: This is an unsupported community template. Use at your own risk. No support will be provided. ⚠️**

A Docker template for Jellyfin Media Server with full NVIDIA GPU support (CUDA 12.9.1), optimized for hardware transcoding on Unraid.

## Prerequisites
- Unraid 6.10+
- NVIDIA GPU with drivers installed (NVIDIA Driver plugin)
- Docker image built and published to your registry (or use the provided one if available)

## Installation in Unraid (One-Click Method)

1.  In your Unraid WebUI, go to the **"Apps"** tab.
2.  **At the bottom of the "CA Apps Search" section**, click the link that says **"Click here to get more results from any Github template URL"**.
    *(Screenshot for clarity: This link is below the search box and app list)*
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

#!/bin/bash
# =============================================================================
# BUILD SCRIPT für Jellyfin NVIDIA CUDA12 Images
# =============================================================================
# Baut alle Image-Varianten: base, main, debug, mqtt
#
# Verwendung:
#   ./build.sh              # Baut alle Images
#   ./build.sh base         # Baut nur base
#   ./build.sh main         # Baut nur main (benötigt base)
#   ./build.sh debug        # Baut nur debug (benötigt base)
#   ./build.sh push         # Pushed alle Images zu Docker Hub
# =============================================================================

REGISTRY="drshyper"
IMAGE_NAME="jellyfin-nvidia-cuda12"
BUILD_DIR="/mnt/cache/system/docker/Build1"

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

build_base() {
    log_info "Building BASE image..."
    docker build -t ${REGISTRY}/${IMAGE_NAME}:base ${BUILD_DIR}/base
    if [ $? -eq 0 ]; then
        log_info "BASE image built successfully"
    else
        log_error "BASE image build failed!"
        exit 1
    fi
}

build_main() {
    log_info "Building MAIN image..."
    docker build \
        --build-arg BASE_IMAGE=${REGISTRY}/${IMAGE_NAME}:base \
        -t ${REGISTRY}/${IMAGE_NAME}:main \
        -t ${REGISTRY}/${IMAGE_NAME}:latest \
        ${BUILD_DIR}/main
    if [ $? -eq 0 ]; then
        log_info "MAIN image built successfully (also tagged as :latest)"
    else
        log_error "MAIN image build failed!"
        exit 1
    fi
}

build_debug() {
    log_info "Building DEBUG image..."
    docker build \
        --build-arg BASE_IMAGE=${REGISTRY}/${IMAGE_NAME}:base \
        -t ${REGISTRY}/${IMAGE_NAME}:debug \
        ${BUILD_DIR}/debug
    if [ $? -eq 0 ]; then
        log_info "DEBUG image built successfully"
    else
        log_error "DEBUG image build failed!"
        exit 1
    fi
}

build_mqtt() {
    if [ -f "${BUILD_DIR}/mqtt/Dockerfile" ]; then
        log_info "Building MQTT image..."
        docker build \
            --build-arg BASE_IMAGE=${REGISTRY}/${IMAGE_NAME}:base \
            -t ${REGISTRY}/${IMAGE_NAME}:mqtt \
            ${BUILD_DIR}/mqtt
        if [ $? -eq 0 ]; then
            log_info "MQTT image built successfully"
        else
            log_error "MQTT image build failed!"
            exit 1
        fi
    else
        log_warn "MQTT Dockerfile not found, skipping..."
    fi
}

push_all() {
    log_info "Pushing all images to Docker Hub..."
    docker push ${REGISTRY}/${IMAGE_NAME}:base
    docker push ${REGISTRY}/${IMAGE_NAME}:main
    docker push ${REGISTRY}/${IMAGE_NAME}:latest
    docker push ${REGISTRY}/${IMAGE_NAME}:debug
    if [ -f "${BUILD_DIR}/mqtt/Dockerfile" ]; then
        docker push ${REGISTRY}/${IMAGE_NAME}:mqtt
    fi
    log_info "All images pushed successfully"
}

build_all() {
    build_base
    build_main
    build_debug
    build_mqtt
}

# Main
case "$1" in
    base)
        build_base
        ;;
    main)
        build_main
        ;;
    debug)
        build_debug
        ;;
    mqtt)
        build_mqtt
        ;;
    push)
        push_all
        ;;
    ""|all)
        build_all
        ;;
    *)
        echo "Verwendung: $0 {base|main|debug|mqtt|push|all}"
        exit 1
        ;;
esac

echo ""
log_info "=== Aktuelle Images ==="
docker images | grep ${IMAGE_NAME}

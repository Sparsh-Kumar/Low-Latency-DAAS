#!/bin/bash

set -e

export DOCKER_BUILDKIT=1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

IMAGE_NAME="live-tickers-job"
DOCKERFILE_PATH="${SCRIPT_DIR}/Dockerfile"

PLATFORM="linux/amd64"

echo "Project root: ${PROJECT_ROOT}"
echo "Dockerfile: ${DOCKERFILE_PATH}"
echo "Building Docker image: ${IMAGE_NAME}"

docker buildx build \
  --platform "${PLATFORM}" \
  -f "${DOCKERFILE_PATH}" \
  -t "${IMAGE_NAME}" \
  "${PROJECT_ROOT}"

echo "Build completed: ${IMAGE_NAME}"


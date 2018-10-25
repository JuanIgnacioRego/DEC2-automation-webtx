#!/bin/bash

#IMG="docker.dev.redbee.io/webtxtest:$(git describe --abbrev=0 --tags 2>/dev/null || echo 'latest')"
#IMG="registry.dev.redbee.io/webtxtest:$(git describe --abbrev=0 --tags 2>/dev/null || echo 'latest')"
IMG="lapp-dvde004:5000/webtxtest:latest"

echo "Building $IMG"
docker build -t "$IMG" . && \
docker push "$IMG"

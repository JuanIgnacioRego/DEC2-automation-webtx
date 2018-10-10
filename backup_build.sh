#!/bin/bash

IMG="lapp-dvde004:5000/webtxtest:latest2"

echo "Building $IMG"
docker build -t "$IMG" . && \
docker push "$IMG"

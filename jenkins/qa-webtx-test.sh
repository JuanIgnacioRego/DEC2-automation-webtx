#!/bin/bash

# Lo siguiente es para pullear desde Github y luego pushear la imagen Docker a la registry. Mantenerlo desactivado,
# sólo lo uso cuando estoy desde casa y la fucking VPN no me permite pushear a la registry.
#git clone https://github.com/jrego-rb/DEC2-automation-webtx.git
#cd DEC2-automation-webtx
#git pull
#bash build.sh
# Fin del pseudoscript

# Selenium/Chrome
docker pull registry.dev.redbee.io/webtxtest:latest

docker run --name selenium_chrome_remote -d --net host -v /dev/shm:/dev/shm selenium/standalone-chrome:3.11.0-californium
docker logs selenium_chrome_remote


docker run -i --rm --net host -v $WORKSPACE:/data/reports/ registry.dev.redbee.io/webtxtest:latest -e jenkins -d remote_headless_chrome --buildversion $BUILD_ID -ts suite.txt
ls -R

# After running
docker rm -f selenium_chrome_remote

#docker run --name selenium_chrome_remote -d --net host -v /dev/shm:/dev/shm -v AFIP_volume:/data/temp selenium/standalone-chrome:3.11.0-californium
#docker run -i --rm --net host -v AFIP_volume:/data/temp/ webtx:local -e desa -d remote_headless_chrome -ts suite.txt
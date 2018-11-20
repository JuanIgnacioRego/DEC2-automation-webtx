# DEC2-automation-webtx
Automation testing over DEC2-webtx, using Selenium and Python.

#How to run locally

docker run -d --net host -v /dev/shm:/dev/shm selenium/standalone-chrome:3.11.0-californium

docker run -i --rm --net host -v /home/{{yourUser}}/{{aPathToStoreReports}}:/reports registry.dev.redbee.io/webtxtest:latest -e desa -d remote_headless_chrome -ts suite.txt

For example:

docker run -i --rm --net host -v /home/juan/Escritorio/origen:/data/reports/ registry.dev.redbee.io/webtxtest:latest -e desa -d selenium_chrome_remote -ts suite.txt
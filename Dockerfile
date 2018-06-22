FROM python:2.7

ADD test_Main.py /data/
ADD Data.py /data/
ADD pages /data/pages/
ADD tools /data/tools/
ADD reports /data/reports/
ADD automation.py /data/
ADD Locators.py /data/
ADD requirements.txt /data/
ADD unittest.cfg /data/
ADD settings.py /data/
ADD QAPI.py /data/
ADD Forms.py /data/
ADD DBConnection.py /data/
ADD suite.txt /data/
ADD Exceptions.py /data/

ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

WORKDIR /data/

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "automation.py"]

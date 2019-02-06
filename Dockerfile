FROM python:2.7

ADD test_WebTx.py /data/
ADD Data.py /data/
ADD pages /data/pages/
ADD reports /data/reports/
ADD services /data/services/
ADD test_modules /data/test_modules/
ADD test_modules/Forms data/test_modules/Forms/
ADD tools /data/tools/
ADD automation.py /data/
ADD Locators.py /data/
ADD requirements.txt /data/
ADD unittest.cfg /data/
ADD settings.py /data/
ADD QAPI.py /data/
ADD deprecated_Forms.py /data/
ADD DBConnection.py /data/
ADD suite.txt /data/
ADD Exceptions.py /data/

ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

WORKDIR /data/

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "automation.py"]

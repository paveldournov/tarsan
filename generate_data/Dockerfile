FROM python:3.7

RUN pip install --upgrade pip setuptools wheel

RUN pip install Pillow

RUN mkdir /component

WORKDIR /component

COPY gen_targets.py /component/
COPY entry_point.py /component/


FROM python:3.7

RUN pip install --upgrade pip setuptools wheel
RUN pip install tensorflow
RUN pip install keras
RUN pip install scikit-image==0.14.2
RUN pip install scikit-learn==0.20.3

RUN mkdir /component

WORKDIR /component

COPY *.py /component/


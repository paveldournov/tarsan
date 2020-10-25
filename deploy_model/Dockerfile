FROM google/cloud-sdk:latest

RUN pip3 install --upgrade six
RUN pip3 install --upgrade google-cloud-storage
RUN pip3 install tensorflow
RUN pip3 install keras
RUN pip3 install scikit-image==0.14.2
RUN pip3 install scikit-learn==0.20.3

RUN mkdir /component

WORKDIR /component

COPY *.py /component/


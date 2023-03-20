ARG FUNCTION_DIR="/"

FROM python:3.10-slim as build-image
##WORKDIR /bpt

#install aws-lambda-cpp build dependencies
RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev

COPY requirements.txt ./
RUN apt-get update                                              && \
    apt-get -y install libpq-dev gcc                            && \
    pip3 install --no-cache-dir --upgrade -r ./requirements.txt && \
    rm -rf /var/lib/apt/lists/*

ARG FUNCTION_DIR
RUN mkdir -p ${FUNCTION_DIR}

COPY src/* ${FUNCTION_DIR}/
COPY src/service/* ${FUNCTION_DIR}/service/
COPY src/utilities/* ${FUNCTION_DIR}/utilities/
RUN pip install \
        --target ${FUNCTION_DIR} \
        awslambdaric


FROM python:3.10-slim

ARG FUNCTION_DIR
WORKDIR ${FUNCTION_DIR}
COPY requirements.txt ./
RUN apt-get update                                              && \
    apt-get -y install libpq-dev gcc                            && \
    pip3 install --no-cache-dir --upgrade -r ./requirements.txt && \
    rm -rf /var/lib/apt/lists/*
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR} 
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "main.handler" ]

FROM python:3.10-slim
WORKDIR /bpt

COPY requirements.txt ./
RUN apt-get update                                              && \
    apt-get -y install libpq-dev gcc                            && \
    pip3 install --no-cache-dir --upgrade -r ./requirements.txt && \
    rm -rf /var/lib/apt/lists/*



COPY src/ ./
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080" ]

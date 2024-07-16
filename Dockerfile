FROM python:3.10.11-slim

RUN mkdir chall
COPY src/* /chall

RUN apt-get update
RUN apt-get install -y socat

WORKDIR /chall
RUN chmod +x server.py
RUN chmod +x flag.py

CMD ["socat", "-d", "tcp-listen:1259,reuseaddr,fork", "exec:'./server.py',stderr"]
EXPOSE 1259
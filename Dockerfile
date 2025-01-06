FROM python:3.10.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=xterm

# Setup the challenge
RUN apt-get update
RUN apt-get install -y socat

RUN mkdir chall
COPY src/* /chall
WORKDIR /chall

RUN python3 -m pip install ecdsa gmpy2
RUN chmod +x server.py
RUN chmod +x flag.py

CMD ["socat", "-d", "tcp-listen:1259,reuseaddr,fork", "exec:'./server.py 12590',stderr"]
EXPOSE 1259
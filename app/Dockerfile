FROM alpine:latest

RUN apk add --no-cache python3-dev && pip3 install --upgrade pip

CMD ls -ltra

WORKDIR /blogs

COPY . /blogs

CMD ls -ltra

RUN pip3 --no-cache-dir install -r requirement.txt

EXPOSE 5000

ENTRYPOINT ["./interface.py"]
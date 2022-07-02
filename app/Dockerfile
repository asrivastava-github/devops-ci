FROM python:3.8-slim-buster

WORKDIR /blogs

COPY . /blogs

RUN pip3 --no-cache-dir install -r requirement.txt

EXPOSE 5000

ENTRYPOINT ["./interface.py"]
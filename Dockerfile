FROM ubuntu

EXPOSE 8001
ENV PYTHONUNBUFFERED 0

RUN useradd app

# Install packages from README
# see https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#apt-get
RUN apt-get -y update && \
    apt-get -y install python3 python3-pip librsvg2-bin ghostscript imagemagick && \
    rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install --no-cache --upgrade pip
RUN mkdir -p /app/printathpi/
WORKDIR /app/
COPY LICENSE /app/
COPY requirements.txt /app/

RUN pip install --no-cache -r requirements.txt

USER app

COPY printathpi/ /app/printathpi/


ENTRYPOINT ["python3", "-m", "printathpi.app"]

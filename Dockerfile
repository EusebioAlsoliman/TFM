FROM ubuntu
MAINTAINER Eusebio Naif Al-Soliman Fuentes eunaif@correo.ugr.es

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /linuxptp

RUN apt update && \
    apt install -y build-essential git sudo net-tools nano iputils-ping && \
    rm -rf /var/lib/apt/lists/*

RUN git clone git://git.code.sf.net/p/linuxptp/code .
RUN make

ENTRYPOINT ["sudo", "./ptp4l" ]

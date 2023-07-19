FROM alpine:3.18.2
MAINTAINER Eusebio Naif Al-Soliman Fuentes eunaif@correo.ugr.es

RUN apk update \
    && apk --no-cache --update add build-base && apk add git linux-headers bsd-compat-headers \
    && apk --no-cache add tzdata

ENV TZ=Europe/Madrid

WORKDIR /linuxptp

RUN git clone git://git.code.sf.net/p/linuxptp/code .
RUN make

ENTRYPOINT [ "./ptp4l" ]

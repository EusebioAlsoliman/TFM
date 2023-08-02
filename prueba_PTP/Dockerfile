FROM alpine:3.18.2
LABEL org.opencontainers.image.authors="eunaif@correo.ugr.es"

RUN apk update \
    && apk --no-cache --update add build-base && apk add git linux-headers bsd-compat-headers \
    && apk --no-cache add tzdata

ENV TZ=Europe/Madrid

WORKDIR /linuxptp

RUN git clone --depth 1 --branch v4.0 git://git.code.sf.net/p/linuxptp/code .
RUN make ptp4l

ENTRYPOINT [ "./ptp4l" ]

FROM openfaas/classic-watchdog:0.13.4 as watchdog

FROM alpine:3.9

RUN mkdir -p /home/app

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

# Install pre-requisite packages.
RUN apk add --no-cache \
    bash \
    coreutils \
    curl \
    drill \
    git \
    procps

# Add non root user
RUN addgroup -S app && adduser app -S -G app
RUN chown app /home/app
WORKDIR /home/app

# Install testssl.sh
RUN git clone --depth=1 https://github.com/drwetter/testssl.sh.git .
RUN cp testssl.sh /usr/local/bin

USER app

# Populate example here - i.e. "cat", "sha512sum" or "node index.js"
ENV fprocess="xargs -r -t -I foobarbaz testssl.sh --quiet --color=0 --jsonfile=/dev/stdout --logfile=/dev/null foobarbaz"
ENV read_timeout="6000"
ENV write_timeout="6000"

# Set to true to see request in function logs
ENV write_debug="false"

EXPOSE 8080

HEALTHCHECK --interval=300s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]

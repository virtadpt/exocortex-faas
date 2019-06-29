FROM openfaas/classic-watchdog:0.13.4 as watchdog

FROM alpine:3.9

RUN mkdir -p /home/app

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

# Add non root user
RUN addgroup -S app && adduser app -S -G app
RUN chown app /home/app

# Copy the Geoplanet database into the container image.
COPY geoplanet.sqlite /home/app

# Install pre-reqs for sandman2.
RUN apk add --no-cache \
    bash \
    python3

# Install sandman2.
RUN pip3 install sandman2

WORKDIR /home/app

USER app

EXPOSE 8080

CMD ["sandman2ctl", "-p", "8080", "-r", "sqlite+pysqlite:///geoplanet.sqlite"]

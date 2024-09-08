FROM ubi9/python-312

LABEL org.opencontainers.image.title="Gandi DDNS"
LABEL org.opencontainers.image.description="Dynamic DNS Update Client for Gandi's LiveDNS"
LABEL org.opencontainers.image.authors="Winston Astrachan, Cyril Cordoui"
LABEL org.opencontainers.image.source="https://github.com/ccordoui/container-gandi-ddns"
LABEL org.opencontainers.image.licenses="MIT"

USER 0
COPY src /tmp/src
RUN /usr/bin/fix-permissions /tmp/src
USER 1001

# Install the dependencies
RUN /usr/libexec/s2i/assemble
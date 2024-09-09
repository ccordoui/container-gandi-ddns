FROM registry.access.redhat.com/ubi9/python-312

LABEL org.opencontainers.image.title="Gandi DDNS"
LABEL org.opencontainers.image.description="Dynamic DNS Update Client for Gandi's LiveDNS"
LABEL org.opencontainers.image.authors="Winston Astrachan, Cyril Cordoui"
LABEL org.opencontainers.image.source="https://github.com/ccordoui/container-gandi-ddns"
LABEL org.opencontainers.image.licenses="MIT"

USER 0
RUN yum -y --setopt=tsflags=nodocs update && bash -c 'rpm -e --nodeps redhat-logos-httpd || /bin/true' && yum -y clean all --enablerepo='*' && rm -rf /var/log/*
RUN pip3 install -U pip setuptools wheel
COPY src /tmp/src
RUN /usr/bin/fix-permissions /tmp/src
USER 1001

# Install the dependencies
RUN /usr/libexec/s2i/assemble

CMD /opt/app-root/src/entrypoint.sh

# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM=ghcr.io/hassio-addons/base:17.2.5
FROM $BUILD_FROM

# Install all packages from Alpine repositories
# librespot is in edge/testing repository
RUN \
    apk add --no-cache \
        dbus \
        nss \
        avahi-compat-libdns_sd \
        avahi \
        snapcast-server \
        shairport-sync \
    && apk add --no-cache \
        --repository=https://dl-cdn.alpinelinux.org/alpine/edge/testing \
        librespot \
    \
    # Create required directories
    && mkdir -p /var/run/dbus \
    && mkdir -p /var/run/avahi-daemon

# Copy root filesystem
COPY rootfs /

# Make all service scripts executable
RUN chmod +x /etc/services.d/*/run /etc/services.d/*/finish 2>/dev/null || true

# Build arguments
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

# Labels
LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="FrancescoRoveda" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.vendor="Audio Distributor Add-on" \
    org.opencontainers.image.authors="FrancescoRoveda" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.url="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.documentation="https://github.com/${BUILD_REPOSITORY}/blob/main/README.md" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}
# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM=ghcr.io/hassio-addons/base:17.2.5
FROM rust:1.88-alpine3.21 AS librespot-builder

RUN \
    apk add --no-cache \
        alsa-lib-dev \
        avahi-dev \
        gcc \
        git \
        musl-dev \
        openssl-dev \
        pkgconf \
        protobuf-dev \
    && git clone --depth 1 --branch dev https://github.com/librespot-org/librespot.git /tmp/librespot \
    && cd /tmp/librespot \
    && RUSTFLAGS="-C target-feature=-crt-static" cargo build --release --locked --no-default-features --features "alsa-backend,with-dns-sd,rustls-tls-native-roots"

FROM $BUILD_FROM

# Install all packages from Alpine repositories
RUN \
    while read -r pkg; do printf '%s\n' "${pkg%%=*}"; done < /etc/apk/world > /tmp/world \
    && mv /tmp/world /etc/apk/world \
    && apk upgrade --no-cache \
    && apk add --no-cache \
        alsa-lib \
        dbus \
        nss \
        avahi-compat-libdns_sd \
        avahi \
        snapcast-server \
        shairport-sync \
        python3 \
        wget \
        unzip \
    \
    # Download and install Snapweb
    && wget -q https://github.com/badaix/snapweb/releases/download/v0.9.3/snapweb.zip \
    && mkdir -p /usr/share/snapserver/snapweb \
    && unzip -o snapweb.zip -d /usr/share/snapserver/snapweb \
    && rm snapweb.zip \
    \
    # Create required directories
    && mkdir -p /var/run/dbus \
    && mkdir -p /var/run/avahi-daemon \
    \
    # Cleanup
    && apk del --no-cache wget unzip

COPY --from=librespot-builder /tmp/librespot/target/release/librespot /usr/bin/librespot

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

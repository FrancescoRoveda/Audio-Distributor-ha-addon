# Audio Distributor

[![GitHub Release][releases-shield]][releases]
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE.md)

Multi-protocol audio distribution server for Home Assistant.

## About

This add-on provides a Snapcast server with integrated:

- **Spotify Connect** for streaming from Spotify (Premium required)
- **AirPlay** for streaming from Apple devices
- **Snapweb** for managing connected clients

Audio is distributed synchronously to all connected Snapcast clients, enabling whole-home audio.

## Features

- 🎵 Stream from Spotify Connect
- 📱 Stream from AirPlay devices
- 🔊 Synchronous multi-room playback
- 🌐 Web interface for client management
- 📊 Configurable logging levels

## Installation

1. Add this repository to Home Assistant
2. Install the "Audio Distributor" add-on
3. Configure your device names
4. Start the add-on

See [DOCS.md](DOCS.md) for detailed configuration.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐
│ Spotify Connect │────▶│                 │
└─────────────────┘     │                 │     ┌──────────────┐
                        │  Snapcast       │────▶│ Client 1     │
┌─────────────────┐     │  Server         │     └──────────────┘
│ AirPlay         │────▶│                 │
└─────────────────┘     │                 │     ┌──────────────┐
                        │                 │────▶│ Client 2     │
┌─────────────────┐     │                 │     └──────────────┘
│ Custom Streams  │────▶│                 │
└─────────────────┘     └─────────────────┘
```

[releases-shield]: https://img.shields.io/github/release/corneyl/hassio-addons.svg
[releases]: https://github.com/corneyl/hassio-addons/releases
[maintenance-shield]: https://img.shields.io/maintenance/yes/2024.svg
[license-shield]: https://img.shields.io/github/license/corneyl/hassio-addons.svg

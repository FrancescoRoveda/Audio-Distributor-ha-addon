<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

## 0.3.15
- Default Snapserver to Opus with a 5000 ms buffer to reduce Wi-Fi dropouts.
- Pass Spotify autoplay, volume normalization, and 100% initial volume explicitly to Snapserver's internal librespot stream.

## 0.3.14
- Stop the placeholder Spotify Connect service from calling `s6-svc` on a non-existent service path, which caused a restart loop while Snapserver already manages librespot internally.

## 0.3.13
- Return Spotify Connect to Snapserver's internal `librespot://` handler so discovery advertises correctly again.
- Bind the internal librespot zeroconf to the primary LAN IPv4 address, matching the device name and volume from add-on options.

## 0.3.12
- Bind Spotify Connect mDNS discovery to the host's primary LAN IPv4 address so Spotify clients do not receive Docker bridge addresses.

## 0.3.11
- Pass the required `on` value to librespot's `--autoplay` option so Spotify Connect starts with librespot 0.8.0.

## 0.3.10
- Build the add-on locally from the repository instead of requiring a prebuilt GHCR image tag.

## 0.3.9
- Run Spotify Connect as a supervised librespot service feeding Snapserver through a FIFO so the `spotify_name` device is advertised reliably.
- Persist Snapserver state under `/data/snapserver` so client volumes survive add-on restarts.
- Add `default_client_volume`, use it as Snapserver's first-connect volume, and lower reconnecting clients above that value to avoid unsafe 100% restart volume.
- Use `default_client_volume` as the Spotify Connect initial volume.

## 0.3.8
- Disable the Snapserver librespot watchdog to prevent Spotify Connect disappearing after idle time.

## 0.3.7
- Fix D-Bus readiness checks so Avahi-dependent services can start after reboot.

## 0.3.3
- Support for amd64, armhf, armv7, i386 architectures.
- Export Librespot options directly for 100% volume and autoplay.

## 0.3.0

### ⚠️ Breaking Changes
- Renamed add-on from "Snapcast server" to "Audio Distributor"
- Updated slug from `snapcast-server` to `audio-distributor`
- Updated base image from 13.0.0 to 17.2.5
- Updated librespot from 0.4.2 to 0.6.0
- Removed Spotify username/password authentication (anonymous mode only)
- Removed local playback client (pure distribution mode)

### New Features
- **AirPlay Support**: Added shairport-sync for receiving audio via AirPlay
  - New config options: `airplay_enabled`, `airplay_name`
  - AirPlay audio appears as a stream in Snapcast
  - Port 5000/tcp for AirPlay connections

### Improvements
- **Enhanced Logging**: 
  - Structured logging with service prefixes (e.g., `[snapcast-server]`)
  - Timeout handling for service dependencies
  - Detailed debug output when log level is set to debug/trace
- **Updated Packages**: 
  - Snapcast: Latest from Alpine repositories
  - Librespot: 0.4.2 → 0.6.0
  - Removed pinned package versions for better compatibility
- Removed PulseAudio (not needed for pure distribution)

---

## 0.2.1

- Wait before starting snapcast-client until snapcast-server is started. 
- Use host `127.0.0.1` for snapcast-client 

## 0.2.0

- Add Snapcast client for local playback through Home Assistant.

## 0.1.0

- Add support for Snapweb: a web-interface for Snapcast.

## 0.0.1

- Initial version based on the Home Assistant Add-on example. Supports Snapcast server and Spotify connect.

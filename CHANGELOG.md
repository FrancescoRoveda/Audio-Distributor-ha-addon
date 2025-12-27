<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

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

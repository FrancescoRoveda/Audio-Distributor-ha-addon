# Audio Distributor

Multi-protocol audio distribution server for Home Assistant with Snapcast, Spotify Connect, and AirPlay support.

## Features

- **Snapcast Server**: Synchronous multi-room audio distribution
- **Spotify Connect**: Stream music from Spotify (Premium required)
- **AirPlay**: Receive audio from Apple devices
- **Snapweb**: Built-in web interface for client management

## Configuration

### Basic Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `spotify_name` | string | "Home Assistant Audio" | Device name shown in Spotify |
| `airplay_enabled` | boolean | true | Enable AirPlay receiver |
| `airplay_name` | string | "Home Assistant AirPlay" | Device name shown on Apple devices |
| `buffer` | int | 1000 | Audio buffer in milliseconds |
| `codec` | list | flac | Audio codec (pcm, flac, vorbis, opus) |
| `sampleformat` | string | "48000:16:2" | Sample rate:bits:channels |
| `log_level` | list | info | Logging verbosity |

### Custom Streams

You can add custom audio streams in the `streams.streams` list. See [Snapcast documentation](https://github.com/badaix/snapcast#configuration) for stream formats.

## Ports

| Port | Protocol | Description |
|------|----------|-------------|
| 1704 | TCP | Snapcast client connections |
| 1705 | TCP | Snapcast control interface |
| 1780 | TCP | Snapweb interface (ingress) |
| 5000 | TCP | AirPlay receiver |

## Usage

1. Install the add-on
2. Configure Spotify and AirPlay device names
3. Start the add-on
4. Access Snapweb through the add-on sidebar panel
5. Connect Snapcast clients to your Home Assistant
6. Play audio via Spotify Connect or AirPlay

## Support

- [GitHub Issues](https://github.com/corneyl/hassio-addons/issues)
- [Snapcast Documentation](https://github.com/badaix/snapcast)

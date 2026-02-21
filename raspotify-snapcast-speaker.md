# Raspotify + Snapcast Speaker Setup Guide

Complete setup guide for a Raspberry Pi Zero 2W with InnoMaker Amp HAT running both Raspotify (Spotify Connect) and Snapcast client.

## Hardware Requirements

- Raspberry Pi Zero 2W
- InnoMaker Amp HAT (Merus Amp)
- MicroSD card with Raspberry Pi OS (Debian)
- Speaker(s)

---

## 1. Boot Configuration

Edit `/boot/firmware/config.txt`:

```bash
# Disable HDMI audio (so InnoMaker Amp becomes card 0)
# Find this line and add ,noaudio:
dtoverlay=vc4-kms-v3d,noaudio

# Add at the end of file:
# InnoMaker Amp HAT
dtoverlay=merus-amp
```

Reboot after changes.

---

## 2. ALSA Configuration (Stereo to Mono + dmix)

Create `/etc/asound.conf`:

```bash
sudo tee /etc/asound.conf > /dev/null << 'EOF'
# Stereo to Mono downmix
pcm.mono {
    type route
    slave.pcm "dmixed"
    ttable {
        0.0 0.5
        1.0 0.5
        0.1 0.5
        1.1 0.5
    }
}

pcm.dmixed {
    type dmix
    ipc_key 1024
    ipc_key_add_uid false
    ipc_perm 0666
    slave {
        pcm "hw:0,0"
        format S32_LE
        rate 44100
        period_time 0
        period_size 1024
        buffer_size 4096
        channels 2
    }
    bindings {
        0 0
        1 1
    }
}

pcm.!default {
    type plug
    slave.pcm "mono"
}

ctl.!default {
    type hw
    card 0
}
EOF
```

---

## 3. Install Raspotify

```bash
curl -sL https://dtcooper.github.io/raspotify/install.sh | sh
```

### Configure Raspotify

Edit `/etc/raspotify/conf`:

```bash
sudo tee /etc/raspotify/conf > /dev/null << 'EOF'
# /etc/raspotify/conf

# 1. Device Name (CHANGE THIS)
LIBRESPOT_NAME="YOUR-SPEAKER-NAME"

# 2. Audio Quality
LIBRESPOT_BITRATE="320"

# 3. Audio Device
LIBRESPOT_DEVICE="default"

# 4. Hardware Mixer Setup
LIBRESPOT_MIXER="alsa"
LIBRESPOT_ALSA_MIXER_DEVICE="hw:0"
LIBRESPOT_ALSA_MIXER_CONTROL="A.Mstr Vol"

# 5. Autoplay
LIBRESPOT_AUTOPLAY="on"

# 6. Volume Behavior
LIBRESPOT_ENABLE_VOLUME_NORMALISATION=false
LIBRESPOT_INITIAL_VOLUME="75"

# 7. Caching
TMPDIR=/tmp
EOF
```

---

## 4. Install Snapclient

```bash
sudo apt-get install -y snapclient
```

### Configure Snapclient (Software Volume)

Edit `/etc/default/snapclient`:

```bash
echo "SNAPCLIENT_OPTS='--host 192.168.1.200 -s default'" | sudo tee /etc/default/snapclient
```

> **Note**: Using software volume (no `--mixer` flag) is recommended. The audio-source-monitor handles hardware volume.

---

## 5. Audio Source Monitor Daemon

This script resets `A.Mstr Vol` to 75% when switching between Raspotify and Snapcast.

### Create the script

```bash
sudo tee /usr/local/bin/audio-source-monitor.sh > /dev/null << 'SCRIPT'
#!/bin/bash
# Audio Source Monitor - Resets A.Mstr Vol when switching between Raspotify and Snapcast

MIXER_CONTROL="A.Mstr Vol"
RASPOTIFY_VOLUME="75%"
SNAPCAST_VOLUME="75%"
CURRENT_SOURCE=""

log() {
    echo "[audio-monitor] $1"
}

reset_volume() {
    local new_source="$1"
    local target_volume="$2"
    if [ -n "$CURRENT_SOURCE" ] && [ "$CURRENT_SOURCE" != "$new_source" ]; then
        log "Source changed from $CURRENT_SOURCE to $new_source - setting volume to $target_volume"
        amixer -c 0 sset "$MIXER_CONTROL" "$target_volume" > /dev/null 2>&1
    fi
    CURRENT_SOURCE="$new_source"
}

log "Starting audio source monitor..."

# Follow both service logs
journalctl -f -u raspotify -u snapclient --no-tail 2>/dev/null | while read -r line; do
    # Detect Raspotify playback (track loading)
    if echo "$line" | grep -q "librespot_playback::player.*Loading"; then
        reset_volume "raspotify" "$RASPOTIFY_VOLUME"
    fi
    
    # Detect Snapcast activity (receiving audio chunks)
    if echo "$line" | grep -q "snapclient.*Codec:\|snapclient.*PCM name:"; then
        reset_volume "snapcast" "$SNAPCAST_VOLUME"
    fi
done
SCRIPT

sudo chmod +x /usr/local/bin/audio-source-monitor.sh
```

### Create systemd service

```bash
sudo tee /etc/systemd/system/audio-source-monitor.service > /dev/null << 'EOF'
[Unit]
Description=Audio Source Monitor - Resets volume when switching between Raspotify and Snapcast
After=raspotify.service snapclient.service
StartLimitIntervalSec=0

[Service]
Type=simple
ExecStart=/usr/local/bin/audio-source-monitor.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable audio-source-monitor
sudo systemctl start audio-source-monitor
```

---

## 6. Auto-Restart Configuration

### Raspotify auto-restart

```bash
sudo mkdir -p /etc/systemd/system/raspotify.service.d
sudo tee /etc/systemd/system/raspotify.service.d/restart.conf > /dev/null << 'EOF'
[Unit]
StartLimitIntervalSec=0

[Service]
Restart=always
RestartSec=30
RestartForceExitStatus=SIGABRT
EOF
```

### Snapclient auto-restart

```bash
sudo mkdir -p /etc/systemd/system/snapclient.service.d
sudo tee /etc/systemd/system/snapclient.service.d/restart.conf > /dev/null << 'EOF'
[Unit]
StartLimitIntervalSec=0

[Service]
Restart=always
RestartSec=30
EOF
```

Apply changes:

```bash
sudo systemctl daemon-reload
```

---

## 7. Verification

### Check audio hardware

```bash
aplay -l
# Should show: card 0: sndrpimerusamp [snd_rpi_merus_amp]

cat /proc/asound/cards
# Should show: 0 [sndrpimerusamp]
```

### Check mixer controls

```bash
amixer -c 0 scontrols | head -3
# Should show: 'A.Mstr Vol', 'B.L Vol', 'C.R Vol'

amixer -c 0 get 'A.Mstr Vol' | grep Mono
# Shows current volume
```

### Check services

```bash
sudo systemctl status raspotify snapclient audio-source-monitor
```

### Monitor audio source switching

```bash
sudo journalctl -f -u audio-source-monitor
```

---

## Architecture Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│                         RASPOTIFY MODE                               │
│  Spotify App → Speaker (direct) → A.Mstr Vol (hardware) → Speaker   │
│  [Spotify Volume controls hardware directly]                         │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                         SNAPCAST MODE                                │
│  Spotify → Snapcast Server → Snapclient → A.Mstr Vol → Speaker      │
│  [Snapcast uses software volume, A.Mstr fixed at 75%]               │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    AUDIO SOURCE MONITOR                              │
│  Watches logs → Detects source switch → Resets A.Mstr to 75%        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Quick Setup Commands (Copy-Paste)

For a new speaker, run these commands in order (replace `YOUR-SPEAKER-NAME` and `YOUR_SNAPCAST_SERVER_IP`):

```bash
# 1. Update config.txt
sudo sed -i 's/dtoverlay=vc4-kms-v3d/dtoverlay=vc4-kms-v3d,noaudio/' /boot/firmware/config.txt
echo -e "\n# InnoMaker Amp HAT\ndtoverlay=merus-amp" | sudo tee -a /boot/firmware/config.txt

# 2. Install packages
curl -sL https://dtcooper.github.io/raspotify/install.sh | sh
sudo apt-get install -y snapclient

# 3. Reboot to apply audio HAT
sudo reboot
```

After reboot, continue with remaining configuration from sections 2-6 above.

---

## Deployed Speakers

| Speaker Name | IP Address | Status |
|--------------|------------|--------|
| Sala | 192.168.1.202 | ✅ Configured |
| Camera-Da-Letto | 192.168.1.204 | ✅ Configured |
| Cucina | 192.168.1.201 | ✅ Configured |
| Bagno | 192.168.1.205 | ✅ Configured |

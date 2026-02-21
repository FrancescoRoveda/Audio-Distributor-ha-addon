# wifi sound house setup
I have 3 rpi zero 2w with an innomaker hifi hat that connects to bookshelf speakers. 
this is the output config: 
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
    slave.pcm "dmixed"
}

ctl.!default {
    type hw
    card 0
}
## amixer scontrols
Simple mixer control 'A.Mstr Vol',0
Simple mixer control 'B.L Vol',0
Simple mixer control 'C.R Vol',0
Simple mixer control 'D.Lim thresh',0
Simple mixer control 'F.Limiter Enable',0
Simple mixer control 'G.Limiter Attck',0
Simple mixer control 'H.Limiter Rls',0
Simple mixer control 'I.Err flycap',0
Simple mixer control 'J.Err overcurr',0
Simple mixer control 'K.Err pllerr',0
Simple mixer control 'L.Err pvddunder',0
Simple mixer control 'M.Err overtempw',0
Simple mixer control 'N.Err overtempe',0
Simple mixer control 'O.Err pinlowimp',0
Simple mixer control 'P.Err dcprot',0
Simple mixer control 'Q.PM Prof',0
Simple mixer control 'R.Power Mode',0

## aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: sndrpimerusamp [snd_rpi_merus_amp], device 0: Merus Audio Amp ma120x0p-amp-0 [Merus Audio Amp ma120x0p-amp-0]
  Subdevices: 1/1
  Subdevice #0: subdevice #0

# ingress 
Each pi is running raspotify airplayshare and snapcast. I want to be able to use all three. 

## cat /etc/shairport-sync.conf
general = {
    name = "Cucina AirPlay";
};

alsa = {
    output_device = "default";
    mixer_control_name = "A.Mstr Vol";
    mixer_device = "hw:0";
};

## cat /etc/default/snapclient
SNAPCLIENT_OPTS='--host 192.168.1.200 -s default --mixer hardware:hw:0?name=A.Mstr%20Vol'


## cat /etc/raspotify/conf
LIBRESPOT_NAME="Cucina"
LIBRESPOT_BITRATE="320"
LIBRESPOT_DEVICE="default"
LIBRESPOT_MIXER="alsa"
LIBRESPOT_ALSA_MIXER_DEVICE="hw:0"
LIBRESPOT_ALSA_MIXER_CONTROL="A.Mstr Vol"
LIBRESPOT_AUTOPLAY="on"
LIBRESPOT_ENABLE_VOLUME_NORMALISATION=false
LIBRESPOT_INITIAL_VOLUME="75"
TMPDIR=/tmp

# Snapcast Volume Control Card Setup Guide

## Step 1: Find Your Snapcast Entity IDs

### Method 1: Using Developer Tools (Recommended)
1. Open Home Assistant
2. Go to **Developer Tools** (⚙️ icon in sidebar) → **States** tab
3. In the filter box, type: `media_player.snapcast`
4. You should see entities like:
   - `media_player.snapcast_group_[name]` - This is your group/master volume
   - `media_player.snapcast_client_[mac_or_name]` - Individual clients

### Method 2: Using Settings
1. Go to **Settings** → **Devices & Services**
2. Find **Snapcast** integration
3. Click on it to see all entities
4. Note down the entity IDs

### Expected Entity IDs
Based on your setup, you're looking for something like:
- **Group**: `media_player.snapcast_group_default` or `media_player.snapcast_group_[your_group_name]`
- **Cucina**: `media_player.snapcast_client_2c_cf_67_a7_b2_2f` (based on MAC: 2c:cf:67:a7:b2:2f)
- **Sala**: `media_player.snapcast_client_2c_cf_67_a7_b3_fd` (based on MAC: 2c:cf:67:a7:b3:fd)

> **Note**: The client entity IDs might use the MAC address or a friendly name depending on your Snapcast configuration.

---

## Step 2: Choose Your Card Style

I've created **3 different card options** for you:

### Option 1: Mushroom Cards (Modern & Beautiful) ⭐ Recommended
**File**: `snapcast-volume-card.yaml`
- **Requires**: [Mushroom Cards](https://github.com/piitaya/lovelace-mushroom) custom component
- **Pros**: Beautiful modern design, compact, great UX
- **Install Mushroom**: HACS → Frontend → Search "Mushroom" → Install

### Option 2: Slider Cards (Compact)
**File**: `snapcast-volume-card-alternative.yaml`
- **Requires**: [slider-entity-row](https://github.com/thomasloven/lovelace-slider-entity-row) custom component
- **Pros**: Very compact, slider-based volume control
- **Install**: HACS → Frontend → Search "slider-entity-row" → Install

### Option 3: Standard Cards (No Custom Components)
**File**: `snapcast-volume-card-simple.yaml`
- **Requires**: Nothing! Uses built-in Home Assistant cards
- **Pros**: Works immediately, no installation needed
- **Cons**: Less compact, basic styling

---

## Step 3: Add the Card to Your Dashboard

1. Open your Home Assistant dashboard
2. Click the **✏️ Edit Dashboard** button (top right)
3. Click **+ ADD CARD** button
4. Scroll down and select **Manual** card
5. Copy the contents from one of the YAML files above
6. **Replace the entity IDs** with your actual entity IDs from Step 1
7. Click **Save**

### Example: Replacing Entity IDs

If your actual entity IDs are:
- Group: `media_player.snapcast_group_living_room`
- Cucina: `media_player.snapcast_client_2c_cf_67_a7_b2_2f`
- Sala: `media_player.snapcast_client_2c_cf_67_a7_b3_fd`

Replace in the YAML:
```yaml
# Change this:
entity: media_player.snapcast_group_default

# To this:
entity: media_player.snapcast_group_living_room
```

---

## Step 4: Customize (Optional)

### Change Icons
Replace the icon values:
```yaml
icon: mdi:speaker-wireless  # or mdi:volume-high, mdi:speaker-bluetooth, etc.
```

### Change Names
```yaml
name: Kitchen  # Instead of Cucina
name: Living Room  # Instead of Sala
```

### Add More Speakers
Just duplicate the speaker card section and change the entity ID:
```yaml
- type: custom:mushroom-media-player-card
  entity: media_player.snapcast_client_bedroom
  name: 🛏️ Bedroom
  icon: mdi:speaker
```

---

## Troubleshooting

### "Entity not found"
- Double-check the entity ID in Developer Tools → States
- Make sure Snapcast integration is properly configured
- Restart Home Assistant if you just added the integration

### "Custom element doesn't exist"
- You need to install the custom card from HACS
- Clear browser cache (Ctrl+F5 or Cmd+Shift+R)
- Restart Home Assistant

### Volume control doesn't work
- Check that the Snapcast clients are connected (green in Snapweb)
- Verify the clients are in a group
- Check Snapcast server logs for errors

---

## Quick Command to Find Entities via SSH

If you have SSH access to your Home Assistant:
```bash
ha entity list | grep snapcast
```

Or using the Home Assistant API:
```bash
curl -H "Authorization: Bearer YOUR_LONG_LIVED_TOKEN" \
     http://homeassistant.local:8123/api/states | \
     grep -i snapcast
```

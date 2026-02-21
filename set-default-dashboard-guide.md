# How to Set Default Dashboard in Home Assistant

## Quick Method (UI - Recommended)

### For Your User Only:
1. Click your **profile** (bottom left corner)
2. Scroll to **"Default dashboard"**
3. Select your preferred dashboard
4. Click **"Update"**

### For All Users (Admin):
1. Go to **Settings** → **Dashboards**
2. Click **⋮** (three dots) next to your dashboard
3. Select **"Set as default"**

---

## Advanced: Via Configuration File

If you want to set it via `configuration.yaml`:

```yaml
# Add to configuration.yaml
lovelace:
  mode: storage
  dashboards:
    lovelace-home:
      mode: yaml
      title: Home
      icon: mdi:home
      show_in_sidebar: true
      filename: dashboards/home.yaml
```

Then create the dashboard file at `/config/dashboards/home.yaml`

---

## Tips

### Hide Unwanted Dashboards
1. **Settings** → **Dashboards**
2. Click **⋮** on the dashboard you want to hide
3. Select **"Show in sidebar"** to toggle visibility

### Reorder Dashboards in Sidebar
1. **Settings** → **Dashboards**
2. Use the **drag handle** (≡) to reorder dashboards
3. The order will be reflected in your sidebar

### Create a New Dashboard
1. **Settings** → **Dashboards**
2. Click **"+ Add Dashboard"** (bottom right)
3. Choose:
   - **"New dashboard from scratch"** - Empty dashboard
   - **"New dashboard from existing"** - Copy another dashboard

---

## Mobile App Default

To set the default dashboard for the Home Assistant mobile app:

1. Open the **Home Assistant mobile app**
2. Go to **Settings** (in the app)
3. Tap **"Default page"**
4. Select your preferred dashboard

---

## Troubleshooting

### Dashboard not showing as default?
- Clear browser cache (Ctrl+F5 or Cmd+Shift+R)
- Log out and log back in
- Check if you have a user-specific default set (it overrides admin default)

### Can't find the dashboard in the list?
- Make sure it's set to **"Show in sidebar"**
- Check **Settings** → **Dashboards** to verify it exists

### Want to reset to Home Assistant default?
- Set **"Overview"** as default
- Or create a new dashboard and set it as default

Linux utility for binding keyboard/mouse/touchpad actions to system actions.

This is an **unofficial** bundle of <https://github.com/taj-ny/InputActions>; please decide for yourself whether to trust it.

The rpmspec can be found at <https://github.com/Silvigarabis/inputactions-rpmspec>

## Usage

1. Enable copr repo:

   ```
   sudo dnf copr enable silvigarabis/inputactions
   ```

2. Choose either the KWin integration or the standalone mode; they are not intended to be used together.

---

### KDE Plasma (KWin Integration)

1. Install the KWin integration package:

   ```
   sudo dnf install inputactions-kwin
   ```

2. Open **System Settings → Desktop Effects**.

3. Enable the InputActions effect.

No systemd service is required when using the KWin integration.

---

### Standalone Mode (systemd Service)

1. Install the standalone package:

   ```
   sudo dnf install inputactions-standalone
   ```

2. Enable and start the systemd service:

   ```
   sudo systemctl enable --now inputactionsd.service
   ```

   A `sock` will appear as /run/inputactions/sock with permission bit 666

3. Start the client application:

   ```
   inputactions-client &
   ```
---

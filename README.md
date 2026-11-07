# Windows 11 Plymouth Theme for Linux

<p align="center">
  <img src="previews/win11_boot_screen_preview.gif" alt="Windows 11 Plymouth Boot Preview" width="400">
</p>

<p align="center">
  <b>Pixel-perfect, authentic Windows 11 boot splash animation for Linux (Plymouth)</b><br>
  Dumped and rendered directly from official Windows 11 boot system resources (<code>bootres.dll</code> and <code>segoe_slboot.ttf</code>).
</p>

---

## ✨ Features

- **100% Authentic Visuals**: Extracted directly from Windows 11 UEFI boot components.
- **Two Animation Styles**:
  - `win11-ring`: The modern Windows 11 progressive ring spinner (119 smooth anti-aliased frames).
  - `win11-dots`: The classic Windows 10/11 spinning circular dots (121 frames).
- **Sub-pixel Centering**: Every frame is mathematically anchored to eliminate any jitter or off-center wobble.
- **LUKS Disk Encryption Support**: Clean password prompt with entry field and bullet indicators for encrypted drives.
- **Universal Linux Compatibility**: Automated installer supporting Ubuntu, Debian, Arch Linux, Manjaro, Fedora, openSUSE, and others.

| Modern Ring (`win11-ring`) | Classic Dots (`win11-dots`) | Official Logo Vector |
| :---: | :---: | :---: |
| <img src="previews/win11_ring_spinner.gif" width="160"> | <img src="previews/win11_dots_spinner.gif" width="160"> | <img src="previews/winlogo_180.png" width="140"> |

---

## 🚀 Quick Install

```bash
git clone https://github.com/besiple/win11-plymouth-theme.git
cd win11-plymouth-theme
sudo ./install.sh
```

To install with the classic dotted spinner instead:
```bash
sudo ./install.sh --dots
```

---

## 🧪 Test Without Rebooting

You can preview the theme in a test window without restarting:

```bash
sudo plymouthd; sudo plymouth --show-splash; sleep 6; sudo plymouth quit
```

---

## 🛠 Manual Installation

1. Copy the desired theme directory to the Plymouth themes folder:
   ```bash
   sudo cp -r win11-ring /usr/share/plymouth/themes/
   # or: sudo cp -r win11-dots /usr/share/plymouth/themes/
   ```

2. Set default theme and rebuild your initramfs:

   ### **Ubuntu / Debian / Linux Mint:**
   ```bash
   sudo update-alternatives --install /usr/share/plymouth/themes/default.plymouth default.plymouth /usr/share/plymouth/themes/win11-ring/win11-ring.plymouth 150
   sudo update-alternatives --set default.plymouth /usr/share/plymouth/themes/win11-ring/win11-ring.plymouth
   sudo update-initramfs -u
   ```

   ### **Arch Linux / Manjaro:**
   ```bash
   sudo plymouth-set-default-theme -R win11-ring
   sudo mkinitcpio -P
   ```
   *(Ensure `plymouth` hook is added to `/etc/mkinitcpio.conf` after `base` and `udev`)*

   ### **Fedora / RHEL:**
   ```bash
   sudo plymouth-set-default-theme -R win11-ring
   sudo dracut -f
   ```

---

## 🔬 How Assets Were Dumped

1. **Boot Logo**: Extracted from `C:\Windows\Boot\Resources\bootres.dll`. Inside PE resource type `10` (RT_RCDATA) `1` resides an embedded WIM container (`bootres.wim`) compressed with LZX containing native `winlogo1.bmp` through `winlogo5.bmp` (284x284).
2. **Boot Spinner Animation**: Windows 11 does not store boot spinners as video or GIF files. Instead, vector curves are stored as TrueType font glyphs inside `C:\Windows\Boot\Fonts\segoe_slboot.ttf`:
   - `U+E100` – `U+E176`: Modern Progressive Ring frames (119 glyphs).
   - `U+E052` – `U+E0CB`: Classic Dotted Circle frames (121 glyphs).
3. The generator script `build_themes.py` reads the font outlines using FreeType/PIL, centers the coordinate bounding boxes, and rasterizes transparent PNG frames at native boot resolution.

All raw extracted dumps and reproduction scripts are included in `raw_extracted/` and `build_themes.py`.

---

## 📜 License

- Theme engine and scripts: MIT License.
- Windows brand graphics and font glyphs are intellectual property of Microsoft Corporation. For educational, personal customization and fair-use boot theming purposes.

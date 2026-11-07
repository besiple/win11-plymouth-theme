#!/bin/bash
set -e

echo "=================================================="
echo "    Windows 11 Plymouth Theme Installer for Linux"
echo "=================================================="

if [ "$EUID" -ne 0 ]; then
  echo "[-] Please run as root: sudo ./install.sh"
  exit 1
fi

THEMES_DIR="/usr/share/plymouth/themes"
mkdir -p "$THEMES_DIR"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[+] Copying themes to $THEMES_DIR..."
cp -r "$SCRIPT_DIR/win11-ring" "$THEMES_DIR/"
cp -r "$SCRIPT_DIR/win11-dots" "$THEMES_DIR/"
chmod -R 755 "$THEMES_DIR/win11-ring" "$THEMES_DIR/win11-dots"

CHOSEN_THEME="win11-ring"

if [ "$1" == "--dots" ]; then
    CHOSEN_THEME="win11-dots"
fi

echo "[+] Setting default theme to '$CHOSEN_THEME'..."

# Ubuntu / Debian / Mint
if command -v update-alternatives &>/dev/null; then
    update-alternatives --install "$THEMES_DIR/default.plymouth" default.plymouth "$THEMES_DIR/$CHOSEN_THEME/$CHOSEN_THEME.plymouth" 150
    update-alternatives --set default.plymouth "$THEMES_DIR/$CHOSEN_THEME/$CHOSEN_THEME.plymouth"
    echo "[+] Updating initramfs..."
    update-initramfs -u
# Arch Linux / Manjaro
elif command -v plymouth-set-default-theme &>/dev/null; then
    plymouth-set-default-theme -R "$CHOSEN_THEME"
    if command -v mkinitcpio &>/dev/null; then
        echo "[+] Updating mkinitcpio..."
        mkinitcpio -P
    elif command -v dracut &>/dev/null; then
        echo "[+] Updating dracut..."
        dracut -f
    fi
# Fedora / RHEL
elif command -v dracut &>/dev/null; then
    plymouth-set-default-theme "$CHOSEN_THEME"
    echo "[+] Updating dracut..."
    dracut -f
else
    echo "[!] Could not detect initramfs tool. Please rebuild your initramfs manually."
fi

echo ""
echo "[✓] Installation complete!"
echo "To test the theme right now without rebooting, run:"
echo "    sudo plymouthd; sudo plymouth --show-splash; sleep 5; sudo plymouth quit"

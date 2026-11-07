import os
import shutil
import tarfile
from PIL import Image, ImageFont, ImageDraw

def build_all():
    base_dir = r'C:\Users\zking\.gemini\antigravity\scratch\win11_boot_dump'
    raw_dir = os.path.join(base_dir, 'raw_extracted')
    preview_dir = os.path.join(base_dir, 'previews')
    theme_ring_dir = os.path.join(base_dir, 'win11-ring')
    theme_dots_dir = os.path.join(base_dir, 'win11-dots')
    font_path = os.path.join(raw_dir, 'segoe_slboot.ttf')

    for d in [raw_dir, preview_dir, theme_ring_dir, theme_dots_dir]:
        os.makedirs(d, exist_ok=True)

    print('[1/6] Processing Windows 11 Logos...')
    logo_bmp = os.path.join(raw_dir, 'winlogo5.bmp')
    im_logo = Image.open(logo_bmp)
    
    # Save raw 284x284 PNG
    im_logo.save(os.path.join(preview_dir, 'winlogo_284.png'))
    
    # Create transparent 284x284
    im_rgba = im_logo.convert('RGBA')
    pixels = im_rgba.load()
    for y in range(im_rgba.height):
        for x in range(im_rgba.width):
            r, g, b, a = pixels[x, y]
            if r < 10 and g < 10 and b < 10:
                pixels[x, y] = (0, 0, 0, 0)
    
    im_rgba.save(os.path.join(preview_dir, 'winlogo_transparent.png'))
    
    # Standard Plymouth logo size (180x180 px, perfectly proportioned for 1080p/1440p)
    logo_180 = im_rgba.resize((180, 180), Image.Resampling.LANCZOS)
    logo_180.save(os.path.join(theme_ring_dir, 'logo.png'))
    logo_180.save(os.path.join(theme_dots_dir, 'logo.png'))
    logo_180.save(os.path.join(preview_dir, 'winlogo_180.png'))
    
    # Create crisp SVG vector logo
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 284 284" width="284" height="284">
  <defs>
    <linearGradient id="win11grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1493df"/>
      <stop offset="100%" stop-color="#047cd6"/>
    </linearGradient>
  </defs>
  <!-- Top-left -->
  <rect x="1" y="1" width="137" height="137" fill="url(#win11grad)"/>
  <!-- Top-right -->
  <rect x="145" y="1" width="137" height="137" fill="url(#win11grad)"/>
  <!-- Bottom-left -->
  <rect x="1" y="145" width="137" height="137" fill="url(#win11grad)"/>
  <!-- Bottom-right -->
  <rect x="145" y="145" width="137" height="137" fill="url(#win11grad)"/>
</svg>'''
    with open(os.path.join(preview_dir, 'winlogo.svg'), 'w', encoding='utf-8') as f:
        f.write(svg_content)

    print('[2/6] Rendering Modern Win11 Ring Spinner Frames...')
    # Target canvas 128x128, font_size 72 gives 96px diameter with 16px padding
    W, H = 128, 128
    font_size = 72
    font = ImageFont.truetype(font_path, size=font_size)
    draw_x = 16.0
    draw_y = 94.0

    ring_frames = []
    ring_gif_frames = []
    for idx, cp in enumerate(range(0xE100, 0xE177)):
        img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((draw_x, draw_y), chr(cp), font=font, fill=(255, 255, 255, 255), anchor='ls')
        frame_name = f'throbber-{idx}.png'
        img.save(os.path.join(theme_ring_dir, frame_name))
        ring_frames.append(img)
        
        # Black background for GIF preview
        gif_im = Image.new('RGB', (W, H), (0, 0, 0))
        gif_im.paste(img, (0, 0), img)
        ring_gif_frames.append(gif_im)

    ring_gif_frames[0].save(
        os.path.join(preview_dir, 'win11_ring_spinner.gif'),
        save_all=True,
        append_images=ring_gif_frames[1:],
        duration=20,
        loop=0
    )

    print('[3/6] Rendering Classic Win10/11 Dots Spinner Frames...')
    dots_frames = []
    dots_gif_frames = []
    for idx, cp in enumerate(range(0xE052, 0xE0CB)):
        img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((draw_x, draw_y), chr(cp), font=font, fill=(255, 255, 255, 255), anchor='ls')
        frame_name = f'throbber-{idx}.png'
        img.save(os.path.join(theme_dots_dir, frame_name))
        dots_frames.append(img)
        
        gif_im = Image.new('RGB', (W, H), (0, 0, 0))
        gif_im.paste(img, (0, 0), img)
        dots_gif_frames.append(gif_im)

    dots_gif_frames[0].save(
        os.path.join(preview_dir, 'win11_dots_spinner.gif'),
        save_all=True,
        append_images=dots_gif_frames[1:],
        duration=20,
        loop=0
    )

    print('[4/6] Creating Full Boot Animation Preview GIF...')
    # Complete boot screen preview (400x500 px)
    prev_w, prev_h = 400, 500
    boot_gif_frames = []
    
    logo_prev = im_rgba.resize((150, 150), Image.Resampling.LANCZOS)
    logo_x = (prev_w - 150) // 2
    logo_y = 120
    spinner_x = (prev_w - W) // 2
    spinner_y = logo_y + 150 + 50

    for f_idx in range(len(ring_frames)):
        bg = Image.new('RGB', (prev_w, prev_h), (0, 0, 0))
        bg.paste(logo_prev, (logo_x, logo_y), logo_prev)
        cur_ring = ring_frames[f_idx]
        bg.paste(cur_ring, (spinner_x, spinner_y), cur_ring)
        boot_gif_frames.append(bg)

    boot_gif_frames[0].save(
        os.path.join(preview_dir, 'win11_boot_screen_preview.gif'),
        save_all=True,
        append_images=boot_gif_frames[1:],
        duration=20,
        loop=0
    )

    print('[5/6] Creating Plymouth Scripts and Configs...')
    # Generate bullet and entry images for password prompt (LUKS encryption)
    bullet = Image.new('RGBA', (12, 12), (0, 0, 0, 0))
    d_b = ImageDraw.Draw(bullet)
    d_b.ellipse((1, 1, 10, 10), fill=(255, 255, 255, 255))
    bullet.save(os.path.join(theme_ring_dir, 'bullet.png'))
    bullet.save(os.path.join(theme_dots_dir, 'bullet.png'))

    entry = Image.new('RGBA', (260, 32), (0, 0, 0, 0))
    d_e = ImageDraw.Draw(entry)
    d_e.rectangle((0, 0, 259, 31), outline=(100, 100, 100, 255), width=1)
    entry.save(os.path.join(theme_ring_dir, 'entry.png'))
    entry.save(os.path.join(theme_dots_dir, 'entry.png'))

    def make_plymouth_files(theme_path, theme_id, theme_name, frame_count):
        plymouth_cfg = f'''[Plymouth Theme]
Name={theme_name}
Description=Authentic Windows 11 Boot Animation
ModuleName=script

[script]
ImageDir=/usr/share/plymouth/themes/{theme_id}
ScriptFile=/usr/share/plymouth/themes/{theme_id}/{theme_id}.script
'''
        with open(os.path.join(theme_path, f'{theme_id}.plymouth'), 'w', encoding='utf-8') as f:
            f.write(plymouth_cfg)

        script_code = f'''# -------------------------------------------------------------
# Windows 11 Plymouth Theme - {theme_name}
# -------------------------------------------------------------

# Screen setup
screen_w = Window.GetWidth();
screen_h = Window.GetHeight();

# Pure black background
Window.SetBackgroundTopColor(0.0, 0.0, 0.0);
Window.SetBackgroundBottomColor(0.0, 0.0, 0.0);

# Logo
logo_img = Image("logo.png");
logo_sprite = Sprite();
logo_sprite.SetImage(logo_img);
logo_w = logo_img.GetWidth();
logo_h = logo_img.GetHeight();
logo_x = screen_w / 2 - logo_w / 2;
logo_y = screen_h / 2 - logo_h / 2 - 50;
logo_sprite.SetX(logo_x);
logo_sprite.SetY(logo_y);
logo_sprite.SetOpacity(1.0);

# Spinner Animation
frame_count = {frame_count};
for (i = 0; i < frame_count; i++) {{
    throbber[i] = Image("throbber-" + i + ".png");
}}

spinner_sprite = Sprite();
spinner_w = throbber[0].GetWidth();
spinner_h = throbber[0].GetHeight();
spinner_x = screen_w / 2 - spinner_w / 2;
spinner_y = logo_y + logo_h + 40;
spinner_sprite.SetX(spinner_x);
spinner_sprite.SetY(spinner_y);

progress = 0;

fun refresh_callback () {{
    frame_idx = progress % frame_count;
    spinner_sprite.SetImage(throbber[frame_idx]);
    progress++;
}}

Plymouth.SetRefreshFunction(refresh_callback);

# Password prompt handling (LUKS disk encryption)
status = "normal";
prompt_sprite = Sprite();
bullet_img = Image("bullet.png");
entry_img = Image("entry.png");
entry_sprite = Sprite();

fun display_password_callback (prompt, bullets) {{
    status = "password";
    logo_sprite.SetOpacity(0.4);
    spinner_sprite.SetOpacity(0.0);

    prompt_img = Image.Text(prompt, 1.0, 1.0, 1.0);
    prompt_sprite.SetImage(prompt_img);
    prompt_sprite.SetX(screen_w / 2 - prompt_img.GetWidth() / 2);
    prompt_sprite.SetY(screen_h / 2 - 40);

    entry_sprite.SetImage(entry_img);
    entry_sprite.SetX(screen_w / 2 - entry_img.GetWidth() / 2);
    entry_sprite.SetY(screen_h / 2);

    # Render password bullets
    bullet_total_w = bullets * 14;
    bullet_start_x = screen_w / 2 - bullet_total_w / 2;
    for (i = 0; i < bullets; i++) {{
        bullets_sprite[i] = Sprite();
        bullets_sprite[i].SetImage(bullet_img);
        bullets_sprite[i].SetX(bullet_start_x + i * 14);
        bullets_sprite[i].SetY(screen_h / 2 + 10);
    }}
}}

fun display_normal_callback () {{
    status = "normal";
    logo_sprite.SetOpacity(1.0);
    spinner_sprite.SetOpacity(1.0);
    prompt_sprite.SetImage(Image(""));
    entry_sprite.SetImage(Image(""));
    for (i = 0; i < 50; i++) {{
        bullets_sprite[i] = null;
    }}
}}

fun display_message_callback (text) {{
    msg_img = Image.Text(text, 0.8, 0.8, 0.8);
    msg_sprite = Sprite();
    msg_sprite.SetImage(msg_img);
    msg_sprite.SetX(screen_w / 2 - msg_img.GetWidth() / 2);
    msg_sprite.SetY(screen_h - 60);
}}

Plymouth.SetDisplayPasswordFunction(display_password_callback);
Plymouth.SetDisplayNormalFunction(display_normal_callback);
Plymouth.SetMessageFunction(display_message_callback);

# Quit callback
fun quit_callback () {{
    logo_sprite.SetOpacity(0.0);
    spinner_sprite.SetOpacity(0.0);
}}
Plymouth.SetQuitFunction(quit_callback);
'''
        with open(os.path.join(theme_path, f'{theme_id}.script'), 'w', encoding='utf-8') as f:
            f.write(script_code)

    make_plymouth_files(theme_ring_dir, 'win11-ring', 'Windows 11 Ring', len(ring_frames))
    make_plymouth_files(theme_dots_dir, 'win11-dots', 'Windows 11 Dots', len(dots_frames))

    # Create master install.sh script for Linux
    install_sh = '''#!/bin/bash
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
'''
    with open(os.path.join(base_dir, 'install.sh'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(install_sh)

    print('[6/6] Packaging themes into win11_plymouth_themes.tar.gz...')
    archive_path = os.path.join(base_dir, 'win11_plymouth_themes.tar.gz')
    with tarfile.open(archive_path, 'w:gz') as tar:
        tar.add(theme_ring_dir, arcname='win11-ring')
        tar.add(theme_dots_dir, arcname='win11-dots')
        tar.add(os.path.join(base_dir, 'install.sh'), arcname='install.sh')
        tar.add(preview_dir, arcname='previews')
        tar.add(raw_dir, arcname='raw_extracted')

    print(f'Archive created: {archive_path} ({os.path.getsize(archive_path)} bytes)')
    print('ALL DONE!')

build_all()

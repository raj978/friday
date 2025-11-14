#!/usr/bin/env python3
"""
Update splash screens with transparent backgrounds
"""

from PIL import Image, ImageDraw
import os

staticdir = "./static/static"

def create_splash_png(size, output_path, dark_mode=False):
    """Create splash screen with transparent background and arc reactor logo"""
    # Transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Arc reactor in center, larger
    logo_size = size // 2  # Make it bigger
    logo_x = (size - logo_size) // 2
    logo_y = (size - logo_size) // 2

    # Colors
    if dark_mode:
        blue = (79, 195, 247, 255)  # Lighter blue for dark mode
        gold = (212, 175, 55, 255)
    else:
        blue = (30, 144, 255, 255)  # Dodger blue
        gold = (212, 175, 55, 255)

    ring_width = max(3, logo_size // 40)

    # Outer gold ring
    draw.ellipse([logo_x, logo_y, logo_x+logo_size, logo_y+logo_size],
                 outline=gold, width=ring_width)

    # Second gold ring (slightly inside)
    offset = ring_width * 3
    draw.ellipse([logo_x+offset, logo_y+offset, logo_x+logo_size-offset, logo_y+logo_size-offset],
                 outline=gold, width=max(1, ring_width//2))

    # Blue energy rings
    blue_ring_size = logo_size * 3 // 4
    blue_margin = (logo_size - blue_ring_size) // 2
    blue_transparent = (blue[0], blue[1], blue[2], 150)
    draw.ellipse([logo_x+blue_margin, logo_y+blue_margin,
                  logo_x+blue_margin+blue_ring_size, logo_y+blue_margin+blue_ring_size],
                 outline=blue_transparent, width=ring_width//2)

    # Another blue ring
    blue_ring_size2 = logo_size // 2
    blue_margin2 = (logo_size - blue_ring_size2) // 2
    draw.ellipse([logo_x+blue_margin2, logo_y+blue_margin2,
                  logo_x+blue_margin2+blue_ring_size2, logo_y+blue_margin2+blue_ring_size2],
                 outline=blue, width=ring_width//2)

    # Center blue circle with glow
    center_size = logo_size // 3
    center_margin = (logo_size - center_size) // 2
    draw.ellipse([logo_x+center_margin, logo_y+center_margin,
                  logo_x+center_margin+center_size, logo_y+center_margin+center_size],
                 fill=(blue[0], blue[1], blue[2], 80),
                 outline=blue, width=ring_width//2)

    # Inner gold ring around core
    inner_size = logo_size // 5
    inner_margin = (logo_size - inner_size) // 2
    draw.ellipse([logo_x+inner_margin, logo_y+inner_margin,
                  logo_x+inner_margin+inner_size, logo_y+inner_margin+inner_size],
                 outline=gold, width=ring_width//2)

    # Bright white center
    core_size = logo_size // 10
    core_margin = (logo_size - core_size) // 2
    # Glow effect
    glow_size = logo_size // 7
    glow_margin = (logo_size - glow_size) // 2
    draw.ellipse([logo_x+glow_margin, logo_y+glow_margin,
                  logo_x+glow_margin+glow_size, logo_y+glow_margin+glow_size],
                 fill=(79, 195, 247, 200) if dark_mode else (30, 144, 255, 200))

    draw.ellipse([logo_x+core_margin, logo_y+core_margin,
                  logo_x+core_margin+core_size, logo_y+core_margin+core_size],
                 fill=(255, 255, 255, 255))

    img.save(output_path, 'PNG')
    print(f"  ✓ Created {os.path.basename(output_path)} ({size}x{size})")

def main():
    print("\n🎨 Updating splash screens (transparent background)\n")

    # Regenerate splash screens with transparent background
    create_splash_png(512, os.path.join(staticdir, "splash.png"), dark_mode=False)
    create_splash_png(512, os.path.join(staticdir, "splash-dark.png"), dark_mode=True)

    print("\n✅ Splash screens updated with transparent background!\n")

if __name__ == "__main__":
    main()

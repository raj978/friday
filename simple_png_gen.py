#!/usr/bin/env python3
"""
Simple PNG generator using PIL/Pillow only
Creates basic colored circles as placeholders for Friday logo
"""

from PIL import Image, ImageDraw, ImageFont
import os

staticdir = "./static/static"

def create_arc_reactor_png(size, output_path, dark_mode=False):
    """Create a simple arc reactor inspired icon"""
    # Create image with transparency
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center = size // 2

    # Colors
    if dark_mode:
        bg_color = (10, 14, 26, 255)  # Dark background
        blue = (79, 195, 247, 255)  # Lighter blue for dark mode
        gold = (212, 175, 55, 255)
    else:
        bg_color = (10, 14, 26, 255)  # Dark background
        blue = (30, 144, 255, 255)  # Dodger blue
        gold = (212, 175, 55, 255)

    # Background circle
    draw.ellipse([0, 0, size-1, size-1], fill=bg_color)

    # Outer gold ring
    ring_width = max(2, size // 40)
    draw.ellipse([ring_width*2, ring_width*2, size-ring_width*2-1, size-ring_width*2-1],
                 outline=gold, width=ring_width)

    # Blue energy rings
    blue_transparent = (blue[0], blue[1], blue[2], 180)
    draw.ellipse([size//4, size//4, size*3//4, size*3//4],
                 outline=blue_transparent, width=max(1, ring_width//2))

    # Center blue circle with glow
    center_size = size // 3
    margin = (size - center_size) // 2
    draw.ellipse([margin, margin, margin+center_size, margin+center_size],
                 fill=(blue[0], blue[1], blue[2], 100),
                 outline=blue, width=max(1, ring_width//2))

    # Inner gold ring
    inner_size = size // 5
    inner_margin = (size - inner_size) // 2
    draw.ellipse([inner_margin, inner_margin, inner_margin+inner_size, inner_margin+inner_size],
                 outline=gold, width=max(1, ring_width//3))

    # Bright center
    core_size = size // 10
    core_margin = (size - core_size) // 2
    draw.ellipse([core_margin, core_margin, core_margin+core_size, core_margin+core_size],
                 fill=(255, 255, 255, 230))

    img.save(output_path, 'PNG')
    print(f"  ✓ Created {os.path.basename(output_path)} ({size}x{size})")

def create_splash_png(size, output_path, dark_mode=False):
    """Create splash screen with Friday text"""
    img = Image.new('RGBA', (size, size), (255, 255, 255, 255) if not dark_mode else (10, 14, 26, 255))
    draw = ImageDraw.Draw(img)

    # Draw arc reactor logo at top
    logo_size = size // 3
    logo_y = size // 4
    logo_x = (size - logo_size) // 2

    # Mini arc reactor
    center_x = size // 2
    center_y = logo_y + logo_size // 2

    blue = (79, 195, 247, 255) if dark_mode else (30, 144, 255, 255)
    gold = (212, 175, 55, 255)

    # Outer ring
    draw.ellipse([logo_x, logo_y, logo_x+logo_size, logo_y+logo_size],
                 outline=gold, width=max(2, logo_size//30))

    # Blue circle
    inner_size = logo_size * 2 // 3
    inner_margin = (logo_size - inner_size) // 2
    draw.ellipse([logo_x+inner_margin, logo_y+inner_margin,
                  logo_x+inner_margin+inner_size, logo_y+inner_margin+inner_size],
                 fill=(blue[0], blue[1], blue[2], 100),
                 outline=blue, width=max(2, logo_size//40))

    # Center
    core_size = logo_size // 6
    core_margin = (logo_size - core_size) // 2
    draw.ellipse([logo_x+core_margin, logo_y+core_margin,
                  logo_x+core_margin+core_size, logo_y+core_margin+core_size],
                 fill=(255, 255, 255, 255))

    # Add "FRIDAY" text
    try:
        font_size = size // 10
        # Try to use a system font
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()

        text = "FRIDAY"
        # Get text size using textbbox
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (size - text_width) // 2
        text_y = size * 3 // 5

        text_color = (79, 195, 247, 255) if dark_mode else (30, 144, 255, 255)
        draw.text((text_x, text_y), text, fill=text_color, font=font)

        # Subtitle
        small_font_size = size // 25
        try:
            small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", small_font_size)
        except:
            small_font = font

        subtitle = "Your AI Assistant"
        bbox = draw.textbbox((0, 0), subtitle, font=small_font)
        subtitle_width = bbox[2] - bbox[0]
        subtitle_x = (size - subtitle_width) // 2
        subtitle_y = text_y + text_height + 20

        subtitle_color = gold if dark_mode else (102, 102, 102, 255)
        draw.text((subtitle_x, subtitle_y), subtitle, fill=subtitle_color, font=small_font)
    except Exception as e:
        print(f"    Warning: Could not add text: {e}")

    img.save(output_path, 'PNG')
    print(f"  ✓ Created {os.path.basename(output_path)} ({size}x{size})")

def main():
    print("\n🎨 Friday Logo PNG Generation (Simple Mode)\n")
    print("Generating PNG files using Pillow...\n")

    # Generate favicons
    create_arc_reactor_png(512, os.path.join(staticdir, "favicon.png"), dark_mode=False)
    create_arc_reactor_png(96, os.path.join(staticdir, "favicon-96x96.png"), dark_mode=False)
    create_arc_reactor_png(512, os.path.join(staticdir, "favicon-dark.png"), dark_mode=True)

    # Generate splash screens
    create_splash_png(512, os.path.join(staticdir, "splash.png"), dark_mode=False)
    create_splash_png(512, os.path.join(staticdir, "splash-dark.png"), dark_mode=True)

    # Generate logo
    create_arc_reactor_png(512, os.path.join(staticdir, "logo.png"), dark_mode=False)

    # Generate PWA icons
    create_arc_reactor_png(180, os.path.join(staticdir, "apple-touch-icon.png"), dark_mode=False)
    create_arc_reactor_png(192, os.path.join(staticdir, "web-app-manifest-192x192.png"), dark_mode=False)
    create_arc_reactor_png(512, os.path.join(staticdir, "web-app-manifest-512x512.png"), dark_mode=False)

    print("\n✅ PNG generation complete!\n")
    print("Note: These are simplified versions. For better quality:")
    print("1. Convert the SVG files using https://cloudconvert.com/svg-to-png")
    print("2. Or install ImageMagick: brew install imagemagick\n")

if __name__ == "__main__":
    main()

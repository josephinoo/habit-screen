import json
import os
import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Configuration
WIDTH = 3840
HEIGHT = 2160
BG_COLOR = "#1F2430"  # Dark Blue-Grey
CARD_COLOR = "#FFFFFF"
SHADOW_COLOR = (0, 0, 0, 80) # Black with transparency
ACTIVE_COLOR = "#FFB86C" # Orange/Yellow
EMPTY_COLOR = "#FDF6E3" # Light Cream
TEXT_COLOR = "#2E3440"

# Grid Config
COLS = 52
ROWS = 7
CELL_SIZE = 30
GAP = 8
GRID_WIDTH = (COLS * CELL_SIZE) + ((COLS - 1) * GAP)
GRID_HEIGHT = (ROWS * CELL_SIZE) + ((ROWS - 1) * GAP)

# Card Config
PADDING = 60
CARD_WIDTH = GRID_WIDTH + (PADDING * 2)
CARD_HEIGHT = GRID_HEIGHT + (PADDING * 2) + 80 # Extra space for header
CORNER_RADIUS = 20

def create_rounded_rectangle(width, height, radius, color):
    """Creates a rounded rectangle image."""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, width, height), radius, fill=color)
    return img

def create_shadow(width, height, radius, offset, blur_radius, color):
    """Creates a shadow for the rounded rectangle."""
    shadow_width = width + 2 * blur_radius
    shadow_height = height + 2 * blur_radius
    shadow = Image.new('RGBA', (shadow_width, shadow_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)

    # Draw the shadow rectangle centered but offset
    shadow_rect = (
        blur_radius + offset[0],
        blur_radius + offset[1],
        blur_radius + offset[0] + width,
        blur_radius + offset[1] + height
    )
    draw.rounded_rectangle(shadow_rect, radius, fill=color)

    # Apply Gaussian blur
    return shadow.filter(ImageFilter.GaussianBlur(blur_radius))

def draw_grid(draw, start_x, start_y, dates):
    """Draws the habit grid."""
    today = datetime.date.today()
    # Calculate start date (364 days ago to cover 52 weeks approx)
    # Actually, let's align so the last column is the current week
    # For simplicity, let's just show the last 364 days ending today.
    start_date = today - datetime.timedelta(days=(COLS * ROWS) - 1)

    date_set = set()
    for d_str in dates:
        try:
            d = datetime.datetime.strptime(d_str, "%Y-%m-%d").date()
            date_set.add(d)
        except ValueError:
            pass

    current_date = start_date

    # We draw column by column
    for col in range(COLS):
        for row in range(ROWS):
            x = start_x + col * (CELL_SIZE + GAP)
            y = start_y + row * (CELL_SIZE + GAP)

            color = EMPTY_COLOR
            if current_date in date_set:
                color = ACTIVE_COLOR

            draw.rounded_rectangle((x, y, x + CELL_SIZE, y + CELL_SIZE), radius=4, fill=color)

            current_date += datetime.timedelta(days=1)

def set_wallpaper(image_path):
    """Sets the wallpaper using the external bash script."""
    abs_path = os.path.abspath(image_path)
    script_path = os.path.abspath("set_wallpaper.sh")

    cmd = f'"{script_path}" "{abs_path}"'

    print(f"Calling bash script: {cmd}")

    try:
        ret = os.system(cmd)
        if ret != 0:
            print(f"Bash script failed with exit code {ret}.")
            print("Please check System Settings -> Privacy & Security -> Automation.")
    except Exception as e:
        print(f"Error executing bash script: {e}")

def main(title, subtitle, dates):
    # 1. Create Background
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)

    # 2. Create Card and Shadow
    card_x = (WIDTH - CARD_WIDTH) // 2
    card_y = (HEIGHT - CARD_HEIGHT) // 2

    shadow = create_shadow(CARD_WIDTH, CARD_HEIGHT, CORNER_RADIUS, (0, 10), 20, SHADOW_COLOR)
    card = create_rounded_rectangle(CARD_WIDTH, CARD_HEIGHT, CORNER_RADIUS, CARD_COLOR)

    # Composite Shadow then Card
    # Shadow position needs to account for the blur padding
    shadow_x = card_x - 20 # 20 is blur radius
    shadow_y = card_y - 20

    img.paste(shadow, (shadow_x, shadow_y), shadow)
    img.paste(card, (card_x, card_y), card)

    draw = ImageDraw.Draw(img)

    # 3. Draw Text
    try:
        # Try to load a nice font, fallback to default
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60, index=0)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30, index=0)
    except IOError:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    draw.text((card_x + PADDING, card_y + PADDING), title, fill=TEXT_COLOR, font=title_font)
    draw.text((card_x + PADDING, card_y + PADDING + 70), subtitle, fill="#888888", font=subtitle_font)

    # 4. Draw Grid (Data is now passed in)
    grid_start_y = card_y + PADDING + 120
    draw_grid(draw, card_x + PADDING, grid_start_y, dates)

    # 5. Save and Set
    timestamp = int(datetime.datetime.now().timestamp())
    output_path = f"wallpaper_{timestamp}.png"
    img.save(output_path)
    print(f"Wallpaper generated: {output_path}")

    set_wallpaper(output_path)

    # Cleanup old wallpapers
    for f in os.listdir("."):
        if f.startswith("wallpaper_") and f.endswith(".png") and f != output_path:
            try:
                os.remove(f)
                print(f"Removed old wallpaper: {f}")
            except OSError:
                pass
    # Also remove the static one if it exists
    if os.path.exists("wallpaper.png"):
        try:
            os.remove("wallpaper.png")
        except OSError:
            pass

if __name__ == "__main__":
    # Load Data
    try:
        with open("habitos.json", "r") as f:
            dates = json.load(f)
    except FileNotFoundError:
        print("habitos.json not found, using empty list.")
        dates = []

    main("READ BIBLE", "Last 365 Days", dates)

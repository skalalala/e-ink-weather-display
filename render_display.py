from datetime import datetime
from zoneinfo import ZoneInfo

from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont

from weather import get_forecast


WIDTH = 800
HEIGHT = 480


WEATHER_QUOTES = {
    "Clear": (
        "Far away in the sunshine are my highest aspirations.",
        "— Louisa May Alcott",
    ),
    "Clouds": (
        "The clouds never overran the sky but that birds put heart into him.",
        "— Thomas Hardy",
    ),
    "Rain": (
        "I bring fresh showers for the thirsting flowers.",
        "— Percy Bysshe Shelley",
    ),
    "Drizzle": (
        "...the drizzle of the rain...",
        "— Kaneko Fumiko",
    ),
    "Snow": (
        "Snow had fallen, snow on snow.",
        "— Christina Rossetti",
    ),
    "Thunderstorm": (
        "We love the lovely thunder.",
        "— Ogden Nash",
    ),
    "Squall": (
        "...there’s a squall coming up, I think.",
        "— Herman Melville",
    ),
    "Tornado": (
        "...rides in the whirlwind and directs the storm.",
        "— Alexander Pope",
    ),
    "Mist": (
        "Fog everywhere. Fog up the river...",
        "— Charles Dickens",
    ),
    "Fog": (
        "Fog everywhere. Fog up the river...",
        "— Charles Dickens",
    ),
    "Haze": (
        "...amid the haze and the chimeras...",
        "— Vladimir Nabokov",
    ),
    "Smoke": (
        "Only thin smoke without flame...",
        "— Thomas Hardy",
    ),
    "Dust": (
        "Dust as we are, the immortal spirit grows...",
        "— William Wordsworth",
    ),
    "Sand": (
        "A wise man can pick up a grain of sand...",
        "— Jack Handey",
    ),
    "Ash": (
        "Dust as we are, the immortal spirit grows...",
        "— William Wordsworth",
    ),
}


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def format_header_date():
    now = datetime.now(ZoneInfo("America/New_York"))
    return now.strftime("%a · %b %d").upper()


def wrap_text(text, draw, font, max_width):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = word if not current else f"{current} {word}"
        bbox = draw.textbbox((0, 0), test, font=font)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def render_display():
    forecast = get_forecast()

    if len(forecast) < 6:
        raise ValueError("Forecast data did not include enough days.")

    today_weather = forecast[0]
    next_five = forecast[1:6]

    img = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    font_header = load_font("assets/fonts/Inter-Regular.ttf", 18)
    font_condition = load_font("assets/fonts/Inter-Regular.ttf", 28)
    font_range = load_font("assets/fonts/Inter-Regular.ttf", 22)
    font_hero = load_font("assets/fonts/Inter-Bold.ttf", 108)
    font_day = load_font("assets/fonts/Inter-Regular.ttf", 20)
    font_forecast_high = load_font("assets/fonts/Inter-Bold.ttf", 28)
    font_forecast_low = load_font("assets/fonts/Inter-Regular.ttf", 22)
    font_quote = load_font("assets/fonts/Inter-Regular.ttf", 22)
    font_quote_attr = load_font("assets/fonts/Inter-Regular.ttf", 16)

    # Header
    draw.text((24, 22), format_header_date(), fill="black", font=font_header)
    draw.text((610, 22), "BROOKLYN, NY", fill="black", font=font_header)

    # Hero temperature
    hero_temp = today_weather.get("current", today_weather["high"])
    hero_text = f'{hero_temp}°'
    draw.text((24, 78), hero_text, fill="black", font=font_hero)

    # Condition
    condition_text = today_weather["condition"].title()
    draw.text((30, 205), condition_text, fill="black", font=font_condition)

    # High / low
    range_text = f'H {today_weather["high"]}°   L {today_weather["low"]}°'
    draw.text((30, 245), range_text, fill="black", font=font_range)

    # Quote block (center-right)
    quote_text, quote_attr = WEATHER_QUOTES.get(
        today_weather["condition"],
        ("Weather is a great metaphor for life.", "— Terri Guillemets"),
    )

    quote_x = 390
    quote_y = 122
    quote_max_width = 320
    line_gap = 8

    wrapped_quote = wrap_text(f'"{quote_text}"', draw, font_quote, quote_max_width)
    current_y = quote_y

    for line in wrapped_quote[:2]:
        draw.text((quote_x, current_y), line, fill="black", font=font_quote)
        bbox = draw.textbbox((0, 0), line, font=font_quote)
        line_height = bbox[3] - bbox[1]
        current_y += line_height + line_gap

    current_y += 6
    draw.text((quote_x, current_y), quote_attr, fill="black", font=font_quote_attr)

    # Bottom 5-day forecast
    start_x = 28
    col_width = 148
    y_day = 360
    y_high = 392
    y_low = 426

    for i, day_weather in enumerate(next_five):
        col_left = start_x + i * col_width

        day_label = datetime.strptime(day_weather["date"], "%Y-%m-%d").strftime("%a").upper()
        high_text = f'{day_weather["high"]}°'
        low_text = f'{day_weather["low"]}°'

        draw.text((col_left, y_day), day_label, fill="black", font=font_day)
        draw.text((col_left, y_high), high_text, fill="black", font=font_forecast_high)
        draw.text((col_left, y_low), low_text, fill="black", font=font_forecast_low)

    img.save("preview.png")
    print("preview.png generated")

    inky_display = auto()
    inky_display.set_image(img)
    inky_display.show()
    print("Inky display updated")


if __name__ == "__main__":
    render_display()

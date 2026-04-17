# e-ink-weather-display
A Python-based weather display for the Pimoroni Inky Impression 7.3" e-ink screen, powered by OpenWeather data and custom-rendered typography.

![Preview](/preview.png)

## Overview
This project fetches current weather data from the OpenWeather API and renders it into a custom visual layout designed for an e-ink display. It was built as a small side project combining API integration, lightweight Python scripting, and visual design for low-power hardware.

The display is intended to feel more considered than a basic dashboard: functional, but with enough typography and layout work to make it feel like a desk object rather than just a utility.

## Features
- Pulls live weather data from OpenWeather
- Renders a custom display image for e-ink
- Uses custom font assets for a more editorial visual style
- Generates a unique quote based on weather pattern variables
- Separates data-fetching logic from rendering logic
- Designed for a lightweight hardware setup

## Stack
- Python
- OpenWeather API
- Pillow
- Pimoroni Inky Impression 7.3"
- Font files from Google Fonts

## Project Structure
```text
inky-weather-display/
├── README.md
├── .gitignore
├── requirements.txt
├── .env.example
├── weather.py
├── render_display.py
├── assets/
│   ├── font-1.ttf
│   └── font-2.ttf
└── output/
    └── sample-display.png

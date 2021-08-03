# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def song_oled(song_str1,song_str="提示："):
    # Raspberry Pi pin configuration:
    RST = 24
    # 128x32 display with hardware I2C:
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

    # Initialize library.
    disp.begin()

    # Clear display.
    disp.clear()
    disp.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('song.ttf', 15)

    # First define some constants to allow easy resizing of shapes.
    padding = 0
    top = padding
    bottom = height-padding

    # 增加 x 值可以将文字向右移动
    x = 1
    draw.text((x, top+1), song_str, font=font, fill=255)
    draw.text((x, top+16), song_str1, font=font, fill=255)
    disp.image(image)
    disp.display()

song_oled("test")
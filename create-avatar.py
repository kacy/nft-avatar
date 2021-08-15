#!/usr/bin/python3
import argparse
import random

from PIL import Image

bg_colors = [
	(105,210,231,255),
	(167,219,216,255),
	(224,228,204,255),
	(243,134,48,255),
	(250,105,0,255),
]

base = Image.open("images/base.png")

mouth_list = [
	"images/mouth-smile.png",
	"images/mouth-tongue.png",
	"images/mouth-wha.png",
	"images/mouth-open.png",
]

hat_list = [
	None,
	"images/head-hat.png",
	"images/head-bandana.png",
	"images/head-sailor.png",
	"images/head-bear.png",
	"images/head-beanie.png",
]

bottom_list = [
	None,
	"images/bottom-jeans.png",
	"images/bottom-swim-flower.png",
	"images/bottom-red.png",
]

parser = argparse.ArgumentParser(description='Randomly generate images.')
parser.add_argument('integers', metavar='N', type=int, 
                    help='an integer for the number to generate')

parser.add_argument("--preview", help="do you want the preview?",
					action="store_true")

args = parser.parse_args()

for i in range(0, args.integers):
	mouth_index = random.randint(0, len(mouth_list) - 1)
	hat_index = random.randint(0, len(hat_list) - 1)
	bottom_index = random.randint(0, len(bottom_list) - 1)
	bg_index = random.randint(0, len(bg_colors) - 1)

	background = Image.new('RGBA', (800,800), bg_colors[bg_index])

	background.paste(base , (0,0), base)

	mouth = Image.open(mouth_list[mouth_index])
	background.paste(mouth, (0, 0), mouth)

	if hat_index != 0:
		hat = Image.open(hat_list[hat_index])
		background.paste(hat, (0, 0), hat)

	if bottom_index != 0:
		bottom = Image.open(bottom_list[bottom_index])
		background.paste(bottom, (0, 0), bottom)
	
	if args.preview:
		background.show()

	background.save(f"images/output/{i}.png", format='PNG')

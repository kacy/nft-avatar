#!/usr/bin/python3
import argparse
import random

from PIL import Image


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
	background = Image.open("images/base.png")
	mouth_chosen = random.randint(0, len(mouth_list) - 1)
	hat_chosen = random.randint(0, len(hat_list) - 1)
	bottom_chosen = random.randint(0, len(bottom_list) - 1)

	mouth = Image.open(mouth_list[mouth_chosen])
	background.paste(mouth, (0, 0), mouth)

	if hat_chosen != 0:
		hat = Image.open(hat_list[hat_chosen])
		background.paste(hat, (0, 0), hat)

	if bottom_chosen != 0:
		bottom = Image.open(bottom_list[bottom_chosen])
		background.paste(bottom, (0, 0), bottom)
	
	if args.preview:
		background.show()

	background.save(f"images/output/{i}.png", format='PNG')

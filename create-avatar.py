#!/usr/bin/python3
import argparse
from datetime import datetime
import json
import os
import random

from PIL import Image
import requests

bg_colors = [
	(105,210,231,255),
	(167,219,216,255),
	(224,228,204,255),
	(243,134,48,255),
	(250,105,0,255),
]

base = Image.open("images/base.png")

mouth_list = [
	("images/mouth-smile.png", "Smile"),
	("images/mouth-tongue.png", "Tongue"), 
	("images/mouth-whoa.png", "Whoa"),
	("images/mouth-open.png", "Open"),
]

hat_list = [
	(None, "Nothing"),
	("images/head-hat.png", "Hat"),
	("images/head-bandana.png", "Bandana"),
	("images/head-sailor.png", "Sailor"),
	("images/head-bear.png", "Bear"),
	("images/head-beanie.png", "Beanie"),
]

bottom_list = [
	(None, "Nothing"),
	("images/bottom-jeans.png", "Jeans"),
	("images/bottom-swim-flower.png", "Flower Swim Shorts"),
	("images/bottom-red.png", "Red Swim Shorts"),
]

parser = argparse.ArgumentParser(description='Randomly generate images.')
parser.add_argument('integers', metavar='N', type=int, 
                    help='an integer for the number to generate')

parser.add_argument("--preview", help="do you want the preview?",
					action="store_true")

parser.add_argument("--upload", help="do you want to upload to IPFS using Infura?",
					action="store_true")

args = parser.parse_args()

def upload_to_infura(file_name):
	infura_url = "https://ipfs.infura.io:5001/api/v0/add?pin=true"
	project_id = os.environ.get('INFURA_PROJECT_ID')
	project_secret = os.environ.get('INFURA_PROJECT_SECRET')

	files = {'upload_file': open(file_name,'rb')}

	if project_id and project_secret:
		try:
			r = requests.post(infura_url, auth=(project_id, project_secret), files=files)
			hash = r.json().get('Hash')
			return f"ipfs://{hash}"
		except Exception as e:
			print(e)

	return None

def generate():
	for i in range(0, args.integers):
		token_id = i + 1
		attributes = []

		bg_index = random.randint(0, len(bg_colors) - 1)

		background = Image.new('RGBA', (800,800), bg_colors[bg_index])

		background.paste(base , (0,0), base)

		# Mouth
		mouth_index = random.randint(0, len(mouth_list) - 1)
		mouth = mouth_list[mouth_index]
		mouth_image = Image.open(mouth[0])
		background.paste(mouth_image, (0, 0), mouth_image)

		mouth_trait = {
			"trait_type": "Mouth",
			"value": mouth[1]
		}

		attributes.append(mouth_trait)

		# Hat
		hat_index = random.randint(0, len(hat_list) - 1)
		hat = hat_list[hat_index]
		if hat_index != 0:
			hat_image = Image.open(hat[0])
			background.paste(hat_image, (0, 0), hat_image)

		hat_trait = {
			"trait_type": "Hat",
			"value": hat[1]
		}
		attributes.append(hat_trait)

		# Bottom
		bottom_index = random.randint(0, len(bottom_list) - 1)
		bottom = bottom_list[bottom_index]
		if bottom_index != 0:
			bottom_image = Image.open(bottom[0])
			background.paste(bottom_image, (0, 0), bottom_image)

		bottom_trait = {
			"trait_type": "Bottom",
			"value": bottom[1]
		}
		attributes.append(bottom_trait)

		if args.preview:
			background.show()

		background.save(f"images/output/{token_id}.png", format='PNG')
		
		ipfs_uri = ""
		if args.upload:
			ipfs_uri = upload_to_infura(f"images/output/{token_id}.png")

		traits = {
			"name": f"Your New PFP #{token_id}",
			"description": "Randomly generated image",
			"external_url": "https://foo.com",
			"attributes": attributes,
			"image": ipfs_uri,
			"tokenId": token_id,
			"mintedAt": datetime.now().strftime("%B %d, %Y at %H:%M"),
		}

		file_name = f"traits/{token_id}.json"
		with open(file_name, 'w') as f:
			f.write(json.dumps(traits))
			f.close()

		print(traits)

if __name__ == "__main__":
	generate()
# -*- coding: utf-8 -*-
from PIL import Image, ImageFilter, ImageDraw, ImageFont

# params are string, float, float. keep the floats to 3 digits left of decimal (ex: 140.44)
def Generate_Stamp(satellite_name, elevation_degrees, azmith_degrees):
	# background
	base = Image.open("BlankStamp2.png")

	# transparent layer for the text
	txt = Image.new('RGBA', base.size, (255, 255, 255, 0))
	
	#add the font for big text, 2nd param is the font point size
	leng = len(satellite_name)
	if (leng < 12):
		fnt = ImageFont.truetype('nasalization-rg.ttf', 220)
		#print("1")
	elif (leng >= 12 and leng < 15):
		fnt = ImageFont.truetype('nasalization-rg.ttf', 180)
		#print("2")
	elif (leng >= 15 and leng < 17):
		fnt = ImageFont.truetype('nasalization-rg.ttf', 150)
		#print("3")
	elif (leng >= 17 and leng < 19):
		fnt = ImageFont.truetype('nasalization-rg.ttf', 130)
		#print("4")
	elif (leng >= 19 and leng < 20):
		fnt = ImageFont.truetype('nasalization-rg.ttf', 120)
		#print("5")
	else:
		fnt = ImageFont.truetype('nasalization-rg.ttf', 100)


	# "get a drawing context" -from PIL website
	# basically makes an image drawable (maybe???)
	d = ImageDraw.Draw(txt)


	# converting to the internal variable I used, a vestage from the previous development
	satName = satellite_name

	# constants for satellite text
	x, y = (2280, 1200)
	w, h = fnt.getsize(satName)

	# Draw some text
	# Params:
	# 1. tuple (x, y)
	# 2. text string
	# 3. font=the_font_you_import
	# 4. fill=(r,g,b,alpha)
	d.text(((x-w)/2,(y-h)/2), satName, font=fnt, fill=(255,255,255,255)) # , align="center"
	# print((y-h)/2) debugging

	# Make the font for the elivation and azmith
	fnt2 = ImageFont.truetype('nasalization-rg.ttf', 60)

	elevationNum = elevation_degrees
	elevationStr = "elevation: " + '%.1f' % elevationNum + "°"
	azmithNum = azmith_degrees
	azmithStr = "azmith: " + '%.1f' % azmithNum + "°"

	# Draw the azmith and elevation
	rightCorner = (x+w)/2 # to left justify these
	width, height = fnt2.getsize(elevationStr) # to place the text box on
	leftCorner = rightCorner - width
	fnt2.getsize(elevationStr) # to place the text box on

	# the y cordinate that the two strings are based on
	eleAsmHeight = 710

	# draw elevation
	d.text((leftCorner, eleAsmHeight), elevationStr, font=fnt2, fill=(255,255,255,255))

	# Azmith line setup
	azmithOffset = 0
	azmithTop = eleAsmHeight + height + azmithOffset
	width2, height2 = fnt2.getsize(azmithStr) # to place the text box on
	leftCorner2 = rightCorner - width2

	# drawing the azmith line
	d.text((leftCorner2, azmithTop), azmithStr, font=fnt2, fill=(255,255,255,255))


	# make the two images into one by superimposing
	out = Image.alpha_composite(base, txt)

	out.save("SatSnapSticker" + ".png")


satName = "1bigsatbatfo"
satEle = 144.2
satAzm = 281.7

Generate_Stamp(satName, satEle, satAzm)

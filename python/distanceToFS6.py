# -*- coding: utf-8 -*-
import ephem
import datetime
from PIL import Image, ImageFilter, ImageDraw, ImageFont


# grab lat, long, and elev from file created by other script

def Generate_Stamp(satellite_name, elevation_degrees, azmith_degrees):
    # background
    base = Image.open("BlankStamp2.png")

    # transparent layer for the text
    txt = Image.new('RGBA', base.size, (255, 255, 255, 0))

    # add the font for big text, 2nd param is the font point size
    leng = len(satellite_name)
    if (leng < 10):
        fnt = ImageFont.truetype('nasalization-rg.ttf', 220)
    # print("1")
    elif (leng >= 10 and leng < 15):
        fnt = ImageFont.truetype('nasalization-rg.ttf', 180)
    # print("2")
    elif (leng >= 15 and leng < 17):
        fnt = ImageFont.truetype('nasalization-rg.ttf', 150)
    # print("3")
    elif (leng >= 17 and leng < 19):
        fnt = ImageFont.truetype('nasalization-rg.ttf', 130)
    # print("4")
    elif (leng >= 19 and leng < 20):
        fnt = ImageFont.truetype('nasalization-rg.ttf', 120)
    # print("5")
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
    d.text(((x - w) / 2, (y - h) / 2), satName, font=fnt, fill=(255, 255, 255, 255))  # , align="center"
    # print((y-h)/2) debugging

    # Make the font for the elivation and azmith
    fnt2 = ImageFont.truetype('nasalization-rg.ttf', 60)
    t = u"\u00b0"

    elevationNum = elevation_degrees
    elevationStr = "elevation: " + str(round(elevationNum, 3)) + t
    azmithNum = azmith_degrees
    azmithStr = "azmith: " + str(round(azmithNum, 3)) + t

    # Draw the azmith and elevation
    rightCorner = (x + w) / 2  # to left justify these
    width, height = fnt2.getsize(elevationStr)  # to place the text box on
    leftCorner = rightCorner - width
    fnt2.getsize(elevationStr)  # to place the text box on

    # the y cordinate that the two strings are based on
    eleAsmHeight = 710

    # draw elevation
    d.text((leftCorner, eleAsmHeight), elevationStr, font=fnt2, fill=(255, 255, 255, 255))

    # Azmith line setup
    azmithOffset = 0
    azmithTop = eleAsmHeight + height + azmithOffset
    width2, height2 = fnt2.getsize(azmithStr)  # to place the text box on
    leftCorner2 = rightCorner - width2

    # drawing the azmith line
    d.text((leftCorner2, azmithTop), azmithStr, font=fnt2, fill=(255, 255, 255, 255))

    # make the two images into one by superimposing
    out = Image.alpha_composite(base, txt)

    out.save(satellite_name + "_" + str(elevation_degrees) + "_" + str(azmith_degrees) + ".png")


def findsat(lat, long, elev):
    currentDT = datetime.datetime.utcnow()
    date = currentDT.strftime("%Y-%m-%d %H:%M:%S")

    observer = ephem.Observer()
    observer.lat = lat
    observer.long = long
    observer.elev = elev  # meters
    observer.date = date

    mercury,venus,mars,jupiter,saturn = ephem.Mercury(), ephem.Venus(), ephem.Mars(), ephem.Jupiter(),ephem.Saturn()
    mercury.compute(observer)
    venus.compute(observer)
    mars.compute(observer)
    jupiter.compute(observer)
    saturn.compute(observer)

    list = [[000, mercury.alt, mercury.az, "Mercury"], [000, venus.alt, venus.az, "Venus"], [000, mars.alt, mars.az, "Mars"], [000, jupiter.alt, jupiter.az, "Jupiter"], [000, saturn.alt, saturn.az, "Saturn"]]
    filename = "tle.txt"
    file = open(filename, "r")
    z = 1
    satname = ""
    line1 = ""
    line2 = ""
    lowest = 0
    lowestindex = 0
    differencelist = [0, 0, 0, 0, 0]
    for line in file:
        if (z == 1):
            z = 2
            satname = line.strip()
        elif (z == 2):
            z = 3
            line1 = line.strip()
        elif (z == 3):
            z = 1
            line2 = line.strip()
        else:
            print("Error in switching in for loop. Error 1")
        if (z == 1):
            sat = ephem.readtle(satname, line1, line2)
            observer.date = date
            sat.compute(observer)
            if (str(sat.rise_time) == "None" or str(sat.set_time) == "None" or len(satname) > 20):
                continue
            satrise = datetime.datetime.strptime(str(sat.rise_time), "%Y/%m/%d %H:%M:%S")
            satset = datetime.datetime.strptime(str(sat.set_time), "%Y/%m/%d %H:%M:%S")
            satalt = str(sat.alt).split(":")
            satalt = float(satalt[0]) + float(satalt[1]) / 60 + float(satalt[2]) / (60 * 60)
            sataz = str(sat.az).split(":")
            sataz = float(sataz[0]) + float(sataz[1]) / 60 + float(sataz[2]) / (60 * 60)
            if (satrise > satset):
                hey = line2.split()
                differencelist = [0, 0, 0, 0, 0]
                for x in range(5):
                    differencelist[x] = satalt - list[x][1]
                lowest = 0
                for x in range(5):
                    if (lowest <= differencelist[x] and differencelist[x] > 0):
                        lowestindex = x
                        lowest = differencelist[x]
                if (lowest > 0):
                    list[lowestindex][0] = hey[1]
                    list[lowestindex][1] = satalt
                    list[lowestindex][2] = sataz
                    list[lowestindex][3] = satname
    file.close()
    return list


sats = findsat("40.0150", "-105.2705", 1623)
for x in range(5):
    Generate_Stamp(sats[x][3].strip(), sats[x][1], sats[x][2])

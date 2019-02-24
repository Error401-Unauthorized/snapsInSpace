import ephem
import datetime

currentDT = datetime.datetime.utcnow()
date = currentDT.strftime("%Y-%m-%d %H:%M:%S")
list = [[0, 0, 0, ""], [0, 0, 0, ""], [0, 0, 0, ""], [0, 0, 0, ""], [0, 0, 0, ""]]

observer = ephem.Observer()
observer.lat = "40.0150"
observer.long = "-105.2705"
observer.elev = 1623 #meters
observer.date = date

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
        if (str(sat.rise_time) == "None" or str(sat.set_time) == "None" or len(satname) > 15):
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
print(list)
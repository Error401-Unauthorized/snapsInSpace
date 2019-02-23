import ephem
import datetime
#INPUTS: lat,long,elev

currentDT = datetime.datetime.utcnow()
date = currentDT.strftime("%Y-%m-%d %H:%M")
print(date)

observer = ephem.Observer()
observer.lat = "40.0150"
observer.long = "-105.2705"
observer.elev = 5328
observer.date = date
fs6 = ephem.readtle("FS6",
    "1 43815U 18099BK  19054.46451949 -.00000110  00000-0 -47213-5 0  9995",
    "2 43815  97.7564 127.7936 0013782   3.8408 356.2916 14.95121012 11909")

observer.date = date
fs6.compute(observer)
print("%s : %s %s %s" % (date, fs6.rise_time, fs6.transit_time, fs6.set_time))

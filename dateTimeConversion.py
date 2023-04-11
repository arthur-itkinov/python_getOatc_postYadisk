import datetime
from datetime import datetime
from datetime import timedelta



def dateTimeConversion(utc_time):
    number = int(str(utc_time)[:-3])
    five_hours = timedelta(hours=5)
    newdate = datetime.utcfromtimestamp(number) + five_hours
    return newdate


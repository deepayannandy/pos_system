from datetime import datetime
import pytz


def getdate():
    IST = pytz.timezone('Asia/Kolkata')
    datetime_ist = datetime.now(IST)
    return datetime_ist.strftime('%a %d/%b/%y')
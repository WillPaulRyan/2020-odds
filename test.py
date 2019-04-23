from datetime import datetime
from dateutil import tz


FMT = '%Y-%m-%d %H:%M:%S'

time = '2019-04-16 19:03:43'

t = datetime.strptime(time, FMT)

print(tz.tzlocal(t))
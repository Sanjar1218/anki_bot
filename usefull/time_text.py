import datetime

# adding time to current time
# td = datetime.timedelta(minutes=10)
# print(datetime.datetime.today() + td)

ct = datetime.datetime.today()

# converts to unix time
unix_time = ct.timestamp()

# deconverst to human readeble time
date_time = datetime.datetime.fromtimestamp(unix_time)

print(date_time)
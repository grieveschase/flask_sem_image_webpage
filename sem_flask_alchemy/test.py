import datetime

t = datetime.datetime.strptime("2019-01-01","%Y-%m-%d")

y = datetime.timedelta(seconds=1)
print(y)
print(t+y)
print(t-y)
print(datetime.datetime.strftime(t+y, "%Y-%m-%d-%H-%M-%S"))

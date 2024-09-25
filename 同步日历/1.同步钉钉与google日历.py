import caldav
import datetime

# 钉钉日历的CalDAV URL
dd_calendar_url = 'https://calendar.dingtalk.com/dav/u_xsbefegr/primary/'

# 用户名和密码
dd_username = 'u_xsbefegr'  # 替换为你的用户名
dd_password = 'f0p46qjl'  # 替换为你的密码

# 创建CalDAV客户端
client = caldav.DAVClient(url=dd_calendar_url, username=dd_username, password=dd_password)

# 获取用户的主要日历
principal = client.principal()
calendars = principal.calendars()

# 假设我们只关心第一个日历
target_calendar = calendars[0]

# 获取指定日期范围内的事件
events = target_calendar.date_search(
    start=datetime.datetime.now() - datetime.timedelta(days=365),
    end=datetime.datetime.now() + datetime.timedelta(days=365),
    expand=True
)

# 打印每个事件的基本信息
for event in events:
    print(f"Summary: {event.summary}")
    print(f"Start Time: {event.start}")
    print(f"End Time: {event.end}")
    print("-----")
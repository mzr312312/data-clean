import requests
from requests.auth import HTTPBasicAuth
import datetime
import logging

# 设置日志记录级别为DEBUG
logging.basicConfig(level=logging.DEBUG)

# 钉钉CalDAV URL
url = 'https://calendar.dingtalk.com/dav/u_whq2z53n/primary/'
auth = HTTPBasicAuth('u_xsbefegr', 'f0p46qjl')  # 替换为实际的用户名和密码

# 构建PROPFIND请求
xml_request = """<?xml version="1.0" encoding="utf-8"?>
<DAV:propfind xmlns:DAV="DAV:" xmlns:C="urn:ietf:params:xml:ns:caldav">
  <DAV:allprop>
    <DAV:prop>
      <DAV:getcontenttype/>
      <DAV:getetag/>
      <C:calendar-data/>
    </DAV:prop>
  </DAV:allprop>
</DAV:propfind>"""

# 构建请求头
headers = {
    'Content-Type': 'application/xml',
    'Depth': '1',
}

# 发送HTTP请求
response = requests.request('PROPFIND', url, headers=headers, data=xml_request, auth=auth)

# 输出响应状态码和内容
print(response.status_code)
print(response.text)
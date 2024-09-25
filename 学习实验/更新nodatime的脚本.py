import os
import requests
import zipfile
import shutil

# 下载 NodaTime 3.1.6.0 的 NuGet 包
url = "https://www.nuget.org/api/v2/package/NodaTime/3.1.6"
download_path = "NodaTime.3.1.6.nupkg"

# 下载文件
response = requests.get(url, stream=True)
if response.status_code == 200:
    with open(download_path, 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)
else:
    print(f"Failed to download NodaTime package. Status code: {response.status_code}")
    exit(1)

# 解压文件
with zipfile.ZipFile(download_path, 'r') as zip_ref:
    zip_ref.extractall("NodaTime")

# 检查解压后的文件结构
for root, dirs, files in os.walk("NodaTime"):
    print(f"Directory: {root}")
    for file in files:
        print(f"  File: {file}")

# 获取 DLL 文件路径
dll_path = os.path.join("NodaTime", "lib", "netstandard2.0", "NodaTime.dll")
xml_path = os.path.join("NodaTime", "lib", "netstandard2.0", "NodaTime.xml")

# 目标目录
target_dir = r"C:\Program Files (x86)\CalDavSynchronizer"  # 请根据实际情况修改

# 检查文件是否存在
if not os.path.exists(dll_path):
    print(f"Error: NodaTime.dll not found at {dll_path}")
    exit(1)

if not os.path.exists(xml_path):
    print(f"Error: NodaTime.xml not found at {xml_path}")
    exit(1)

# 复制 DLL 和 XML 文件
shutil.copy(dll_path, target_dir)
shutil.copy(xml_path, target_dir)

# 清理临时文件
os.remove(download_path)
shutil.rmtree("NodaTime")

print("NodaTime 3.1.6.0 DLL 文件已成功更新到目标目录。")
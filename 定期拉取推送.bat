@echo off
:: 设置仓库目录
set REPO_DIR=D:\PycharmProjects\pythonProject
cd /d %REPO_DIR%

echo 开始同步代码...

:: 添加所有更改到暂存区
git add .

:: 设置时间戳
set TIMESTAMP=%date:~0,4%-%date:~5,2%-%date:~8,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%

:: 提交更改
git commit -m "Auto commit at %TIMESTAMP%"
if %errorlevel% neq 0 (
    echo 没有新的更改需要提交。
) else (
    echo 已提交本地更改。
)

:: 拉取远程更改并与本地合并
git pull origin main
if %errorlevel% neq 0 (
    echo 拉取远程更改时出错，请手动解决冲突。
    exit /b 1
)

:: 推送本地提交到远程仓库
git push origin main
if %errorlevel% neq 0 (
    echo 推送到远程仓库时出错，请检查网络连接或远程仓库状态。
    exit /b 1
) else (
    echo 同步成功！
)

:: 5秒倒计时
echo 脚本将在5秒后退出...
timeout /t 5 /nobreak >nul
exit

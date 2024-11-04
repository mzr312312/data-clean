@echo off
:: 设置仓库目录
set REPO_DIR="D:\PycharmProjects\pythonProject"
cd /d %REPO_DIR%

:: 拉取远程更改（先同步仓库）
git pull origin main

:: 检查拉取是否成功
if %errorlevel% neq 0 (
    echo "Error occurred while pulling the remote repository" 
    exit /b 1
)

:: 添加所有更改到 Git 暂存区
git add .

:: 提交更改
git commit -m "Auto commit at %date% %time%"

:: 推送更改到 GitHub（使用 SSH）
git push origin main

:: 检查推送是否成功
if %errorlevel% neq 0 (
    echo "Error when pushing to remote warehouse"
    exit /b 1
)

:: 成功完成操作
echo " Operation Success"

:: 5秒倒计时
echo "script will exit in 5 seconds..."
timeout /t 5 /nobreak >nul
exit

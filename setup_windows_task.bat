@echo off
REM 以管理员身份运行：注册 Datalane 每日 00:00 任务
set TASK_NAME=Datalane_Daily
set RUN_SCRIPT=%~dp0run_daily.bat

schtasks /create /tn "%TASK_NAME%" /tr "\"%RUN_SCRIPT%\"" /sc daily /st 00:00 /f

if %ERRORLEVEL% equ 0 (
    echo [OK] 计划任务: %TASK_NAME%
    echo      每天 00:00 -^> run_job.py dongqiudi
    echo 删除: schtasks /delete /tn "%TASK_NAME%" /f
) else (
    echo [FAIL] 请以管理员身份运行
)

pause

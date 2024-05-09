@echo off

@REM 切换至bat当前路径
cd /d %~dp0

@REM 运行脚本
python computer_checker.py

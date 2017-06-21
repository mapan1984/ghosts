@echo off
title "download hosts"
python D:\ghosts\ghosts.py %*
if %errorlevel% == 0 (ipconfig /flushdns) else echo "don't flush dns"
echo on

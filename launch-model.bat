@echo off
title Python Library Installer

echo ======================================================================
echo  Python Library Installer
echo  Created by Evan O
echo ======================================================================
echo.
echo  DISCLAIMER
echo.
echo  This script will use pip to download and install Python libraries
echo  (OpenCV, MediaPipe, NumPy, Open3D) from the Python Package
echo  Index (PyPI) over the internet.
echo.
echo  By proceeding, you acknowledge that you are installing third-party
echo  software onto your system.
echo.
echo ======================================================================
echo.

set /p "choice=Do you understand and wish to proceed? (Y/N): "
if /i not "%choice%"=="y" (
    echo Installation cancelled.
    goto :eof
)

echo.
echo Installing libraries... Please wait.
pip install opencv-python mediapipe numpy open3d --user

echo.
echo ======================================================================
echo.
echo  Installation complete!
echo  The program will now launch automatically...
echo.
echo ======================================================================
echo.

call model.py

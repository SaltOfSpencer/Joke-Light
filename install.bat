@echo off
setlocal enabledelayedexpansion

::ffmpeg installation

:: Setting ffmpeg installation directory
set "INSTALL_DIR=%SystemDrive%\FFmpeg"
set "FFMPEG_URL=https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
set "ZIP_FILE=%TEMP%\ffmpeg.zip"

:: Creating installation directory
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Download ffmpeg
echo Downloading ffmpeg...
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%FFMPEG_URL%', '%ZIP_FILE%')"

echo Extracting...
powershell -Command "Expand-Archive -Path '%ZIP_FILE%' -DestinationPath '%INSTALL_DIR%' -Force"

:: Locate extracted folder
for /d %%I in ("%INSTALL_DIR%\ffmpeg-*") do set "FFMPEG_FOLDER=%%I"

:: Update path environment variable
set "NEW_PATH=%FFMPEG_FOLDER%\bin"
echo Adding FFmpeg to system PATH...
setx /M PATH "%PATH%;%NEW_PATH%"

:: Cleanup
del "%ZIP_FILE%"

::Python and libraries installation

:: Define Python version and installation URL
set PYTHON_VERSION=3.10.11
set PYTHON_INSTALLER=python-3.10.11-amd64.exe
set PYTHON_URL=https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
set INSTALL_DIR=%SystemDrive%\Python_3.10.11

:: Create installation directory
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Download Python installer
echo Downloading Python !PYTHON_VERSION!...
powershell -Command "Invoke-WebRequest -Uri '!PYTHON_URL!' -OutFile '%SystemDrive%\Python_3.10.11\!PYTHON_INSTALLER!'"

:: Install Python
if not exist "!INSTALL_DIR!\python.exe" (
    echo Installing Python !PYTHON_VERSION!...
    start /wait !INSTALL_DIR!\!PYTHON_INSTALLER! /quiet InstallAllUsers=1 PrependPath=1 TargetDir="!INSTALL_DIR!"
)

:: Set environment variables
setx PATH "!INSTALL_DIR!;!INSTALL_DIR!\Scripts;!PATH!" /M

:: Verify installation
echo.
echo Python version installed:
"!INSTALL_DIR!\python.exe" --version
powershell Invoke-WebRequest -Uri "https://aka.ms/vs/17/release/vc_redist.x64.exe" -OutFile %SystemDrive%\Python_3.10.11\vc_redist.x64.exe
%SystemDrive%\Python_3.10.11\vc_redist.x64.exe /norestart -Wait

start cmd /c install2.bat

echo Installation complete. You may need to restart your system for changes to take effect.

pause


@echo off
setlocal enabledelayedexpansion
python.exe -m pip install git+https://github.com/openai/whisper.git
python.exe -m pip install git+https://github.com/ultralytics/ultralytics.git@main
python.exe -m pip install vaderSentiment
python.exe -m pip install opencv-python
python.exe -m pip install mss
python.exe -m pip install pillow
echo Installation complete. You may need to restart your system for changes to take effect.
pause
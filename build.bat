@echo off

echo Creating venv ...
python -m venv .venv

REM 만약 파이썬이 설치되어있지 않다면
if not errorlevel 0 goto FAIL

copy icon.ico .venv
copy gui.py .venv
copy logic.py .venv
cd .venv

REM venv 안에 모듈을 설치
echo Installing pillow ...
Scripts\pip.exe install pillow
if not errorlevel 0 goto FAIL

echo Installing pyinstaller ...
Scripts\pip.exe install pyinstaller
if not errorlevel 0 goto FAIL


REM EXE를 추출함
echo creating save_my_save.exe ...
Scripts\pyinstaller.exe --icon=icon.ico --onefile -w gui.py -n save_my_save.exe
goto SUCCESS


REM 분기목록
:FAIL
echo Python is not installed on your computer. Please install Python.
goto QUIT


:SUCCESS
move dist\save_my_save.exe ..\save_my_save.exe
echo SUCCESS! save_my_save.exe has been created.
goto QUIT


:QUIT
pause
exit
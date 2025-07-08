@echo off
REM Installation script for ComfyUI Contact Sheet Image Loader (Windows)

echo Installing ComfyUI Contact Sheet Image Loader...

if "%1"=="" (
    echo Usage: %0 C:\path\to\ComfyUI
    echo Please provide the path to your ComfyUI installation
    pause
    exit /b 1
)

set COMFYUI_PATH=%1
set CUSTOM_NODES_PATH=%COMFYUI_PATH%\custom_nodes

if not exist "%COMFYUI_PATH%" (
    echo Error: ComfyUI directory not found at %COMFYUI_PATH%
    pause
    exit /b 1
)

if not exist "%CUSTOM_NODES_PATH%" (
    echo Error: custom_nodes directory not found at %CUSTOM_NODES_PATH%
    pause
    exit /b 1
)

REM Create target directory
set TARGET_DIR=%CUSTOM_NODES_PATH%\comfy-contact-sheet-image-loader

if exist "%TARGET_DIR%" (
    echo Warning: Directory already exists at %TARGET_DIR%
    set /p overwrite="Do you want to overwrite it? (y/N): "
    if /i not "%overwrite%"=="y" (
        echo Installation cancelled.
        pause
        exit /b 1
    )
    rmdir /s /q "%TARGET_DIR%"
)

REM Copy files
echo Copying files to %TARGET_DIR%...
mkdir "%TARGET_DIR%"
xcopy /e /i /h /y * "%TARGET_DIR%\"

echo Installation completed!
echo.
echo Next steps:
echo 1. Restart ComfyUI
echo 2. Look for 'Contact Sheet Image Loader' in the node menu under 'image/loaders'
echo 3. See USAGE.md for detailed usage instructions
echo.
echo Enjoy your new contact sheet image loader!
pause

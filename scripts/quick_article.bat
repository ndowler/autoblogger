@echo off
REM Quick article generation script for Windows
REM Usage: quick_article.bat "Your Article Topic"

if "%~1"=="" (
    echo Usage: quick_article.bat "Your Article Topic"
    echo.
    echo Example: quick_article.bat "Home Office Tax Deduction Guide"
    exit /b 1
)

python generate_article.py --topic "%~1"

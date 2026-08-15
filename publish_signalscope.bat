@echo off
setlocal

rem This script always operates on the folder IT lives in, not wherever you
rem double-clicked it from, so it is safe against the "pushed everything"
rem mistake as long as this .bat file stays inside z5529169_projectB.
cd /d "%~dp0"

echo ================================================================
echo  SignalScope publish script
echo  Working folder: %CD%
echo ================================================================
echo.

rem --- Sanity check: are we really inside z5529169_projectB? ---
if not exist "app.py" (
    echo ERROR: app.py was not found in this folder.
    echo This script must stay inside z5529169_projectB. Aborting.
    pause
    exit /b 1
)
if not exist "streamlit_app.py" (
    echo ERROR: streamlit_app.py was not found in this folder.
    echo This script must stay inside z5529169_projectB. Aborting.
    pause
    exit /b 1
)

rem --- Check Git is installed ---
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not on PATH.
    echo Install it from https://git-scm.com/downloads, then re-run this script.
    pause
    exit /b 1
)

rem --- Check Git identity is configured (commits fail silently otherwise) ---
git config --global user.name >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git does not know who you are yet.
    echo Run these two commands once, then re-run this script:
    echo   git config --global user.name "Your Name"
    echo   git config --global user.email "you@example.com"
    pause
    exit /b 1
)
git config --global user.email >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git does not know your email yet.
    echo Run these two commands once, then re-run this script:
    echo   git config --global user.name "Your Name"
    echo   git config --global user.email "you@example.com"
    pause
    exit /b 1
)

rem --- Init a repo scoped ONLY to this folder ---
if exist ".git" (
    echo A git repository already exists in this exact folder. Reusing it.
) else (
    echo Initialising a new git repository in this folder...
    git init
)

echo.
echo Staging files (this uses the .gitignore already in this folder, so raw
echo data and secrets are excluded, but results\ is included)...
git add .

echo.
echo Files staged for commit:
git status --short
echo.
echo Review the list above. It should be ONLY files from z5529169_projectB
echo (app.py, streamlit_app.py, requirements.txt, src\, results\, report\,
echo docs\, the .md files, etc). Press Ctrl+C now to abort if anything looks
echo wrong, otherwise press any key to continue.
pause >nul

git commit -m "Initial public commit: SignalScope Project B"
if errorlevel 1 (
    echo.
    echo NOTE: Commit did not complete. This usually means there were no
    echo changes to commit ^(e.g. you already committed on a previous run^).
    echo Continuing to branch/push in case that's the case...
)

git branch -M main

echo.
echo ----------------------------------------------------------------
echo  Before continuing: go to https://github.com/new and create a
echo  NEW, EMPTY, PUBLIC repository (do not add a README or .gitignore).
echo  Then come back here and paste its URL below.
echo ----------------------------------------------------------------
echo.
set /p REPO_URL="Paste the new repo's URL (e.g. https://github.com/farhanjamilhikal/signalscope.git): "

git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%

echo.
echo Pushing to %REPO_URL% ...
echo A browser window may open asking you to sign in to GitHub - that's normal.
git push -u origin main

echo.
echo ================================================================
echo  Done. If the push above succeeded, go back to the Streamlit
echo  deploy screen and use:
echo    Repository:      (your new repo, e.g. farhanjamilhikal/signalscope)
echo    Branch:          main
echo    Main file path:  streamlit_app.py
echo ================================================================
pause

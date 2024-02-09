@echo off
SET "repoPath=C:\Users\justi\Dropbox\Scrivener\Macros\Instruction Sets\Author's Toolbox"
SET "commitMessage=Your default commit message"

REM Change to your repository's directory
cd /d "%repoPath%"

REM Stage all changes
git add .

REM Commit changes
SET /P commitMessage="Enter commit message (or press Enter to skip): "
if not "%commitMessage%"=="" (
    git commit -m "%commitMessage%"
)

REM Pull with rebase
git pull --rebase origin main
if %ERRORLEVEL% neq 0 (
    echo Error pulling changes from remote. Resolve any conflicts and try again.
    pause
    exit /b %ERRORLEVEL%
)

REM Push changes to remote
git push origin main
if %ERRORLEVEL% neq 0 (
    echo Error pushing changes to remote. Check the error message above for details.
    pause
    exit /b %ERRORLEVEL%
)

echo Changes pushed successfully.
pause
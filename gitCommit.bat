@echo off
SET "repoPath=C:\Users\justi\Dropbox\Scrivener\Macros\Instruction Sets\Author's Toolbox"
SET "commitMessage=Your default commit message"

REM Change to your repository's directory
cd /d "%repoPath%"

REM Add all changes to staging
git add .

REM Commit changes
SET /P commitMessage="Enter commit message (or press Enter to use default): "
if "%commitMessage%"=="" SET commitMessage="Your default commit message"
git commit -m "%commitMessage%"

REM Optionally push changes to remote
git push origin main

echo Commit and push (if enabled) completed.
pause

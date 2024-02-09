@echo off
SET "repoPath=C:\Users\justi\Dropbox\Scrivener\Macros\Instruction Sets\Author's Toolbox"
SET "branch=main"
SET "logFile=C:\Users\justi\Dropbox\Scrivener\Macros\Instruction Sets\Author's Toolbox\gitOperations.log"

REM Start new log
echo Starting Git operations on %DATE% at %TIME% > "%logFile%"

REM Navigate to the repository
cd /d "%repoPath%"
if %ERRORLEVEL% neq 0 (
    echo Failed to change directory to %repoPath% >> "%logFile%"
    goto end
)

echo Changed directory to %repoPath% >> "%logFile%"

REM Checkout the branch
git checkout %branch% >> "%logFile%" 2>&1
if %ERRORLEVEL% neq 0 (
    echo Failed to checkout branch %branch% >> "%logFile%"
    goto end
)

echo Checked out branch %branch% >> "%logFile%"

REM Pull changes from the remote branch and rebase
git pull --rebase origin %branch% >> "%logFile%" 2>&1
if %ERRORLEVEL% neq 0 (
    echo Failed to pull and rebase from origin %branch% >> "%logFile%"
    goto end
)

echo Successfully pulled and rebased from origin %branch% >> "%logFile%"

REM Push local changes to the remote repository
git push origin %branch% >> "%logFile%" 2>&1
if %ERRORLEVEL% neq 0 (
    echo Failed to push local changes to origin %branch% >> "%logFile%"
    goto end
)

echo Successfully pushed local changes to origin %branch% >> "%logFile%"

echo Operations completed successfully! >> "%logFile%"
goto end

:end
echo Operation log saved to %logFile%
type "%logFile%"
pause

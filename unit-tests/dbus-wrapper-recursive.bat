@echo off
setlocal

:: Note: a D-Bus session must be running with DBUS_SESSION_BUS_ADDRESS
:: set until autolaunch is supported by dbus-cxx on Windows

start /B test-recursive server %1
pathping 127.0.0.1 -n -q 1 -p 100 > nul

test-recursive client %1
:: Get the exit code
set EXIT_CODE=%ERRORLEVEL%

:: Wait for the server to finish
taskkill /FI "IMAGENAME eq test-recursive*" /T /F

:: Exit with the test-recursive client exit code
exit /B %EXIT_CODE%

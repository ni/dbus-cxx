@echo off
setlocal

:: Note: a D-Bus session must be running with DBUS_SESSION_BUS_ADDRESS
:: set until autolaunch is supported by dbus-cxx on Windows

start /B test-property server %1
pathping 127.0.0.1 -n -q 1 -p 100 > nul

test-property client %1
:: Get the exit code
set EXIT_CODE=%ERRORLEVEL%

:: Wait for the server to finish
taskkill /FI "IMAGENAME eq test-property*" /T /F

:: Exit with the test-property client exit code
exit /B %EXIT_CODE%

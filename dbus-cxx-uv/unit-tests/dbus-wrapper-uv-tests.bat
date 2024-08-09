@echo off
setlocal

:: Note: a D-Bus session must be running with DBUS_SESSION_BUS_ADDRESS
:: set until autolaunch is supported by dbus-cxx on Windows

:: Run the test-uv-dispatcher executable
start /B test-uv-dispatcher
pathping 127.0.0.1 -n -q 1 -p 100 > nul

:: Run the uv-caller executable
uv-caller
set EXIT_CODE=%ERRORLEVEL%

:: Wait for the server to finish
taskkill /FI "IMAGENAME eq test-uv-dispatcher*" /T /F

:: Exit with the uv-caller exit code
exit /B %EXIT_CODE%

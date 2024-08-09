@echo off
setlocal

:: Launch a D-Bus session
:: start "" /B dbus-launch > ???
:: set DBUS_SESSION_BUS_ADDRESS

:: Run the test-uv-dispatcher executable
start "" /B test-uv-dispatcher
set SERVER_PID=%ERRORLEVEL%
timeout /T 0.1 /NOBREAK

:: Run the uv-caller executable
uv-caller
set EXIT_CODE=%ERRORLEVEL%

:: Wait for the server to finish
taskkill /F /PID %SERVER_PID%

:: Clean up (if needed)
:: kill dbus session somehow

:: Exit with the uv-caller exit code
exit /B %EXIT_CODE%

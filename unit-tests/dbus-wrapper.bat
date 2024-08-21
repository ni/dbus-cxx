@echo off
setlocal

:: Note: a D-Bus session must be running with DBUS_SESSION_BUS_ADDRESS
:: set until autolaunch is supported by dbus-cxx on Windows

:: Run whatever was passed to us
%1 %2 %3
:: Get the exit code
set EXIT_CODE=%ERRORLEVEL%

exit /B %EXIT_CODE%

#include <winsock2.h>

#include <dbus-cxx/error.h>

class WinsockInitializer {
public:
    WinsockInitializer() {
        if( int result = WSAStartup(MAKEWORD(2, 2), &wsaData); result != 0) {
            throw DBus::ErrorFailed();
        }
    }

    ~WinsockInitializer() {
        WSACleanup();
    }

private:
    WSADATA wsaData;
};

// Global object to ensure WSAStartup is called before main()
WinsockInitializer winsockInit;

from conan import ConanFile
from conan.tools.cmake import cmake_layout, CMakeDeps, CMakeToolchain, CMake


class DbusCXX(ConanFile):
    name = "dbus-cxx"
    version = "2.4.0"

    settings = "os", "compiler", "build_type", "arch"

    # Default to a relocatable static library
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": False}

    # The package is defined in the same repo as the source so we can
    # use the exports_sources attribute rather than have an explicit
    # 'def source():' method.
    exports_sources = "CMakeLists.txt", "*.cmake", "dbus-cxx.h", "dbus-cxx/*", "dbus-cxx-uv/*", "compat/*", "cmake-tests/*", "unit-tests/*"

    def requirements(self):
        self.requires("libsigcpp/[^3.0.7]", transitive_headers=True)
        self.requires("expat/[^2.5.0]")
        self.requires("libuv/[^1.46.0]")

    def layout(self):
        cmake_layout(self)

    generators = "CMakeToolchain", "CMakeDeps"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = []
        self.cpp_info.requires = []

        # TODO: when dbus-cxx-uv is an option, add it here only when option picked
        self.cpp_info.libs.append("dbus-cxx-uv")
        self.cpp_info.requires.append("libuv::libuv")

        # Add the main dbus-cxx library last so that symbols needed by
        # the loop integration libraries are kept (alternative would
        # be --whole-archive)
        self.cpp_info.libs.append("dbus-cxx")
        self.cpp_info.requires.append("libsigcpp::sigc++")
        self.cpp_info.requires.append("expat::expat")

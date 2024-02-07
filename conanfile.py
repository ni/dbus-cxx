from conan import ConanFile
from conan.tools.cmake import cmake_layout, CMakeDeps, CMakeToolchain, CMake


class DbusCXX(ConanFile):
    name = "dbus-cxx"
    version = "2.4.0"

    settings = "os", "compiler", "build_type", "arch"

    default_options = {"libuv/(*:static": True}

    # The package is defined in the same repo as the source so we can
    # use the exports_sources attribute rather than have an explicit
    # 'def source():' method.
    exports_sources = "CMakeLists.txt", "*.cmake", "dbus-cxx.h", "dbus-cxx/*", "dbus-cxx-uv/*", "compat/*", "cmake-tests/*", "unit-tests/*"

    def requirements(self):
        self.requires("libsigcpp/[^3.0.7]")
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
        # order the dependent library first so it links correctly (hopefully)
        self.cpp_info.libs = ["dbus-cxx-uv", "dbus-cxx"]

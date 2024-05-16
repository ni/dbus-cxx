from conan import ConanFile
from conan.tools.cmake import cmake_layout, CMakeDeps, CMakeToolchain, CMake


class DbusCXX(ConanFile):
    name = "dbus-cxx"
    version = "2.4.0"

    settings = "os", "compiler", "build_type", "arch"

    # Default to a relocatable static library
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # The package is defined in the same repo as the source so we can
    # use the exports_sources attribute rather than have an explicit
    # 'def source():' method.
    exports_sources = "CMakeLists.txt", "*.cmake", "dbus-cxx.h", "dbus-cxx/*", "dbus-cxx-uv/*", "compat/*", "cmake-tests/*", "unit-tests/*"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC");

    def requirements(self):
        self.requires("libsigcpp/[^3.0.7]", transitive_headers=True)
        self.requires("expat/[^2.5.0]")

        # To support the gcc 7.3 toolchain we have to limit the libuv
        # version. RedHat 7 support was dropped in 1.45
        self.requires("libuv/[<=1.44.0]")

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

        # Add the main dbus-cxx library last so it appears last on the
        # client link command so that symbols needed by the loop
        # integration libraries above are kept (alternative would be
        # --whole-archive)
        self.cpp_info.libs.append("dbus-cxx")

        # Propagate dependencies
        self.cpp_info.requires.append("libsigcpp::sigc++")
        self.cpp_info.requires.append("expat::expat")

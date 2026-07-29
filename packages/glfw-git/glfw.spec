%global commit 364b214c6f3a962caa782104c08f905653012481
%global git_tag 3.4
%global git_abbr_commit 112-g364b214c

%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global abbr_release %(c=%{git_abbr_commit}; echo ${c//-/.})
%global capture_date 20260729

# 跟随上游设置
Epoch:          1

Name:           glfw
Version:        %(c=%{git_tag}; echo "${c}")

# Keep Release above Fedora's package so the git build remains preferred.
Release:        100.%{abbr_release}%{?dist}
Summary:        an Open Source, multi-platform library for OpenGL, OpenGL ES and Vulkan application development

License:        GPL-3.0-only
URL:            https://www.glfw.org/

Source0:        git-src.tar.zst

BuildRequires:  systemd-rpm-macros
BuildRequires:  cmake
BuildRequires:  wayland-devel libxkbcommon-devel libXcursor-devel libXi-devel libXinerama-devel libXrandr-devel 

%description
GLFW is an Open Source, multi-platform library for OpenGL, OpenGL ES and Vulkan
application development.  It provides a simple, platform-independent API for
creating windows, contexts and surfaces, reading input, handling events, etc.

%dnl ------------------------------------------------------------------------------------

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%files devel
%{_docdir}/GLFW
%{_includedir}/GLFW
%{_libdir}/libglfw.so
%{_libdir}/pkgconfig/glfw3.pc
%{_libdir}/cmake/glfw3

%dnl ------------------------------------------------------------------------------------

%prep
# Unpack the main source (Source0) into the build directory
%autosetup -n git-src -T -b 0

%build
%cmake\
    -DGLFW_BUILD_X11=ON \
    -DGLFW_BUILD_WAYLAND=ON
%cmake_build

%install
%cmake_install

%files
%license LICENSE.md
%{_libdir}/libglfw.so.3*

%changelog
* Wed Jul 29 2026 Silvigarabis - 3.4-3.4-112-g364b214c
- Update to latest master version
* Sat Jul 4 2026 Silvigarabis <silvigarabis@outlook.com> - 3.4-107-ged6452b1
- Initial packages


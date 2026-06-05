%global commit f1b86e1ca7982b5b9f47d21ac2cb5c2adfb45902
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name: wallpaper-engine-kde-plugin-qt6
Version: 0.0.1
Release: 1%{?dist}.git%{shortcommit}
Summary: A kde wallpaper plugin integrating wallpaper engine
Group: Development/System 
License: GPLv2
URL: https://github.com/catsout/wallpaper-engine-kde-plugin

# wallpaper-engine-kde-plugin-{commit}
# -> /
Source0: https://github.com/eemmmmg/wallpaper-engine-kde-plugin/archive/%{commit}.tar.gz#/wallpaper-engine-kde-plugin-%{commit}.tar.gz

# glslang-11.8.0
# -> /glslang-11.8.0
# -> /src/backend_scene/third_party/glslang
Source1: https://github.com/KhronosGroup/glslang/archive/refs/tags/11.8.0.tar.gz#/glslang-11.8.0.tar.gz

# wallpaper-scene-renderer-8dde7e7454c1d3906189d7294fd93a3c97bb4ff0
# -> /src/backend_scene
Source2: https://github.com/catsout/wallpaper-scene-renderer/archive/8dde7e7454c1d3906189d7294fd93a3c97bb4ff0.tar.gz#/wallpaper-scene-renderer-8dde7e7454c1d3906189d7294fd93a3c97bb4ff0.tar.gz

# SPIRV-Reflect-vulkan-sdk-1.4.335.0
# -> /src/backend_scene/third_party/SPIRV-Reflect
Source3:  https://github.com/KhronosGroup/SPIRV-Reflect/archive/refs/tags/vulkan-sdk-1.4.335.0.tar.gz#/SPIRV-Reflect-vulkan-sdk-1.4.335.0.tar.gz

# googletest-1.17.0
# -> /src/backend_scene/third_party/SPIRV-Reflect/third_party/googletest
Source4:  https://github.com/google/googletest/archive/refs/tags/v1.17.0.tar.gz#/googletest-1.17.0.tar.gz

# json-3.12.0
# -> /src/backend_scene/third_party/nlohmann
Source5:  https://github.com/nlohmann/json/archive/refs/tags/v3.12.0.tar.gz#/json-3.12.0.tar.gz

# miniaudio-0.11.24
# -> /src/backend_scene/third_party/miniaudio
Source6:  https://github.com/mackron/miniaudio/archive/refs/tags/0.11.24.tar.gz#/miniaudio-0.11.24.tar.gz

# eigen-3.4.1
# -> /src/backend_scene/third_party/Eigen
Source7:  https://gitlab.com/libeigen/eigen/-/archive/3.4.1/eigen-3.4.1.tar.bz2#/eigen-3.4.1.tar.bz2

BuildRequires: mpv-libs-devel
BuildRequires: vulkan-headers
BuildRequires: plasma-workspace-devel
BuildRequires: kf6-plasma-devel
BuildRequires: lz4-devel
BuildRequires: qt6-qtbase-private-devel
BuildRequires: qt5-qtx11extras-devel

Requires: plasma-workspace
Requires: gstreamer1-libav
Requires: mpv-libs
Requires: lz4
Requires: python3-websockets
Requires: qt6-qtwebchannel-devel
Requires: qt6-qtwebsockets-devel

%description

%package -n libglslang
Summary: libglslang
Version: 11.8.0

%description -n libglslang

%prep
%setup -n wallpaper-engine-kde-plugin-%{commit}

mkdir -p glslang-11.8.0
mkdir -p src/backend_scene
mkdir -p src/backend_scene/third_party/SPIRV-Reflect
mkdir -p src/backend_scene/third_party/SPIRV-Reflect/third_party/googletest
mkdir -p src/backend_scene/third_party/nlohmann
mkdir -p src/backend_scene/third_party/miniaudio
mkdir -p src/backend_scene/third_party/Eigen
mkdir -p src/backend_scene/third_party/glslang

tar --strip 1 -C . -xf %{SOURCE0}
tar --strip 1 -C glslang-11.8.0 -xf %{SOURCE1}
tar --strip 1 -C src/backend_scene -xf %{SOURCE2}
tar --strip 1 -C src/backend_scene/third_party/SPIRV-Reflect -xf %{SOURCE3}
tar --strip 1 -C src/backend_scene/third_party/SPIRV-Reflect/third_party/googletest -xf %{SOURCE4}
tar --strip 1 -C src/backend_scene/third_party/nlohmann -xf %{SOURCE5}
tar --strip 1 -C src/backend_scene/third_party/miniaudio -xf %{SOURCE6}
tar --strip 1 -C src/backend_scene/third_party/glslang -xf %{SOURCE1}
tar --strip 1 -C src/backend_scene/third_party/Eigen -xf %{SOURCE7}

%build
%cmake -DUSE_PLASMAPKG=ON
%cmake_build

%install
%cmake_install
mkdir -p %{buildroot}%{_datadir}/plasma/wallpapers
cp -r plugin %{buildroot}%{_datadir}/plasma/wallpapers/com.github.catsout.wallpaperEngineKde
install -m 0755 %{_vpath_builddir}/src/backend_scene/third_party/glslang/SPIRV/libSPIRV.so %{buildroot}%{_libdir}
install -m 0755 %{_vpath_builddir}/src/backend_scene/third_party/glslang/glslang/libglslang.so.11.8.0 %{buildroot}%{_libdir}
ln -s libglslang.so.11.8.0 %{buildroot}%{_libdir}/libglslang.so.11.8
ln -s libglslang.so.11.8 %{buildroot}%{_libdir}/libglslang.so.11

%files
%attr(0755,root,root) %{_libdir}/qt6/qml/com/github/catsout/wallpaperEngineKde/libWallpaperEngineKde.so
%attr(0644,root,root) %{_libdir}/qt6/qml/com/github/catsout/wallpaperEngineKde/qmldir
%{_datadir}/plasma/wallpapers/com.github.catsout.wallpaperEngineKde/*

%files -n libglslang
%{_libdir}/libglslang.so.11.8.0
%{_libdir}/libglslang.so.11.8
%{_libdir}/libglslang.so.11
%{_libdir}/libSPIRV.so

%changelog 
* Mon Jan 19 2026 Silvigarabis <silvigarabis@outlook.com> - 0.0.1
- Initial spec

%global commit 7ffc5b6c930031b9bded124a12651ffb452aa7ce
%global commit_short %(echo %{commit} | cut -c1-7)
%global commit_libevdev_cpp 43ed222120ca33bc2f87a9f5e99dbf5cdef7986f
%global commit_libinput_cpp 012bd22757bfe67239d46bd91da7378bf465d03c

Name:           inputactions
Version:        0.0.1
Release:        1%{?dist}.git%{commit_short}
Summary:        Linux utility for binding keyboard/mouse/touchpad actions

License:        GPL-3.0
URL:            https://github.com/taj-ny/InputActions
Source0:        https://github.com/taj-ny/InputActions/archive/%{commit}.tar.gz#/InputActions-%{version}.tar.gz
Source1:        https://github.com/InputActions/libevdev-cpp/archive/%{commit_libevdev_cpp}.tar.gz#/InputActions-libevdev-cpp-%{version}.tar.gz
Source2:        https://github.com/InputActions/libinput-cpp/archive/%{commit_libinput_cpp}.tar.gz#/InputActions-libinput-cpp-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc-c++
BuildRequires:  qt6-qtbase-devel
BuildRequires:  kwin-devel
BuildRequires:  kf6-ki18n-devel
BuildRequires:  kf6-kguiaddons-devel
BuildRequires:  kf6-kcmutils-devel
BuildRequires:  kf6-kconfigwidgets-devel
BuildRequires:  yaml-cpp-devel
BuildRequires:  libevdev-devel
BuildRequires:  wayland-devel
BuildRequires:  libinput-devel
BuildRequires:  libudev-devel
BuildRequires:  cli11-devel
BuildRequires:  qt6-qtbase
BuildRequires:  libepoxy-devel
BuildRequires:  libdrm-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  systemd

Recommends: %{name}-kwin, %{name}-standalone, %{name}-cli

%description
Linux utility for binding keyboard/mouse/touchpad actions to system actions.

%package ctl
Summary: CLI tool
%description ctl
Requires: inputactions = %{version}-%{release}
Command line interface for InputActions.

%package standalone
Summary: Standalone application
%description standalone
Requires: inputactions = %{version}-%{release}
Standalone GUI application for InputActions.

%package kwin
Summary: KWin plugin and KCM module
Requires: kwin
Requires: kf6-ki18n
Requires: kf6-kguiaddons
Requires: kf6-kcmutils
Requires: inputactions = %{version}-%{release}
%description kwin
KWin effects plugin and configuration module.

%prep
# Unpack the main source (Source0) into the build directory
%autosetup -n InputActions-%{commit}

mkdir -p lib
rm -rf lib/libevdev-cpp lib/libinput-cpp
tar zxvf %{SOURCE1} -C lib/
tar zxvf %{SOURCE2} -C lib/
mv lib/libevdev-cpp-%{commit_libevdev_cpp} lib/libevdev-cpp
mv lib/libinput-cpp-%{commit_libinput_cpp} lib/libinput-cpp

%build
cmake -B build \
    -DINPUTACTIONS_BUILD_CTL=ON \
    -DINPUTACTIONS_BUILD_STANDALONE=ON \
    -DINPUTACTIONS_BUILD_KWIN=ON
cmake --build build -j$(nproc)

%install
mkdir -p %{buildroot}/usr
env DESTDIR=%{buildroot} cmake --install build --prefix /usr

%files
%doc README.md
%license LICENSE

%files ctl
/usr/bin/inputactions

%files standalone
/usr/share/inputactions/gnome/inputactions@inputactions.org/extension.js
/usr/share/inputactions/gnome/inputactions@inputactions.org/metadata.json
/usr/share/inputactions/plasma/script.js
/usr/bin/inputactions-client
/usr/bin/inputactionsd
/usr/lib/systemd/system/inputactionsd.service

%files kwin
/usr/lib64/qt6/plugins/kwin/effects/configs/inputactions_kwin_kcm.so
/usr/lib64/qt6/plugins/kwin/effects/plugins/kwin_gestures.so

%changelog
* Sun Jan 18 2026 Silvigarabis <silvigarabis@outlook.com> - 0.0.1
- Initial multi-subpackage spec

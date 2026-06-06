%global commit 7ffc5b6c930031b9bded124a12651ffb452aa7ce
%global commit_short %(echo %{commit} | cut -c1-7)
%global commit_libevdev_cpp 43ed222120ca33bc2f87a9f5e99dbf5cdef7986f
%global commit_libinput_cpp 012bd22757bfe67239d46bd91da7378bf465d03c

Name:           inputactions
Version:        0.0.4
Release:        1%{?dist}.git%{commit_short}
Summary:        Linux utility for binding keyboard/mouse/touchpad actions

License:        GPL-3.0-or-later
URL:            https://github.com/taj-ny/InputActions
Source0:        https://github.com/taj-ny/InputActions/archive/%{commit}.tar.gz#/InputActions-%{commit}.tar.gz
Source1:        https://github.com/InputActions/libevdev-cpp/archive/%{commit_libevdev_cpp}.tar.gz#/InputActions-libevdev-cpp-%{commit_libevdev_cpp}.tar.gz
Source2:        https://github.com/InputActions/libinput-cpp/archive/%{commit_libinput_cpp}.tar.gz#/InputActions-libinput-cpp-%{commit_libinput_cpp}.tar.gz

BuildRequires:  systemd-rpm-macros
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

%description
Linux utility for binding keyboard/mouse/touchpad actions to system actions.
This package is the Command line interface for InputActions.

%package standalone
Summary: Standalone application
Requires: inputactions = %{version}-%{release}
%description standalone
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

mkdir -p lib/libevdev-cpp lib/libinput-cpp
tar -C lib/libevdev-cpp --strip 1 -zxvf %{SOURCE1}
tar -C lib/libinput-cpp --strip 1 -zxvf %{SOURCE2}

%build
%cmake\
    -DINPUTACTIONS_BUILD_CTL=ON \
    -DINPUTACTIONS_BUILD_STANDALONE=ON \
    -DINPUTACTIONS_BUILD_KWIN=ON
%cmake_build

%install
%cmake_install

%files
%{_bindir}/inputactions
%doc README.md
%license LICENSE

%files standalone
%{_datadir}/inputactions/gnome/inputactions@inputactions.org/extension.js
%{_datadir}/inputactions/gnome/inputactions@inputactions.org/metadata.json
%{_datadir}/inputactions/plasma/script.js
%{_bindir}/inputactions-client
%{_bindir}/inputactionsd
%{_unitdir}/inputactionsd.service

%files kwin
%{_libdir}/qt6/plugins/kwin/effects/configs/inputactions_kwin_kcm.so
%{_libdir}/qt6/plugins/kwin/effects/plugins/kwin_gestures.so

%post standalone
%systemd_post inputactionsd.service

%preun standalone
%systemd_preun inputactionsd.service

%postun standalone
%systemd_postun_with_restart inputactionsd.service

%changelog
* Mon Jan 19 2026 Silvigarabis <silvigarabis@outlook.com> - 0.0.3
- Optimized packaging
* Sun Jan 18 2026 Silvigarabis <silvigarabis@outlook.com> - 0.0.2
- Merge ctl subpackage to mainpackage
* Sun Jan 18 2026 Silvigarabis <silvigarabis@outlook.com> - 0.0.1
- Initial multi-subpackage spec

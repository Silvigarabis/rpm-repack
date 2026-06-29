%global commit 7ffc5b6c930031b9bded124a12651ffb452aa7ce
%global git_tag v0.8.1
%global git_abbr_commit 169-g7ffc5b6

%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global abbr_release %(c=%{git_abbr_commit}; echo ${c//-/.})

Name:           inputactions
Version:        %(c=%{git_tag}; echo "${c#?}")
Release:        2.%{abbr_release}%{?dist}
Summary:        Linux utility for binding keyboard/mouse/touchpad actions

License:        GPL-3.0-only
URL:            https://github.com/taj-ny/InputActions

Source0:        git-src.tar.zst

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
%autosetup -n git-src -T -b 0

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
* Sat Jun 6 2026 Silvigarabis <silvigarabis@outlook.com> - 0.8.1-2.169.g7ffc5b6
- Use git describe tag as version and release string
* Mon Jan 19 2026 Silvigarabis <silvigarabis@outlook.com> - 0.0.3
- Optimized packaging
* Sun Jan 18 2026 Silvigarabis <silvigarabis@outlook.com> - 0.0.2
- Merge ctl subpackage to mainpackage
* Sun Jan 18 2026 Silvigarabis <silvigarabis@outlook.com> - 0.0.1
- Initial multi-subpackage spec


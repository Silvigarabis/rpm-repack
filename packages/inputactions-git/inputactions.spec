%global commit 537a1fca46487251acdff55136d44f51686cbca9
%global git_tag v0.9.0
%global git_abbr_commit 10-g537a1fc

%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global abbr_release %(c=%{git_abbr_commit}; echo ${c//-/.})

Name:           inputactions
Version:        %(c=%{git_tag}; echo "${c#?}")
Release:        3.%{abbr_release}%{?dist}
Summary:        Linux utility for binding keyboard/mouse/touchpad actions

License:        GPL-3.0-only
URL:            https://github.com/taj-ny/InputActions

Source0:        git-src.tar.zst
Source1:        71-touchpad.rules

Suggests:       %{name}-kwin
Suggests:       %{name}-standalone

BuildRequires:  systemd-rpm-macros
BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc-c++
BuildRequires:  qt6-qtbase-devel
BuildRequires:  kwin-devel
BuildRequires:  kf6-rpm-macros
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
Summary: Standalone application varient of %{name}
Requires: %{name} = %{version}-%{release}
%description standalone
Standalone GUI application for InputActions.

%package kwin
Summary: KWin plugin and KCM module varient of %{name}
Requires: kwin
Requires: kf6-ki18n
Requires: kf6-kguiaddons
Requires: kf6-kcmutils
Requires: %{name} = %{version}-%{release}
Recommends: %{name}-udev-rules
%description kwin
KWin effects plugin and configuration module.

%package udev-rules
Summary: Introduce udev rules for evdev usages.
BuildArch:      noarch
Requires:       systemd-udev
Suggests:       %{name}-kwin = %{version}-%{release}

%description udev-rules
Linux utility for binding keyboard/mouse/touchpad actions to system actions.
This package is the udev rules container about evdev usages of touchpad

%prep
# Unpack the main source (Source0) into the build directory
%autosetup -n git-src -T -b 0

cp %{SOURCE1} 71-touchpad.rules

%build
pushd ctl
%cmake
%cmake_build 
popd

pushd standalone
%cmake 
%cmake_build 
popd

pushd kwin
%cmake_kf6
%cmake_build 
popd

%install

pushd ctl
%cmake_install
popd

pushd standalone
%cmake_install
popd

pushd kwin
%cmake_install
popd

install -D -m 0644 71-touchpad.rules %{buildroot}%{_sysconfdir}/udev/rules.d/71-%{name}-touchpad.rules 

%files
%{_bindir}/%{name}
%doc README.md
%license LICENSE

%files standalone
%{_datadir}/%{name}/gnome/%{name}@%{name}.org/extension.js
%{_datadir}/%{name}/gnome/%{name}@%{name}.org/metadata.json
%{_datadir}/%{name}/plasma/script.js
%{_bindir}/%{name}-client
%{_bindir}/%{name}d
%{_unitdir}/%{name}d.service

%files kwin
%{_kf6_archdatadir}/plugins/kwin/effects/configs/%{name}_kwin_kcm.so
%{_kf6_archdatadir}/plugins/kwin/effects/plugins/kwin_gestures.so

%files udev-rules
%{_sysconfdir}/udev/rules.d/71-touchpad.rules 


%post udev-rules
if [ -S /run/udev/control ]; then
    udevadm control --reload
    udevadm trigger
fi

%post standalone
%systemd_post %{name}d.service

%preun standalone
%systemd_preun %{name}d.service

%postun standalone
%systemd_postun_with_restart %{name}d.service

%changelog
* Wed Aug 12 2026 Silvigarabis <silvigarabis@outlook.com> - 0.9.0-3.10-g537a1fc
- Add post script to reload udev rules
* Wed Aug 12 2026 Silvigarabis <silvigarabis@outlook.com> - 0.9.0-2.10-g537a1fc
- Update sources to latest git main branch
* Sat Jun 6 2026 Silvigarabis <silvigarabis@outlook.com> - 0.8.1-2.169.g7ffc5b6
- Use git describe tag as version and release string
* Mon Jan 19 2026 Silvigarabis <silvigarabis@outlook.com> - 0.0.3
- Optimized packaging
* Sun Jan 18 2026 Silvigarabis <silvigarabis@outlook.com> - 0.0.2
- Merge ctl subpackage to mainpackage
* Sun Jan 18 2026 Silvigarabis <silvigarabis@outlook.com> - 0.0.1
- Initial multi-subpackage spec


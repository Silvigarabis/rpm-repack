Name:           inputactions-kwin
Version:        0.8.4
Release:        1%{?dist}
Summary:        InputActions KWin integration for KDE Plasma

License:        GPL-3.0-only
URL:            https://github.com/taj-ny/InputActions
Source0: https://github.com/taj-ny/InputActions/archive/refs/tags/v%{version}.tar.gz#/InputActions-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc-c++

BuildRequires:  qt6-qtbase-devel
BuildRequires:  kwin-devel
BuildRequires:  kf6-ki18n-devel
BuildRequires:  kf6-kguiaddons-devel
BuildRequires:  kf6-kcmutils-devel
BuildRequires:  kf6-kconfigwidgets-devel

BuildRequires:  wayland-devel
BuildRequires:  libepoxy-devel
BuildRequires:  libdrm-devel
BuildRequires:  libevdev-devel
BuildRequires:  yaml-cpp-devel

Requires:       kwin

%description
InputActions is a Linux utility for binding keyboard, mouse, and touchpad
actions to system actions.

This package provides the KWin integration for KDE Plasma on Wayland,
allowing InputActions to interact directly with the KWin compositor.

%prep
%autosetup -n InputActions-%{version}

%build
%cmake -DINPUTACTIONS_BUILD_KWIN=ON
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md

%{_libdir}/qt6/plugins/kwin/effects/plugins/*
%{_libdir}/qt6/plugins/kwin/effects/configs/*

%changelog
* Sun Jan 18 2026 Silvigarabis <silvigarabis@outlook.com> - 0.8.4
- Initial RPM package for InputActions KWin integration

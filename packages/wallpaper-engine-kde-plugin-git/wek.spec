%global commit f1b86e1ca7982b5b9f47d21ac2cb5c2adfb45902
%global git_tag v0.5.4
%global git_abbr_commit 118-gf1b86e1

%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global abbr_release %(c=%{git_abbr_commit}; echo ${c//-/.})

Name:           wallpaper-engine-kde-plugin-qt6
Version:        %(c=%{git_tag}; echo "${c#?}")
Release:        3.%{abbr_release}%{?dist}
Summary:        A kde wallpaper plugin integrating wallpaper engine
Group:          Development/System 
License:        GPLv2
URL:            https://github.com/catsout/wallpaper-engine-kde-plugin

Source0:        git-src.tar.zst
Patch0:         01-force-glslang-static.patch

BuildRequires: mpv-libs-devel
BuildRequires: vulkan-headers
BuildRequires: plasma-workspace-devel
BuildRequires: kf6-plasma-devel
BuildRequires: lz4-devel
BuildRequires: qt6-qtbase-private-devel
BuildRequires: qt5-qtx11extras-devel
BuildRequires: extra-cmake-modules
BuildRequires: kf6-kcoreaddons-devel

Requires: plasma-workspace
Requires: gstreamer1-libav
Requires: mpv-libs
Requires: lz4
Requires: python3-websockets
# Requires by 'plugin/contents/ui/Pyext.qml', intend to use '-devel' package
Requires: qt6-qtwebsockets-devel
Requires: qt6-qtwebchannel-devel

%description

%prep
%setup -T -n git-src -b 0
%patch -P 0

%build
%cmake -DUSE_PLASMAPKG=ON
%cmake_build

%install
%cmake_install
mkdir -p %{buildroot}%{_datadir}/plasma/wallpapers
cp -r plugin %{buildroot}%{_datadir}/plasma/wallpapers/com.github.catsout.wallpaperEngineKde

%files
%attr(0755,root,root) %{_libdir}/qt6/qml/com/github/catsout/wallpaperEngineKde/libWallpaperEngineKde.so
%attr(0644,root,root) %{_libdir}/qt6/qml/com/github/catsout/wallpaperEngineKde/qmldir
%{_datadir}/plasma/wallpapers/com.github.catsout.wallpaperEngineKde/*

%changelog 
* Sat Jun 6 2026 Silvigarabis <silvigarabis@outlook.com> - 0.5.4-3.118.gf1b86e1
- Fix libglslang link
* Sat Jun 6 2026 Silvigarabis <silvigarabis@outlook.com> - 0.5.4-2.118.gf1b86e1
- Use git describe tag as version and release string
* Mon Jan 19 2026 Silvigarabis <silvigarabis@outlook.com> - 0.0.1
- Initial spec

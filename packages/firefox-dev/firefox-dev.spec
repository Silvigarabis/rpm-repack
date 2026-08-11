Name:           firefox-dev
Version:        154.0b9
Release:        0
Summary:        Mozilla Firefox Web browser

License:        LicenseRef-Callaway-MPLv1.1 OR GPL-2.0-or-later OR LicenseRef-Callaway-LGPLv2+
URL:            https://www.firefox.com/zh-CN/channel/desktop/developer/

BuildArch:      x86_64

BuildRequires:  patchelf tar xz

Packager:       Silvigarabis

Source0:        https://ftp.mozilla.org/pub/devedition/releases/154.0b9/linux-x86_64/zh-CN/firefox-154.0b9.tar.xz
Source1:        firefox-launcher.sh
Source2:        firefox-dev.desktop

%description
Mozilla Firefox is an open-source web browser, designed for standards compliance, performance and portability.

%prep
mkdir -p unpack
tar -C unpack -xf %{SOURCE0}
cp %{SOURCE1} firefox-launcher.sh
cp %{SOURCE2} org.mozilla.firefox-dev.desktop 

%build

%install

install -D -m 0755 firefox-launcher.sh %{buildroot}%{_bindir}/firefox-dev

install -d %{buildroot}%{_libdir}
cp -r unpack/firefox %{buildroot}%{_libdir}/firefox-dev
patchelf --remove-rpath %{buildroot}%{_libdir}/firefox-dev/libonnxruntime.so

install -D -m 0644 unpack/firefox/browser/chrome/icons/default/default16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/firefox-dev.png
install -D -m 0644 unpack/firefox/browser/chrome/icons/default/default32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/firefox-dev.png
install -D -m 0644 unpack/firefox/browser/chrome/icons/default/default48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/firefox-dev.png
install -D -m 0644 unpack/firefox/browser/chrome/icons/default/default64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/firefox-dev.png
install -D -m 0644 unpack/firefox/browser/chrome/icons/default/default128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/firefox-dev.png

install -D -m 0644 org.mozilla.firefox-dev.desktop %{buildroot}%{_datadir}/applications/org.mozilla.firefox-dev.desktop

%post

%preun

%postun

%files

%{_bindir}/firefox-dev

%{_libdir}/firefox-dev/*

%{_datadir}/icons/hicolor/16x16/apps/firefox-dev.png
%{_datadir}/icons/hicolor/32x32/apps/firefox-dev.png
%{_datadir}/icons/hicolor/48x48/apps/firefox-dev.png
%{_datadir}/icons/hicolor/64x64/apps/firefox-dev.png
%{_datadir}/icons/hicolor/128x128/apps/firefox-dev.png

%{_datadir}/applications/org.mozilla.firefox-dev.desktop 

# ===== 变更日志 =====
%changelog

* Wed Aug 12 2026 Silvigarabis - 154.0b9-0
- Initial package


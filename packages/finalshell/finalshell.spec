Name:           finalshell
Version:        0
Release:        4.6.4~20260318%{?dist}
Summary:        FinalShell SSH tool

License:        Proprietary
URL:            https://www.hostbuf.com/

# 架构（你原来是 amd64）
BuildArch:      x86_64

# 依赖（从 Depends 转换）
Requires:       glibc, xdg-utils, zlib
BuildRequires:  dpkg

# 可选
Packager:       Silvigarabis

# ===== 宏定义区（方便以后改）=====
%global _appname finalshell
%global _appdir  /usr/lib/%{_appname}
%global _bindir  /usr/bin

# ===== 源（你可以改成 tar 包）=====
Source0:        https://dl.hostbuf.com/finalshell3/finalshell_linux_x64.deb#/finalshell_linux_x64.deb

# ===== 构建阶段（占位）=====
%description
FinalShell

# ===== 准备阶段 =====
%prep
mkdir -p unpack && cd unpack
mkdir -p data control
dpkg-deb -x %{SOURCE0} data
dpkg-deb -e %{SOURCE0} control

mkdir -p data/usr/share/icons/hicolor/scalable/apps data/usr/share/applications


# ===== 构建阶段（目前没用）=====
%build
# 预留：如果以后需要编译可以写这里

# ===== 安装阶段 =====
%install

mkdir -p %{buildroot}/usr/lib/
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
mkdir -p %{buildroot}%{_datadir}/applications/

cp -r unpack/data/usr/lib/finalshell %{buildroot}/usr/lib/

cp unpack/data/usr/lib/finalshell/lib/app/img/finalshell.png %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
cp unpack/data/usr/lib/finalshell/lib/finalshell-FinalShell.desktop %{buildroot}%{_datadir}/applications/

# ===== 安装后脚本（预留）=====
%post
# 例如以后需要 setcap 可以写这里
# /usr/sbin/setcap cap_net_raw,cap_net_admin=eip %{_appdir}/bin/FinalShell || :

# ===== 卸载前 =====
%preun
# 预留

# ===== 卸载后 =====
%postun
# 预留

# ===== 文件列表 =====
%files
/usr/lib/finalshell/**
%{_datadir}/applications/finalshell-FinalShell.desktop
%{_datadir}/icons/hicolor/scalable/apps/finalshell.png

# ===== 变更日志 =====
%changelog
* Wed Mar 18 2026 Silvigarabis - 0
- Initial package

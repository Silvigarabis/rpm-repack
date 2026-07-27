Name:           bitcomet
Version:        2.21.2
Release:        0
Summary:        BitComet is a powerful download client that supports BitTorrent, HTTP, and FTP protocols.

License:        Proprietary
URL:            https://www.bitcomet.com/

# 架构（你原来是 amd64）
BuildArch:      x86_64

# 依赖（从 Depends 转换）
BuildRequires:  dpkg patchelf

# 可选
Packager:       Silvigarabis

# ===== 宏定义区（方便以后改）=====

# ===== 源（你可以改成 tar 包）=====
Source0:        https://download.bitcomet.com/linux/x86_64/BitComet-2.21.2-x86_64.deb#/BitComet-2.21.2-x86_64.deb

# ===== 构建阶段（占位）=====
%description
BitComet is a powerful download client that supports BitTorrent, HTTP, and FTP protocols.
 The graphical user interface (GUI) version of the program is BitComet, and it requires libwebkit2gtk-4.0 as a dependency.
 On the other hand, the console mode program is bitcometd, which can be conveniently operated through a Web user interface.

# ===== 准备阶段 =====
%prep
mkdir -p unpack && cd unpack
mkdir -p data control
dpkg-deb -x %{SOURCE0} data
dpkg-deb -e %{SOURCE0} control

#mkdir -p data/usr/share/icons/hicolor/scalable/apps data/usr/share/applications


# ===== 构建阶段（目前没用）=====
%build
# 预留：如果以后需要编译可以写这里

# ===== 安装阶段 =====
%install

mkdir %{buildroot}%{_prefix}

cp -r unpack/data/usr/bin/ %{buildroot}%{_bindir}
cp -r unpack/data/usr/share/ %{buildroot}%{_datadir}

patchelf --remove-rpath %{buildroot}%{_bindir}/BitComet
patchelf --remove-rpath %{buildroot}%{_bindir}/bitcometd

# ===== 安装后脚本（预留）=====
%post
# 例如以后需要 setcap 可以写这里
# /usr/sbin/setcap cap_net_raw,cap_net_admin=eip %{_appdir}/bin/FinalShell || :


     echo ""
     echo "The installation of BitComet has been completed. Welcome to start using it!"
     echo "To launch the graphical user interface (GUI) version of the program, type \"BitComet\"."
     echo "To launch the console version of the program with Web UI, type \"bitcometd\"."
     echo ""

# ===== 卸载前 =====
%preun
# 预留

# ===== 卸载后 =====
%postun
# 预留

# ===== 文件列表 =====
%files

%{_bindir}/BitComet
%{_bindir}/bitcometd

%{_datadir}/applications/bitcomet.desktop 
%{_datadir}/icons/hicolor/512x512/apps/bitcomet.png
%{_datadir}/bitcomet/*

# ===== 变更日志 =====
%changelog
* Tue Jul 28 2026 Silvigarabis - 2.21.2-0
- Initial package


Name:           bitcometd
Version:        2.21.2
Release:        1
Summary:        BitComet is a powerful download client that supports BitTorrent, HTTP, and FTP protocols.

License:        Proprietary
URL:            https://www.bitcomet.com/

BuildArch:      x86_64

BuildRequires:  dpkg patchelf

Packager:       Silvigarabis

Source0:        https://download.bitcomet.com/linux/x86_64/BitComet-2.21.2-x86_64.deb#/BitComet-2.21.2-x86_64.deb

%description
BitComet is a powerful download client that supports BitTorrent, HTTP, and FTP protocols.
 On the other hand, the console mode program is bitcometd, which can be conveniently operated through a Web user interface.

%package -n BitComet
Summary:        BitComet is a powerful download client that supports BitTorrent, HTTP, and FTP protocols.
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n BitComet
BitComet is a powerful download client that supports BitTorrent, HTTP, and FTP protocols.
 The graphical user interface (GUI) version of the program is BitComet, and it requires libwebkit2gtk-4.0 as a dependency.

%prep
mkdir -p unpack && cd unpack
mkdir -p data control
dpkg-deb -x %{SOURCE0} data
dpkg-deb -e %{SOURCE0} control

%build

%install

mkdir %{buildroot}%{_prefix}

cp -r unpack/data/usr/bin/ %{buildroot}%{_bindir}
cp -r unpack/data/usr/share/ %{buildroot}%{_datadir}

patchelf --remove-rpath %{buildroot}%{_bindir}/BitComet
patchelf --remove-rpath %{buildroot}%{_bindir}/bitcometd

%files
%{_bindir}/bitcometd
%{_datadir}/bitcomet/*

%files -n BitComet
%{_bindir}/BitComet
%{_datadir}/applications/bitcomet.desktop 
%{_datadir}/icons/hicolor/512x512/apps/bitcomet.png

%post -n BitComet
     echo ""
     echo "The installation of BitComet has been completed. Welcome to start using it!"
     echo "To launch the graphical user interface (GUI) version of the program, type \"BitComet\"."
     echo "To launch the console version of the program with Web UI, type \"bitcometd\"."
     echo ""

%changelog
* Wed Aug 12 2026 Silvigarabis - 2.21.2-1
- split packages

* Tue Jul 28 2026 Silvigarabis - 2.21.2-0
- Initial package


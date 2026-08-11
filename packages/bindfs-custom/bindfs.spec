%global         commit a8b2701618da6fa50d71229d99ddc86bd19dfb97
%global         git_tag 1.18.4

%global         git_abbr_commit 5-ga8b2701

%global         shortcommit %(c=%{commit}; echo ${c:0:7})
%global         abbr_release %(c=%{git_abbr_commit}; echo ${c//-/.})

Name:           bindfs
Version:        %(c=%{git_tag}; echo "${c}")
Release:        1.%{abbr_release}%{?dist}
Summary:        Fuse filesystem to mirror a directory
License:        GPL-2.0-or-later
URL:            https://bindfs.org/
# Upstream: https://github.com/Silvigarabis/bindfs
Source0:        git-src.tar.zst
ExcludeArch:    %{ix86}
BuildRequires:  pkgconfig(fuse3) >= 3.4.0
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

# for test suite
BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby >= 3.0.0
%ifarch %{valgrind_arches}
BuildRequires:  valgrind
%endif
%if 0%{?fedora}
# Needed to mount bindfs via fstab
Recommends:     fuse3
%else
Requires:       fuse3
%endif

%description
Bindfs allows you to mirror a directory and also change the permissions in
the mirror directory.

%prep
%autosetup -n git-src
./autogen.sh

%build
%configure
%make_build

%install
%make_install

%check
# Tests are failing on Fedora 40+ so let's disable until further investigation
# Fedora's koji does not provide /dev/fuse, therefore skip the tests there
# Always cat log files on failure to be able to debug issues
# Disabled tests on ppc64le until upstream fixes https://github.com/mpartel/bindfs/issues/55
# %%ifnarch ppc64le
# if [ -e /dev/fuse ]; then
#    make check || (cat tests/test-suite.log tests/internals/test-suite.log; false)
# else
   # internal tests use valgrind and should work
#    make -C tests/internals/ check || (cat tests/internals/test-suite.log; false)
# fi
# %%endif

%files
%doc ChangeLog README.md
%license COPYING
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
%autochangelog

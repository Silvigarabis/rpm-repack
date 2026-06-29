%global commit 2d53565c74d3b1db9e035f55c5d67868147b568f
%global git_tag 0.11
%global git_abbr_commit 50-g2d53565

%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global abbr_release %(c=%{git_abbr_commit}; echo ${c//-/.})

Name:           bees-git
Version:        %{git_tag}
Release:        1.%{abbr_release}%{?dist}
Summary:        Best-Effort Extent-Same btrfs deduplication daemon

License:        GPL-3.0-only
URL:            https://github.com/Zygo/bees
Source0:        git-src.tar.zst

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  discount
BuildRequires:  systemd-rpm-macros
BuildRequires:  libatomic

Requires:       util-linux
Requires:       btrfs-progs

Provides:       bees
Conflicts:      bees

%description
BEES (Best-Effort Extent-Same) is a background deduplication daemon
for btrfs filesystems.

%prep
%setup -n git-src -T -b 0

%build
export CXXFLAGS="$CXXFLAGS -Wno-error=restrict -Wno-error=maybe-uninitialized"
export CFLAGS="$CFLAGS -Wno-error=restrict -Wno-error=maybe-uninitialized"

%make_build all scripts BEES_VERSION=%{git_tag}-%{git_abbr_commit} SYSTEMD_SYSTEM_UNIT_DIR=%{_unitdir} LIBEXEC_PREFIX=%{_libexecdir} BINDIR=bin

%install

%make_install BEES_VERSION=%{git_tag}-%{git_abbr_commit} SYSTEMD_SYSTEM_UNIT_DIR=%{_unitdir} LIBEXEC_PREFIX=%{_libexecdir} BINDIR=bin

%files
%{_sysconfdir}/bees/beesd.conf.sample
%{_bindir}/beesd
%{_libexecdir}/bees
%{_unitdir}/beesd@.service

%license COPYING
%doc README.md

%changelog
* Sat Jun 06 2026 Silvigarabis <Silvigarabis@outlook.com> - 0.11-1.50.g2d53565
- Update package version string format
* Sat Jun 06 2026 Silvigarabis <Silvigarabis@outlook.com> - 0.11-0.50.g2d53565.git2d53565
- Initial package

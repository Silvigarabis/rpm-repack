%global commit 2d53565c74d3b1db9e035f55c5d67868147b568f
%global git_tag 0.11
%global git_abbr_commit 50-g2d53565

%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global abbr_release %(c=%{git_abbr_commit}; echo ${c//-/.})

Name:           bees-git
Version:        %{git_tag}
Release:        0.%{abbr_release}.git%{shortcommit}%{?dist}
Summary:        Best-Effort Extent-Same btrfs deduplication daemon

License:        GPL-3.0-only
URL:            https://github.com/Zygo/bees
Source0:        https://github.com/Zygo/bees/archive/%{commit}.tar.gz#/%{name}-%{git_tag}-%{git_abbr_commit}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  discount
BuildRequires:  systemd-rpm-macros

Requires:       util-linux
Requires:       bash
Requires:       btrfs-progs

Provides:       bees
Conflicts:      bees

%description
BEES (Best-Effort Extent-Same) is a background deduplication daemon
for btrfs filesystems.

%prep
%setup -n bees-%{commit} -T -a 0

%build
%make_build all scripts BEES_VERSION=%{version}

%install
%make_install BEES_VERSION=%{version}

%files
%{_etcdir}/bees/beesd.conf.sample
%{_libexecdir}/bees/bees
%{_bindir}/beesd
%{_unitdir}/beesd@.service

%license COPYING
%doc README.md

%changelog
* Sat Jun 06 2026 Silvigarabis <Silvigarabis@outlook.com> - 0.11-0.50.g2d53565.git2d53565
- Initial package


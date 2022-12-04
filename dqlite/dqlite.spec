Name:           dqlite
Version:        1.12.0
Release:        0.1%{?dist}
Summary:        Embeddable, replicated and fault tolerant SQL engine

License:        LGPLv3 with exception
URL:            https://github.com/canonical/dqlite
Source0:        %{URL}/archive/v%{version}.tar.gz

BuildRequires:  autoconf libtool
BuildRequires:  gcc
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libuv)
BuildRequires:  pkgconfig(raft) >= 0.16.0
BuildRequires:  pkgconfig(sqlite3)

%description
dqlite is a C library that implements an embeddable and replicated SQL database
engine with high-availability and automatic failover.

%package devel
Summary:        Development libraries for dqlite
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers and library for dqlite.

%prep
%setup -q -n %{name}-%{version}

%build
autoreconf -i
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libdqlite.la

%check
%make_build check

%ldconfig_scriptlets

%files
%doc AUTHORS README.md
%license LICENSE
%{_libdir}/libdqlite.so.*

%files devel
%{_libdir}/libdqlite.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}.h

%changelog
* Sun Dec 04 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.12.0-0.1
- Update to 1.12.0.

* Sat Oct 01 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.11.1-0.2
- Fix build dependencies
- Add patch to fix test issue

* Wed Jul 13 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.11.1-0.1
- Update to 1.11.1.

* Sat Jul 09 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.11.0-0.1
- dqlite: Update to 1.11.0.

* Mon Apr 18 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.10.0-0.1
- Update to 1.10.0.

* Mon Feb 14 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.9.1-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Jan 30 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.9.1-0.1
- Update to 1.9.1.

* Mon Aug 23 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.9.0-0.1
- Update to 1.9.0.

* Mon Jun 28 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.8.0-0.1
- Update to 1.8.0.

* Thu May 13 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.7.0-0.1
- Update to 1.7.0

* Wed Apr 28 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.6.0-0.2.20210317gitc0699eb
- Update to git snapshot c0699eb

* Sun Mar 14 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.6.0-0.2.20201229gita89301a
- Skip failing test on Fedora 32

* Sat Mar 13 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.6.0-0.1.20201229gita89301a
- Update to git snapshot a89301a

* Wed Nov 25 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.6.0-0.1.20200926git867d7b2
- Initial package.

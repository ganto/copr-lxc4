Name:           dqlite
Version:        1.8.0
Release:        0.1%{?dist}
Summary:        Embeddable, replicated and fault tolerant SQL engine

License:        LGPLv3
URL:            https://github.com/canonical/dqlite
Source0:        https://github.com/canonical/%{name}/archive/v%{version}.tar.gz

BuildRequires:  autoconf libtool
BuildRequires:  gcc
BuildRequires:  libuv-devel
BuildRequires:  raft-devel
BuildRequires:  sqlite-devel

%description
dqlite is a C library that implements an embeddable and replicated SQL database
engine with high-availability and automatic failover.

%package devel
Summary:        Development libraries for dqlite
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers and library for dqlite.

%package static
Summary:        Static library for dqlite
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description static
Static library (.a) version of dqlite.


%prep
%setup -q -n %{name}-%{version}

%build
autoreconf -i
%configure
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

%files static
%{_libdir}/libdqlite.a

%changelog
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


Name:           cowsql
Version:        1.15.8
Release:        0.1%{?dist}
Summary:        Embeddable, replicated and fault tolerant SQL engine

License:        LGPL-3.0-only WITH LGPL-3.0-linking-exception
URL:            https://github.com/cowsql/cowsql
Source0:        %{URL}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  autoconf libtool
BuildRequires:  gcc
BuildRequires:  pkgconfig(libuv)
BuildRequires:  pkgconfig(raft) >= 0.18.2
BuildRequires:  pkgconfig(sqlite3)

%description
cowsql is a C library that implements an embeddable and replicated SQL database
engine with high-availability and automatic failover.

%package devel
Summary:        Development libraries for cowsql
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers and library for cowsql.

%prep
%autosetup -n %{name}-%{version}

%build
autoreconf -i
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libcowsql.la

%check
%make_build check

%ldconfig_scriptlets

%files
%doc AUTHORS README.md
%license LICENSE
%{_libdir}/libcowsql.so.*

%files devel
%{_libdir}/libcowsql.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}.h

%changelog
* Mon Feb 03 2025 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.15.8-0.1
- Update to 1.15.8

* Sat Apr 06 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.15.6-0.1
- Update to 1.15.6

* Fri Dec 22 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.15.4-0.1
- Update to 1.15.4.

* Mon Oct 30 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.15.3-0.1
- Update to 1.15.3

* Sun Oct 15 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0-20230921.a1d49d0.0.1
- Initial package


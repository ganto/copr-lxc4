%global forgeurl https://github.com/cowsql/cowsql
Version:        1.15.9
%forgemeta

Name:           cowsql
Release:        0.1%{?dist}
Summary:        Embeddable, replicated and fault tolerant SQL engine
License:        LGPL-3.0-only WITH LGPL-3.0-linking-exception
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  gcc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(libuv)
BuildRequires:  pkgconfig(raft) >= 0.18.2

%description
cowsql is a C library that implements an embeddable and replicated SQL database
engine with high availability and automatic failover.

cowsql extends SQLite with a network protocol that can connect together various
instances of your application and have them act as a highly-available cluster,
with no dependency on external databases.

The name "cowsql" loosely refers to the "pets vs. cattle" concept, since it's
generally fine to delete or rebuild a particular node of an application that
uses cowsql for data storage.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains development files for %{name}.

%prep
%forgeautosetup -p1

%build
autoreconf -i
%configure --disable-static
%make_build

%install
%make_install

%check
make check


%files
%license LICENSE
%doc AUTHORS README.md
%{_libdir}/libcowsql.so.0*

%files devel
%{_libdir}/libcowsql.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}.h

%changelog
* Fri Aug 01 2025 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.15.9-0.1
- Update to 1.15.9

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


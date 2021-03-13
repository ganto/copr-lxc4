%global commit a89301a62e902df22e45649722a31bf1fbd6857a
%global commitdate 20201229
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           dqlite
Version:        1.6.0
Release:        0.1.%{commitdate}git%{shortcommit}%{?dist}
Summary:        Embeddable, replicated and fault tolerant SQL engine

License:        LGPLv3
URL:            https://github.com/canonical/dqlite
Source0:        https://github.com/canonical/%{name}/archive/%{commit}.tar.gz

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
%autosetup -n %{name}-%{commit} -p1

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
* Wed Nov 25 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.6.0-0.1.20200926git867d7b2
- Initial package.


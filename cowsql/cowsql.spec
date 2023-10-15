%global commitdate      20230921
%global commit          a1d49d0d3e40b32ba655fffe14b7669c2aa1bcec
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           cowsql
Version:        0
Release:        %{commitdate}.%{shortcommit}.0.1%{?dist}
Summary:        Embeddable, replicated and fault tolerant SQL engine

License:        LGPL-3.0-only WITH LGPL-3.0-linking-exception
URL:            https://github.com/cowsql/cowsql
Source0:        %{URL}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz

BuildRequires:  autoconf libtool
BuildRequires:  gcc
BuildRequires:  pkgconfig(libuv)
BuildRequires:  pkgconfig(raft) >= 0.17.1
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
%autosetup -n %{name}-%{commit}

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

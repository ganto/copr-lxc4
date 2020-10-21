%global commit 976124272a741c11dfe9662d164d5e67c161eec7
%global commitdate 20201015
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           raft 
Version:        0.9.25
Release:        0.1.%{commitdate}git%{shortcommit}%{?dist}
Summary:        C implementation of the Raft consensus protocol

License:        LGPLv3 
URL:            https://github.com/canonical/raft
Source0:        https://github.com/canonical/%{name}/archive/%{commit}.tar.gz

BuildRequires:  autoconf libtool
BuildRequires:  gcc
BuildRequires:  libuv-devel

%description
Fully asynchronous C implementation of the Raft consensus protocol. It consists
of a core part that implements the core Raft algorithm logic and a pluggable
interface defining the I/O implementation for networking and disk persistence. 

%package devel
Summary:        Development libraries for raft
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers and library for raft.

%package static
Summary:        Static library for raft
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description static
Static library (.a) version of raft.


%prep
%autosetup -n %{name}-%{commit} -p1

%build
autoreconf -i 
%configure
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libraft.la

%check
%make_build check

%ldconfig_scriptlets

%files
%doc AUTHORS README.md
%license LICENSE
%{_libdir}/libraft.so.*

%files devel
%{_libdir}/libraft.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/raft.h
%{_includedir}/raft/

%files static
%{_libdir}/libraft.a

%changelog
* Tue Oct 20 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.9.25-0.1.20201015git9761242
- Initial package

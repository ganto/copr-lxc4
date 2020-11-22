%global commit c1539a7854ad11febd88a6c610d4237c58b36068
%global commitdate 20201027
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           raft 
Version:        0.9.25
Release:        0.2.%{commitdate}git%{shortcommit}%{?dist}
Summary:        C implementation of the Raft consensus protocol

License:        LGPLv3 
URL:            https://github.com/canonical/raft
Source0:        https://github.com/canonical/%{name}/archive/%{commit}.tar.gz
# Fix test when run on tmpfs for Fedora <33
Patch0:         raft-0.9.25-Always-skip-init-oom-test.patch

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
%setup -q -n %{name}-%{commit}
%if 0%{?fedora} && 0%{?fedora} < 33
%patch0 -p1
%endif

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
* Thu Oct 22 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.9.25-0.2.20201015git9761242
- Add patch to fix test for x86_64/aarch64

* Tue Oct 20 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.9.25-0.1.20201015git9761242
- Initial package


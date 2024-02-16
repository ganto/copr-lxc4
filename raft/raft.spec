Name:           raft
Version:        0.22.0
Release:        0.1%{?dist}
Summary:        C implementation of the Raft consensus protocol

License:        LGPL-3.0-only WITH LGPL-3.0-linking-exception
URL:            https://raft.readthedocs.io/
Source0:        %{URL}/archive/v%{version}.tar.gz

BuildRequires:  autoconf libtool
BuildRequires:  gcc
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libuv)
# Breaking header change
Conflicts:      dqlite < 1.16.0-0.2
Conflicts:      cowsql < 1.15.4

%description
Fully asynchronous C implementation of the Raft consensus protocol. It consists
of a core part that implements the core Raft algorithm logic and a pluggable
interface defining the I/O implementation for networking and disk persistence.

%package benchmark
Summary:        Benchmark operating system disk write performance
BuildRequires:  pkgconfig(liburing)

%description benchmark
Benchmark operating system disk write performance.

%package devel
Summary:        Development libraries for raft
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers and library for raft.

%package doc
Summary:        C-Raft documentation
BuildArch:      noarch
BuildRequires:  python-sphinx

%description doc
This package contains the C-Raft documentation in HTML format.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
autoreconf -i
%configure --disable-static --enable-benchmark
%make_build
sphinx-build -b html -d docs/_build/doctrees docs docs/_build/html
rm -vf docs/_build/html/.buildinfo

%install
%make_install
rm -f %{buildroot}%{_libdir}/libraft.la

%check
# parallel testing is broken: https://github.com/ganto/copr-lxc4/issues/35
%global _smp_mflags -j1
%make_build check

%ldconfig_scriptlets

%files
%doc AUTHORS README.md
%license LICENSE
%{_libdir}/libraft.so.*

%files benchmark
%license LICENSE
%{_bindir}/raft-benchmark

%files devel
%{_libdir}/libraft.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/raft.h
%{_includedir}/raft/

%files doc
%license LICENSE
%doc docs/_build/html/

%changelog
* Fri Dec 22 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.18.3-0.2
- Correctly indicate broken upgrade paths

* Thu Dec 21 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.18.3-0.1
- Switch upstream to https://github.com/cowsql/raft
- Update to 0.18.3

* Fri Jan 20 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.17.1-0.2
- Define conflict with old dqlite

* Fri Jan 20 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.17.1-0.1
- Update to 0.17.1.

* Sun Dec 04 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.16.0-0.2
- Switch to SPDX license expression

* Mon Nov 21 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.16.0-0.1
- Update to 0.16.0.

* Sat Aug 27 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.15.0-0.1
- Update to 0.15.0.

* Wed Jun 29 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.14.0-0.1
- Update to 0.14.0.

* Mon Apr 18 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.13.0-0.1
- Update to 0.13.0.

* Sun Feb 13 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.11.3-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Feb 13 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.11.3-0.4
- Fix tests on armv7hl architecture.

* Sat Feb 05 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.11.3-0.3
- Replace tmpfs patch with upstream fix

* Sat Feb 05 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.11.3-0.2
- Re-add patch to fix build failures on COPR

* Sat Jan 22 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.11.3-0.1
- Update to 0.11.3.

* Wed Oct 27 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.11.2-0.2
- Add -doc and -benchmark subpackages
- Remove -static subpackage
- Various spec file cleanups related to packaging guidelines

* Mon Aug 23 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.11.2-0.1
- Update to 0.11.2.

* Sun Jun 20 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.11.1-0.1
- Update to 0.11.1.

* Tue May 11 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.10.1-0.1
- Update to 0.10.1

* Thu Apr 22 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.10.0-0.1.20210409gite318fd8
- Update to git snapshot e318fd8

* Sat Apr 03 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.10.0-0.1
- Update to 0.10.0

* Sat Mar 13 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.9.25-0.2.20210203git329e3d8
- Update to git snapshot 329e3d8

* Mon Jan 18 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.9.25-0.2.20201206gitf205aaf
- Update to git snapshot f205aaf5

* Sun Nov 22 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.9.25-0.2.20201027gitc1539a7
- Update to git snapshot c1539a7.

* Thu Oct 22 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.9.25-0.2.20201015git9761242
- Add patch to fix test for x86_64/aarch64

* Tue Oct 20 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.9.25-0.1.20201015git9761242
- Initial package


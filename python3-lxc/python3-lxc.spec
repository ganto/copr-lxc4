%global srcname python3-lxc

Name:           %{srcname}
Version:        3.0.4
Release:        0.3%{?dist}
Summary:        Python 3 bindings for LXC

License:        LGPLv2+
URL:            https://linuxcontainers.org/lxc
Source0:        https://linuxcontainers.org/downloads/lxc/%{srcname}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  lxc-devel >= 3
BuildRequires:  pkgconfig(python3) >= 3.2

%description
%{summary}

%prep
%autosetup -n %{srcname}-%{version}

# fix python shebang in examples
sed -i 's|/usr/bin/env python3|/usr/bin/python3|g' examples/*
chmod -x examples/*

%build
%py3_build

%install
%py3_install

%check

%files
%license COPYING
%doc README.md
%doc examples/
%{python3_sitearch}/*


%changelog
* Sun Sep 13 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.4-0.3
- Cleanup EPEL 7 compatibility from spec file

* Sat Sep 28 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.4-0.2
- Rebuild for EPEL-8

* Thu Aug 15 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.4-0.1
- Update to 3.0.4
- Build Python 3.4 and 3.6 packages for CentOS
- Install examples

* Wed Nov 28 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.3-0.1
- Update to 3.0.3

* Sat Sep 22 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.2-0.2
- Fix build no C compiler is in the base build environment

* Sat Sep 15 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.2-0.1
- Update to 3.0.2

* Wed Jun 20 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.1-0.2
- Fix dependency and upgrade issues on CentOS 7

* Sat Mar 31 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.1-0.1
- Initial package


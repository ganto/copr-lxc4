Name:           lxc-templates-extra
Version:        3.0.4
Release:        0.2%{?dist}
Summary:        Old style template scripts for LXC

License:        LGPLv2+
URL:            https://linuxcontainers.org
Source0:        https://linuxcontainers.org/downloads/lxc/lxc-templates-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  autoconf
BuildRequires:  automake
# not actually used, but build will fail due to autoconf check:
# "configure: error: no acceptable C compiler found in $PATH"
BuildRequires:  gcc

Requires:       lxc-templates >= 3.0.3-0.2
# Package was renamed after lxc-templates-3.0.3-0.1 to not conflict with the
# Fedora package layout used by lxc-templates-3.0.3-1
Obsoletes:      lxc-templates = 3.0.3-0.1
Conflicts:      lxc-templates = 3.0.3-0.1
# Note: Requirements for the template scripts (busybox, dpkg,                       
# debootstrap, rsync, openssh-server, dhclient, apt, pacman, zypper,
# ubuntu-cloudimg-query etc...) are not explicitly mentioned here:
# their presence varies wildly on supported Fedora/EPEL releases and
# archs, and they are in most cases needed for a single template
# only. Also, the templates normally fail graciously when such a tool
# is missing. Moving each template to its own subpackage on the other
# hand would be overkill.

%global debug_package   %{nil}

%description
%{summary}.
The modern approach to build container images is distrobuilder.

%prep
%autosetup -n lxc-templates-%{version}
./autogen.sh
%configure

%build
%{make_build} %{?_smp_mflags}

%install
%{make_install} %{?_smp_mflags}

%files
%defattr(-,root,root)
%doc CONTRIBUTING MAINTAINERS
%license COPYING
%{_datadir}/lxc/config/* 
%{_datadir}/lxc/templates/lxc-*      

%changelog
* Sat Sep 28 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.4-0.2
- Rebuild for EPEL-8

* Wed Aug 14 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.4-0.1
- Update to 3.0.4

* Sat Feb 09 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.3-0.2
- Rename package to lxc-templates-extra

* Wed Nov 28 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.3-0.1
- Update to 3.0.3

* Sat Sep 22 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.2-0.2
- Fix build when no C compiler is in the base bulid environment

* Sat Sep 22 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.2-0.1
- Update to 3.0.2

* Tue Jun 26 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.1-0.1
- Update to 3.0.1

* Wed Jun 06 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.0-0.2
- Fix lxc-libs dependency

* Sun Apr 01 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.0-0.1
- Update to 3.0.0

* Mon Mar 26 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.0.beta1-0.1
- Initial package


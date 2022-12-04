%bcond_without  check

# enable debug for non-go code
%global with_debug 1

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

# https://github.com/lxc/lxd
%global goipath github.com/lxc/lxd
Version:        5.7

%gometa

%global godocs      AUTHORS
%global golicenses  COPYING

Name:           lxd
Release:        0.1%{?dist}
Summary:        Container hypervisor based on LXC

# Upstream license specification: Apache-2.0
License:        ASL 2.0
URL:            https://linuxcontainers.org/lxd
Source0:        https://linuxcontainers.org/downloads/%{name}/%{name}-%{version}.tar.gz
Source1:        %{name}.socket
Source2:        %{name}.service
Source3:        lxd-containers.service
Source4:        lxd.dnsmasq
Source5:        lxd.logrotate
Source6:        shutdown
Source7:        lxd.sysctl
Source8:        lxd.profile
Source9:        lxd-agent.service
Source10:       lxd-agent-setup
# Upstream bug fixes merged to master for next release
# https://github.com/lxc/lxd/issues/11042
Patch0:         lxd-5.7-Device-Speed-up-getting-NIC-host-name-info.patch
# https://github.com/lxc/lxd/issues/11072
Patch1:         lxd-5.7-Network-Adds-MTU-DHCP-option-when-using-bridge-fan-mode.patch
# https://github.com/lxc/lxd/issues/11073
Patch2:         lxd-5.7-lxd-device-tpm-Handle-TPM-device-in-profiles.patch
# https://github.com/lxc/lxd/issues/11083
Patch3:         lxd-5.7-lxd-Remove-shadowed-variable-name.patch
# https://github.com/lxc/lxd/issues/11084
Patch4:         lxd-5.7-Storage-Dont-check-project-limits-when-doing-a-volume-snapshot-restore.patch
# https://github.com/lxc/lxd/issues/11126
Patch5:         lxd-5.8-Device-Fix-attaching-cephfs-disk-volumes-to-VMs.patch

BuildRequires:  gettext
BuildRequires:  help2man
BuildRequires:  pkgconfig(dqlite)
BuildRequires:  pkgconfig(libacl)
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(libseccomp)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(lxc)
BuildRequires:  pkgconfig(raft)
BuildRequires:  pkgconfig(sqlite3)

Requires: acl
Requires: attr
Requires: dnsmasq
Requires: (nftables or (ebtables and iptables))
Requires: lxd-client = %{version}-%{release}
Requires: lxcfs
Requires: rsync
Requires: shadow-utils >= 4.1.5
Requires: squashfs-tools
Requires: tar
Requires: xdelta
Requires: xz
%{?systemd_requires}
Requires(pre): container-selinux >= 2:2.38
Requires(pre): shadow-utils

%if %{with check}
BuildRequires:  btrfs-progs
BuildRequires:  dnsmasq
BuildRequires:  ebtables
BuildRequires:  iptables
%endif

Obsoletes: lxd-libs < %{version}-%{release}

Suggests: logrotate

# Virtual machine support requires additional packages
Suggests: edk2-ovmf
Suggests: genisoimage
%if 0%{?fedora} && 0%{?fedora} >= 34
Suggests: qemu-char-spice
Suggests: qemu-device-display-virtio-vga
Suggests: qemu-device-display-virtio-gpu
%endif
Suggests: qemu-device-usb-redirect
Suggests: qemu-img
Suggests: qemu-system-x86-core

%description
Container hypervisor based on LXC
LXD offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains the LXD daemon.

%godevelpkg

%package client
Summary:        Container hypervisor based on LXC - Client

Requires:       gettext

%description client
LXD offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains the command line client.

%package tools
Summary:        Container hypervisor based on LXC - Extra Tools

%description tools
LXD offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains extra tools provided with LXD.
 - fuidshift - A tool to map/unmap filesystem uids/gids
 - lxc-to-lxd - A tool to migrate LXC containers to LXD
 - lxd-benchmark - A LXD benchmark utility

%package migrate
Summary:        A physical to container migration tool
#Requires:       netcat
Requires:       rsync
Obsoletes:      %{name}-p2c < %{version}
Conflicts:      %{name}-p2c < %{version}

%description migrate
Physical to container migration tool

This tool lets you turn any Linux filesystem (including your current one)
into a LXD container on a remote LXD host.

It will setup a clean mount tree made of the root filesystem and any
additional mount you list, then transfer this through LXD's migration
API to create a new container from it.

%package agent
Summary:        LXD guest agent

%description agent
This packages provides an agent to run inside LXD virtual machine guests.

It has to be installed on the LXD host if you want to allow agent
injection capability when creating a virtual machine.

%package doc
Summary:        Container hypervisor based on LXC - Documentation
BuildArch:      noarch

%description doc
LXD offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains user documentation.

%prep
%goprep -k
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
export CGO_LDFLAGS_ALLOW="(-Wl,-wrap,pthread_create)|(-Wl,-z,now)"
for cmd in lxd lxc fuidshift lxd-benchmark lxc-to-lxd; do
    BUILDTAGS="libsqlite3" %gobuild -o %{gobuilddir}/bin/$cmd %{goipath}/$cmd
done

export CGO_ENABLED=0
BUILDTAGS="netgo" %gobuild -o %{gobuilddir}/bin/lxd-migrate %{goipath}/lxd-migrate
BUILDTAGS="agent netgo" %gobuild -o %{gobuilddir}/bin/lxd-agent %{goipath}/lxd-agent
unset CGO_ENABLED

# build translations
rm -f po/ber.po po/zh_Hans.po po/zh_Hant.po    # remove invalid locales
make %{?_smp_mflags} build-mo

# generate man-pages
%{gobuilddir}/bin/lxd manpage .
%{gobuilddir}/bin/lxc manpage .
help2man %{gobuilddir}/bin/fuidshift -n "uid/gid shifter" --no-info --no-discard-stderr > fuidshift.1
help2man %{gobuilddir}/bin/lxd-benchmark -n "The container lightervisor - benchmark" --no-info --no-discard-stderr > lxd-benchmark.1
help2man %{gobuilddir}/bin/lxd-migrate -n "Physical to container migration tool" --no-info --no-discard-stderr > lxd-migrate.1
help2man %{gobuilddir}/bin/lxc-to-lxd -n "Convert LXC containers to LXD" --no-info --no-discard-stderr > lxc-to-lxd.1
help2man %{gobuilddir}/bin/lxd-agent -n "LXD virtual machine guest agent" --no-info --no-discard-stderr > lxd-agent.1

%install
%gopkginstall

# install binaries
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

# extra configs
install -Dpm 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/dnsmasq.d/lxd
install -Dpm 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/lxd
install -Dpm 0644 %{SOURCE7} %{buildroot}%{_sysconfdir}/sysctl.d/10-lxd-inotify.conf
install -Dpm 0644 %{SOURCE8} %{buildroot}%{_sysconfdir}/profile.d/lxd.sh

# install bash completion
install -Dpm 0644 scripts/bash/lxd-client %{buildroot}%{_datadir}/bash-completion/completions/lxd-client

# install systemd units
install -d -m 0755 %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/
install -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/
install -p -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/
install -p -m 0644 %{SOURCE9} %{buildroot}%{_unitdir}/
install -d -m 0755 %{buildroot}/lib/systemd
install -p -m 0755 %{SOURCE10} %{buildroot}/lib/systemd/

# install shutdown wrapper
install -d -m 0755 %{buildroot}%{_libexecdir}/%{name}
install -p -m 0755 %{SOURCE6} %{buildroot}%{_libexecdir}/%{name}

# install manpages
install -d %{buildroot}%{_mandir}/man1
cp -p lxd.1 %{buildroot}%{_mandir}/man1/
cp -p lxc*.1 %{buildroot}%{_mandir}/man1/
cp -p fuidshift.1 %{buildroot}%{_mandir}/man1/
cp -p lxd-benchmark.1 %{buildroot}%{_mandir}/man1/
cp -p lxd-migrate.1 %{buildroot}%{_mandir}/man1/
cp -p lxc-to-lxd.1 %{buildroot}%{_mandir}/man1/
cp -p lxd-agent.1 %{buildroot}%{_mandir}/man1/

# cache and log directories
install -d -m 0711 %{buildroot}%{_localstatedir}/lib/%{name}
install -d -m 0755 %{buildroot}%{_localstatedir}/log/%{name}

# language files
install -dm 0755 %{buildroot}%{_datadir}/locale
for mofile in po/*.mo ; do
install -Dpm 0644 ${mofile} %{buildroot}%{_datadir}/locale/$(basename ${mofile%%.mo})/LC_MESSAGES/%{name}.mo
done
%find_lang lxd

%if %{with check}
%check
export GOPATH=%{buildroot}/%{gopath}:%{gopath}

# Add libsqlite3 tag to go test
%define gotestflags -buildmode pie -compiler gc -v -tags libsqlite3

# Tests must ignore potential LXD_SOCKET from environment
unset LXD_SOCKET

export CGO_LDFLAGS_ALLOW="(-Wl,-wrap,pthread_create)|(-Wl,-z,now)"

%gocheck -v \
    -d %{goipath}/lxc-to-lxd  # lxc-to-lxd test fails, see ganto/copr-lxc3#10

%endif

%pre
# check for existence of lxd group, create it if not found
getent group %{name} > /dev/null || groupadd -r %{name}

%post
%systemd_post %{name}.socket
%systemd_post %{name}.service
%systemd_post %{name}-containers.service

%post agent
%systemd_post %{name}-agent.service

%preun
%systemd_preun %{name}.socket
%systemd_preun %{name}.service
%systemd_preun %{name}-containers.service

%preun agent
%systemd_preun %{name}-agent.service

%files
%license %{golicenses}
%config(noreplace) %{_sysconfdir}/dnsmasq.d/lxd
%config(noreplace) %{_sysconfdir}/logrotate.d/lxd
%config(noreplace) %{_sysconfdir}/sysctl.d/10-lxd-inotify.conf
%config(noreplace) %{_sysconfdir}/profile.d/lxd.sh
%{_bindir}/%{name}
%{_unitdir}/%{name}.socket
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-containers.service
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/*
%{_mandir}/man1/%{name}.1.*
%dir %{_localstatedir}/log/%{name}
%defattr(-, root, root, 0711)
%dir %{_localstatedir}/lib/%{name}

%gopkgfiles

%files client -f lxd.lang
%license %{golicenses}
%{_bindir}/lxc
%{_datadir}/bash-completion/completions/lxd-client
%{_mandir}/man1/lxc.*1.*

%files tools
%license %{golicenses}
%{_bindir}/fuidshift
%{_bindir}/lxd-benchmark
%{_bindir}/lxc-to-lxd
%{_mandir}/man1/fuidshift.1.*
%{_mandir}/man1/lxd-benchmark.1.*
%{_mandir}/man1/lxc-to-lxd.1.*

%files migrate
%license %{golicenses}
%{_bindir}/lxd-migrate
%{_mandir}/man1/lxd-migrate.1.*

%files agent
%license %{golicenses}
%{_bindir}/lxd-agent
%{_unitdir}/%{name}-agent.service
/lib/systemd/%{name}-agent-setup
%{_mandir}/man1/lxd-agent.1.*

%files doc
%license %{golicenses}
%doc doc/*

%changelog
* Sun Dec 04 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.7-0.1
- Update to 5.7

* Sat Oct 22 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.6-0.1
- Update to 5.6.

* Sun Oct 02 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.5-0.1
- Update to 5.5.

* Thu Aug 11 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.4-0.1
- Update to 5.4.

* Wed Aug 10 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.3-0.2
- Fix lxc-5.0 compatibility

* Fri Jul 01 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.3-0.1
- Update to 5.3.

* Mon Apr 18 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.24-0.2
- Rebuild because of raft so-library version update

* Thu Apr 14 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.24-0.1
- Update to 4.24.

* Sun Mar 27 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.23-0.1
- Update to 4.23.
- Replace lxd-p2c with lxd-migrate following upstream change.

* Sun Mar 13 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.22-0.1
- Update to 4.22.
- Add missing dependency to setfattr

* Sat Jan 15 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.21-0.1
- Update to 4.21

* Tue Dec 07 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.20-0.1
- Update to 4.20.

* Tue Nov 02 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.19-0.1
- Update to 4.19.

* Sun Jun 20 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.15-0.1
- Update to 4.15.
- Cleanup Fedora 32 compatibility.

* Sat May 15 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.14-0.2
- Fix user lookup test for Fedora >= 34

* Fri May 14 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.14-0.1
- Update to 4.14.

* Sat May 01 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.13-0.2
- Apply bugfix patch for nftables firewall
- Apply patch to fix spice compatibility on Fedora 34 (link@sub-pop.net)
- Update package suggestions for Fedora 33/34 (link@sub-pop.net)

* Thu Apr 29 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.13-0.1
- Update to 4.13.

* Mon Apr 05 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.12-0.1
- Update to 4.12.
- Cleanup build steps
- Update lxd-agent systemd service

* Sun Mar 14 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.11-0.1
- Update to 4.11.
- Remove bundled raft and dqlite

* Sun Feb 07 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.10-0.1
- Update to 4.10.

* Mon Jan 18 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.9-0.1
- Update to 4.9.

* Thu Dec 17 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.8-0.1
- Update to 4.8.

* Sun Nov 22 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.7-0.1
- Update to 4.7.

* Sat Oct 03 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.6-0.1
- Update to 4.6.

* Sat Sep 12 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.5-0.2
- Add RPM_LD_FLAGS to libdqlite linker flags
- Update to latest go-/dqlite to avoid linker issues with libco on
  Fedora >=33

* Tue Sep 08 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.5-0.1
- Update to 4.5.

* Sun Aug 02 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.3-0.1
- Update to 4.3.

* Sun May 10 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.22-0.1
- Update to 3.22

* Thu Feb 20 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.21-0.1
- Update to 3.21

* Fri Feb 07 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.20-0.1
- Update to 3.20

* Sun Feb 02 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.19-0.1
- Update to 3.19
- Add new sub-package lxd-agent
- Depend on >kernel-headers-3.10 (e.g. ELRepo) when building for CentOS 7

* Sat Feb 01 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.18-0.2
- Fix typo when calling systemd macros for lxd-containers service
- Remove redundant chrpath to fix build on aarch64 (gsfjohnson@gmail.com)

* Fri Oct 25 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.18-0.1
- Update to 3.18

* Mon Oct 21 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.17-0.2
- Rebuild for EPEL-8

* Wed Oct 16 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.17-0.1
- Update to 3.17

* Wed Aug 14 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.16-0.1
- Update to 3.16

* Fri Jul 26 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.15-0.1
- Update to 3.15

* Mon Jul 01 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.14-0.1
- Update to 3.14

* Wed May 15 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.13-0.1
- Update to 3.13

* Sat Apr 20 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.12-0.1
- Update to 3.12

* Sat Mar 09 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.11-0.1
- Update to 3.11

* Sun Feb 17 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.10-0.1
- Update to 3.10

* Sun Feb 03 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.9-0.1
- Update to 3.9

* Thu Dec 27 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.8-0.1
- Update to 3.8
- Fix build macros for CentOS and simplify build env variables
- Set --libdir and rpath to avoid LD_LIBRARY_PATH wrapper
- Add upstream patch to fix test failure in github.com/lxc/lxd/lxd
- Generate and package gettext translations

* Sun Sep 30 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.5-0.1
- Update to 3.5
- Fix rpath of embedded libdqlite.so
- Finally fix Provides/Requires of embedded libraries

* Mon Sep 17 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.4-0.1
- Update to 3.4
- Run test with 'libsqlite3' tag
- Install headers of embedded libraries
- Don't auto-provide embedded libraries (e.g. sqlite)

* Fri Aug 10 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.3-0.1
- Update to 3.3

* Wed Jun 27 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.2-0.1
- Update to 3.2

* Thu May 31 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.1-0.3
- Fix build regression with EPEL 7

* Thu May 31 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.1-0.2
- Fix build error on Fedora 26

* Thu May 31 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.1-0.1
- Update to 3.1
- Added LXD_SOCKET override to lxd-containers service (mrd@redhat.com)
- Added support for LXD_SOCKET to lxc-to-lxd

* Thu May 10 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.0-0.5
- Fix build with golang-1.8.x (e.g. CentOS <=7.4)
- Experimental patch to fix container startup via LXD_SOCKET

* Fri Apr 27 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.0-0.4
- Make sure LXD_SOCKET is not set when running %%check

* Tue Apr 24 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.0-0.3
- Add upstream patches according to lxd-3.0.0-0ubuntu4
- Add new sub-package lxd-p2c
- Fix lxd.socket path in systemd .service and .socket

* Sun Apr 15 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.0-0.2
- Add bundled modules to devel
- Use new LXD_SOCKET option and set it to /run/lxd.socket
- Add upstream patches according to lxd-3.0.0-0ubuntu3

* Mon Apr 02 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3.0.0-0.1
- Update to 3.0.0
- Build with bundled go dependencies by default

* Wed Jan 31 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.21-2
- Fix build with bundled go modules
- Correctly specify scriptlet dependencies
- Run systemd preun scriptlet
- Use /usr/libexec instead of /usr/lib for helper script (GH #11)

* Thu Jan 25 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.21-1
- Update to 2.21 (with patches from 2.21-0ubuntu2)

* Tue Jan 23 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.20-1
- Update to 2.20 (with patches from 2.20-0ubuntu4)
- Major rework of the spec file
- Enable tests

* Fri Nov 03 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.19-2
- Work-around syntax issue on Fedora 27.
- Runtime detect liblxc version.

* Mon Oct 30 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.19-1
- Update to 2.19.
- Update embedded go-lxc to commit 74fb852
- Drop hard dependency to lxc-2.1
- Various RPM metadata fixes

* Wed Oct 04 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.18-3
- Link against libsqlite3
- Update go-sqlite3 dependency to fix startup issue on Fedora 26
- Add upstream patches according to lxd-2.18-0ubuntu3

* Thu Sep 28 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.18-2
- Add upstream patches according to lxd-2.18-0ubuntu2
- Fix xdelta dependency, tighten liblxc version dependency

* Thu Sep 21 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.18-1
- Version bump to lxd-2.18
- Update embedded go-lxc to commit 89b06ca

* Mon Aug 28 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.17-3
- Add upstream patches according to lxd-2.17-0ubuntu2

* Thu Aug 24 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.17-2
- Fix man pages wrongly added to multiple packages

* Thu Aug 24 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.17-1
- Version bump to lxd-2.17

* Wed Jul 26 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.16-1
- Version bump to lxd-2.16

* Wed Jul 19 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.15-3
- Tweak timeouts for systemd units
- Add upstream patches according to lxd-2.15-0ubuntu6

* Mon Jul 03 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.15-2
- Rebuild with latest golang-github-gorilla-websocket

* Mon Jul 03 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.15-1
- Version bump to lxd-2.15
- Add upstream patches according to lxd-2.15-0ubuntu4

* Sat Jun 10 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.14-2
- Add some upstream patches according to lxd-2.14-0ubuntu3

* Wed Jun 07 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.14-1
- Version bump to lxd-2.14
- Update embedded go-lxc to commit de2c8bf
- "infinity" for NOFILE doesn't work, set fixed value

* Mon May 01 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.13-1
- Version bump to lxd-2.13
- Add lxc-benchmark to lxd-tools package

* Fri Mar 24 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.12-1
- Version bump to lxd-2.12
- Update embedded go-lxc to commit 8304875

* Thu Mar 09 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.11-1
- Version bump to lxd-2.11
- Add 'lvm-use-ff-with-vgremove.patch' from lxd-2.11-0ubuntu2

* Tue Mar 07 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.10.1-1
- Version bump to lxd-2.10.1

* Thu Mar 02 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.10-1
- Version bump to lxd-2.10, bump websocket dependency due to build errors

* Fri Feb 24 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.9.3-1
- Version bump to lxd-2.9.3

* Tue Feb 21 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.9.2-1
- Version bump to lxd-2.9.2

* Mon Feb 20 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.9.1-1
- Version bump to lxd-2.9.1
- Update embedded go-lxc to commit aeb7ce4

* Thu Jan 26 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.8-1
- Version bump to lxd-2.8, fix some gopath requires/provides

* Tue Dec 27 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.7-1
- Version bump to lxd-2.7, set LXD_DIR to mode 0711
- Add lxc-to-lxd migration script to lxd-tools package

* Wed Dec 14 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.6.2-5
- Don't restrict world access to /var/{lib,log}/lxd

* Sun Dec 11 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.6.2-4
- Fix cache directory permissions, add more suggested packages

* Sat Dec 10 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.6.2-3
- Fix /var/lib/lxd, add shutdown script, new lxd-doc RPM

* Sat Dec 10 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.6.2-2
- Big spec file cleanup, fix devel RPM

* Sun Dec 4 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.6.2-1
- Initial packaging

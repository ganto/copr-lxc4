%bcond_without  check

# https://github.com/canonical/lxd
%global goipath github.com/canonical/lxd
Version:        5.20

%gometa

%global godocs AUTHORS CODE_OF_CONDUCT.md CONTRIBUTING.md README.md SECURITY.md
%global golicenses COPYING

Name:           lxd
Release:        0.2%{?dist}
Summary:        Container hypervisor based on LXC
License:        AGPL-3.0-or-later and Apache-2.0
URL:            https://ubuntu.com/lxd
Source0:        https://github.com/canonical/lxd/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz

# Systemd units
Source101:      %{name}.socket
Source102:      %{name}.service
Source103:      %{name}-containers.service

# Ensure lxd group exists
Source104:      %{name}-sysusers.conf

# Ensure state directories (/var/lib/lxd, /var/cache/lxd, /var/log/lxd) exists
Source105:      %{name}-tmpfiles.conf

# Ensure system dnsmasq ignores lxd network bridge
Source106:      %{name}-dnsmasq.conf

# Raise number of inotify user instances
Source107:      %{name}-sysctl.conf

# Helper script for lxd shutdown
Source108:      shutdown

# SELinux file labels
Source109:      %{name}.fc

# Web scripts shipped with API documentation
# Latest downloads from https://github.com/swagger-api/swagger-ui/tree/master/dist
Source201:      swagger-ui-bundle.js
Source202:      swagger-ui-standalone-preset.js
Source203:      swagger-ui.css

# Upstream bug fixes merged to master for next release

# https://github.com/canonical/lxd/issues/12730
Patch0:         lxd-5.20-lxd-instance-qemu-Start-using-seabios-as-CSM-firmware.patch
# https://github.com/canonical/lxd/issues/12808
Patch1:         lxd-5.20-VM-Dont-leak-file-descriptor-when-probing-for-Direct-IO-support.patch

# Allow offline builds
Patch2:         lxd-5.19-doc-Remove-downloads-from-sphinx-build.patch
Patch3:         lxd-5.20-doc-Enhance-related-links-definitions-for-offline-build.patch

%global bashcompletiondir %(pkg-config --variable=completionsdir bash-completion 2>/dev/null || :)
%global selinuxtype targeted

BuildRequires:  gettext
BuildRequires:  help2man
BuildRequires:  pkgconfig(bash-completion)
BuildRequires:  pkgconfig(dqlite)
BuildRequires:  pkgconfig(libacl)
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(libseccomp)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(lxc)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  systemd-rpm-macros
%{?sysusers_requires_compat}

Requires:       %{name}-client = %{version}-%{release}
Requires:       (%{name}-selinux = %{version}-%{release} if selinux-policy-%{selinuxtype})
Requires:       attr
Requires:       dnsmasq
Requires:       iptables, ebtables
Requires:       (nftables if iptables-nft)
Requires:       lxcfs
Requires:       rsync
Requires:       shadow-utils >= 4.1.5
Requires:       squashfs-tools
Requires:       tar
Requires:       xdelta
Requires:       xz
%{?systemd_requires}

%if %{with check}
BuildRequires:  btrfs-progs
BuildRequires:  dnsmasq
BuildRequires:  nftables
%endif

Recommends:     lxd-agent = %{version}-%{release}
Recommends:     lxd-ui
Suggests:       lxd-doc

%description
Container hypervisor based on LXC
LXD offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains the LXD daemon.

%godevelpkg

%package selinux
Summary:        Container hypervisor based on LXC - SELinux policy
BuildArch:      noarch

Requires:       container-selinux
Requires(post): container-selinux
BuildRequires:  selinux-policy-devel
%{?selinux_requires}

%description selinux
Incus offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains the SELinux policy.

%package client
Summary:        Container hypervisor based on LXC - Client
License:        Apache-2.0

Requires:       gettext

%description client
LXD offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains the command line client.

%package tools
Summary:        Container hypervisor based on LXC - Extra Tools
License:        Apache-2.0

Requires:       lxd%{?_isa} = %{version}-%{release}
# fuidshift is also shipped with incus
Conflicts:      incus-tools

%description tools
LXD offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains extra tools provided with LXD.
 - fuidshift - A tool to map/unmap filesystem uids/gids
 - lxc-to-lxd - A tool to migrate LXC containers to LXD
 - lxd-benchmark - A LXD benchmark utility

%package migrate
Summary:        A physical to container migration tool
License:        Apache-2.0

Requires:       rsync

%description migrate
Physical to container migration tool

This tool lets you turn any Linux filesystem (including your current one)
into a LXD container on a remote LXD host.

It will setup a clean mount tree made of the root filesystem and any
additional mount you list, then transfer this through LXD's migration
API to create a new container from it.

%package agent
Summary:        LXD guest agent
License:        Apache-2.0

Requires:       lxd%{?_isa} = %{version}-%{release}
# Virtual machine support requires additional packages
Recommends:     edk2-ovmf
Recommends:     genisoimage
Recommends:     qemu-char-spice
Recommends:     qemu-device-display-virtio-vga
Recommends:     qemu-device-display-virtio-gpu
Recommends:     qemu-device-usb-redirect
Recommends:     qemu-img
Recommends:     qemu-kvm-core

%description agent
This packages provides an agent to run inside LXD virtual machine guests.

It has to be installed on the LXD host if you want to allow agent
injection capability when creating a virtual machine.

%package doc
Summary:        Container hypervisor based on LXC - Documentation
# This project is Apache-2.0. Other files bundled with the documentation have the
# following licenses:
# - _static/basic.css: BSD-2-Clause
# - _static/clipboard.min.js: MIT
# - _static/copy*: MIT
# - _static/doctools.js: BSD-2-Clause
# - _static/*/furo*: MIT
# - _static/jquery*.js: MIT
# - _static/language_data.js: BSD-2-Clause
# - _static/pygments.css: BSD-2-Clause
# - _static/searchtools.js: BSD-2-Clause
# - _static/swagger-ui/*: Apache-2.0
# - _static/underscore*.js: MIT
License:        Apache-2.0 AND BSD-2-Clause AND MIT
BuildArch:      noarch

BuildRequires:  python3-furo
BuildRequires:  python3-linkify-it-py
BuildRequires:  python3-lxd-sphinx-extensions
BuildRequires:  python3-myst-parser
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx-copybutton
BuildRequires:  python3-sphinx-design
BuildRequires:  python3-sphinx-notfound-page
BuildRequires:  python3-sphinx-remove-toctrees
BuildRequires:  python3-sphinx-reredirects
BuildRequires:  python3-sphinx-tabs
BuildRequires:  python3-sphinxcontrib-applehelp
BuildRequires:  python3-sphinxcontrib-devhelp
BuildRequires:  python3-sphinxcontrib-htmlhelp
BuildRequires:  python3-sphinxcontrib-jquery
BuildRequires:  python3-sphinxcontrib-jsmath
BuildRequires:  python3-sphinxcontrib-qthelp
BuildRequires:  python3-sphinxcontrib-serializinghtml
BuildRequires:  python3-sphinxext-opengraph

%description doc
LXD offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains user documentation.

%prep
%goprep -k
%autopatch -v -p1

%build
export CGO_LDFLAGS_ALLOW="(-Wl,-wrap,pthread_create)|(-Wl,-z,now)"
for cmd in lxd lxc fuidshift lxd-benchmark lxc-to-lxd; do
    BUILDTAGS="libsqlite3" %gobuild -o %{gobuilddir}/bin/$cmd %{goipath}/$cmd
done

# upstream %gobuildflags contain '-linkmode=external' which conflicts with CGO_ENABLED=0
%global gobuildflags -tags="${BUILDTAGS:-}" -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x

export CGO_ENABLED=0
BUILDTAGS="netgo" %gobuild -o %{gobuilddir}/bin/lxd-migrate %{goipath}/lxd-migrate
BUILDTAGS="agent netgo" %gobuild -o %{gobuilddir}/bin/lxd-agent %{goipath}/lxd-agent
unset CGO_ENABLED

# build documentation
mkdir -p doc/.sphinx/_static/swagger-ui
cp %{SOURCE201} %{SOURCE202} %{SOURCE203} doc/.sphinx/_static/swagger-ui
sed -i 's|lxc.bin|_build/bin/lxc|' doc/myconf.py doc/custom_conf.py
sphinx-build -c doc/ -b dirhtml doc/ doc/html/
rm -vrf doc/html/{.buildinfo,.doctrees}
# remove duplicate files
rm -vrf doc/html/{_sources,_sphinx_design_static}

# build translations
rm -f po/ber.po po/zh_Hans.po po/zh_Hant.po    # remove invalid locales
make %{?_smp_mflags} build-mo

# generate man-pages
mkdir %{gobuilddir}/man
%{gobuilddir}/bin/lxd manpage %{gobuilddir}/man/
%{gobuilddir}/bin/lxc manpage %{gobuilddir}/man/
help2man %{gobuilddir}/bin/fuidshift -n "uid/gid shifter" --no-info --no-discard-stderr > %{gobuilddir}/man/fuidshift.1
help2man %{gobuilddir}/bin/lxd-benchmark -n "The container lightervisor - benchmark" --no-info --no-discard-stderr > %{gobuilddir}/man/lxd-benchmark.1
help2man %{gobuilddir}/bin/lxd-migrate -n "Physical to container migration tool" --no-info --no-discard-stderr > %{gobuilddir}/man/lxd-migrate.1
help2man %{gobuilddir}/bin/lxc-to-lxd -n "Convert LXC containers to LXD" --no-info --no-discard-stderr > %{gobuilddir}/man/lxc-to-lxd.1
help2man %{gobuilddir}/bin/lxd-agent -n "LXD virtual machine guest agent" --no-info --no-discard-stderr > %{gobuilddir}/man/lxd-agent.1

# SELinux policy
mkdir selinux
cp -p %{SOURCE109} selinux/
pushd selinux
# generate the type enforcement file as it has no other content
echo 'policy_module(%{name},1.0)' >%{name}.te
%{__make} NAME=%{selinuxtype} -f %{_datadir}/selinux/devel/Makefile %{name}.pp
bzip2 -9 %{name}.pp
popd

%install
%gopkginstall

# install binaries
install -d %{buildroot}%{_bindir}
install -m0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

# install systemd units
install -d %{buildroot}%{_unitdir}
install -m0644 -vp %{SOURCE101} %{buildroot}%{_unitdir}/
install -m0644 -vp %{SOURCE102} %{buildroot}%{_unitdir}/
install -m0644 -vp %{SOURCE103} %{buildroot}%{_unitdir}/
install -D -m0644 -vp %{SOURCE104} %{buildroot}%{_sysusersdir}/%{name}.conf
install -D -m0644 -vp %{SOURCE105} %{buildroot}%{_tmpfilesdir}/%{name}.conf

# extra configs
install -D -m0644 -vp %{SOURCE106} %{buildroot}%{_sysconfdir}/dnsmasq.d/%{name}.conf
install -D -m0644 -vp %{SOURCE107} %{buildroot}%{_sysconfdir}/sysctl.d/10-lxd-inotify.conf

# selinux policy
install -D -m0644 -vp selinux/%{name}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.bz2

# install shutdown wrapper
install -D -m0755 -vp %{SOURCE108} %{buildroot}%{_libexecdir}/%{name}/shutdown

# install manpages
install -d %{buildroot}%{_mandir}/man1
cp -p %{gobuilddir}/man/*.1 %{buildroot}%{_mandir}/man1/

# install bash completion
install -D -m0644 -vp scripts/bash/lxd-client %{buildroot}%{bashcompletiondir}/lxd-client

# cache and log directories
install -d -m0700 %{buildroot}%{_localstatedir}/cache/%{name}
install -d -m0700 %{buildroot}%{_localstatedir}/log/%{name}
install -d -m0711 %{buildroot}%{_localstatedir}/lib/%{name}

# language files
for mofile in po/*.mo ; do
    install -D -m0644 -vp ${mofile} %{buildroot}%{_datadir}/locale/$(basename ${mofile%%.mo})/LC_MESSAGES/%{name}.mo
done
%find_lang lxd

%if %{with check}
%check
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
export CGO_LDFLAGS_ALLOW="(-Wl,-wrap,pthread_create)|(-Wl,-z,now)"

# Add libsqlite3 tag to go test
%define gotestflags -buildmode pie -compiler gc -v -tags libsqlite3

# https://github.com/ganto/copr-lxc4/issues/46
rm -f shared/util_linux_test.go

%gocheck -v -t %{goipath}/test \
    -d %{goipath}/lxc-to-lxd  # lxc-to-lxd test fails, see ganto/copr-lxc3#10
%endif

%pre
%sysusers_create_package %{name} %{SOURCE104}
%tmpfiles_create_package %{name} %{SOURCE105}

%pre selinux
%selinux_relabel_pre -s %{selinuxtype}

%post
%sysctl_apply 10-lxd-inotify.conf
%systemd_post %{name}.socket
%systemd_post %{name}.service
%systemd_post %{name}-containers.service

%post selinux
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.bz2
%selinux_relabel_post -s %{selinuxtype}

%preun
%systemd_preun %{name}.socket
%systemd_preun %{name}.service
%systemd_preun %{name}-containers.service

%postun
%systemd_postun_with_restart %{name}.socket
%systemd_postun_with_restart %{name}.service

%postun selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{name}
    %selinux_relabel_post -s %{selinuxtype}
fi

%posttrans selinux
%selinux_relabel_post -s %{selinuxtype}

%files
%license %{golicenses}
%config(noreplace) %{_sysconfdir}/dnsmasq.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysctl.d/10-lxd-inotify.conf
%{_bindir}/%{name}
%{_unitdir}/%{name}.socket
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-containers.service
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/*
%{_sysusersdir}/%{name}.conf
%{_tmpfilesdir}/%{name}.conf
%{_mandir}/man1/%{name}.*1.*
%exclude %{_mandir}/man1/lxd-agent.1.*
%exclude %{_mandir}/man1/lxd-benchmark.1.*
%exclude %{_mandir}/man1/lxd-migrate.1.*
%attr(700,root,root) %dir %{_localstatedir}/cache/%{name}
%attr(700,root,root) %dir %{_localstatedir}/log/%{name}
%attr(711,root,root) %dir %{_localstatedir}/lib/%{name}
%gopkgfiles

%files selinux
%{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.*
%ghost %verify(not md5 size mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{name}

%files client -f lxd.lang
%license %{golicenses}
%{_bindir}/lxc
%dir %{bashcompletiondir}
%{bashcompletiondir}/lxd-client
%{_mandir}/man1/lxc.*1.*
%exclude %{_mandir}/man1/lxc-to-lxd.1.*

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
%{_mandir}/man1/lxd-agent.1.*

%files doc
%license %{golicenses}
%doc doc/html

%changelog
* Sat Apr 27 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.20-0.1
- Update to 5.20.
- Add lxd-selinux sub package
- Update swagger-ui to v5.17.2

* Fri Dec 29 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.19-0.1
- Update to 5.19
- Update swagger-ui to v5.10.5
- Use systemd sysusers/tmpfiles
- Update dependencies to use 'Recommends'
- Remove unneeded lxd-agent script and systemd unit

* Sun Nov 19 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.18-0.2
- Add VM dependencies and UI as suggests

* Fri Nov 03 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.18-0.1
- Update to 5.18.
- Update swagger-ui to v5.9.1

* Wed Oct 04 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.17-0.1
- Update to 5.17.
- Update swagger-ui to v5.9.0

* Sun Aug 27 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.16-0.1
- Update to 5.16.
- Update swagger-ui to v5.4.2
* Mon Aug 07 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.15-0.1
- Update to 5.15.
- Build documentation with sphinx instead of only distributing the markdown files

* Tue Jul 04 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.14-0.1
- Update to 5.14.

* Thu Jun 01 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.13-0.1
- Update to 5.13.

* Sat Apr 22 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.12-0.1
- Update to lxd-5.12.

* Wed Mar 15 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.11-0.1
- Update to lxd-5.11.

* Sat Feb 11 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.10-0.2
- Update to 5.10.

* Mon Jan 23 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.9-0.2
- Rebuild because of raft so-library version update

* Sat Jan 14 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.9-0.1
- Update to 5.9.

* Fri Dec 23 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.8-0.1
- Update to 5.8.

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

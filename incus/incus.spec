# Disable documentation due to missing dependencies
%bcond doc 1

# Swagger version to download for documentation
%global swaggerui_version 5.31.0
%global swaggerui_source_baseurl https://github.com/swagger-api/swagger-ui/raw/v%{swaggerui_version}/dist/

# Enable tests
%bcond check 1

# https://github.com/lxc/incus
%global goipath github.com/lxc/incus
Version:        6.19.1

%gometa

%global godocs AUTHORS CODE_OF_CONDUCT.md CONTRIBUTING.md README.md SECURITY.md
%global golicenses COPYING


# Set build macro for static builds
%define gocompilerflags_static -compiler gc
%define gobuild_baseflags_static %{gocompilerflags_static} -tags="rpm_crashtraceback ${GO_BUILDTAGS-${BUILDTAGS-}}" -a -v
%define gobuild_ldflags_static ${GO_LDFLAGS-${LDFLAGS-}} %{?currentgoldflags} -B 0x$(echo "%{name}-%{version}-%{release}-${SOURCE_DATE_EPOCH:-}" | sha1sum | cut -d ' ' -f1) -compressdwarf=false
%define gobuildflags_static() %{expand:%{gobuild_baseflags_static} -ldflags "%{gobuild_ldflags_static}"}
%define gobuild_static(-) %{expand:
  %{?gobuilddir:GOPATH="%{gobuilddir}:${GOPATH:+${GOPATH}:}%{?gopath}"} %{?gomodulesmode} \\
  CGO_ENABLED=0 go build %{gobuildflags_static} %{?**};
}


Name:           incus
Release:        0.2%{?dist}
Summary:        Powerful system container and virtual machine manager
License:        Apache-2.0
URL:            https://linuxcontainers.org/incus
Source0:        https://linuxcontainers.org/downloads/%{name}/%{name}-%{version}.tar.xz

# Systemd units
Source101:      %{name}.socket
Source102:      %{name}.service
Source103:      %{name}-startup.service
Source104:      %{name}-user.socket
Source105:      %{name}-user.service

# Ensure Incus groups exist
Source106:      %{name}-sysusers.conf

# Ensure state directories (/var/lib/incus, /var/cache/incus, /var/log/incus) exist
Source107:      %{name}-tmpfiles.conf

# Ensure system dnsmasq ignores Incus network bridge
Source108:      %{name}-dnsmasq.conf

# Raise number of inotify user instances
Source109:      %{name}-sysctl.conf

# Helper script for incusd shutdown
Source110:      shutdown

# SELinux file labels
Source111:      %{name}.fc

# Web scripts shipped with API documentation
Source201:      %{swaggerui_source_baseurl}/swagger-ui-bundle.js#/swagger-ui-%{swaggerui_version}-bundle.js
Source202:      %{swaggerui_source_baseurl}/swagger-ui-standalone-preset.js#/swagger-ui-%{swaggerui_version}-standalone-preset.js
Source203:      %{swaggerui_source_baseurl}/swagger-ui.css#/swagger-ui-%{swaggerui_version}.css

# Patches upstream or proposed upstream

# Downstream only patches
## Allow offline builds
Patch1002:      incus-0.2-doc-Remove-downloads-from-sphinx-build.patch

%global bashcompletiondir %(pkg-config --variable=completionsdir bash-completion 2>/dev/null || :)
%global selinuxtype targeted

BuildRequires:  gettext
BuildRequires:  glibc-static
BuildRequires:  help2man
BuildRequires:  pkgconfig(bash-completion)
BuildRequires:  pkgconfig(cowsql)
BuildRequires:  pkgconfig(libacl)
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(libseccomp)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(lxc)
BuildRequires:  pkgconfig(raft)
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
Requires:       shadow-utils
Requires:       squashfs-tools
Requires:       tar
Requires:       xdelta
Requires:       xz
%{?systemd_requires}

%ifnarch %{ix86} %{arm32}
Requires:       skopeo
# Not yet packaged in Fedora
#Requires:       umoci
%endif

%if %{with check}
BuildRequires:  btrfs-progs
BuildRequires:  dnsmasq
BuildRequires:  nftables
%endif

Recommends:     %{name}-agent = %{version}-%{release}
Suggests:       %{name}-doc

%description
Container hypervisor based on LXC
Incus offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains the Incus daemon.

%pre
%sysusers_create_package %{name} %{SOURCE106}
%tmpfiles_create_package %{name} %{SOURCE107}

%post
%sysctl_apply 10-incus-inotify.conf
%systemd_post %{name}.socket
%systemd_post %{name}.service
%systemd_post %{name}-startup.service
%systemd_post %{name}-user.socket
%systemd_post %{name}-user.service

%preun
%systemd_preun %{name}.socket
%systemd_preun %{name}.service
%systemd_preun %{name}-startup.service
%systemd_preun %{name}-user.socket
%systemd_preun %{name}-user.service

%postun
%systemd_postun_with_restart %{name}.socket
%systemd_postun_with_restart %{name}.service
%systemd_postun_with_restart %{name}-user.socket
%systemd_postun_with_restart %{name}-user.service

%files
%license %{golicenses}
%config(noreplace) %{_sysconfdir}/dnsmasq.d/%{name}.conf
%{_sysctldir}/10-incus-inotify.conf
%{_unitdir}/%{name}.socket
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-startup.service
%{_unitdir}/%{name}-user.socket
%{_unitdir}/%{name}-user.service
%{_libexecdir}/%{name}/
%{_sysusersdir}/%{name}.conf
%{_tmpfilesdir}/%{name}.conf
%{_mandir}/man1/incusd*.1.*
%attr(700,root,root) %dir %{_localstatedir}/cache/%{name}
%attr(700,root,root) %dir %{_localstatedir}/log/%{name}
%attr(711,root,root) %dir %{_localstatedir}/lib/%{name}

%dnl ----------------------------------------------------------------------------

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

%pre selinux
%selinux_relabel_pre -s %{selinuxtype}

%post selinux
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.bz2
%selinux_relabel_post -s %{selinuxtype}

%postun selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{name}
    %selinux_relabel_post -s %{selinuxtype}
fi

%posttrans selinux
%selinux_relabel_post -s %{selinuxtype}

%files selinux
%{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.*
%ghost %verify(not md5 size mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{name}

%dnl ----------------------------------------------------------------------------

%package client
Summary:        Container hypervisor based on LXC - Client
License:        Apache-2.0

Requires:       gettext

%description client
Incus offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains the command line client.

%files client -f incus.lang
%license %{golicenses}
%{_bindir}/%{name}
%dir %{bashcompletiondir}
%{bashcompletiondir}/%{name}
%dir %{fish_completions_dir}
%{fish_completions_dir}/%{name}.fish
%dir %{zsh_completions_dir}
%{zsh_completions_dir}/_%{name}
%{_mandir}/man1/%{name}*.1.*
%exclude %{_mandir}/man1/incusd*.1.*
%exclude %{_mandir}/man1/incus-agent.1.*
%exclude %{_mandir}/man1/incus-benchmark.1.*
%exclude %{_mandir}/man1/incus-migrate.1.*
%exclude %{_mandir}/man1/lxc-to-incus.1.*
%exclude %{_mandir}/man1/lxd-to-incus.1.*

%dnl ----------------------------------------------------------------------------

%package tools
Summary:        Container hypervisor based on LXC - Extra Tools
License:        Apache-2.0

Requires:       incus%{?_isa} = %{version}-%{release}
# fuidshift is also shipped with lxd
Conflicts:      lxd-tools

%description tools
Incus offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains extra tools provided with Incus.
 - fuidshift - A tool to map/unmap filesystem uids/gids
 - lxc-to-incus - A tool to migrate LXC containers to Incus
 - lxd-to-incus - A tool to migrate an existing LXD environment to Incus
 - incus-benchmark - A Incus benchmark utility
 - incus-migrate - A physical to container migration tool

%files tools
%license %{golicenses}
%{_bindir}/fuidshift
%{_bindir}/incus-benchmark
%{_bindir}/incus-migrate
%{_bindir}/lxc-to-incus
%{_bindir}/lxd-to-incus
%{_mandir}/man1/fuidshift.1.*
%{_mandir}/man1/incus-benchmark.1.*
%{_mandir}/man1/incus-migrate.1.*
%{_mandir}/man1/lxc-to-incus.1.*
%{_mandir}/man1/lxd-to-incus.1.*

%dnl ----------------------------------------------------------------------------

%package agent
Summary:        Incus guest agent
License:        Apache-2.0

Requires:       incus%{?_isa} = %{version}-%{release}
# Virtual machine support requires additional packages
Recommends:     edk2-ovmf
Recommends:     xorriso
Recommends:     qemu-char-spice
Recommends:     qemu-device-display-virtio-vga
Recommends:     qemu-device-display-virtio-gpu
Recommends:     qemu-device-usb-redirect
Recommends:     qemu-img
Recommends:     qemu-kvm-core

%description agent
This packages provides an agent to run inside Incus virtual machine guests.

It has to be installed on the Incus host if you want to allow agent
injection capability when creating a virtual machine.

%files agent
%license %{golicenses}
%{_bindir}/incus-agent
%{_mandir}/man1/incus-agent.1.*

%dnl ----------------------------------------------------------------------------

%if %{with doc}
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

BuildRequires:  python3-canonical-sphinx-extensions
BuildRequires:  python3-furo
BuildRequires:  python3-linkify-it-py
BuildRequires:  python3-myst-parser
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx-copybutton
BuildRequires:  python3-sphinx-design
BuildRequires:  python3-sphinx-notfound-page
BuildRequires:  python3-sphinx-remove-toctrees
BuildRequires:  python3-sphinx-reredirects
BuildRequires:  python3-sphinx-tabs
BuildRequires:  python3-sphinxcontrib-jquery
BuildRequires:  python3-sphinxext-opengraph

%description doc
Incus offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains user documentation.

%files doc
%license %{golicenses}
%doc doc/html
%endif

%dnl ----------------------------------------------------------------------------

%prep
%goprep -k
%autopatch -v -p1

%build
export CGO_LDFLAGS_ALLOW="(-Wl,-wrap,pthread_create)|(-Wl,-z,now)"
for cmd in incusd incus-user; do
    BUILDTAGS="libsqlite3" %gobuild -o %{gobuilddir}/lib/$cmd %{goipath}/cmd/$cmd
done
for cmd in incus fuidshift incus-benchmark lxc-to-incus lxd-to-incus; do
    BUILDTAGS="libsqlite3" %gobuild -o %{gobuilddir}/bin/$cmd %{goipath}/cmd/$cmd
done

# Build incus-migrate and incus-agent statically (cf. rhbz#2419661)
BUILDTAGS="netgo" %gobuild_static -o %{gobuilddir}/bin/incus-migrate %{goipath}/cmd/incus-migrate
BUILDTAGS="agent netgo" %gobuild_static -o %{gobuilddir}/bin/incus-agent %{goipath}/cmd/incus-agent

# build shell completions
mkdir %{gobuilddir}/completions
%{gobuilddir}/bin/%{name} completion bash > %{gobuilddir}/completions/%{name}.bash
%{gobuilddir}/bin/%{name} completion fish > %{gobuilddir}/completions/%{name}.fish
%{gobuilddir}/bin/%{name} completion zsh > %{gobuilddir}/completions/%{name}.zsh


%if %{with doc}
# build documentation
mkdir -p doc/.sphinx/_static/swagger-ui
install -pm 0644 %{SOURCE201} doc/.sphinx/_static/swagger-ui/swagger-ui-bundle.js
install -pm 0644 %{SOURCE202} doc/.sphinx/_static/swagger-ui/swagger-ui-standalone-preset.js
install -pm 0644 %{SOURCE203} doc/.sphinx/_static/swagger-ui/swagger-ui.css
sed -i 's|^path.*$|path = "%{gobuilddir}"|' doc/conf.py
sphinx-build -c doc/ -b dirhtml doc/ doc/html/
rm -vrf doc/html/{.buildinfo,.doctrees}
# remove duplicate files
rm -vrf doc/html/{_sources,_sphinx_design_static}
%endif

# build translations
rm -f po/zh_Hans.po po/zh_Hant.po    # remove invalid locales
make %{?_smp_mflags} build-mo

# generate man-pages
mkdir %{gobuilddir}/man
%{gobuilddir}/bin/incus manpage %{gobuilddir}/man/
%{gobuilddir}/lib/incusd manpage %{gobuilddir}/man/
help2man %{gobuilddir}/bin/fuidshift -n "uid/gid shifter" --no-info --no-discard-stderr > %{gobuilddir}/man/fuidshift.1
help2man %{gobuilddir}/bin/incus-benchmark -n "The container lightervisor - benchmark" --no-info --no-discard-stderr > %{gobuilddir}/man/incus-benchmark.1
help2man %{gobuilddir}/bin/incus-migrate -n "Physical to container migration tool" --no-info --no-discard-stderr > %{gobuilddir}/man/incus-migrate.1
help2man %{gobuilddir}/bin/lxc-to-incus -n "Convert LXC containers to Incus" --no-info --no-discard-stderr > %{gobuilddir}/man/lxc-to-incus.1
help2man %{gobuilddir}/bin/lxd-to-incus -n "LXD to Incus migration tool" --no-info --no-discard-stderr > %{gobuilddir}/man/lxd-to-incus.1
help2man %{gobuilddir}/bin/incus-agent -n "Incus virtual machine guest agent" --no-info --no-discard-stderr > %{gobuilddir}/man/incus-agent.1

# SELinux policy
mkdir selinux
cp -p %{SOURCE111} selinux/
pushd selinux
# generate the type enforcement file as it has no other content
echo 'policy_module(%{name},1.0)' >%{name}.te
%{__make} NAME=%{selinuxtype} -f %{_datadir}/selinux/devel/Makefile %{name}.pp
bzip2 -9 %{name}.pp
popd

%install
# install binaries
install -d %{buildroot}%{_bindir}
install -m0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

# install systemd units
install -d %{buildroot}%{_unitdir}
install -m0644 -vp %{SOURCE101} %{buildroot}%{_unitdir}/
install -m0644 -vp %{SOURCE102} %{buildroot}%{_unitdir}/
install -m0644 -vp %{SOURCE103} %{buildroot}%{_unitdir}/
install -m0644 -vp %{SOURCE104} %{buildroot}%{_unitdir}/
install -m0644 -vp %{SOURCE105} %{buildroot}%{_unitdir}/
install -D -m0644 -vp %{SOURCE106} %{buildroot}%{_sysusersdir}/%{name}.conf
install -D -m0644 -vp %{SOURCE107} %{buildroot}%{_tmpfilesdir}/%{name}.conf

# extra configs
install -D -m0644 -vp %{SOURCE108} %{buildroot}%{_sysconfdir}/dnsmasq.d/%{name}.conf
install -D -m0644 -vp %{SOURCE109} %{buildroot}%{_sysctldir}/10-incus-inotify.conf

# selinux policy
install -D -m0644 -vp selinux/%{name}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.bz2

# install helper libs
install -d %{buildroot}%{_libexecdir}/%{name}
install -m0755 -vp %{SOURCE110} %{buildroot}%{_libexecdir}/%{name}/
install -m0755 -vp %{gobuilddir}/lib/* %{buildroot}%{_libexecdir}/%{name}/

# install manpages
install -d %{buildroot}%{_mandir}/man1
cp -p %{gobuilddir}/man/*.1 %{buildroot}%{_mandir}/man1/

# install shell completions
install -D -m0644 -vp %{gobuilddir}/completions/%{name}.bash %{buildroot}%{bashcompletiondir}/%{name}
install -D -m0644 -vp %{gobuilddir}/completions/%{name}.fish %{buildroot}%{fish_completions_dir}/%{name}.fish
install -D -m0644 -vp %{gobuilddir}/completions/%{name}.zsh %{buildroot}%{zsh_completions_dir}/_%{name}

# cache and log directories
install -d -m0700 %{buildroot}%{_localstatedir}/cache/%{name}
install -d -m0700 %{buildroot}%{_localstatedir}/log/%{name}
install -d -m0711 %{buildroot}%{_localstatedir}/lib/%{name}

# language files
for mofile in po/*.mo ; do
    install -D -m0644 -vp ${mofile} %{buildroot}%{_datadir}/locale/$(basename ${mofile%%.mo})/LC_MESSAGES/%{name}.mo
done
%find_lang incus

%if %{with check}
%check
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
export CGO_LDFLAGS_ALLOW="(-Wl,-wrap,pthread_create)|(-Wl,-z,now)"

# Add libsqlite3 tag to go test
%define gotestflags -buildmode pie -compiler gc -v -tags libsqlite3

%gocheck -v -t %{goipath}/test \
    -d %{goipath}/cmd/lxc-to-incus  # lxc-to-incus test fails, see ganto/copr-lxc4#23
%endif

%changelog
* Sat Dec 13 2025 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.19.1-0.1
- Update to 6.19.1
- Rework static build according to Fedora spec
- Update swagger-ui to v5.31.0

* Sun Aug 03 2025 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.15-0.1
- Update to 6.15

* Fri Aug 01 2025 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.14-0.2
- Fix build for Fedora 42 (Go 1.24)

* Mon Jun 30 2025 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.14-0.1
- Update to 6.14
- Update swagger-ui to v5.24.2

* Sun Jun 01 2025 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.13-0.1
- Update to 6.13
- Update swagger-ui to v5.22.0

* Sun May 04 2025 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.12-0.3
- Fix build failures with Go 1.24

* Thu May 01 2025 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.12-0.2
- Update to 6.12
- Update swagger-ui to v5.21.0

* Mon Mar 31 2025 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.11-0.2
- Add patches to fix build tests and QEMU issues

* Sat Mar 29 2025 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.11-0.1
- Update to 6.11
- Update swagger-ui to v5.20.2

* Wed Mar 05 2025 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.10.1-0.1
- Update to 6.10.1

* Sun Mar 02 2025 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.10-0.2
- Add patch to fix Ceph regression

* Sat Mar 01 2025 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.10-0.1
- Update to 6.10
- Update swagger-ui to v5.20.0

* Tue Jan 28 2025 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.9-0.1
- Update to 6.9

* Fri Dec 13 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.8-0.1
- Update to 6.8

* Sun Nov 24 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.7-0.1
- Update to 6.7

* Sat Oct 05 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.6-0.1
- Update to 6.6

* Mon Sep 23 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.5-0.1
- Update to 6.5

* Fri Aug 09 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.4-0.1
- Update to 6.4

* Sat Jul 20 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.3-0.3
- Revert socket dir to /var/lib/incus
- Fix permission for incus rundir

* Mon Jul 15 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.3-0.2
- Fix /usr/libexec/incus and /run/incus path references

* Sun Jul 14 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.3-0.1
- Update to 6.3

* Wed Jun 05 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.2-0.1
- Update to 6.2
- Update swagger-ui to v5.17.14

* Sun May 05 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.1-0.1
- Update to 6.1
- Update swagger-ui to v5.17.3

* Tue Apr 09 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.0.0-0.1
- Update to 6.0.0
- Update swagger-ui to v5.14.0

* Fri Mar 29 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.7-0.1
- Update to 0.7
- Update swagger-ui to v5.12.3

* Thu Feb 29 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.6-0.1
- Update to 0.6
- Update swagger-ui to v5.11.8

* Thu Feb 08 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.5.1-0.1
- Update to 0.5.1
- Update swagger-ui to v5.11.3

* Sat Jan 27 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.5-0.1
- Update to 0.5
- Update swagger-ui to v5.11.1

* Wed Jan 10 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.4-0.4
- Add incus-selinux sub package

* Thu Dec 28 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.4-0.3
- Fix typo in tmpfiles config

* Wed Dec 27 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.4-0.2
- Use systemd sysusers/tmpfiles
- Update dependencies to use 'Recommends'
- Remove unneeded incus-agent script and systemd unit

* Thu Dec 21 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.4-0.1
- Update to 0.4
- Update swagger-ui to v5.10.5

* Fri Nov 10 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.2-0.2
- Fix envvar for OVMF and documentation

* Mon Oct 30 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.2-0.1
- Update to 0.2
- Update swagger-ui to v5.9.1

* Sun Oct 15 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.1-0.2
- Fix libdir path

* Sun Oct 15 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.1-0.1
- Initial package

# Disable documentation due to missing dependencies
%bcond doc 1

# Swagger version to download for documentation
%global swaggerui_version 5.33.0
%global swaggerui_source_baseurl https://github.com/swagger-api/swagger-ui/raw/v%{swaggerui_version}/dist/

# Enable tests
%bcond check 1

# https://github.com/lxc/incus
%global goipath github.com/lxc/incus
Version:        7.4

%gometa

%global godocs AUTHORS CODE_OF_CONDUCT.md CONTRIBUTING.md README.md SECURITY.md
%global golicenses COPYING

# Upstream's agent-loader tree: udev rule, systemd unit and setup script for incus-agent
%global agentloaderdir internal/server/instance/drivers/agent-loader


# Set build macro for static builds
# Uses GO111MODULE=on -mod=vendor instead of %%gomodulesmode (GO111MODULE=off)
# to ensure vendored dependencies are correctly resolved (rhbz#2419661)
%define gocompilerflags_static -compiler gc
%define gobuild_baseflags_static %{gocompilerflags_static} -mod=vendor -tags="rpm_crashtraceback ${GO_BUILDTAGS-${BUILDTAGS-}}" -a -v
%define gobuild_ldflags_static ${GO_LDFLAGS-${LDFLAGS-}} %{?currentgoldflags} -B 0x$(echo "%{name}-%{version}-%{release}-${SOURCE_DATE_EPOCH:-}" | sha1sum | cut -d ' ' -f1) -compressdwarf=false
%define gobuildflags_static() %{expand:%{gobuild_baseflags_static} -ldflags "%{gobuild_ldflags_static}"}
%define gobuild_static(-) %{expand:
  GO111MODULE=on CGO_ENABLED=0 go build %{gobuildflags_static} %{?**};
}


Name:           incus
Release:        0.1%{?dist}
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

# Web scripts shipped with API documentation
Source201:      %{swaggerui_source_baseurl}/swagger-ui-bundle.js#/swagger-ui-%{swaggerui_version}-bundle.js
Source202:      %{swaggerui_source_baseurl}/swagger-ui-standalone-preset.js#/swagger-ui-%{swaggerui_version}-standalone-preset.js
Source203:      %{swaggerui_source_baseurl}/swagger-ui.css#/swagger-ui-%{swaggerui_version}.css

# Downstream only patches
## Allow offline builds
Patch1002:      incus-0.2-doc-Remove-downloads-from-sphinx-build.patch

## %%gobuild builds without a main module (GO111MODULE=off), so the toolchain falls
## back to the pre-Go-1.22 GODEBUG defaults, where httpmuxgo121=1 selects the old
## http.ServeMux. incusd's wildcard routes ("/{$}", "/1.0/operations/{id}/wait")
## then never match and most of the API answers 404. Upstream only sets this for
## cmd/incus-agent (lxc/incus#3239); incusd builds with a main module upstream.
Patch1003:      incus-7.4-incusd-Set-httpmuxgo121-0-GODEBUG-default.patch

%global bashcompletiondir %(pkg-config --variable=completionsdir bash-completion 2>/dev/null || :)

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

%if %{with check}
BuildRequires:  btrfs-progs
BuildRequires:  dnsmasq
BuildRequires:  nftables
%endif

Requires:       incus-minimal = %{version}-%{release}
Requires:       incus-agent = %{version}-%{release}
%ifarch x86_64
Requires:       edk2-ovmf
%endif
%ifarch aarch64
Requires:       edk2-aarch64
%endif
Requires:       xorriso
# Not built for ppc64le and s390x
%ifarch x86_64 aarch64
Requires:       qemu-audio-spice
Requires:       qemu-char-spice
%endif
Requires:       qemu-device-display-virtio-vga
Requires:       qemu-device-display-virtio-gpu
Requires:       qemu-device-usb-redirect
Requires:       qemu-img
Requires:       qemu-kvm-core
Requires:       virtiofsd
# Only needed for vTPM devices
Recommends:     swtpm
Recommends:     swtpm-tools

%description
Meta-package that installs all Incus components including the daemon,
guest agent, and virtual machine support packages.

%files

%dnl ----------------------------------------------------------------------------

%package minimal
Summary:        Powerful system container and virtual machine manager
License:        Apache-2.0

Requires:       %{name}-client = %{version}-%{release}
Requires:       (container-selinux >= 2.245.0 if selinux-policy)
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
%{?sysusers_requires_compat}

%ifnarch %{ix86} %{arm32}
Requires:       skopeo
# Not yet packaged in Fedora
#Requires:       umoci
%endif

# This package no longer exists as container-selinux supersedes it
Obsoletes: %{name}-selinux < 6.19.1-4
Conflicts: %{name}-selinux < 6.19.1-4

Suggests:       %{name}-doc

%description minimal
Container hypervisor based on LXC
Incus offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains the Incus daemon.

%pre minimal
%sysusers_create_package %{name} %{SOURCE106}
%tmpfiles_create_package %{name} %{SOURCE107}
# Upgrading from before the split (incus < 7.0.0), incus-minimal is a *fresh* install
# that finds the units already on disk from the old incus. %%systemd_post would then run
# `systemctl preset` and, with no incus preset shipped, disable the units the admin had
# enabled. Flag that case here so %%post leaves the enablement state alone. Clear any
# flag an interrupted transaction left behind first, or a fresh install would skip presets.
if [ $1 -eq 1 ]; then
    rm -rf %{_localstatedir}/lib/rpm-state/%{name}
    if [ -e %{_unitdir}/%{name}.socket ]; then
        mkdir -p %{_localstatedir}/lib/rpm-state/%{name}
        touch %{_localstatedir}/lib/rpm-state/%{name}/split-upgrade
    fi
fi

%post minimal
%sysctl_apply 10-incus-inotify.conf
if [ -e %{_localstatedir}/lib/rpm-state/%{name}/split-upgrade ]; then
    rm -rf %{_localstatedir}/lib/rpm-state/%{name}
else
%systemd_post %{name}.socket
%systemd_post %{name}.service
%systemd_post %{name}-startup.service
%systemd_post %{name}-user.socket
%systemd_post %{name}-user.service
fi

%preun minimal
%systemd_preun %{name}.socket
%systemd_preun %{name}.service
%systemd_preun %{name}-startup.service
%systemd_preun %{name}-user.socket
%systemd_preun %{name}-user.service

%postun minimal
%systemd_postun_with_restart %{name}.socket
%systemd_postun_with_restart %{name}.service
%systemd_postun_with_restart %{name}-user.socket
%systemd_postun_with_restart %{name}-user.service

%files minimal
%license %{golicenses}
%config(noreplace) %{_sysconfdir}/dnsmasq.d/%{name}.conf
%{_sysctldir}/10-incus-inotify.conf
%{_unitdir}/%{name}.socket
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-startup.service
%{_unitdir}/%{name}-user.socket
%{_unitdir}/%{name}-user.service
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/incusd
%{_libexecdir}/%{name}/incus-user
%{_libexecdir}/%{name}/shutdown
%{_sysusersdir}/%{name}.conf
%{_tmpfilesdir}/%{name}.conf
%{_mandir}/man1/incusd*.1.*
%attr(700,root,root) %dir %{_localstatedir}/cache/%{name}
%attr(700,root,root) %dir %{_localstatedir}/log/%{name}
%attr(711,root,root) %dir %{_localstatedir}/lib/%{name}
%ghost %attr(711,root,root) %dir /run/%{name}

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
%exclude %{_mandir}/man1/incus-simplestreams.1.*

%dnl ----------------------------------------------------------------------------

%package tools
Summary:        Container hypervisor based on LXC - Extra Tools
License:        Apache-2.0

Requires:       rsync
# fuidshift is also shipped with lxd
Conflicts:      lxd-tools

%description tools
Incus offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains extra tools provided with Incus.
 - fuidshift - A tool to map/unmap filesystem uids/gids
 - lxc-to-incus - A tool to migrate LXC containers to Incus
 - incus-benchmark - A Incus benchmark utility
 - incus-migrate - A physical to container migration tool
 - incus-simplestreams - Maintain an Incus-compatible simplestreams tree

%files tools
%license %{golicenses}
%{_bindir}/fuidshift
%{_bindir}/incus-benchmark
%{_bindir}/incus-migrate
%{_bindir}/incus-simplestreams
%{_bindir}/lxc-to-incus
%{_mandir}/man1/fuidshift.1.*
%{_mandir}/man1/incus-benchmark.1.*
%{_mandir}/man1/incus-migrate.1.*
%{_mandir}/man1/incus-simplestreams.1.*
%{_mandir}/man1/lxc-to-incus.1.*

%dnl ----------------------------------------------------------------------------

%package agent
Summary:        Incus guest agent
License:        Apache-2.0
# incus-agent-setup calls eject(1) to detach the agent config drive, which the host uses
# as its cue to detach the media (qmp DEVICE_TRAY_MOVED).
Recommends:     util-linux
%{?systemd_requires}

%description agent
This package provides the agent that runs inside Incus virtual machine
guests. Installed in a guest (or image), it is started automatically on an
Incus VM and runs the packaged binary, so its version should track the
host's Incus release. Don't also run the install.sh from the agent share:
it replaces the packaged unit with one that runs the host-supplied agent.

Installed on an Incus host, it provides the agent binary that incusd shares
with virtual machines that don't carry their own.

# No %%post: unlike the incus-minimal units, incus-agent.service has no [Install]
# section. It is started by the udev rule on the virtio port
# (ENV{SYSTEMD_WANTS}), so %%systemd_post's `systemctl preset` has nothing to link
# and is a silent no-op. The daemon-reload comes from systemd's own file trigger on
# %%{_unitdir}, not from here.
# No %%postun either: processes started by `incus exec` live in the agent's cgroup,
# so %%systemd_postun_with_restart would kill them -- including the `dnf upgrade`
# running this very transaction. The new agent takes over at the next boot.
# %%preun stays: its `disable --now` is what stops a running agent when the package
# is removed inside a guest. The `disable` half is the no-op, the `--now` is not.
%preun agent
%systemd_preun %{name}-agent.service

%files agent
%license %{golicenses}
# co-owned with incus-minimal: the agent installs standalone in a guest, where
# nothing else owns this directory
%dir %{_libexecdir}/%{name}
%dir %{_libexecdir}/%{name}/agents
%{_libexecdir}/%{name}/agents/%{name}-agent.linux.%{_target_cpu}
%{_libexecdir}/%{name}/%{name}-agent
%{_libexecdir}/%{name}/%{name}-agent-setup
%{_udevrulesdir}/60-%{name}-agent.rules
%{_unitdir}/%{name}-agent.service
%{_mandir}/man1/%{name}-agent.1.*

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
for cmd in incus fuidshift incus-benchmark incus-simplestreams lxc-to-incus; do
    BUILDTAGS="libsqlite3" %gobuild -o %{gobuilddir}/bin/$cmd %{goipath}/cmd/$cmd
done

# Build incus-migrate and incus-agent statically (cf. rhbz#2419661)
# Uses GO111MODULE=on -mod=vendor, so paths must be relative to module root
pushd %{currentgosourcedir}
BUILDTAGS="netgo" %gobuild_static -o %{gobuilddir}/bin/incus-migrate ./cmd/incus-migrate
BUILDTAGS="agent netgo" %gobuild_static -o %{gobuilddir}/lib/incus-agent ./cmd/incus-agent
popd

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
rm -vrf doc/html/{.buildinfo,.buildinfo.bak,.doctrees}
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
help2man %{gobuilddir}/bin/incus-simplestreams -n "Maintain an Incus-compatible simplestreams tree" --no-info --no-discard-stderr > %{gobuilddir}/man/incus-simplestreams.1
help2man %{gobuilddir}/bin/lxc-to-incus -n "Convert LXC containers to Incus" --no-info --no-discard-stderr > %{gobuilddir}/man/lxc-to-incus.1
help2man %{gobuilddir}/lib/incus-agent -n "Incus virtual machine guest agent" --no-info --no-discard-stderr > %{gobuilddir}/man/incus-agent.1

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

# install helper libs
install -d %{buildroot}%{_libexecdir}/%{name}
install -m0755 -vp %{SOURCE110} %{buildroot}%{_libexecdir}/%{name}/
install -m0755 -vp %{gobuilddir}/lib/* %{buildroot}%{_libexecdir}/%{name}/

# incusd shares INCUS_AGENT_PATH (see incus.service) into VMs over 9p, where the loader
# copies incus-agent.<os>.<arch> out of it. A dedicated directory keeps incusd and the
# other helpers out of the guests' view.
install -d %{buildroot}%{_libexecdir}/%{name}/agents
mv %{buildroot}%{_libexecdir}/%{name}/%{name}-agent \
    %{buildroot}%{_libexecdir}/%{name}/agents/%{name}-agent.linux.%{_target_cpu}
ln -s agents/%{name}-agent.linux.%{_target_cpu} %{buildroot}%{_libexecdir}/%{name}/%{name}-agent

# install agent helpers from upstream's agent-loader tree
install -D -m0644 -vp %{agentloaderdir}/systemd/%{name}-agent.rules \
    %{buildroot}%{_udevrulesdir}/60-%{name}-agent.rules
install -D -m0755 -vp %{agentloaderdir}/%{name}-agent-setup-linux \
    %{buildroot}%{_libexecdir}/%{name}/%{name}-agent-setup
install -D -m0644 -vp %{agentloaderdir}/systemd/%{name}-agent.service \
    %{buildroot}%{_unitdir}/%{name}-agent.service
# upstream's install-linux.sh substitutes this placeholder when installing from the
# 9p mount; the packaged unit gets the fixed path instead. Like Debian, run the
# packaged agent rather than the one copied off the host's config drive, and skip
# the unit outside an Incus VM (rhbz#2421161).
sed -i -e 's|TARGET/systemd/%{name}-agent-setup|%{_libexecdir}/%{name}/%{name}-agent-setup|' \
    -e 's|^ExecStart=.*|ExecStart=%{_libexecdir}/%{name}/%{name}-agent|' \
    -e '/^\[Unit\]/a ConditionPathExists=/dev/virtio-ports/org.linuxcontainers.incus' \
    %{buildroot}%{_unitdir}/%{name}-agent.service

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
* Mon Apr 06 2026 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.23-0.2
- Fix static builds of vendored dependencies

* Mon Apr 06 2026 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.23-0.1
- Update to 6.23
- Drop selinux subpackage in favor of container-selinux
- Follow upstream RPM to adjust socket path to /run
- Update swagger-ui to v5.32.1

* Sat Dec 13 2025 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.19.1-0.2
- Fix Sphinx documentation build

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

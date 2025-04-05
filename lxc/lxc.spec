%if 0%{?fedora}
%bcond_without seccomp
%bcond_without static_init
%endif

%if 0%{?rhel} >= 7
%ifarch %{ix86} x86_64 %{arm} aarch64
%bcond_without seccomp
%endif
%endif

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:           lxc
Version:        6.0.4
Release:        0.1%{?dist}
Summary:        Linux Resource Containers
# Automatically converted from old format: LGPLv2+ and GPLv2 - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2+ AND GPL-2.0-only
URL:            https://linuxcontainers.org/lxc
Source0:        https://linuxcontainers.org/downloads/%{name}/%{name}-%{version}.tar.gz
Source1:        lxc-net
Patch0:         lxc-2.0.7-fix-init.patch
Patch1:         lxc-4.0.1-fix-lxc-net.patch

BuildRequires:  cmake
BuildRequires:  docbook2X
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  glibc-headers
BuildRequires:  kernel-headers
BuildRequires:  libcap
BuildRequires:  libcap-devel
%if %{?with_seccomp}
BuildRequires:  pkgconfig(libseccomp)
%endif
BuildRequires:  libselinux-devel
BuildRequires:  meson >= 0.61
BuildRequires:  openssl-devel
BuildRequires:  pam
BuildRequires:  pam-devel
BuildRequires:  pkg-config
BuildRequires:  systemd-devel
BuildRequires:  pkgconfig(dbus-1)
%if %{?with_static_init}
BuildRequires:  libcap-static
BuildRequires:  glibc-static
%endif
# lxc-extra subpackage not needed anymore, lxc-ls has been rewriten in
# C and does not depend on the Python3 binding anymore
Provides:       lxc-extra = %{version}-%{release}
Obsoletes:      lxc-extra < 1.1.5-3

# https://bugzilla.redhat.com/show_bug.cgi?id=2274215
Requires: lxc-libs%{?_isa} = %{version}-%{release}
Requires: lxcfs
Requires: openssl
Requires: rsync
# Requires: dnsmasq
# Requires: bridge-utils
# Needed to create openSUSE containers using template.
# Recommends: build
# Recommends: criu >= 2.0

%description
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.


%package           libs
Summary:           Runtime library files for %{name}
# rsync is called in bdev.c, e.g. by lxc-clone
Requires:          rsync
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd
Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig


%description    libs
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The %{name}-libs package contains libraries for running %{name} applications.


%package        templates
Summary:        Templates for %{name}
BuildArch:      noarch
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
# Note: Not all requirements for the template scripts (busybox, dpkg,
# debootstrap, rsync, openssh-server, dhclient, apt, pacman, zypper,
# ubuntu-cloudimg-query etc...) are explicitly mentioned here: their
# presence varies wildly on supported Fedora/EPEL releases and archs,
# and they are in most cases needed for a single template only. Also,
# the templates normally fail graciously when such a tool is
# missing. Moving each template to its own subpackage on the other
# hand would be overkill.
#
# Add some packages used by the 'download' template (see also #1828032)
Requires:       gnupg
Requires:       wget
Requires:       xz


%description    templates
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The %{name}-templates package contains templates for creating containers.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description    doc
This package contains documentation for %{name}.


%prep
%autosetup -p1


%build
%meson \
	-D examples=true \
	-D man=true \
	-D tools=true \
	-D commands=true \
	-D capabilities=true \
	-D openssl=true \
	-D selinux=true \
%if 0%{?with_seccomp}
	-D seccomp=true \
%endif
	-D memfd-rexec=true \
	-D thread-safety=true \
	-D dbus=true \
	-D tests=false \
	-D init-script=systemd \
	-D systemd-unitdir=%{_unitdir} \
	-D distrosysconfdir=sysconfig \
	-D pam-cgroup=true \
	-D runtime-path=%{_rundir} \
	%{nil}
%meson_build

# See https://github.com/lxc/lxc/issues/4156
cd doc/api/ && doxygen


%install
%meson_install
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

# docs
mkdir -p %{buildroot}%{_pkgdocdir}/api
cp -a AUTHORS README.md %{buildroot}%{_pkgdocdir}
cp -a doc/api/html/* %{buildroot}%{_pkgdocdir}/api/

# cache dir
mkdir -p %{buildroot}%{_localstatedir}/cache/%{name}

# remove libtool .a file
rm -r %{buildroot}%{_libdir}/liblxc.a

# lxc-net config file
cp -a %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-net

%check
%meson_test


%post libs
%systemd_post %{name}-net.service
%systemd_post %{name}.service
%systemd_post lxc-monitord.service

%preun libs
%systemd_preun %{name}-net.service
%systemd_preun %{name}.service
%systemd_preun lxc-monitord.service


%postun libs
%systemd_postun %{name}-net.service
%systemd_postun %{name}.service
%systemd_postun lxc-monitord.service


%files
%{_bindir}/%{name}-*
%{_mandir}/man1/%{name}*
%{_mandir}/*/man1/%{name}*
# in lxc-libs:
%exclude %{_bindir}/%{name}-autostart
%exclude %{_mandir}/man1/%{name}-autostart*
%exclude %{_mandir}/*/man1/%{name}-autostart*
%exclude %{_mandir}/man1/%{name}-user-nic*
%exclude %{_mandir}/*/man1/%{name}-user-nic*
%{_datadir}/%{name}/%{name}.functions
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/_%{name}
%{_datadir}/bash-completion/completions/%{name}-*


%files libs
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/templates
%dir %{_datadir}/%{name}/config
%{_datadir}/%{name}/hooks
%{_datadir}/%{name}/%{name}-patch.py*
%{_datadir}/%{name}/selinux
%{_libdir}/liblxc.so.*
%{_libdir}/%{name}
%{_libexecdir}/%{name}
# fixme: should be in libexecdir?
%{_sbindir}/init.%{name}
%if %{?with_static_init}
%{_sbindir}/init.%{name}.static
%endif
%{_bindir}/%{name}-autostart
%{_sharedstatedir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/default.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-net
%{_mandir}/man1/%{name}-autostart*
%{_mandir}/*/man1/%{name}-autostart*
%{_mandir}/man1/%{name}-user-nic*
%{_mandir}/*/man1/%{name}-user-nic*
%{_mandir}/man5/%{name}*
%{_mandir}/man7/%{name}*
%{_mandir}/*/man5/%{name}*
%{_mandir}/*/man7/%{name}*
%{_mandir}/man8/pam_cgfs*
%{_mandir}/*/man8/pam_cgfs*
%dir %{_pkgdocdir}
%{_pkgdocdir}/AUTHORS
%{_pkgdocdir}/README.md
%{_pkgdocdir}/examples
%license COPYING
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}@.service
%{_unitdir}/%{name}-net.service
%{_unitdir}/%{name}-monitord.service
%dir %{_localstatedir}/cache/%{name}
%{_libdir}/security/pam_cgfs.so


%files templates
%{_datadir}/%{name}/templates/lxc-*
%{_datadir}/%{name}/config/*


%files devel
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/lxc
%{_libdir}/liblxc.so


%files doc
%dir %{_pkgdocdir}
# README, AUTHORS and COPYING intentionally duplicated because -doc
# can be installed on its own.
%{_pkgdocdir}/*
%license COPYING


%changelog
* Sat Apr 05 2025 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.0.4-0.1
- Update lxc to 6.0.4

* Sat Feb 15 2025 Sérgio Basto <sergio@serjux.com> - 6.0.3-1
- Update lxc to 6.0.3 (#2333359)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Sep 21 2024 Sérgio Basto <sergio@serjux.com> - 6.0.2-1
- Update lxc to 6.0.2 (#2313692)

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 6.0.1-2
- convert license to SPDX

* Fri Jul 19 2024 Sérgio Basto <sergio@serjux.com> - 6.0.1-1
- Update lxc to 6.0.1 (#2097935)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Apr 09 2024 Sérgio Basto <sergio@serjux.com> - 5.0.3-2
- (#2274215) force lxc requires lxc-libs
- Add more Requires

* Fri Jan 26 2024 Sérgio Basto <sergio@serjux.com> - 5.0.3-1
- Update lxc to 5.0.3 (inspired in https://build.opensuse.org/package/show/Virtualization:containers/lxc)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu May 26 2022 Thomas Moschny <thomas.moschny@gmx.de> - 4.0.12-1
- Update to 4.0.12.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Sep 18 2021 Thomas Moschny <thomas.moschny@gmx.de> - 4.0.10-1
- Update to 4.0.10.

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 4.0.9-3
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May  8 2021 Thomas Moschny <thomas.moschny@gmx.de> - 4.0.9-1
- Update to 4.0.9.

* Sat May  1 2021 Thomas Moschny <thomas.moschny@gmx.de> - 4.0.8-1
- Update to 4.0.8.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Thomas Moschny <thomas.moschny@gmx.de> - 4.0.6-1
- Update to 4.0.6.

* Sat Nov 14 2020 Thomas Moschny <thomas.moschny@gmx.de> - 4.0.5-1
- Update to 4.0.5.
- Enable LXC bridge per default.
- Add wget dependency for the templates subpackage.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 30 2020 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 3.2.1-3
- reapplying patch to fix cgroups cpuset initialization (rhbz#1816949)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Dec 15 2019 Thomas Moschny <thomas.moschny@gmx.de> - 3.2.1-1
- Update to 3.2.1.
- Include pam_cgfs.
- Use OpenSSL.

* Mon Sep  9 2019 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.4-2
- Add patches to fix cgroups cpuset initialization (rhbz#1750031).

* Fri Aug 16 2019 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.4-1
- Update to 3.0.4.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Apr 28 2019 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.3-3
- Add patch for CVE-2019-5736.
- Build and include init.lxc.static where possible (rhbz#1654366).

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 23 2018 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.3-1
- Update to 3.0.3.

* Fri Aug 17 2018 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.2-1
- Update to 3.0.2.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.1-1
- Update to 3.0.1.

* Fri Apr  6 2018 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.0-1
- Update to 3.0.0.
- Language bindings are separate projects now.
- Update spec file and remove obsolete constructs.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.9-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 20 2017 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.9-1
- Update to 2.0.9.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 10 2017 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.8-2
- Fix for EL6 build failure.
- Fix bash completion on epel6 (rhbz#1408173).

* Tue Jun  6 2017 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.8-1
- Update to 2.0.8.

* Thu Mar  9 2017 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.7-2
- Add fix for CVE-2017-5985.

* Wed Feb 15 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.0.7-1.2
- Rebuild for brp-python-bytecompile

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 29 2017 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.7-1
- Update to 2.0.7.

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.0.6-2.1
- Rebuild for Python 3.6

* Sun Dec  4 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.6-2
- Enable python3 on epel7 builds.
- Fix dependency on network-online.target for lxc-net.service.

* Sat Dec  3 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.6-1
- Update to 2.0.6.

* Wed Oct  5 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.5-1
- Update to 2.0.5.

* Tue Aug 16 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.4-1
- Update to 2.0.4.
- Remove conditional for eol'ed Fedora releases.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-1.1
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 29 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.3-1
- Update to 2.0.3.
- Merge spec file cleanups by Thierry Vignaud (tvignaud@redhat.com).

* Fri Jun  3 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.1-1
- Update to 2.0.1.
- Remove patch no longer needed.

* Wed Apr 20 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.0-1
- Update to 2.0.0.
- Obsolete the -extra subpackage.
- Move the completion file to %%{_datadir}.

* Tue Mar  1 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.5-2
- Power64 and s390(x) now have libseccomp support

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 15 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.5-1
- Update to 1.1.5.
- Update patch.

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2.1
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 21 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.4-2
- Add patch to fix bootorder (rhbz#1263612).

* Sat Oct 17 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.4-1
- Update to 1.1.4.

* Thu Oct  1 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.3-2
- Add security fix, see rhbz#1267844.

* Sat Aug 15 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.3-1
- Update to 1.1.3.
- Remove patches applied upstream.

* Sun Aug  2 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.2-2
- Add security fixes, see rhbz#1245939 and rhbz#1245941.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 20 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.2-1
- Update to 1.1.2.
- Add patch to fix building of the lua bindings.

* Tue Mar 17 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.1-2
- Use %%license only where possible.

* Tue Mar 17 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.1-1
- Update to 1.1.1.
- Add dependency on rsync (rhbz#1177981).
- Tag COPYING with %%licence.

* Mon Feb 16 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.0-3
- aarch64 now has seccomp support

* Tue Feb 10 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.0-2
- lxc-top no longer relies on the lua bindings.
- lxc-device no longer relies on the python3 bindings.
- Spec file cleanups.

* Sun Feb  8 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.0-1
- Update to 1.1.0.

* Sat Aug 30 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.0-0.3.alpha1
- Add missing dependency on lua-alt-getopt (rhbz#1131707).

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.2.alpha1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 11 2014 Jakub Čajka <jcajka@redhat.com> - 1.1.0-0.2.alpha1
- Fixed build dependencies on s390(x) and ppc(64(le))

* Sun Aug 10 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.0-0.1.alpha1
- Update to 1.1.0.alpha1.

* Fri Aug  8 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.5-2
- Include sysvinit resp. systemd support for autostart of containers.
- Do not list explicit requirements for templates.
- Add missing dependency on lxc-lua for lxc-top.
- Include apidocs.

* Fri Aug  8 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.5-1
- Update to 1.0.5

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun  4 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.3-1
- Update to 1.0.3.
- Remove obsolete patches.
- Add systemd support.
- Lua bindings are not optional (needed e.g. for lxc-top).

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Jan 30 2014 Marek Goldmann <mgoldman@redhat.com> - 0.9.0-3
- There is still no Python 3 available in EPEL 7

* Wed Sep  4 2013 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.0-2
- Small fix to the included Fedora template.

* Sun Sep  1 2013 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.0-1
- Update to 0.9.0.
- Make the -libs subpackage installable on its own:
  - Move files needed by the libraries to the subpackage.
  - Let packages depend on -libs.
- Add rsync as dependency to the templates package.
- Add (optional) subpackages for Python3 and Lua bindings.
- Add upstream patches for the Fedora template.
- Define and use the _pkgdocdir macro, also fixing rhbz#1001235.
- Update License tag.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar  2 2013 Thomas Moschny <thomas.moschny@gmx.de> - 0.8.0-2
- Add upstream patch fixing the release url in the Fedora template.

* Fri Feb 15 2013 Thomas Moschny <thomas.moschny@gmx.de> - 0.8.0-1
- Update to 0.8.0.
- Modernize spec file.
- Include more templates.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 26 2012 Thomas Moschny <thomas.moschny@gmx.de> - 0.7.5-1
- Update to upstream 0.7.5
- No need to run autogen.sh
- Fix: kernel header asm/unistd.h was not found
- Specfile cleanups

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 06 2011 Adam Miller <maxamillion@fedoraproject.org> - 0.7.4.2-1
- Update to upstream 0.7.4.2

* Fri Mar 25 2011 Silas Sewell <silas@sewell.ch> - 0.7.4.1-1
- Update to 0.7.4.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 26 2010 Silas Sewell <silas@sewell.ch> - 0.7.2-1
- Update to 0.7.2
- Remove templates

* Tue Jul 06 2010 Silas Sewell <silas@sewell.ch> - 0.7.1-1
- Update to 0.7.1

* Wed Feb 17 2010 Silas Sewell <silas@sewell.ch> - 0.6.5-1
- Update to latest release
- Add /var/lib/lxc directory
- Patch for sys/stat.h

* Fri Nov 27 2009 Silas Sewell <silas@sewell.ch> - 0.6.4-1
- Update to latest release
- Add documentation sub-package

* Mon Jul 27 2009 Silas Sewell <silas@sewell.ch> - 0.6.3-2
- Apply patch for rawhide kernel

* Sat Jul 25 2009 Silas Sewell <silas@sewell.ch> - 0.6.3-1
- Initial package

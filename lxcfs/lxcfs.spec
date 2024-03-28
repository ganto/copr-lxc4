Name:		  lxcfs
Version:	  6.0.0
Release:	  0.1%{?dist}
Summary:	  FUSE based filesystem for LXC
License:	  ASL 2.0
URL:		  https://linuxcontainers.org/lxcfs
Source0:	  https://linuxcontainers.org/downloads/%{name}/%{name}-%{version}.tar.gz
Source1:	  %{name}-tmpfiles.conf
BuildRequires:	  meson
BuildRequires:	  gcc
BuildRequires:	  python3-jinja2
BuildRequires:	  gawk
BuildRequires:	  make
BuildRequires:	  fuse-devel
BuildRequires:	  help2man
BuildRequires:	  systemd
BuildRequires:	  systemd-rpm-macros
Requires(post):	  systemd
Requires(preun):  systemd
Requires(postun): systemd
# for /usr/share/lxc/config/common.conf.d:
Requires:	  lxc-templates


%description
LXCFS is a small FUSE filesystem written with the intention of making
Linux containers feel more like a virtual machine. It started as a
side-project of LXC but is usable by any runtime.

LXCFS will take care that the information provided by crucial files in
procfs are container aware such that the values displayed (e.g. in
/proc/uptime) really reflect how long the container is running and not
how long the host is running.


%prep
%autosetup -p1


%build
%meson
%meson_build


%install
%meson_install
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
install -D -m0644 -vp %{SOURCE1} %{buildroot}%{_tmpfilesdir}/%{name}.conf


%post
%tmpfiles_create %{_tmpfilesdir}/%{name}.conf
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun %{name}.service


%files
%doc AUTHORS
# empty:
#doc ChangeLog NEWS README
%license COPYING
%{_bindir}/lxcfs
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/lib%{name}.so
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/lxc.mount.hook
%{_datadir}/%{name}/lxc.reboot.hook
%{_mandir}/man1/%{name}.1*
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%{_datadir}/lxc/config/common.conf.d/00-lxcfs.conf
%dir %{_sharedstatedir}/%{name}


%changelog
* Thu Mar 28 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 6.0.0-0.1
- Update to 6.0.0.

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug  2 2023 Thomas Moschny <thomas.moschny@gmx.de> - 5.0.4-1
- Update to 5.0.4.

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Thomas Moschny <thomas.moschny@gmx.de> - 5.0.3-1
- Update to 5.0.3.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Sep  2 2022 Thomas Moschny <thomas.moschny@gmx.de> - 5.0.2-1
- Update to 5.0.2.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 25 2022 Thomas Moschny <thomas.moschny@gmx.de> - 5.0.0-1
- Update to 5.0.0.

* Sat Mar  5 2022 Thomas Moschny <thomas.moschny@gmx.de> - 4.0.12-1
- Update to 4.0.12.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Oct 23 2021 Thomas Moschny <thomas.moschny@gmx.de> - 4.0.11-1
- Update to 4.0.11.

* Wed Jul 21 2021 Thomas Moschny <thomas.moschny@gmx.de> - 4.0.9-1
- Update to 4.0.9.

* Sat May  1 2021 Thomas Moschny <thomas.moschny@gmx.de> - 4.0.8-1
- Update to 4.0.8.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 2021 Thomas Moschny <thomas.moschny@gmx.de> - 4.0.7-1
- Update to 4.0.7.

* Sun Oct 25 2020 Thomas Moschny <thomas.moschny@gmx.de> - 4.0.6-1
- Update to 4.0.6.

* Wed Aug  5 2020 Thomas Moschny <thomas.moschny@gmx.de> - 4.0.5-1
- Update to 4.0.5.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jun 20 2020 Thomas Moschny <thomas.moschny@gmx.de> - 4.0.4-1
- Update to 4.0.4.

* Fri Apr 24 2020 Thomas Moschny <thomas.moschny@gmx.de> - 4.0.3-1
- Update to 4.0.3.

* Fri Apr 10 2020 Thomas Moschny <thomas.moschny@gmx.de> - 4.0.2-1
- Update to 4.0.2.

* Sat Mar 21 2020 Thomas Moschny <thomas.moschny@gmx.de> - 4.0.1-1
- Update to 4.0.1.

* Sat Mar  7 2020 Thomas Moschny <thomas.moschny@gmx.de> - 4.0.0-1
- Update to 4.0.0.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Dec 15 2019 Thomas Moschny <thomas.moschny@gmx.de> - 3.1.2-1
- Update to 3.1.2.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul  7 2019 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.4-1
- Update to 3.0.4.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 23 2018 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.3-2
- Explicitly set the init system in the configure step.

* Fri Nov 23 2018 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.3-1
- Update to 3.0.3.

* Fri Aug 17 2018 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.2-1
- Update to 3.0.2.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun  2 2018 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.1-1
- Update to 3.0.1.

* Wed Apr  4 2018 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.0-1
- New package.

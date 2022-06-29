# https://github.com/lxc/distrobuilder
%global goipath github.com/lxc/distrobuilder
Version:        2.1
%gometa

%global godocs      AUTHORS CONTRIBUTING.md
%global golicenses  COPYING

Name:           distrobuilder
Release:        0.1%{?dist}
Summary:        System container image builder for LXC and LXD

License:        ASL 2.0
URL:            %{gourl}
Source0:        https://linuxcontainers.org/downloads/distrobuilder/%{name}-%{version}.tar.gz
Patch0:         %{name}-%{version}-Disable-online-tests.patch

BuildRequires:  gnupg
BuildRequires:  help2man
BuildRequires:  squashfs-tools

Requires:       gnupg
Requires:       rsync
Requires:       squashfs-tools
Requires:       tar
Requires:       xz

Suggests:       debootstrap
Suggests:       genisoimage

%description
%{summary}.

%gopkg

%prep
%goprep -k
%patch0 -p1

%generate_buildrequires

%build

%gobuild -o %{gobuilddir}/bin/%{name} %{goipath}/%{name}

help2man %{gobuilddir}/bin/%{name} -n "System container image builder" --no-info --no-discard-stderr > %{name}.1

%install
%gopkginstall
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

install -m 0755 -vd                     %{buildroot}%{_mandir}/man1
install -m 0644 -vp %{name}.1           %{buildroot}%{_mandir}/man1/

%check
%gocheck

%files
%license %{golicenses}
%doc
%doc doc/*.md
%doc doc/examples
%{_bindir}/*
%{_mandir}/man1/%{name}.1.*

%gopkgfiles

%changelog
* Sun Feb 27 2022 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.0-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Oct 28 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.0-0.1
- Update to 2.0.

* Sun Aug 22 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.3-0.1
- Update to 1.3.

* Wed Apr 14 2021 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.2-0.1
- Update to 1.2.

* Sat Oct 03 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.1-0.1
- Update to 1.1.

* Thu Oct 24 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.0-0.1
- Update to 1.0
- Add man-page through help2man

* Wed Jul 10 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0-0.1.20190710gitd686c88
- Update to commit d686c88 from July 10, 2019

* Sat Sep 22 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0-0.1.20180707git7274ea2
- Update to commit 7274ea2 from Jul 7, 2018

* Fri Jun 01 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0-0.1.20180522gita15b067
- Update to commit a15b067 from May 22, 2018

* Tue May 08 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0-0.1.20180428git406fd5f
- Update to commit 406fd5f from Apr 28, 2018

* Wed Apr 04 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0-0.1.20180403gitc0e1763
- Initial package

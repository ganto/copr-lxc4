%global srcname python3-lxc

%if 0%{?rhel} == 7
# Optional python3.4 support for CentOS 7
%global with_python34 1
%endif

%if 0%{?with_python34}
%global __python34 /usr/bin/python3.4
%define python34_sitelib %(%{__python34} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%define python34_sitearch %(%{__python34} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%define python34_version %(%{__python34} -c "import sys; sys.stdout.write(sys.version[:3])")
%define python34_version_nodots %(%{__python34} -c "import sys; sys.stdout.write(sys.version[:3].replace('.',''))")
%define python34_platform %(%{__python34} -Ic "import sysconfig; print(sysconfig.get_platform())")

%define py34_build() %{expand:\\\
  CFLAGS="%{optflags}" %{__python34} %{py_setup} %{?py_setup_args} build --executable="%{__python34} %{py3_shbang_opts}" %{?*}
  sleep 1
}

%define py34_install() %{expand:\\\
  CFLAGS="%{optflags}" %{__python34} %{py_setup} %{?py_setup_args} install -O1 --skip-build --root %{buildroot} %{?*}
}
%endif

%if 0%{?rhel} == 7
Name:           python36-lxc
%else
Name:           %{srcname}
%endif
Version:        3.0.4
Release:        0.2%{?dist}
Summary:        Python 3 bindings for LXC

Group:          Development/Libraries
License:        LGPLv2+
URL:            https://linuxcontainers.org/lxc
Source0:        https://linuxcontainers.org/downloads/lxc/%{srcname}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  lxc-devel >= 3
BuildRequires:  pkgconfig(python3) >= 3.2
%if 0%{?rhel} == 7
BuildRequires:  python36-setuptools
Provides:       %{srcname} = %{version}-%{release}
%endif

%description
%{summary}

%if 0%{?with_python34}
%package -n python34-lxc
Summary:        Python 3 bindings for LXC
BuildRequires:  python34-devel
BuildRequires:  python34-setuptools

%description -n python34-lxc
%{summary}
%endif


%prep
%autosetup -n %{srcname}-%{version}

# fix python shebang in examples
sed -i 's|/usr/bin/env python3|/usr/bin/python3|g' examples/*
chmod -x examples/*

%build
%py3_build
%if 0%{?with_python34}
%py34_build
%endif

%install
%py3_install
%if 0%{?with_python34}
%py34_install
%endif


%check

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README.md
%doc examples/
%{python3_sitearch}/*

%if 0%{?with_python34}
%files -n python34-lxc
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README.md
%doc examples/
%{python34_sitearch}/*
%endif

%changelog
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


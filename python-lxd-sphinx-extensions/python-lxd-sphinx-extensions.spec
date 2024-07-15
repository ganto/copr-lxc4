%global pypi_name lxd-sphinx-extensions

Name:           python-%{pypi_name}
Version:        0.0.15
Release:        0.2%{?dist}
Summary:        A collection of Sphinx extensions used in LXD
License:        ASL 2.0
URL:            https://github.com/canonical/lxd-sphinx-extensions
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%global common_desc \
This package provides several Sphinx extensions that are used in the LXD \
documentation, but can also be useful for other documentation sets.

%description
%common_desc

%package -n python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python3-%{pypi_name}
%common_desc


%prep
%autosetup -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files '*' +auto


%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE


%changelog
* Mon Jul 15 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.0.15-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Nov 02 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.0.15-0.1
- Update to 0.0.15

* Wed Oct 04 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.0.14-0.1
- Update to 0.0.14

* Sat Sep 09 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.0.12-0.1
- Update to 0.0.12

* Sat Sep 02 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.0.11-0.1
- Update to 0.0.11

* Thu Aug 24 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.0.10-0.1
- Update to 0.0.10

* Sun Aug 6 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 0.0.9-0.1
- Initial packaging

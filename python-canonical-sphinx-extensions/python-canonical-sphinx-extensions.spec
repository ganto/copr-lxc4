%global srcname   canonical_sphinx_extensions
%global pypi_name canonical-sphinx-extensions

Name:           python-%{pypi_name}
Version:        0.0.33
Release:        0.1%{?dist}
Summary:        Sphinx extensions used by Canonical
License:        Apache-2.0
URL:            https://github.com/canonical/canonical-sphinx-extensions
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%global common_desc \
This package provides several Sphinx extensions that are used in Canonical \
documentation.

%description
%common_desc

%package -n python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python3-%{pypi_name}
%common_desc


%prep
%autosetup -n %{srcname}-%{version}

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
* Sat Nov 30 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.0.23-0.1
- Initial package


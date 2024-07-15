Name:           python-sphinxcontrib-jquery
Version:        4.1
Release:        4%{?dist}
Summary:        Extension to include jQuery on newer Sphinx releases

# The project is 0BSD
# _sphinx_javascript_frameworks_compat.js is BSD-2-Clause
# jquery-3.6.0.js and jquery.js are MIT
License:        0BSD AND BSD-2-Clause AND MIT
URL:            https://github.com/sphinx-contrib/jquery/
Source:         %{url}/archive/v%{version}/sphinxcontrib-jquery-%{version}.tar.gz


BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest

%global _description %{expand:
sphinxcontrib-jquery is a Sphinx extension that ensures that jQuery
is always installed for use in Sphinx themes or extensions.}


%description %_description

%package -n     python3-sphinxcontrib-jquery
Summary:        %{summary}

%description -n python3-sphinxcontrib-jquery %_description


%prep
%autosetup -p1 -n jquery-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files 'sphinxcontrib*'


%check
%pytest


%files -n python3-sphinxcontrib-jquery -f %{pyproject_files}
%doc README.rst
%license LICENCE


%changelog
* Mon Jul 15 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 4.1-2
- Rebuilt for Python 3.12

* Wed Mar 29 2023 Karolina Surma <ksurma@redhat.com> - 4.1-1
- Update to 4.1
Resolves rhbz#2178260

* Mon Feb 27 2023 Karolina Surma <ksurma@redhat.com> - 3.0.0-1
- Initial package

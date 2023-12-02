Name:       lxd-ui
Version:    0.5
Release:    0.1%{?dist}
Summary:    A browser interface for LXD
License:    GPLv3
URL:        https://github.com/canonical/lxd-ui

# Source0 contains the tagged upstream sources
Source0:    https://github.com/canonical/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

# Source1 contains the bundled Node.js dependencies
# Note: In case there were no changes to this tarball, the NVR of this tarball
# lags behind the NVR of this package.
Source1:    lxd-ui-vendor-%{version}-1.tar.xz

BuildArch:  noarch

Requires:         lxd
BuildRequires:    nodejs
BuildRequires:    nodejs-npm
BuildRequires:    yarnpkg

%description
LXD-UI is a browser frontend for LXD. It enables easy and accessible container
and virtual machine management. Targets small and large scale private clouds.

%prep
%setup -q -T -D -b 0
%setup -q -T -D -b 1
yarn --offline config set cache-folder $(pwd)/.cache/yarn/
yarn --offline install --frozen-lockfile

%build
yarn --offline run build

%install
install -d %{buildroot}%{_datadir}/%{name}
cp -a build/ui %{buildroot}%{_datadir}/%{name}

%files
%license LICENSE
%doc README.md ARCHITECTURE.MD
%{_datadir}/%{name}

%changelog
* Sat Dec 02 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.5-0.1
- Update to 0.5.

* Thu Nov 16 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.3-0.3
- Use vendored cache instead of node_modules to fix non-x86 builds

* Sun Nov 12 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.3-0.2
- Fix typo in doc file reference

* Sun Nov 12 2023 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.3-0.1
- Initial package


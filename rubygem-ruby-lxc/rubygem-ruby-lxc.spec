%global gem_name ruby-lxc

Name:       rubygem-%{gem_name}
Version:    1.2.3
Release:    0.3%{?dist}
Summary:    Ruby bindings for liblxc
License:    LGPLv2+
URL:        https://github.com/lxc/ruby-lxc
Source0:    https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1:    README.md
Source2:    LICENSE
Patch0:     ruby-lxc-1.2.3-Fix-compatibility-with-liblxc-4.0.4.patch

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: ruby-devel
# Compiler is required for build of gem binary extension.
# https://fedoraproject.org/wiki/Packaging:C_and_C++#BuildRequires_and_Requires
BuildRequires: gcc
BuildRequires: lxc-devel

%description
Ruby-LXC is a Ruby binding for the liblxc library, allowing
Ruby scripts to create and manage Linux containers.


%package doc
Summary:    Documentation for %{name}
Requires:   %{name} = %{version}-%{release}
BuildArch:  noarch

%description doc
Documentation for %{name}

%prep
%setup -q -n %{gem_name}-%{version}
%patch0 -p1

%build
# Create the gem as gem install only works on a gem file
gem build ../%{gem_name}-%{version}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

# If there are C extensions, copy them to the extdir.
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,lxc} %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/

cp %{SOURCE1} .
cp %{SOURCE2} .

%files
%doc LICENSE
%dir %{gem_instdir}
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc README.md


%changelog
* Sun Nov 15 2020 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.2.3-0.3
- Fix build against lxc-4.0.4

* Wed Aug 14 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.2.3-0.2
- Add LICENSE file
- Fix error with module lookup on Fedora

* Wed Aug 14 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.2.3-0.1
- Update to 1.2.3
- Fix build failure on CentOS 7

* Fri Jun 08 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.2.2-0.1
- Initial package

# Copied from:
# https://download.copr.fedorainfracloud.org/results/ktdreyer/python-pgpy/fedora-42-x86_64/05965353-python-pgpy/python-pgpy.spec

%global pypi_name pgpy13
%global package_name pgpy
%global pypi_version 0.6.1rc1

Name:           python-%{package_name}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        Pretty Good Privacy for Python

License:        BSD-3-Clause
URL:            https://github.com/memory/PGPy
Source0:        https://files.pythonhosted.org/packages/27/4a/49f87efd9c320d25b2edda4d9bda520607fbc12338cd1030468d830f29bb/pgpy13-0.6.1rc1.tar.gz
BuildArch:      noarch

%if 0%{?fedora}%{?rhel}
BuildRequires:  python3-devel
BuildRequires:  python3dist(cryptography)
BuildRequires:  python3dist(pyasn1)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(pytest)
%elif 0%{?suse_version}%{?sle_version}
BuildRequires:  python313-devel
BuildRequires:  python313-cryptography
BuildRequires:  python313-pyasn1
BuildRequires:  python313-setuptools
BuildRequires:  python313-pytest
%else
%{error: unsupported distribution}
%endif

%description
PGPy: Pretty Good Privacy for Python :target:

%package -n     python3-%{package_name}
Summary:        %{summary}

%if 0%{?fedora}%{?rhel}
%{?python_provide:%python_provide python3-%{package_name}}
%elif 0%{?suse_version}%{?sle_version}
%{?python_provide:%python_provide python313-%{package_name}}
%else
%{error: unsupported distribution}
%endif

%description -n python3-%{package_name}
PGPy: Pretty Good Privacy for Python :target:

%prep
%autosetup -p1 -n pgpy13-%{pypi_version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{package_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/*

%changelog
* Sat Jun 28 2025 Aditya Garg <gargaditya08@live.com> - 0.6.1rc1-1
- Initial package.

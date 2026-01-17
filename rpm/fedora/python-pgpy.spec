%global pypi_name pgpy13
%global package_name pgpy
%global pypi_version 0.6.1rc1

Name:           python-%{package_name}
Version:        %{pypi_version}
Release:        3%{?dist}
Summary:        Pretty Good Privacy for Python

License:        BSD-3-Clause
URL:            https://github.com/memory/PGPy
Source:         %{pypi_source %{pypi_name}}

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%py_provides %{package_name}

%global _description %{expand:\
PGPy is a Python library for implementing Pretty Good Privacy into Python programs,
conforming to the OpenPGP specification per RFC 4880.}

%description %_description

%package -n python3-%{package_name}
Summary:        %{summary}

%description -n python3-%{package_name} %_description

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{package_name}

%check
%pyproject_check_import
# Currently disabled because legacy encrpytion is disabled
# %pytest

%files -n python3-%{package_name} -f %{pyproject_files}


%changelog
* Sat Aug 23 2025 Aditya Garg <gargaditya08@live.com> - 0.6.1rc1-3
- Fix missing dependencies

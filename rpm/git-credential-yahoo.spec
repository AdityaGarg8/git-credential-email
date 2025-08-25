Name:           git-credential-yahoo
Version:        5.3.6
Release:        1%{?dist}
Summary:        Git credential helper for Yahoo accounts

License:        Apache-2.0
URL:            https://github.com/AdityaGarg8/git-credential-email
Source0:        %{url}/archive/refs/tags/v5.3.6.tar.gz

BuildArch:      noarch
Requires:       git-email

%if 0%{?fedora}%{?rhel}
Requires:       python-keyring
Requires:       python-requests
Suggests:       python-pyqt6-webengine
%elif 0%{?suse_version}%{?sle_version}
Requires:       python3-keyring
Requires:       python3-requests
Suggests:       python3-PyQt6-WebEngine
%else
%{error: unsupported distribution}
%endif

%description
Git credential helper for Yahoo accounts.

%prep
%autosetup -n git-credential-email-5.3.6

%build

%install
install -D -m0755 git-credential-yahoo %{buildroot}%{_bindir}/git-credential-yahoo

%files
%license LICENSE-APACHE NOTICE
%doc README.md
%{_bindir}/git-credential-yahoo

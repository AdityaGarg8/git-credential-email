Name:           git-credential-yahoo
Version:        5.3
Release:        1%{?dist}
Summary:        Git credential helper for Yahoo accounts

License:        Apache-2.0
URL:            https://github.com/AdityaGarg8/git-credential-email
Source0:        %{url}/archive/refs/tags/v5.3.tar.gz

BuildArch:      noarch
Requires:       git-email
Requires:       python-keyring
Requires:       python-requests
Suggests:       python-pyqt6-webengine

%description
Git credential helper for Yahoo accounts.

%prep
%autosetup -n git-credential-email-5.3

%build

%install
install -D -m0755 git-credential-yahoo %{buildroot}%{_bindir}/git-credential-yahoo

%files
%license LICENSE-APACHE NOTICE
%doc README.md
%{_bindir}/git-credential-yahoo

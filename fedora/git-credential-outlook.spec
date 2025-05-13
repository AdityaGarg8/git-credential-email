Name:           git-credential-outlook
Version:        4.0
Release:        1%{?dist}
Summary:        Git credential helper for Microsoft Outlook accounts.

License:        Apache-2.0
URL:            https://github.com/AdityaGarg8/git-credential-email
Source0:        %{url}/archive/refs/tags/v4.0.tar.gz

BuildArch:      noarch
Requires:       git-email
Requires:       python-msal
Requires:       python-keyring
Requires:       python-pyqt6
Requires:       python-pyqt6-webengine

%description
Git credential helper for Microsoft Outlook accounts.

%prep
%autosetup -n git-credential-email-4.0

%build

%install
install -D -m0755 git-credential-outlook %{buildroot}%{_bindir}/git-credential-outlook

%files
%license LICENSE
%doc README.md
%{_bindir}/git-credential-outlook

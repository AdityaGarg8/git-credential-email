Name:           git-credential-outlook
Version:        5.1
Release:        1%{?dist}
Summary:        Git credential helper for Microsoft Outlook accounts

License:        Apache-2.0
URL:            https://github.com/AdityaGarg8/git-credential-email
Source0:        %{url}/archive/refs/tags/v5.1.tar.gz

BuildArch:      noarch
Requires:       git-email
Requires:       python-keyring
Suggests:       python-pyqt6-webengine

%description
Git credential helper for Microsoft Outlook accounts.

%prep
%autosetup -n git-credential-email-5.1

%build

%install
install -D -m0755 git-credential-outlook %{buildroot}%{_bindir}/git-credential-outlook

%files
%license LICENSE-APACHE NOTICE
%doc README.md
%{_bindir}/git-credential-outlook

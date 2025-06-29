Name:           git-msgraph
Version:        5.1.1
Release:        1%{?dist}
Summary:        Git helper to use Microsoft Graph API instead of SMTP to send emails

License:        Apache-2.0
URL:            https://github.com/AdityaGarg8/git-credential-email
Source0:        %{url}/archive/refs/tags/v5.1.1.tar.gz

BuildArch:      noarch
Requires:       git-email
Requires:       python-keyring
Suggests:       python-pyqt6-webengine

%description
Git helper to use Microsoft Graph API instead of SMTP to send emails

%prep
%autosetup -n git-credential-email-5.1.1

%build

%install
install -D -m0755 git-msgraph %{buildroot}%{_bindir}/git-msgraph

%files
%license LICENSE-APACHE NOTICE
%doc README.md
%{_bindir}/git-msgraph

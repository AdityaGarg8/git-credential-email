Name:           git-msgraph
Version:        5.0
Release:        1%{?dist}
Summary:        Git helper to use Microsoft Graph API instead of SMTP to send emails

License:        Apache-2.0
URL:            https://github.com/AdityaGarg8/git-credential-email
Source0:        %{url}/archive/refs/tags/v5.0.tar.gz

BuildArch:      noarch
Requires:       git-email
Requires:       python-keyring

%description
Git helper to use Microsoft Graph API instead of SMTP to send emails

%prep
%autosetup -n git-credential-email-5.0

%build

%install
install -D -m0755 git-msgraph %{buildroot}%{_bindir}/git-msgraph

%files
%license LICENSE NOTICE
%doc README.md
%{_bindir}/git-msgraph

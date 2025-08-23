Name:           git-msgraph
Version:        5.3.2
Release:        1%{?dist}
Summary:        Git helper to use Microsoft Graph API instead of SMTP to send emails

License:        Apache-2.0
URL:            https://github.com/AdityaGarg8/git-credential-email
Source0:        %{url}/archive/refs/tags/v5.3.2.tar.gz

BuildArch:      noarch
Requires:       git-email

%if 0%{?fedora}%{?rhel}
Requires:       python-keyring
Requires:       python-requests
Suggests:       python-pyqt6-webengine
%elif 0%{?suse_version}%{?sle_version}
Requires:       python313-keyring
Requires:       python313-requests
Suggests:       python313-PyQt6-WebEngine
%else
%{error: unsupported distribution}
%endif

%description
Git helper to use Microsoft Graph API instead of SMTP to send emails

%prep
%autosetup -n git-credential-email-5.3.2

%build

%install
install -D -m0755 git-msgraph %{buildroot}%{_bindir}/git-msgraph

%files
%license LICENSE-APACHE NOTICE
%doc README.md
%{_bindir}/git-msgraph

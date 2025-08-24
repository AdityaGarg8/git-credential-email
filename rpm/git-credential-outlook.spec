Name:           git-credential-outlook
Version:        5.3.4
Release:        1%{?dist}
Summary:        Git credential helper for Microsoft Outlook accounts

License:        Apache-2.0
URL:            https://github.com/AdityaGarg8/git-credential-email
Source0:        %{url}/archive/refs/tags/v5.3.4.tar.gz

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
Git credential helper for Microsoft Outlook accounts.

%prep
%autosetup -n git-credential-email-5.3.4

%build

%install
install -D -m0755 git-credential-outlook %{buildroot}%{_bindir}/git-credential-outlook

%files
%license LICENSE-APACHE NOTICE
%doc README.md
%{_bindir}/git-credential-outlook

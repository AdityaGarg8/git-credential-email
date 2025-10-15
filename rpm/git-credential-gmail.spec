Name:           git-credential-gmail
Version:        5.5.2
Release:        1%{?dist}
Summary:        Git credential helper for Gmail accounts

License:        Apache-2.0
URL:            https://github.com/AdityaGarg8/git-credential-email
Source0:        %{url}/archive/refs/tags/v5.5.2.tar.gz

BuildArch:      noarch
Requires:       git-email

%if 0%{?fedora}%{?rhel}
Requires:       python-keyring
Requires:       python-requests
Recommends:     python-qrcode
Suggests:       python-pyqt6-webengine
%elif 0%{?suse_version}%{?sle_version}
Requires:       python3-keyring
Requires:       python3-requests
Recommends:     python3-qrcode
Suggests:       python3-PyQt6-WebEngine
%else
%{error: unsupported distribution}
%endif

%description
Git credential helper for Gmail accounts.

%prep
%autosetup -n git-credential-email-5.5.2

%build

%install
install -D -m0755 git-credential-gmail %{buildroot}%{_bindir}/git-credential-gmail

%files
%license LICENSE-APACHE NOTICE
%doc README.md
%{_bindir}/git-credential-gmail

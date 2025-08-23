Name:           git-protonmail
Version:        5.3.3
Release:        1%{?dist}
Summary:        Git helper to use ProtonMail API to send emails

License:        GPL-3.0-only
URL:            https://github.com/AdityaGarg8/git-credential-email
Source0:        %{url}/archive/refs/tags/v5.3.3.tar.gz

BuildArch:      noarch
Requires:       git-email

%if 0%{?fedora}%{?rhel}
Requires:       python-bcrypt
Requires:       python-cryptography
Requires:       python-keyring
Requires:       python-pgpy
Requires:       python-requests
Requires:       python-requests-toolbelt
Requires:       python-typing-extensions
Recommends:     python-pyqt6-webengine
Suggests:       python-opencv
Suggests:       python-numpy
%elif 0%{?suse_version}%{?sle_version}
Requires:       python3-bcrypt
Requires:       python3-cryptography
Requires:       python3-keyring
Requires:       python3-pgpy
Requires:       python3-requests
Requires:       python3-requests-toolbelt
Requires:       python3-typing-extensions
Recommends:     python3-PyQt6-WebEngine
Suggests:       python3-opencv
Suggests:       python3-numpy
%else
%{error: unsupported distribution}
%endif

%description
Git helper to use ProtonMail API to send emails

%prep
%autosetup -n git-credential-email-5.3.3

%build

%install
install -D -m0755 git-protonmail %{buildroot}%{_bindir}/git-protonmail

%files
%license LICENSE-GPL3
%doc README.md
%{_bindir}/git-protonmail

Name:           git-protonmail
Version:        5.1.4
Release:        1%{?dist}
Summary:        Git helper to use ProtonMail API to send emails

License:        GPL-3.0-only
URL:            https://github.com/AdityaGarg8/git-credential-email
Source0:        %{url}/archive/refs/tags/v5.1.4.tar.gz

BuildArch:      noarch
Requires:       git-email
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

%description
Git helper to use ProtonMail API to send emails

%prep
%autosetup -n git-credential-email-5.1.4

%build

%install
install -D -m0755 git-protonmail %{buildroot}%{_bindir}/git-protonmail

%files
%license LICENSE-GPL3
%doc README.md
%{_bindir}/git-protonmail

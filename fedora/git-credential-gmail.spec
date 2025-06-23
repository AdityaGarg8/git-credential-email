Name:           git-credential-gmail
Version:        4.7.1
Release:        1%{?dist}
Summary:        Git credential helper for Gmail accounts.

License:        Apache-2.0
URL:            https://github.com/AdityaGarg8/git-credential-email
Source0:        %{url}/archive/refs/tags/v4.7.1.tar.gz

BuildArch:      noarch
Requires:       git-email
Requires:       python-keyring

%description
Git credential helper for Gmail accounts.

%prep
%autosetup -n git-credential-email-4.7.1

%build

%install
install -D -m0755 git-credential-gmail %{buildroot}%{_bindir}/git-credential-gmail

%files
%license LICENSE NOTICE
%doc README.md
%{_bindir}/git-credential-gmail

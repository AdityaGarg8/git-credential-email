Name:           git-credential-yahoo
Version:        5.0
Release:        1%{?dist}
Summary:        Git credential helper for Yahoo accounts

License:        Apache-2.0
URL:            https://github.com/AdityaGarg8/git-credential-email
Source0:        %{url}/archive/refs/tags/v5.0.tar.gz

BuildArch:      noarch
Requires:       git-email
Requires:       python-keyring

%description
Git credential helper for Yahoo accounts.

%prep
%autosetup -n git-credential-email-5.0

%build

%install
install -D -m0755 git-credential-yahoo %{buildroot}%{_bindir}/git-credential-yahoo

%files
%license LICENSE NOTICE
%doc README.md
%{_bindir}/git-credential-yahoo

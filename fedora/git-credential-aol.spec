Name:           git-credential-aol
Version:        5.0
Release:        1%{?dist}
Summary:        Git credential helper for AOL accounts

License:        Apache-2.0
URL:            https://github.com/AdityaGarg8/git-credential-email
Source0:        %{url}/archive/refs/tags/v5.0.tar.gz

BuildArch:      noarch
Requires:       git-email
Requires:       python-keyring

%description
Git credential helper for AOL accounts.

%prep
%autosetup -n git-credential-email-5.0

%build

%install
install -D -m0755 git-credential-aol %{buildroot}%{_bindir}/git-credential-aol

%files
%license LICENSE NOTICE
%doc README.md
%{_bindir}/git-credential-aol

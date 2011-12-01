Name:           perl-Mail-DKIM
Version:        0.37
Release:        2%{?dist}
Summary:        Sign and verify Internet mail with DKIM/DomainKey signatures

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://dkimproxy.sourceforge.net/
Source0:        http://search.cpan.org/CPAN/authors/id/J/JA/JASLONG/Mail-DKIM-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::Simple) perl(Net::DNS) perl(Mail::Address)
BuildRequires:  perl(Crypt::OpenSSL::RSA) perl(Digest::SHA)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module implements the various components of the DKIM and DomainKeys
message-signing and verifying standards for Internet mail. It currently
tries to implement RFC4871 (for DKIM) and RFC4870 (DomainKeys).

It is required if you wish to enable DKIM checking in SpamAssassin via the
Mail::SpamAssassin::Plugin::DKIM plugin.

%prep
%setup -q -n Mail-DKIM-%{version}
# Make the example scripts non-executable
%{__chmod} -x scripts/*.pl

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
# Conditionally disable tests that require DNS lookups
%{?!_with_network_tests: rm t/policy.t t/public_key.t }
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog Changes HACKING.DKIM README TODO scripts/*.pl
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.37-2
- rebuild against perl 5.10.1

* Wed Sep 9 2009 Warren Togami <wtogami@redhat.com> - 0.37-1
- 0.37

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Kyle VanderBeek <kylev@kylev.com> - 0.33-2
- Revise network-driven testing exclusions.

* Wed Jun 10 2009 Kyle VanderBeek <kylev@kylev.com> - 0.33-1
- Update to 0.33

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jun 23 2008 Kyle VanderBeek <kylev@kylev.com> - 0.32-3
- Disable some tests that require network access and fail inside koji

* Wed Jun 18 2008 Kyle VanderBeek <kylev@kylev.com> - 0.32-2
- Make example scripts non-executable to avoid dep detection bloat.

* Tue Jun 17 2008 Kyle VanderBeek <kylev@kylev.com> - 0.32-1
- Initial version.


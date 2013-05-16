%define	major 1
%define libname	%mklibname skey %{major}

Summary:	S/Key suite of programs
Name:		skey
Version:	1.1.5
Release:	11
License:	BSD
Group:		System/Libraries
Source0:	%{name}-%{version}.tar.bz2
Patch0:		skey-1.1.5-gentoo.diff
Patch1:		skey-login_name_max.diff
Patch2:		skey-1.1.5-fPIC.patch
Patch3:		skey-1.1.5-bind-now.patch
Patch4:		skey-1.1.5-otp.diff
# This url is wrong, but it is impossible to find it else where...
#URL: ftp://thumper.bellcore.com/pub/nmh/
BuildRequires:	libcrack-devel
# if not using BuildConflicts here the binaries could link against installed libs
BuildConflicts:	skey-devel

%description
This is an S/Key implementation ported from OpenBSD.

S/Key provides One Time Password functionality, and can be used to
increase system security.

%package -n	%{libname}
Summary:	Shared S/Key library
Group:          System/Libraries

%description -n	%{libname}
This is an S/Key implementation ported from OpenBSD.

S/Key provides One Time Password functionality, and can be used to
increase system security.

%package -n	%{libname}-devel
Summary:	Header files for the S/Key library
Group:		Development/C
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{version}
Provides:	lib%{name}-devel = %{version}
Requires:	%{libname} = %{version}

%description -n	%{libname}-devel
This is an S/Key implementation ported from OpenBSD.

S/Key provides One Time Password functionality, and can be used to
increase system security.

This package contains development files for the S/Key library.

%package -n	%{libname}-static-devel
Summary:	Static S/Key library
Group:		Development/C
Obsoletes:	%{name}-static-devel
Provides:	%{name}-static-devel = %{version}
Provides:	lib%{name}-static-devel = %{version}
Requires:	%{libname}-devel = %{version}
Requires:	%{libname} = %{version}

%description -n	%{libname}-static-devel
This is an S/Key implementation ported from OpenBSD.

S/Key provides One Time Password functionality, and can be used to
increase system security.

This package contains the static S/Key library.

%prep

%setup -q
%patch0 -p1 -b .gentoo
%patch1 -p1 -b .skey-login_name_max
%patch2 -p0 -b .skey-fPIC
%patch3 -p0 -b .skey-bind-now
%patch4 -p1 -b .skey-otp

# fix one small thing...
perl -pi -e "s|/etc/skeykeys|%{_sysconfdir}/%{name}/skeykeys|g" skeyprune.pl

%build
export SENDMAIL="%{_sbindir}/sendmail"
export CFLAGS="$RPM_OPT_FLAGS -DSKEY_HASH_DEFAULT=1"

%configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --libdir=%{_libdir}

make CC=%{__cc}

%install
%makeinstall_std

install -d %{buildroot}%{_sbindir}

mv %{buildroot}%{_bindir}/skeyprune %{buildroot}%{_sbindir}/

install -m0755 skeyaudit.sh %{buildroot}%{_bindir}/skeyaudit

ln -snf skey %{buildroot}%{_bindir}/otp-md4
ln -snf skey %{buildroot}%{_bindir}/otp-sha1
ln -snf skey %{buildroot}%{_bindir}/otp-md5

# make install is borked...
ln -snf libskey.so.%{version} %{buildroot}%{_libdir}/libskey.so.1.1
ln -snf libskey.so.%{version} %{buildroot}%{_libdir}/libskey.so.1
ln -snf libskey.so.%{version} %{buildroot}%{_libdir}/libskey.so

chmod 755 %{buildroot}%{_bindir}/*
chmod 755 %{buildroot}%{_libdir}/libskey.so*
chmod 644 %{buildroot}%{_libdir}/libskey.a

# cleanup
rm -f %{buildroot}%{_bindir}/libskey.a

%files
%doc CHANGES INSTALL README
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/%{name}/skeykeys
%attr(4755,root,root) %{_bindir}/skeyinit
%attr(4755,root,root) %{_bindir}/skeyinfo
%attr(4755,root,root) %{_bindir}/skeyaudit
%attr(0755,root,root) %{_bindir}/skey
%attr(0755,root,root) %{_bindir}/otp-md4
%attr(0755,root,root) %{_bindir}/otp-sha1
%attr(0755,root,root) %{_bindir}/otp-md5
%attr(0755,root,root) %{_sbindir}/skeyprune
%{_mandir}/*/*

%files -n %{libname}
%attr(0755,root,root) %{_libdir}/*.so.*

%files -n %{libname}-devel
%attr(0644,root,root) %{_includedir}/*
%attr(0755,root,root) %{_libdir}/*.so

%files -n %{libname}-static-devel
%attr(0644,root,root) %{_libdir}/libskey.a


%changelog
* Tue Sep 08 2009 Thierry Vignaud <tvignaud@mandriva.com> 1.1.5-10mdv2010.0
+ Revision: 433919
- rebuild

* Wed Jul 23 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.1.5-9mdv2009.0
+ Revision: 242691
- rebuild

* Tue Jul 22 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.5-8mdv2009.0
+ Revision: 240157
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Thierry Vignaud <tvignaud@mandriva.com>
    - fix no-buildroot-tag
    - kill re-definition of %%buildroot on Pixel's request

* Wed Jun 27 2007 Andreas Hasenack <andreas@mandriva.com> 1.1.5-7mdv2008.0
+ Revision: 45103
- rebuild with new rpm-mandriva-setup (-fstack-protector)


* Sun Mar 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1.1.5-6mdv2007.1
+ Revision: 141289
- fix deps

* Wed Mar 07 2007 Oden Eriksson <oeriksson@mandriva.com> 1.1.5-5mdv2007.1
+ Revision: 134499
- Import skey

* Wed Jun 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.5-5mdv2007.0
- rebuild

* Sun Nov 06 2005 Oden Eriksson <oeriksson@mandriva.com> 1.1.5-4mdk
- added a lot of gentoo changes

* Fri Oct 21 2005 Olivier Thauvin <nanardon@mandriva.org> 1.1.5-3mdk
- rebuild
- I can't find the project on the net :\


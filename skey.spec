%define	major 1
%define libname	%mklibname skey %{major}

Summary:	S/Key suite of programs
Name:		skey
Version:	1.1.5
Release:	%mkrel 6
License:	BSD
Group:		System/Libraries
Source:		%{name}-%{version}.tar.bz2
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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
export CFLAGS="%{optflags} -DSKEY_HASH_DEFAULT=1"

%configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --libdir=%{_libdir}

make

%install
rm -rf %{buildroot}

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

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
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
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%attr(0644,root,root) %{_includedir}/*
%attr(0755,root,root) %{_libdir}/*.so

%files -n %{libname}-static-devel
%defattr(-,root,root)
%attr(0644,root,root) %{_libdir}/libskey.a



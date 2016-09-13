# TODO
# - should c and c++ have separate -devel packages?

# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Binary-based efficient object serialization library
Name:		msgpack
Version:	1.4.1
Release:	1
License:	Boost
Group:		Libraries
Source0:	https://github.com/msgpack/msgpack-c/releases/download/cpp-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	fde8da1388d4f8daf21faee5536a53cf
URL:		http://msgpack.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pkgconfig
%if %{with tests}
BuildRequires:	gtest-devel
BuildRequires:	zlib-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MessagePack is a binary-based efficient object serialization library.
It enables to exchange structured objects between many languages like
JSON. But unlike JSON, it is very fast and small.

%package devel
Summary:	Libraries and header files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Libraries and header files for %{name}

%prep
%setup -q

%build
%{__aclocal}
%{__libtoolize}
%{__autoconf}
%{__autoheader}
%{__automake} --force-missing
%configure \
	--disable-static
%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmsgpackc.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NOTICE README README.md
%attr(755,root,root) %{_libdir}/libmsgpackc.so.*.*.*
%ghost %{_libdir}/libmsgpackc.so.2

%files devel
%defattr(644,root,root,755)
%{_includedir}/msgpack.h
%{_includedir}/msgpack.hpp
%{_includedir}/msgpack
%{_libdir}/libmsgpackc.so
%{_pkgconfigdir}/msgpack.pc

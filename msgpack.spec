# TODO
# - should c and c++ have separate -devel packages?

# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Binary-based efficient object serialization library
Name:		msgpack
Version:	3.3.0
Release:	1
License:	Boost
Group:		Libraries
Source0:	https://github.com/msgpack/msgpack-c/releases/download/cpp-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e676575d52caae974e579c3d5f0ba6a2
URL:		https://msgpack.org/
BuildRequires:	cmake >= 2.8.0
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
install -d build
cd build
%cmake \
	-DMSGPACK_CXX11=ON \
	..
%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

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
%{_libdir}/cmake/msgpack/msgpack*.cmake

#
# Conditional build:
%bcond_with	tests		# build without tests

Summary:	Binary-based efficient object serialization library
Summary(pl.UTF-8):	Biblioteka do wydajnej, binarnej serializacji obiektów
Name:		msgpack
Version:	3.3.0
Release:	2
License:	Boost v1.0
Group:		Libraries
#Source0Download: https://github.com/msgpack/msgpack-c/releases
Source0:	https://github.com/msgpack/msgpack-c/releases/download/cpp-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e676575d52caae974e579c3d5f0ba6a2
URL:		https://msgpack.org/
BuildRequires:	cmake >= 2.8.12
BuildRequires:	libstdc++-devel >= 6:4.7
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

%description -l pl.UTF-8
MessagePack to biblioteka do wydajnej, binarnej serializacji obiektów.
Pozwala wymieniać ustrukturyzowane obiekty między wieloma językami,
podobnie jak przy użyciu formatu JSON. Ale w przeciwieństwie do
JSON-a, ten format jest bardzo szybki i mały.

%package devel
Summary:	Header files for MessagePack library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki MessagePack
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for MessagePack library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki MessagePack.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	-DMSGPACK_CXX11=ON

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
%doc COPYING ChangeLog LICENSE_1_0.txt NOTICE README.md
%attr(755,root,root) %{_libdir}/libmsgpackc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmsgpackc.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmsgpackc.so
%{_includedir}/msgpack.h
%{_includedir}/msgpack.hpp
%{_includedir}/msgpack
%{_pkgconfigdir}/msgpack.pc
%{_libdir}/cmake/msgpack

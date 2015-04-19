#
# Conditional build:
%bcond_without	colorhug	# ColorHug support
%bcond_without	efi		# UEFI support
%bcond_without	static_libs	# static library
#
%ifnarch %{ix86} %{x8664} arm aarch64 ia64
%undefine	with_efi
%endif
Summary:	System daemon for installing device firmware
Summary(pl.UTF-8):	Demon systemowy do instalowania firmware'u urządzeń
Name:		fwupd
Version:	0.1.1
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz
# Source0-md5:	87819887a63bbf953e9ee4e3aa54359a
URL:		https://github.com/hughsie/fwupd
BuildRequires:	appstream-glib-devel >= 0.3.5
%{?with_colorhug:BuildRequires:	colord-devel >= 1.2.9}
BuildRequires:	docbook-utils
%{?with_efi:BuildRequires:	fwupdate-devel}
BuildRequires:	gcab-devel
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	glib2-devel >= 1:2.36.0
BuildRequires:	gobject-introspection-devel >= 0.9.8
BuildRequires:	intltool >= 0.35.0
%{?with_colorhug:BuildRequires:	libgusb-devel >= 0.2.2}
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.103
BuildRequires:	rpmbuild(macros) >= 1.644
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-glib-devel
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	appstream-glib >= 0.3.5
%{?with_colorhug:Requires:	colord-libs >= 1.2.9}
%{?with_colorhug:Requires:	libgusb >= 0.2.2}
Requires:	polkit >= 0.103
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
fwupd is a simple daemon to allow session software to update device
firmware on your local machine. It's designed for desktops, but this
project is probably quite interesting for phones, tablets and server
farms.

%description -l pl.UTF-8
fwupd to prosty demon pozwalający programom sesyjnym na aktualizację
firmware'u urządzeń na maszynie lokalnej. Jest zaprojektowany dla
komputerów osobistych, ale może być interesujący także dla telefonów,
tabletów i farm serwerów.

%package libs
Summary:	Library for fwupd device firmware installing daemon
Summary(pl.UTF-8):	Biblioteka dla demona fwupd instalującego aktualizacje firmware'u
Group:		Libraries
Requires:	glib2-devel >= 1:2.36.0

%description libs
Library for fwupd device firmware installing daemon.

%description libs -l pl.UTF-8
Biblioteka dla demona fwupd instalującego aktualizacje firmware'u.

%package devel
Summary:	Header files for fwupd library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki fwupd
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.36.0

%description devel
Header files for fwupd library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki fwupd.

%package static
Summary:	Static fwupd library
Summary(pl.UTF-8):	Statyczna biblioteka fwupd
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static fwupd library.

%description static -l pl.UTF-8
Statyczna biblioteka fwupd.

%prep
%setup -q

%build
%configure \
	%{!?with_static_libs:--disable-static} \
	%{!?with_efi:--disable-uefi} \
	--with-systemdsystemunitdir=%{systemdunitdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libfwupd.la

%{__mv} $RPM_BUILD_ROOT%{_localedir}/{hi_IN,hi}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS README.md
%attr(755,root,root) %{_bindir}/fwupdmgr
%attr(755,root,root) %{_libexecdir}/fwupd
%{systemdunitdir}/fwupd.service
/etc/dbus-1/system.d/org.freedesktop.fwupd.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.fwupd.service
%{_datadir}/polkit-1/actions/org.freedesktop.fwupd.policy
%{_datadir}/polkit-1/rules.d/org.freedesktop.fwupd.rules
%dir /var/lib/fwupd
%{_mandir}/man1/fwupdmgr.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfwupd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfwupd.so.1
%{_libdir}/girepository-1.0/Fwupd-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfwupd.so
%{_includedir}/fwupd-1
%{_datadir}/gir-1.0/Fwupd-1.0.gir
%{_datadir}/dbus-1/interfaces/org.freedesktop.fwupd.xml
%{_pkgconfigdir}/fwupd.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfwupd.a
%endif

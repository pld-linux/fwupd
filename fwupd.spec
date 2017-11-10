# TODO: polkit >= 0.114 when available
#
# Conditional build:
%bcond_without	colorhug	# ColorHug support
%bcond_without	efi		# UEFI (and dell) support
%bcond_without	thunderbolt	# Thunderbolt support

%ifnarch %{ix86} %{x8664} x32 %{arm} aarch64 ia64
%undefine	with_efi
%endif
%if %{without efi}
%undefine	with_thunderbolt
%endif
Summary:	System daemon for installing device firmware
Summary(pl.UTF-8):	Demon systemowy do instalowania firmware'u urządzeń
Name:		fwupd
Version:	1.0.1
Release:	1
License:	LGPL v2.1+
Group:		Applications/System
Source0:	https://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz
# Source0-md5:	248c26e0daac6f4d193f68fea3a14dad
URL:		https://github.com/hughsie/fwupd
BuildRequires:	appstream-glib-devel >= 0.5.10
%{?with_colorhug:BuildRequires:	colord-devel >= 1.2.12}
BuildRequires:	docbook-utils
BuildRequires:	docbook-dtd41-sgml
%{?with_efi:BuildRequires:	efivar-devel}
# pkgconfig(libelf); can be also libelf-devel
BuildRequires:	elfutils-devel >= 0.166
%{?with_efi:BuildRequires:	fwupdate-devel >= 5}
BuildRequires:	gcab-devel
BuildRequires:	gettext-tools >= 0.19.7
BuildRequires:	glib2-devel >= 1:2.45.8
BuildRequires:	gobject-introspection-devel >= 0.9.8
BuildRequires:	gpgme-devel
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libarchive-devel
BuildRequires:	libgpg-error-devel
BuildRequires:	libgusb-devel >= 0.2.9
# for dell (which depends on fwupdate too)
%{?with_efi:BuildRequires:	libsmbios-devel >= 2.3.0}
BuildRequires:	libsoup-devel >= 2.52
# pkgconfig(libtbtfwu) >= 1
%{?with_thunderbolt:BuildRequires:	libtbtfwu-devel >= 0-0.2017.01.19}
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 0.37.0
BuildRequires:	ninja >= 1.6
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.103
BuildRequires:	python3-pillow
BuildRequires:	python3-pycairo
BuildRequires:	rpmbuild(macros) >= 1.726
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	systemd-units
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	udev-glib-devel
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	appstream-glib >= 0.5.10
%{?with_colorhug:Requires:	colord-libs >= 1.2.12}
%{?with_efi:Requires:	fwupdate-libs >= 5}
Requires:	libgusb >= 0.2.9
Requires:	libsoup >= 2.52
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
Summary:	Libraries for fwupd device firmware installing daemon
Summary(pl.UTF-8):	Biblioteki dla demona fwupd instalującego aktualizacje firmware'u
Group:		Libraries
Requires:	glib2-devel >= 1:2.45.8

%description libs
Libraries for fwupd device firmware installing daemon.

%description libs -l pl.UTF-8
Biblioteki dla demona fwupd instalującego aktualizacje firmware'u.

%package devel
Summary:	Header files for fwupd libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek fwupd
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.45.8
Obsoletes:	fwupd-static

%description devel
Header files for fwupd libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek fwupd.

%package apidocs
Summary:	API documentation for fwupd libraries
Summary(pl.UTF-8):	Dokumentacja API do bibliotek fwupd
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for fwupd libraries.

%description apidocs -l pl.UTF-8
Dokumentacja API do bibliotek fwupd.

%prep
%setup -q

%build
%meson build \
	-Denable-tests=false \
	%{!?with_thunderbolt:-Denable-thunderbolt=false} \
	%{!?with_efi:-Denable-uefi=false} \
	%{!?with_efi:-Denable-dell=false}

%meson_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install -C build

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS README.md
%attr(755,root,root) %{_bindir}/dfu-tool
%attr(755,root,root) %{_bindir}/fwupdmgr
%attr(755,root,root) %{_libexecdir}/fwupd
%dir %{_libdir}/fwupd-plugins-3
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_altos.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_amt.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_colorhug.so
%if %{with efi}
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_dell.so
%endif
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_dfu.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_ebitdo.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_raspberrypi.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_steelseries.so
%if %{with efi}
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_synapticsmst.so
%endif
%if %{with thunderbolt}
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_thunderbolt.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_thunderbolt_power.so
%endif
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_udev.so
%if %{with efi}
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_uefi.so
%endif
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_unifying.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_upower.so
%dir %{_sysconfdir}/fwupd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/daemon.conf
%dir %{_sysconfdir}/fwupd/remotes.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/fwupd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/lvfs-testing.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/lvfs.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/vendor.conf
%dir /etc/pki/fwupd
/etc/pki/fwupd/GPG-KEY-Hughski-Limited
/etc/pki/fwupd/GPG-KEY-Linux-Vendor-Firmware-Service
/etc/pki/fwupd/LVFS-CA.pem
%dir /etc/pki/fwupd-metadata
/etc/pki/fwupd-metadata/GPG-KEY-Linux-Vendor-Firmware-Service
/etc/pki/fwupd-metadata/LVFS-CA.pem
%{systemdunitdir}/fwupd.service
%{systemdunitdir}/fwupd-offline-update.service
%{systemdunitdir}/system-update.target.wants/fwupd-offline-update.service
/lib/udev/rules.d/90-fwupd-devices.rules
/etc/dbus-1/system.d/org.freedesktop.fwupd.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.fwupd.service
%dir %{_datadir}/fwupd
%attr(755,root,root) %{_datadir}/fwupd/firmware-packager
%dir %{_datadir}/fwupd/quirks.d
%{_datadir}/fwupd/quirks.d/dell.quirk
%{_datadir}/fwupd/quirks.d/dfu.quirk
%dir %{_datadir}/fwupd/remotes.d
%{_datadir}/fwupd/remotes.d/fwupd
%{_datadir}/fwupd/remotes.d/vendor
%{_datadir}/metainfo/org.freedesktop.fwupd.metainfo.xml
%{_datadir}/polkit-1/actions/org.freedesktop.fwupd.policy
%{_datadir}/polkit-1/rules.d/org.freedesktop.fwupd.rules
%dir /var/lib/fwupd
%dir /var/lib/fwupd/builder
/var/lib/fwupd/builder/README.md
%{_mandir}/man1/dfu-tool.1*
%{_mandir}/man1/fwupdmgr.1*

%files libs
%defattr(644,root,root,755)
%{_libdir}/girepository-1.0/Fwupd-2.0.typelib
%attr(755,root,root) %{_libdir}/libfwupd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfwupd.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfwupd.so
%{_includedir}/fwupd-1
%{_datadir}/gir-1.0/Fwupd-2.0.gir
%{_datadir}/dbus-1/interfaces/org.freedesktop.fwupd.xml
%{_pkgconfigdir}/fwupd.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libfwupd

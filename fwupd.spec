#
# Conditional build:
%bcond_without	colorhug	# ColorHug support
%bcond_without	efi		# UEFI (and dell, redfish) support
%bcond_without	thunderbolt	# Thunderbolt support

%ifnarch %{ix86} %{x8664} x32 %{arm} aarch64
%undefine	with_efi
%endif
Summary:	System daemon for installing device firmware
Summary(pl.UTF-8):	Demon systemowy do instalowania firmware'u urządzeń
Name:		fwupd
Version:	1.1.3
Release:	1
License:	LGPL v2.1+
Group:		Applications/System
Source0:	https://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz
# Source0-md5:	3f76eadf496d21b547d46299f925ecf3
Patch0:		%{name}-bashcomp.patch
URL:		https://github.com/hughsie/fwupd
BuildRequires:	appstream-glib-devel >= 0.7.4
%{?with_cairo:BuildRequires:	cairo-devel}
%{?with_colorhug:BuildRequires:	colord-devel >= 1.2.12}
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils
%{?with_efi:BuildRequires:	efivar-devel >= 33}
# pkgconfig(libelf); can be also libelf-devel
BuildRequires:	elfutils-devel >= 0.166
%{?with_fontconfig:BuildRequires:	fontconfig-devel}
%{?with_fontconfig:BuildRequires:	freetype-devel >= 2}
%{?with_efi:BuildRequires:	fwupdate-devel >= 5}
BuildRequires:	gcab-devel >= 1.0
# C99
BuildRequires:	gcc >= 5:3.2
%ifarch x32
BuildRequires:	gcc-multilib-64 >= 5:3.2
%endif
BuildRequires:	gettext-tools >= 0.19.7
BuildRequires:	glib2-devel >= 1:2.55.0
%{?with_efi:BuildRequires:	gnu-efi}
BuildRequires:	gnutls-devel >= 3.4.4.1
BuildRequires:	gobject-introspection-devel >= 0.9.8
BuildRequires:	gpgme-devel
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	intltool >= 0.35.0
BuildRequires:	json-glib-devel >= 1.1.1
BuildRequires:	libarchive-devel
BuildRequires:	libgpg-error-devel
BuildRequires:	libgudev-devel >= 232
BuildRequires:	libgusb-devel >= 0.2.9
# for dell (which depends on fwupdate too)
%{?with_efi:BuildRequires:	libsmbios-devel >= 2.4.0}
BuildRequires:	libsoup-devel >= 2.52
BuildRequires:	libuuid-devel
BuildRequires:	libxslt-progs
# for <linux/nvme_ioctl.h>
BuildRequires:	linux-libc-headers >= 7:4.4
BuildRequires:	meson >= 0.43.0
BuildRequires:	ninja >= 1.6
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.114
BuildRequires:	python3-pillow
BuildRequires:	python3-pycairo
BuildRequires:	rpmbuild(macros) >= 1.726
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	systemd-units >= 1:211
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
%{?with_thunderbolt:BuildRequires:	umockdev-devel}
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	appstream-glib >= 0.7.4
%{?with_colorhug:Requires:	colord-libs >= 1.2.12}
%{?with_efi:Requires:	fwupdate-libs >= 5}
Requires:	gcab >= 1.0
Requires:	gnutls-libs >= 3.4.4.1
Requires:	libgudev >= 232
Requires:	libgusb >= 0.2.9
%{?with_efi:Requires:	libsmbios >= 2.4.0}
Requires:	libsoup >= 2.52
Requires:	polkit >= 0.114
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

%package -n bash-completion-fwupd
Summary:	Bash completion for fwupd commands
Summary(pl.UTF-8):	Bashowe dopełnianie składni poleceń fwupd
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0

%description -n bash-completion-fwupd
Bash completion for fwupd commands.

%description -n bash-completion-fwupd -l pl.UTF-8
Bashowe dopełnianie składni poleceń fwupd.

%package libs
Summary:	Libraries for fwupd device firmware installing daemon
Summary(pl.UTF-8):	Biblioteki dla demona fwupd instalującego aktualizacje firmware'u
Group:		Libraries
Requires:	glib2-devel >= 1:2.55.0
Requires:	json-glib >= 1.1.1

%description libs
Libraries for fwupd device firmware installing daemon.

%description libs -l pl.UTF-8
Biblioteki dla demona fwupd instalującego aktualizacje firmware'u.

%package devel
Summary:	Header files for fwupd libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek fwupd
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.55.0
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

%package -n vala-fwupd
Summary:	Vala API for fwupd library
Summary(pl.UTF-8):	API języka Vala do biblioteki fwupd
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala-libsoup >= 2.52

%description -n vala-fwupd
Vala API for fwupd library.

%description -n vala-fwupd -l pl.UTF-8
API języka Vala do biblioteki fwupd.

%prep
%setup -q
%patch0 -p1

%ifarch x32
# -m64 is needed to build x64 EFI
%{__sed} -i -e "/^if efi_arch == 'x86_64'/,/^elif/ s/'-mno-red-zone',/& '-m64',/" plugins/uefi/efi/meson.build
%endif

%build
%meson build \
	-Dbash_completiondir=%{bash_compdir} \
	%{!?with_efi:-Dplugin_dell=false} \
	%{!?with_efi:-Dplugin_redfish=false} \
	%{!?with_thunderbolt:-Dplugin_thunderbolt=false} \
	%{!?with_efi:-Dplugin_uefi=false} \
	-Dtests=false

%meson_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install -C build

for pdoc in plugins/*/README.md ; do
	pname=$(basename $(dirname $pdoc))
	cp -p plugins/${pname}/README.md README-${pname}.md
done

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS README.md README-*.md
%attr(755,root,root) %{_bindir}/dfu-tool
%attr(755,root,root) %{_bindir}/fwupdmgr
%dir %{_libexecdir}/fwupd
%attr(755,root,root) %{_libexecdir}/fwupd/fwupd
%attr(755,root,root) %{_libexecdir}/fwupd/fwupdate
%attr(755,root,root) %{_libexecdir}/fwupd/fwupdtool
%dir %{_libexecdir}/fwupd/efi
%{_libexecdir}/fwupd/efi/fwupd*.efi
%dir %{_libdir}/fwupd-plugins-3
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_altos.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_amt.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_colorhug.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_csr.so
%if %{with efi}
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_dell.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_dell_esrt.so
%endif
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_dell_dock.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_dfu.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_ebitdo.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_flashrom.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_nitrokey.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_nvme.so
%if %{with efi}
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_redfish.so
%endif
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_rts54hid.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_rts54hub.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_steelseries.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_superio.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_synapticsmst.so
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
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_wacomhid.so
%dir %{_sysconfdir}/fwupd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/daemon.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/redfish.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/uefi.conf
%dir %{_sysconfdir}/fwupd/remotes.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/fwupd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/lvfs.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/lvfs-testing.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/vendor.conf
%dir %{_sysconfdir}/pki/fwupd
%{_sysconfdir}/pki/fwupd/GPG-KEY-Hughski-Limited
%{_sysconfdir}/pki/fwupd/GPG-KEY-Linux-Foundation-Firmware
%{_sysconfdir}/pki/fwupd/GPG-KEY-Linux-Vendor-Firmware-Service
%{_sysconfdir}/pki/fwupd/LVFS-CA.pem
%dir %{_sysconfdir}/pki/fwupd-metadata
%{_sysconfdir}/pki/fwupd-metadata/GPG-KEY-Linux-Foundation-Metadata
%{_sysconfdir}/pki/fwupd-metadata/GPG-KEY-Linux-Vendor-Firmware-Service
%{_sysconfdir}/pki/fwupd-metadata/LVFS-CA.pem
%{systemdunitdir}/fwupd.service
%{systemdunitdir}/fwupd-offline-update.service
%{systemdunitdir}/system-update.target.wants/fwupd-offline-update.service
/lib/udev/rules.d/90-fwupd-devices.rules
/etc/dbus-1/system.d/org.freedesktop.fwupd.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.fwupd.service
%dir %{_datadir}/fwupd
%attr(755,root,root) %{_datadir}/fwupd/firmware-packager
%{_datadir}/fwupd/quirks.d
%dir %{_datadir}/fwupd/remotes.d
%{_datadir}/fwupd/remotes.d/fwupd
%{_datadir}/fwupd/remotes.d/vendor
%{_datadir}/metainfo/org.freedesktop.fwupd.metainfo.xml
%dir %{_datadir}/fwupd/metainfo
%{_datadir}/fwupd/metainfo/org.freedesktop.fwupd.remotes.lvfs-testing.metainfo.xml
%{_datadir}/fwupd/metainfo/org.freedesktop.fwupd.remotes.lvfs.metainfo.xml
%{_datadir}/polkit-1/actions/org.freedesktop.fwupd.policy
%{_datadir}/polkit-1/rules.d/org.freedesktop.fwupd.rules
%lang(ca) %{_localedir}/ca/LC_IMAGES
%lang(cs) %{_localedir}/cs/LC_IMAGES
%lang(en) %{_localedir}/en/LC_IMAGES
%lang(fi) %{_localedir}/fi/LC_IMAGES
%lang(fur) %{_localedir}/fur/LC_IMAGES
%lang(hr) %{_localedir}/hr/LC_IMAGES
%lang(hu) %{_localedir}/hu/LC_IMAGES
%lang(id) %{_localedir}/id/LC_IMAGES
%lang(it) %{_localedir}/it/LC_IMAGES
%lang(ko) %{_localedir}/ko/LC_IMAGES
%lang(pl) %{_localedir}/pl/LC_IMAGES
%lang(pt_BR) %{_localedir}/pt_BR/LC_IMAGES
%lang(ru) %{_localedir}/ru/LC_IMAGES
%lang(sr) %{_localedir}/sr/LC_IMAGES
%lang(sv) %{_localedir}/sv/LC_IMAGES
%lang(uk) %{_localedir}/uk/LC_IMAGES
%lang(zh_CN) %{_localedir}/zh_CN/LC_IMAGES
%lang(zh_TW) %{_localedir}/zh_TW/LC_IMAGES
%dir /var/lib/fwupd
%dir /var/lib/fwupd/builder
/var/lib/fwupd/builder/README.md
%{_mandir}/man1/dfu-tool.1*
%{_mandir}/man1/fwupdmgr.1*

%files -n bash-completion-fwupd
%defattr(644,root,root,755)
%{bash_compdir}/fwupdmgr
%{bash_compdir}/fwupdtool

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfwupd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfwupd.so.2
%{_libdir}/girepository-1.0/Fwupd-2.0.typelib

%files devel
%defattr(644,root,root,755)
%doc libfwupd/README.md
%attr(755,root,root) %{_libdir}/libfwupd.so
%{_includedir}/fwupd-1
%{_datadir}/gir-1.0/Fwupd-2.0.gir
%{_datadir}/dbus-1/interfaces/org.freedesktop.fwupd.xml
%{_pkgconfigdir}/fwupd.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libfwupd

%files -n vala-fwupd
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/fwupd.deps
%{_datadir}/vala/vapi/fwupd.vapi

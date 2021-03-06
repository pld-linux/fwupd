#
# Conditional build:
%bcond_without	apidocs
%bcond_without	efi		# UEFI (and dell, redfish) support
%bcond_without	flashrom	# flashrom plugin
%bcond_without	modemmanager	# modem_manager plugin
%bcond_without	thunderbolt	# Thunderbolt support

%ifnarch %{ix86} %{x8664} x32 %{arm} aarch64
%undefine	with_efi
%endif
Summary:	System daemon for installing device firmware
Summary(pl.UTF-8):	Demon systemowy do instalowania firmware'u urządzeń
Name:		fwupd
Version:	1.4.6
Release:	2
License:	LGPL v2.1+
Group:		Applications/System
Source0:	https://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz
# Source0-md5:	2e5ae3c97c955cc0cb7d1c53323279e5
Patch0:		%{name}-bashcomp.patch
Patch1:		%{name}-flashrom.patch
URL:		https://github.com/hughsie/fwupd
%{?with_modemmanager:BuildRequires:	ModemManager-devel >= 1.10.0}
%{?with_cairo:BuildRequires:	cairo-devel}
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils
%{?with_efi:BuildRequires:	efivar-devel >= 33}
# pkgconfig(libelf); can be also libelf-devel
BuildRequires:	elfutils-devel >= 0.166
%{?with_fontconfig:BuildRequires:	fontconfig-devel}
%{?with_fontconfig:BuildRequires:	freetype-devel >= 2}
BuildRequires:	gcab-devel >= 1.0
# C99
BuildRequires:	gcc >= 5:3.2
%ifarch x32
BuildRequires:	gcc-multilib-64 >= 5:3.2
%endif
BuildRequires:	gettext-tools >= 0.19.7
BuildRequires:	glib2-devel >= 1:2.55.0
%{?with_efi:BuildRequires:	gnu-efi}
BuildRequires:	gnutls-devel >= 3.6.0
BuildRequires:	gobject-introspection-devel >= 0.9.8
BuildRequires:	gpgme-devel
%{?with_doc:BuildRequires:	gtk-doc >= 1.14}
BuildRequires:	intltool >= 0.35.0
BuildRequires:	json-glib-devel >= 1.1.1
BuildRequires:	libarchive-devel
%{?with_flashrom:BuildRequires:	libflashrom-devel}
BuildRequires:	libgpg-error-devel
BuildRequires:	libgudev-devel >= 232
BuildRequires:	libgusb-devel >= 0.2.9
BuildRequires:	libjcat-devel >= 0.1.0
%{?with_modemmanager:BuildRequires:	libqmi-devel >= 1.22.0}
# for dell (which requires also uefi plugin and efivar)
%{?with_efi:BuildRequires:	libsmbios-devel >= 2.4.0}
BuildRequires:	libsoup-devel >= 2.52
BuildRequires:	libuuid-devel
BuildRequires:	libxmlb-devel >= 0.1.13
BuildRequires:	libxslt-progs
# for <linux/nvme_ioctl.h>
BuildRequires:	linux-libc-headers >= 7:4.4
BuildRequires:	meson >= 0.47.0
BuildRequires:	ninja >= 1.6
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.114
BuildRequires:	python3 >= 1:3.0
BuildRequires:	python3-pillow
BuildRequires:	python3-pycairo
BuildRequires:	rpmbuild(macros) >= 1.726
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	systemd-units >= 1:211
BuildRequires:	tar >= 1:1.22
BuildRequires:	tpm2-tss-devel >= 2.0
BuildRequires:	udev-devel
%{?with_thunderbolt:BuildRequires:	umockdev-devel}
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
%{?with_modemmanager:BuildRequires:	ModemManager-libs >= 1.10.0}
Requires:	gcab >= 1.0
Requires:	gnutls-libs >= 3.6.0
Requires:	libgudev >= 232
Requires:	libgusb >= 0.2.9
Requires:	libjcat >= 0.1.0
%{?with_modemmanager:Requires:	libqmi >= 1.22.0}
%{?with_efi:Requires:	libsmbios >= 2.4.0}
Requires:	libsoup >= 2.52
Requires:	libxmlb >= 0.1.7
Requires:	polkit >= 0.114
Requires:	tpm2-tss >= 2.0
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

%package -n fish-completion-fwupd
Summary:	Fish completion for fwupd commands
Summary(pl.UTF-8):	Dopełnianie składni poleceń fwupd w fish
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	fish

%description -n fish-completion-fwupd
Fish completion for fwupd commands.

%description -n fish-completion-fwupd -l pl.UTF-8
Dopełnianie składni poleceń fwupd w fish.

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
BuildArch:	noarch

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
%patch1 -p1

%ifarch x32
# -m64 is needed to build x64 EFI
%{__sed} -i -e "/^if efi_arch == 'x86_64'/,/^elif/ s/'-mno-red-zone',/& '-m64',/" plugins/uefi/efi/meson.build
%endif

%build
%meson build \
	-Dbash_completiondir=%{bash_compdir} \
	-Dgtkdoc=%{__true_false apidocs} \
	%{!?with_efi:-Dplugin_dell=false} \
	%{?with_flashrom:-Dplugin_flashrom=true} \
	%{?with_modemmanager:-Dplugin_modem_manager=true} \
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
%doc AUTHORS MAINTAINERS README.md README-*.md
%{?with_efi:%attr(755,root,root) %{_bindir}/dbxtool}
%attr(755,root,root) %{_bindir}/dfu-tool
%attr(755,root,root) %{_bindir}/fwupdagent
%{?with_efi:%attr(755,root,root) %{_bindir}/fwupdate}
%attr(755,root,root) %{_bindir}/fwupdmgr
%attr(755,root,root) %{_bindir}/fwupdtool
%attr(755,root,root) %{_bindir}/fwupdtpmevlog
%dir %{_libexecdir}/fwupd
%attr(755,root,root) %{_libexecdir}/fwupd/fwupd
%attr(755,root,root) %{_libexecdir}/fwupd/fwupdoffline
%if %{with efi}
%dir %{_libexecdir}/fwupd/efi
%{_libexecdir}/fwupd/efi/fwupd*.efi
%endif
%dir %{_libdir}/fwupd-plugins-3
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_altos.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_amt.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_ata.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_colorhug.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_coreboot.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_ccgx.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_cpu.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_csr.so
%if %{with efi}
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_dell.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_dell_esrt.so
%endif
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_dell_dock.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_dfu.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_ebitdo.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_emmc.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_ep963x.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_fastboot.so
%if %{with flashrom}
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_flashrom.so
%endif
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_fresco_pd.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_jabra.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_logind.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_logitech_hidpp.so
%if %{with modemmanager}
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_modem_manager.so
%endif
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_nitrokey.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_nvme.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_optionrom.so
%if %{with efi}
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_redfish.so
%endif
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_rts54hid.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_rts54hub.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_solokey.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_steelseries.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_superio.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_synaptics_cxaudio.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_synaptics_mst.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_synaptics_prometheus.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_synaptics_rmi.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_thelio_io.so
%if %{with thunderbolt}
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_thunderbolt.so
%endif
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_tpm.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_tpm_eventlog.so
%if %{with efi}
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_uefi.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_uefi_dbx.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_uefi_recovery.so
%endif
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_upower.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_vli.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_wacom_raw.so
%attr(755,root,root) %{_libdir}/fwupd-plugins-3/libfu_plugin_wacom_usb.so
%dir %{_sysconfdir}/fwupd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/ata.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/daemon.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/thunderbolt.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/upower.conf
%if %{with efi}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/redfish.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/uefi.conf
%endif
%dir %{_sysconfdir}/fwupd/remotes.d
%if %{with efi}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/dell-esrt.conf
%endif
#%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/fwupd-tests.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/lvfs.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/lvfs-testing.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/vendor.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/vendor-directory.conf
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
%{systemdunitdir}/fwupd-refresh.service
%{systemdunitdir}/fwupd-refresh.timer
%{systemdunitdir}/system-update.target.wants/fwupd-offline-update.service
/lib/systemd/system-preset/fwupd-refresh.preset
/lib/systemd/system-shutdown/fwupd.shutdown
/lib/udev/rules.d/90-fwupd-devices.rules
%{_datadir}/dbus-1/system.d/org.freedesktop.fwupd.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.fwupd.service
%dir %{_datadir}/fwupd
%attr(755,root,root) %{_datadir}/fwupd/add_capsule_header.py
%attr(755,root,root) %{_datadir}/fwupd/firmware_packager.py
%attr(755,root,root) %{_datadir}/fwupd/install_dell_bios_exe.py
%attr(755,root,root) %{_datadir}/fwupd/simple_client.py
%{_datadir}/fwupd/quirks.d
%dir %{_datadir}/fwupd/remotes.d
%if %{with efi}
%{_datadir}/fwupd/remotes.d/dell-esrt
%endif
%{_datadir}/fwupd/remotes.d/vendor
%{_datadir}/metainfo/org.freedesktop.fwupd.metainfo.xml
%dir %{_datadir}/fwupd/metainfo
%{_datadir}/fwupd/metainfo/org.freedesktop.fwupd.remotes.lvfs-testing.metainfo.xml
%{_datadir}/fwupd/metainfo/org.freedesktop.fwupd.remotes.lvfs.metainfo.xml
%{_datadir}/polkit-1/actions/org.freedesktop.fwupd.policy
%{_datadir}/polkit-1/rules.d/org.freedesktop.fwupd.rules
%{_iconsdir}/hicolor/scalable/apps/org.freedesktop.fwupd.svg
%if %{with efi}
%lang(ca) %{_localedir}/ca/LC_IMAGES
%lang(cs) %{_localedir}/cs/LC_IMAGES
%lang(da) %{_localedir}/da/LC_IMAGES
%lang(de) %{_localedir}/de/LC_IMAGES
%lang(en) %{_localedir}/en/LC_IMAGES
%lang(fi) %{_localedir}/fi/LC_IMAGES
%lang(fur) %{_localedir}/fur/LC_IMAGES
%lang(hr) %{_localedir}/hr/LC_IMAGES
%lang(hu) %{_localedir}/hu/LC_IMAGES
%lang(id) %{_localedir}/id/LC_IMAGES
%lang(it) %{_localedir}/it/LC_IMAGES
%lang(ko) %{_localedir}/ko/LC_IMAGES
%lang(lt) %{_localedir}/lt/LC_IMAGES
%lang(pl) %{_localedir}/pl/LC_IMAGES
%lang(pt_BR) %{_localedir}/pt_BR/LC_IMAGES
%lang(ru) %{_localedir}/ru/LC_IMAGES
%lang(sr) %{_localedir}/sr/LC_IMAGES
%lang(sv) %{_localedir}/sv/LC_IMAGES
%lang(tr) %{_localedir}/tr/LC_IMAGES
%lang(uk) %{_localedir}/uk/LC_IMAGES
%lang(zh_CN) %{_localedir}/zh_CN/LC_IMAGES
%lang(zh_TW) %{_localedir}/zh_TW/LC_IMAGES
%endif
%dir /var/lib/fwupd
%dir /var/lib/fwupd/builder
/var/lib/fwupd/builder/README.md
%{?with_efi:%{_mandir}/man1/dbxtool.1*}
%{_mandir}/man1/dfu-tool.1*
%{_mandir}/man1/fwupdagent.1*
%{?with_efi:%{_mandir}/man1/fwupdate.1*}
%{_mandir}/man1/fwupdmgr.1*
%{_mandir}/man1/fwupdtool.1*
%{_mandir}/man1/fwupdtpmevlog.1*

%files -n bash-completion-fwupd
%defattr(644,root,root,755)
%{bash_compdir}/fwupdagent
%{bash_compdir}/fwupdmgr
%{bash_compdir}/fwupdtool

%files -n fish-completion-fwupd
%defattr(644,root,root,755)
%{_datadir}/fish/vendor_completions.d/fwupdmgr.fish

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfwupd.so.*.*.*
%attr(755,root,root) %{_libdir}/libfwupdplugin.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfwupd.so.2
%attr(755,root,root) %ghost %{_libdir}/libfwupdplugin.so.1
%{_libdir}/girepository-1.0/Fwupd-2.0.typelib
%{_libdir}/girepository-1.0/FwupdPlugin-1.0.typelib

%files devel
%defattr(644,root,root,755)
%doc libfwupd/README.md
%attr(755,root,root) %{_libdir}/libfwupd.so
%attr(755,root,root) %{_libdir}/libfwupdplugin.so
%{_includedir}/fwupd-1
%{_datadir}/gir-1.0/Fwupd-2.0.gir
%{_datadir}/gir-1.0/FwupdPlugin-1.0.gir
%{_datadir}/dbus-1/interfaces/org.freedesktop.fwupd.xml
%{_pkgconfigdir}/fwupd.pc
%{_pkgconfigdir}/fwupdplugin.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/fwupd
%endif

%files -n vala-fwupd
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/fwupd.deps
%{_datadir}/vala/vapi/fwupd.vapi
%{_datadir}/vala/vapi/fwupdplugin.deps
%{_datadir}/vala/vapi/fwupdplugin.vapi

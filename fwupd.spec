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
Version:	1.8.1
Release:	1
License:	LGPL v2.1+
Group:		Applications/System
Source0:	https://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz
# Source0-md5:	bf76925cb36c8da4c1c626cdabb53799
URL:		https://github.com/hughsie/fwupd
%{?with_modemmanager:BuildRequires:	ModemManager-devel >= 1.10.0}
BuildRequires:	bash-completion-devel >= 2.0
%{?with_cairo:BuildRequires:	cairo-devel}
BuildRequires:	curl-devel >= 7.62.0
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
# or gi-docgen >= 2021.1 with -Ddocs=docgen
%{?with_doc:BuildRequires:	gtk-doc >= 1.14}
BuildRequires:	intltool >= 0.35.0
BuildRequires:	json-glib-devel >= 1.1.1
BuildRequires:	libarchive-devel
BuildRequires:	libcbor-devel >= 0.7.0
%{?with_flashrom:BuildRequires:	libflashrom-devel >= 1.2}
BuildRequires:	libgpg-error-devel
BuildRequires:	libgudev-devel >= 232
BuildRequires:	libgusb-devel >= 0.3.5
BuildRequires:	libjcat-devel >= 0.1.4
%{?with_modemmanager:BuildRequires:	libmbim-devel >= 1.22.0}
%{?with_modemmanager:BuildRequires:	libqmi-devel >= 1.23.1}
# for dell (which requires also uefi plugin and efivar)
%{?with_efi:BuildRequires:	libsmbios-devel >= 2.4.0}
BuildRequires:	libsoup-devel >= 2.52
BuildRequires:	libuuid-devel
BuildRequires:	libxmlb-devel >= 0.1.13
BuildRequires:	libxslt-progs
# for <linux/nvme_ioctl.h>
BuildRequires:	linux-libc-headers >= 7:4.4
BuildRequires:	meson >= 0.60.0
BuildRequires:	ninja >= 1.6
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.114
BuildRequires:	python3 >= 1:3.0
BuildRequires:	python3-pillow
BuildRequires:	python3-pycairo
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	systemd-units >= 1:211
BuildRequires:	tar >= 1:1.22
BuildRequires:	tpm2-tss-devel >= 2.0
BuildRequires:	udev-devel
%{?with_thunderbolt:BuildRequires:	umockdev-devel}
BuildRequires:	xz
BuildRequires:	xz-devel
Requires:	%{name}-libs = %{version}-%{release}
%{?with_modemmanager:BuildRequires:	ModemManager-libs >= 1.10.0}
Requires:	curl-libs >= 7.62.0
Requires:	gcab >= 1.0
Requires:	gnutls-libs >= 3.6.0
Requires:	libcbor >= 0.7.0
Requires:	libgudev >= 232
Requires:	libgusb >= 0.3.5
Requires:	libjcat >= 0.1.4
%{?with_modemmanager:Requires:	libmbim >= 1.22.0}
%{?with_modemmanager:Requires:	libqmi >= 1.23.1}
%{?with_efi:Requires:	libsmbios >= 2.4.0}
Requires:	libsoup >= 2.52
Requires:	libxmlb >= 0.1.7
Requires:	polkit >= 0.114
Requires:	tpm2-tss >= 2.0
%if %{with efi}
Suggests:	fwupd-efi
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		fwupd_plugins_dir	%{_libdir}/fwupd-plugins-6

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

%description devel
Header files for fwupd libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek fwupd.

%package static
Summary:	Static fwupd libraries
Summary(pl.UTF-8):	Statyczne biblioteki fwupd
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static fwupd libraries.

%description static -l pl.UTF-8
Statyczne biblioteki fwupd.

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

%build
%meson build \
	-Dbluez=true \
	-Defi_binary=false \
	-Ddocs=%{?with_apidocs:gtkdoc}%{!?with_apidocs:none} \
	-Dlzma=true \
	%{!?with_efi:-Dplugin_dell=false} \
	%{?with_flashrom:-Dplugin_flashrom=true} \
	-Dplugin_intel_spi=true \
	%{?with_modemmanager:-Dplugin_modem_manager=true} \
	-Dplugin_platform_integrity=true \
	%{!?with_efi:-Dplugin_redfish=false} \
	%{!?with_thunderbolt:-Dplugin_thunderbolt=false} \
	%{!?with_efi:-Dplugin_uefi_capsule=false} \
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
%doc AUTHORS MAINTAINERS README.md README-*.md SECURITY.md
%{?with_efi:%attr(755,root,root) %{_bindir}/dbxtool}
%attr(755,root,root) %{_bindir}/dfu-tool
%attr(755,root,root) %{_bindir}/fwupdagent
%{?with_efi:%attr(755,root,root) %{_bindir}/fwupdate}
%attr(755,root,root) %{_bindir}/fwupdmgr
%attr(755,root,root) %{_bindir}/fwupdtool
%dir %{_libexecdir}/fwupd
%attr(755,root,root) %{_libexecdir}/fwupd/fwupd
%attr(755,root,root) %{_libexecdir}/fwupd/fwupd-detect-cet
%attr(755,root,root) %{_libexecdir}/fwupd/fwupdoffline
%dir %{fwupd_plugins_dir}
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_acpi_dmar.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_acpi_facp.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_acpi_ivrs.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_acpi_phat.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_analogix.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_amt.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_ata.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_bcm57xx.so
%if %{with efi}
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_bios.so
%endif
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_ccgx.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_cfu.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_ch341a.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_colorhug.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_corsair.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_cpu.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_cros_ec.so
%if %{with efi}
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_dell.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_dell_esrt.so
%endif
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_dell_dock.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_dfu.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_dfu_csr.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_ebitdo.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_elanfp.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_elantp.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_emmc.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_ep963x.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_fastboot.so
%if %{with flashrom}
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_flashrom.so
%endif
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_fresco_pd.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_genesys.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_goodixmoc.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_gpio.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_hailuck.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_intel_spi.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_iommu.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_jabra.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_lenovo_thinklmi.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_linux_lockdown.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_linux_sleep.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_linux_swap.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_linux_tainted.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_logind.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_logitech_bulkcontroller.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_logitech_hidpp.so
%if %{with modemmanager}
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_modem_manager.so
%endif
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_msr.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_mtd.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_nitrokey.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_nordic_hid.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_nvme.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_optionrom.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_parade_lspcon.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_pci_bcr.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_pci_mei.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_pixart_rf.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_platform_integrity.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_powerd.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_realtek_mst.so
%if %{with efi}
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_redfish.so
%endif
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_rts54hid.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_rts54hub.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_scsi.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_steelseries.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_superio.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_synaptics_cape.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_synaptics_cxaudio.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_synaptics_mst.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_synaptics_prometheus.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_synaptics_rmi.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_system76_launch.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_thelio_io.so
%if %{with thunderbolt}
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_thunderbolt.so
%endif
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_tpm.so
%if %{with efi}
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_uefi_capsule.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_uefi_dbx.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_uefi_pk.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_uefi_recovery.so
%endif
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_uf2.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_upower.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_usi_dock.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_vli.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_wacom_raw.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_wacom_usb.so
%dir %{_sysconfdir}/fwupd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/daemon.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/msr.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/thunderbolt.conf
%if %{with efi}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/redfish.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/uefi_capsule.conf
%endif
%dir %{_sysconfdir}/fwupd/remotes.d
%if %{with efi}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/dell-esrt.conf
%endif
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/lvfs.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/lvfs-testing.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/vendor.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/vendor-directory.conf
#/etc/grub.d/35_fwupd
%dir %{_sysconfdir}/pki/fwupd
%{_sysconfdir}/pki/fwupd/GPG-KEY-Linux-Foundation-Firmware
%{_sysconfdir}/pki/fwupd/GPG-KEY-Linux-Vendor-Firmware-Service
%{_sysconfdir}/pki/fwupd/LVFS-CA.pem
%dir %{_sysconfdir}/pki/fwupd-metadata
%{_sysconfdir}/pki/fwupd-metadata/GPG-KEY-Linux-Foundation-Metadata
%{_sysconfdir}/pki/fwupd-metadata/GPG-KEY-Linux-Vendor-Firmware-Service
%{_sysconfdir}/pki/fwupd-metadata/LVFS-CA.pem
#/lib/modules-load.d/fwupd-msr.conf
#/lib/modules-load.d/fwupd-platform-integrity.conf
#/lib/modules-load.d/fwupd-redfish.conf
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
%if %{with efi}
%{_datadir}/fwupd/uefi-capsule-ux.tar.xz
%endif
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
%{?with_efi:%{_mandir}/man1/dbxtool.1*}
%{_mandir}/man1/dfu-tool.1*
%{_mandir}/man1/fwupdagent.1*
%{?with_efi:%{_mandir}/man1/fwupdate.1*}
%{_mandir}/man1/fwupdmgr.1*
%{_mandir}/man1/fwupdtool.1*

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
%attr(755,root,root) %ghost %{_libdir}/libfwupd.so.2
%attr(755,root,root) %{_libdir}/libfwupdplugin.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfwupdplugin.so.6
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

%files static
%defattr(644,root,root,755)
%{_libdir}/libfwupd.a
%{_libdir}/libfwupdplugin.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/fwupd
%endif

%files -n vala-fwupd
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/fwupd.deps
%{_datadir}/vala/vapi/fwupd.vapi

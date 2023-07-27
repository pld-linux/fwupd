#
# Conditional build:
%bcond_without	apidocs
%bcond_without	dell		# Dell-specific support
%bcond_without	efi		# UEFI (and dell, redfish) support
%bcond_without	flashrom	# flashrom plugin
%bcond_without	modemmanager	# modem_manager plugin
%bcond_without	thunderbolt	# Thunderbolt support

%ifnarch %{ix86} %{x8664} x32 %{arm} aarch64
%undefine	with_efi
%endif
# libsmbios archs
%ifnarch	%{ix86} %{x8664} x32
%undefine	with_dell
%endif
%if %{without efi}
%undefine	with_dell
%endif
%ifarch %{ix86} %{x8664} x32
%define		with_intel_spi	1
%endif
Summary:	System daemon for installing device firmware
Summary(pl.UTF-8):	Demon systemowy do instalowania firmware'u urządzeń
Name:		fwupd
Version:	1.8.17
Release:	1
License:	LGPL v2.1+
Group:		Applications/System
#Source0Download: https://github.com/hughsie/fwupd/releases
Source0:	https://github.com/hughsie/fwupd/releases/download/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	12b5ee390019a9fbfec2733597f53ced
URL:		https://github.com/hughsie/fwupd
%{?with_modemmanager:BuildRequires:	ModemManager-devel >= 1.10.0}
BuildRequires:	bash-completion-devel >= 1:2.0
%{?with_cairo:BuildRequires:	cairo-devel}
BuildRequires:	curl-devel >= 7.62.0
%{?with_efi:BuildRequires:	efivar-devel >= 33}
# pkgconfig(libelf); can be also libelf-devel
BuildRequires:	gcab-devel >= 1.0
# C11
BuildRequires:	gcc >= 6:4.7
%ifarch x32
BuildRequires:	gcc-multilib-64 >= 6:4.7
%endif
BuildRequires:	gettext-tools >= 0.19.7
BuildRequires:	glib2-devel >= 1:2.55.0
BuildRequires:	gnutls-devel >= 3.6.0
BuildRequires:	gobject-introspection-devel >= 0.9.8
%{?with_doc:BuildRequires:	gi-docgen >= 2022.2}
BuildRequires:	json-glib-devel >= 1.1.1
BuildRequires:	libarchive-devel
BuildRequires:	libcbor-devel >= 0.7.0
%{?with_flashrom:BuildRequires:	libflashrom-devel >= 1.2}
BuildRequires:	libgudev-devel >= 232
BuildRequires:	libgusb-devel >= 0.3.5
BuildRequires:	libjcat-devel >= 0.1.4
%{?with_modemmanager:BuildRequires:	libmbim-devel >= 1.22.0}
%{?with_modemmanager:BuildRequires:	libqmi-devel >= 1.23.1}
# for dell (which requires also uefi plugin and efivar)
%{?with_dell:BuildRequires:	libsmbios-devel >= 2.4.0}
BuildRequires:	libsoup-devel >= 2.52
BuildRequires:	libuuid-devel
BuildRequires:	libxmlb-devel >= 0.1.15
# for <linux/nvme_ioctl.h>
BuildRequires:	linux-libc-headers >= 7:4.4
BuildRequires:	meson >= 0.61.0
BuildRequires:	ninja >= 1.6
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.114
BuildRequires:	python3 >= 1:3.0
%{?with_doc:BuildRequires:	python3-markdown >= 3.2}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	systemd-devel >= 1:209
BuildRequires:	systemd-units >= 1:211
BuildRequires:	tar >= 1:1.22
BuildRequires:	tpm2-tss-devel >= 2.0
BuildRequires:	udev-devel
%{?with_thunderbolt:BuildRequires:	umockdev-devel}
BuildRequires:	xz
BuildRequires:	xz-devel
# efi capsule splash (po/test-deps)
%if %{with efi}
# any Sans font
BuildRequires:	fonts-TTF-DejaVu
BuildRequires:	pango >= 1:1.26.0
BuildRequires:	python3-pycairo
BuildRequires:	python3-pygobject3
%endif
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
%{?with_dell:Requires:	libsmbios >= 2.4.0}
Requires:	libsoup >= 2.52
Requires:	libxmlb >= 0.1.15
Requires:	polkit >= 0.114
Requires:	tpm2-tss >= 2.0
%if %{with efi}
Suggests:	fwupd-efi
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		fwupd_plugins_dir	%{_libdir}/fwupd-%{version}

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
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

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
BuildArch:	noarch

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
	-Dbluez=enabled \
	-Dcompat_cli=true \
	-Defi_binary=false \
	-Ddocs=%{__enabled_disabled apidocs} \
	-Dlzma=enabled \
	%{!?with_dell:-Dplugin_dell=disabled} \
	%{!?with_flashrom:-Dplugin_flashrom=disabled} \
	%{?with_intel_spi:-Dplugin_intel_spi=true} \
	%{!?with_modemmanager:-Dplugin_modem_manager=disabled} \
	%{!?with_efi:-Dplugin_redfish=disabled} \
	%{!?with_efi:-Dplugin_uefi_capsule=disabled} \
	%{!?with_efi:-Dplugin_uefi_pk=disabled} \
	-Dtests=false

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

for pdoc in plugins/*/README.md ; do
	pname=$(basename $(dirname $pdoc))
	cp -p plugins/${pname}/README.md README-${pname}.md
done

%if %{with apidocs}
# FIXME: where to package gi-docgen generated docs?
install -d $RPM_BUILD_ROOT%{_gtkdocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/*fwupd* $RPM_BUILD_ROOT%{_gtkdocdir}
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc MAINTAINERS README.md README-*.md SECURITY.md
%{?with_efi:%attr(755,root,root) %{_bindir}/dbxtool}
%attr(755,root,root) %{_bindir}/dfu-tool
%attr(755,root,root) %{_bindir}/fwupdagent
%{?with_efi:%attr(755,root,root) %{_bindir}/fwupdate}
%attr(755,root,root) %{_bindir}/fwupdmgr
%attr(755,root,root) %{_bindir}/fwupdtool
%dir %{_libexecdir}/fwupd
%attr(755,root,root) %{_libexecdir}/fwupd/fwupd
%ifarch %{ix86} %{x8664} x32
%attr(755,root,root) %{_libexecdir}/fwupd/fwupd-detect-cet
%endif
%attr(755,root,root) %{_libexecdir}/fwupd/fwupdoffline
%if %{with flashrom}
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_flashrom.so
%endif
%if %{with modemmanager}
%attr(755,root,root) %{fwupd_plugins_dir}/libfu_plugin_modem_manager.so
%endif
%dir %{_sysconfdir}/fwupd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/daemon.conf
%ifarch %{ix86} %{x8664} x32
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/msr.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/thunderbolt.conf
%endif
%if %{with efi}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/redfish.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/uefi_capsule.conf
%endif
%dir %{_sysconfdir}/fwupd/bios-settings.d
%dir %{_sysconfdir}/fwupd/remotes.d
%if %{with dell}
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
%if %{with dell}
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
%{bash_compdir}/fwupdmgr
%{bash_compdir}/fwupdtool

%files -n fish-completion-fwupd
%defattr(644,root,root,755)
%{_datadir}/fish/vendor_completions.d/fwupdmgr.fish

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfwupd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfwupd.so.2
%{_libdir}/girepository-1.0/Fwupd-2.0.typelib
%dir %{fwupd_plugins_dir}
%attr(755,root,root) %{fwupd_plugins_dir}/libfwupdengine.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfwupdplugin.so
%attr(755,root,root) %{fwupd_plugins_dir}/libfwupdutil.so

%files devel
%defattr(644,root,root,755)
%doc libfwupd/README.md
%attr(755,root,root) %{_libdir}/libfwupd.so
%{_includedir}/fwupd-1
%{_datadir}/gir-1.0/Fwupd-2.0.gir
%{_datadir}/dbus-1/interfaces/org.freedesktop.fwupd.xml
%{_pkgconfigdir}/fwupd.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libfwupd.a
%{fwupd_plugins_dir}/libfwupdengine.a
%{fwupd_plugins_dir}/libfwupdplugin.a
%{fwupd_plugins_dir}/libfwupdutil.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/fwupd
%{_gtkdocdir}/libfwupd
%{_gtkdocdir}/libfwupdplugin
%endif

%files -n vala-fwupd
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/fwupd.deps
%{_datadir}/vala/vapi/fwupd.vapi

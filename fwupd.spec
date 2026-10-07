# TODO: fwupd-refresh user
#
# Conditional build:
%bcond_without	apidocs
%bcond_without	modemmanager	# modem_manager plugin
%bcond_without	static_libs	# static libraries
%bcond_with	tests		# build without tests

# no build options for these: UEFI plugins follow allow_uefi, HSI follows host CPU
%ifarch %{x8664} x32 aarch64 loongarch64 riscv64
%define		with_efi	1
%endif
%ifarch %{ix86} %{x8664} x32
%define		with_hsi	1
%endif
Summary:	System daemon for installing device firmware
Summary(pl.UTF-8):	Demon systemowy do instalowania firmware'u urządzeń
Name:		fwupd
Version:	2.1.8
Release:	1
License:	LGPL v2.1+
Group:		Applications/System
#Source0Download: https://github.com/fwupd/fwupd/releases
Source0:	https://github.com/fwupd/fwupd/releases/download/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	5d67e87d1dd7057d6e850af60c72bc17
Patch0:		%{name}-arch-independent-docs.patch
URL:		https://github.com/fwupd/fwupd
%{?with_modemmanager:BuildRequires:	ModemManager-devel >= 1.22.0}
BuildRequires:	bash-completion-devel >= 1:2.0
BuildRequires:	curl-devel >= 7.62.0
# C17
BuildRequires:	gcc >= 6:8
%ifarch x32
BuildRequires:	gcc-multilib-64 >= 6:8
%endif
BuildRequires:	gettext-tools >= 0.19.7
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	glib2-devel >= 1:2.68.0
# or openssl with -Dgnutls=disabled -Dopenssl=enabled
BuildRequires:	gnutls-devel >= 3.6.0
BuildRequires:	gobject-introspection-devel >= 0.9.8
BuildRequires:	libblkid-devel
BuildRequires:	libdrm-devel >= 2.4.113
%{?with_modemmanager:BuildRequires:	libmbim-devel >= 1.28.0}
%{?with_modemmanager:BuildRequires:	libqmi-devel >= 1.32.0}
BuildRequires:	libmnl-devel
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	libxmlb-devel >= 0.3.19
# for <linux/nvme_ioctl.h>
BuildRequires:	linux-libc-headers >= 7:4.4
BuildRequires:	meson >= 0.63.0
BuildRequires:	ninja >= 1.6
BuildRequires:	passim-devel >= 0.1.6
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.114
BuildRequires:	python3 >= 1:3.0
%{?with_tests:BuildRequires:	python3-dbusmock}
BuildRequires:	python3-jinja2
%{?with_apidocs:BuildRequires:	python3-markdown >= 3.2}
BuildRequires:	readline-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	systemd-devel >= 1:249
BuildRequires:	systemd-units >= 1:249
BuildRequires:	tar >= 1:1.22
BuildRequires:	tpm2-tss-devel >= 2.0
%{?with_tests:BuildRequires:	umockdev-devel}
BuildRequires:	vala
BuildRequires:	xz
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
# efi capsule splash (po/test-deps)
%if %{with efi}
# any Sans font
BuildRequires:	fonts-TTF-DejaVu
BuildRequires:	pango >= 1:1.26.0
BuildRequires:	python3-pycairo
BuildRequires:	python3-pygobject3
%endif
%{?with_modemmanager:BuildRequires:	ModemManager-libs >= 1.22.0}
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name}-libs = %{version}-%{release}
%{?with_modemmanager:Requires:	libmbim >= 1.28.0}
%{?with_modemmanager:Requires:	libqmi >= 1.32.0}
Requires:	polkit >= 0.114
%if %{with efi}
Suggests:	fwupd-efi
%endif
Provides:	group(fwupd-refresh)
Provides:	user(fwupd-refresh)
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
Requires:	curl-libs >= 7.62.0
Requires:	glib2 >= 1:2.68.0
Requires:	gnutls-libs >= 3.6.0
Requires:	hwdata
Requires:	libxmlb >= 0.3.19
Requires:	passim-libs >= 0.1.6
Requires:	polkit-libs >= 0.114
Requires:	tpm2-tss >= 2.0

%description libs
Libraries for fwupd device firmware installing daemon.

%description libs -l pl.UTF-8
Biblioteki dla demona fwupd instalującego aktualizacje firmware'u.

%package devel
Summary:	Header files for fwupd libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek fwupd
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	curl-devel >= 7.62.0
Requires:	glib2-devel >= 1:2.68.0

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

%description -n vala-fwupd
Vala API for fwupd library.

%description -n vala-fwupd -l pl.UTF-8
API języka Vala do biblioteki fwupd.

%prep
%setup -q
%patch -P0 -p1

%{__sed} -i -e '1s,/usr/bin/env python3$,%{__python3},' contrib/firmware_packager/*.py

%build
%meson \
	%{!?with_static_libs:--default-library=shared} \
	-Dblkid=enabled \
	-Dbluez=enabled \
	-Ddocs=%{__enabled_disabled apidocs} \
	-Defi_binary=false \
	-Dgnutls=enabled \
	-Dhsi=%{__enabled_disabled hsi} \
	-Dintrospection=enabled \
	-Dlibdrm=enabled \
	-Dlibmnl=enabled \
	-Dlogind=enabled \
	-Dopenssl=disabled \
	-Dpassim=enabled \
	-Dplugin_modem_manager=%{__enabled_disabled modemmanager} \
	-Dpolkit=enabled \
	-Dpython=%{__python3} \
	-Dreadline=enabled \
	-Dsupported_build=disabled \
	-Dsystemd=enabled \
	-Dtests=%{__true_false tests} \
	-Dumockdev_tests=%{__enabled_disabled tests} \
	-Dvalgrind=disabled \
	-Dvendor_ids_dir=/lib/hwdata

%meson_build

%if %{with tests}
%meson_test
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/lib/fwupd

%meson_install

%if %{with tests}
%{__rm} -r $RPM_BUILD_ROOT%{_libexecdir}/installed-tests \
	$RPM_BUILD_ROOT%{_datadir}/installed-tests
%endif

for pdoc in plugins/*/README.md ; do
	pname=$(basename $(dirname $pdoc))
	cp -p plugins/${pname}/README.md README-${pname}.md
done

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/*fwupd* $RPM_BUILD_ROOT%{_gidocdir}
%endif

%if %{with efi}
# PLD grub2 patches grub_mkconfig_dir to /lib/grub.d; /etc/grub.d is never read
install -d $RPM_BUILD_ROOT/lib
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/grub.d $RPM_BUILD_ROOT/lib/grub.d
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 366 fwupd-refresh
%useradd -u 366 -d /var/lib/fwupd -g fwupd-refresh -c "Firmware update daemon" fwupd-refresh

%postun
if [ "$1" = "0" ]; then
	%userremove fwupd-refresh
	%groupremove fwupd-refresh
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc MAINTAINERS README.md README-*.md SECURITY.md
%if %{with efi}
%attr(755,root,root) %{_bindir}/dbxtool
%endif
%attr(755,root,root) %{_bindir}/fwupdmgr
%attr(755,root,root) %{_bindir}/fwupdtool
%dir %{_libexecdir}/fwupd
%attr(755,root,root) %{_libexecdir}/fwupd/fwupd
%ifarch %{x8664} x32
%attr(755,root,root) %{_libexecdir}/fwupd/fwupd-detect-cet
%endif
%if %{with modemmanager}
%{fwupd_plugins_dir}/libfu_plugin_modem_manager.so
%endif
%dir %{_sysconfdir}/fwupd
%dir %{_sysconfdir}/fwupd/bios-settings.d
%{_sysconfdir}/fwupd/bios-settings.d/README.md
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/fwupd.conf
%dir %{_sysconfdir}/fwupd/remotes.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/lvfs.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/lvfs-embargo.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/lvfs-testing.conf
# used with -Dvendor_metadata=true (see data/remotes.d/README.md)
#%config(noreplace missingok) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/vendor.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fwupd/remotes.d/vendor-directory.conf
%dir %{_sysconfdir}/pki/fwupd
%{_sysconfdir}/pki/fwupd/LVFS-CA.pem
%{_sysconfdir}/pki/fwupd/LVFS-CA-2025PQ.pem
%dir %{_sysconfdir}/pki/fwupd-metadata
%{_sysconfdir}/pki/fwupd-metadata/LVFS-CA.pem
%{_sysconfdir}/pki/fwupd-metadata/LVFS-CA-2025PQ.pem
%{_prefix}/lib/modules-load.d/fwupd-i2c.conf
%if %{with hsi}
%{_prefix}/lib/modules-load.d/fwupd-msr.conf
%endif
%if %{with efi}
%dir /lib/grub.d
%attr(755,root,root) /lib/grub.d/35_fwupd
%endif
%attr(700,root,root) %dir /var/lib/fwupd
%{systemdunitdir}/fwupd.service
%{systemdunitdir}/fwupd-refresh.service
%{systemdunitdir}/fwupd-refresh.timer
%attr(754,root,root) /lib/systemd/system-shutdown/fwupd.shutdown
%{_prefix}/lib/sysusers.d/fwupd.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.fwupd.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.fwupd.service
%dir %{_datadir}/fwupd
%attr(755,root,root) %{_datadir}/fwupd/add_capsule_header.py
%attr(755,root,root) %{_datadir}/fwupd/firmware_packager.py
%attr(755,root,root) %{_datadir}/fwupd/install_dell_bios_exe.py
%attr(755,root,root) %{_datadir}/fwupd/simple_client.py
%if %{with efi}
%{_datadir}/fwupd/uefi-capsule-ux.zip
%endif
%{_datadir}/fwupd/quirks.d
%dir %{_datadir}/fwupd/remotes.d
%{_datadir}/fwupd/remotes.d/vendor
%{_datadir}/metainfo/org.freedesktop.fwupd.metainfo.xml
%dir %{_datadir}/fwupd/metainfo
%{_datadir}/fwupd/metainfo/org.freedesktop.fwupd.remotes.lvfs-testing.metainfo.xml
%{_datadir}/fwupd/metainfo/org.freedesktop.fwupd.remotes.lvfs.metainfo.xml
%{_datadir}/polkit-1/actions/org.freedesktop.fwupd.policy
%{_datadir}/polkit-1/rules.d/org.freedesktop.fwupd.rules
%{_iconsdir}/hicolor/64x64/apps/org.freedesktop.fwupd.png
%{_iconsdir}/hicolor/128x128/apps/org.freedesktop.fwupd.png
%{_iconsdir}/hicolor/scalable/apps/org.freedesktop.fwupd.svg
%if %{with efi}
%{_mandir}/man1/dbxtool.1*
%endif
%{_mandir}/man1/fwupdmgr.1*
%{_mandir}/man1/fwupdtool.1*
%{_mandir}/man5/fwupd-remotes.d.5*
%{_mandir}/man5/fwupd.conf.5*
%{_mandir}/man8/fwupd-refresh.service.8*

%files -n bash-completion-fwupd
%defattr(644,root,root,755)
%{bash_compdir}/fwupdmgr
%{bash_compdir}/fwupdtool

%files -n fish-completion-fwupd
%defattr(644,root,root,755)
%{fish_compdir}/fwupdmgr.fish

%files libs
%defattr(644,root,root,755)
%{_libdir}/libfwupd.so.*.*.*
%ghost %{_libdir}/libfwupd.so.3
%{_libdir}/girepository-1.0/Fwupd-2.0.typelib
%dir %{fwupd_plugins_dir}
%{fwupd_plugins_dir}/libfwupdengine.so
%{fwupd_plugins_dir}/libfwupdplugin.so
%{fwupd_plugins_dir}/libfwupdutil.so

%files devel
%defattr(644,root,root,755)
%doc libfwupd/README.md
%{_libdir}/libfwupd.so
%{_includedir}/fwupd-3
%{_datadir}/gir-1.0/Fwupd-2.0.gir
%{_datadir}/dbus-1/interfaces/org.freedesktop.fwupd.xml
%{_pkgconfigdir}/fwupd.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfwupd.a
%{fwupd_plugins_dir}/libfwupdengine.a
%{fwupd_plugins_dir}/libfwupdplugin.a
%{fwupd_plugins_dir}/libfwupdutil.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/fwupd
%{_gidocdir}/libfwupd
%{_gidocdir}/libfwupdplugin
%endif

%files -n vala-fwupd
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/fwupd.deps
%{_datadir}/vala/vapi/fwupd.vapi

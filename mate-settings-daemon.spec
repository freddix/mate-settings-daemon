Summary:	MATE Settings Daemon
Name:		mate-settings-daemon
Version:	1.8.1
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	ba264ff243f70136de486923f502710e
Patch0:		%{name}-freddix.patch
URL:		http://wiki.mate-desktop.org/mate-settings-daemon
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-devel
BuildRequires:	mate-desktop-devel >= 1.8.1
BuildRequires:	libmatekbd-devel >= 1.8.0
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	libxklavier-devel
BuildRequires:	pkg-config
BuildRequires:	pulseaudio-devel
BuildRequires:	xorg-libXxf86misc-devel
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
MATE Settings Daemon.

%package devel
Summary:	Header file for developing MATE Settings Daemon clients
Group:		Development/Libraries

%description devel
Header file for developing MATE Settings Daemon clients.

%prep
%setup -q
%patch0 -p1

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-compile	\
	--disable-silent-rules		\
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	icondir=%{_iconsdir}/hicolor

%{__rm} $RPM_BUILD_ROOT%{_libdir}/mate-settings-daemon/*.la
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/*.convert
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%update_icon_cache hicolor
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/mate-settings-daemon
%attr(755,root,root) %{_libexecdir}/*.so
%attr(755,root,root) %{_libexecdir}/msd-datetime-mechanism
%attr(755,root,root) %{_libexecdir}/msd-locate-pointer
%{_libexecdir}/*.mate-*-plugin

%{_datadir}/dbus-1/services/org.mate.SettingsDaemon.service
%{_datadir}/dbus-1/system-services/org.mate.SettingsDaemon.DateTimeMechanism.service
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml
%{_datadir}/mate-settings-daemon
%{_datadir}/polkit-1/actions/org.mate.settingsdaemon.datetimemechanism.policy
%{_sysconfdir}/dbus-1/system.d/org.mate.SettingsDaemon.DateTimeMechanism.conf
%{_sysconfdir}/xdg/autostart/mate-settings-daemon.desktop
%{_iconsdir}/hicolor/*/*/*.*
%{_mandir}/man1/mate-settings-daemon.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/mate-settings-daemon
%{_pkgconfigdir}/mate-settings-daemon.pc


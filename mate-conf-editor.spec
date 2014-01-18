# NOTE: deprecated, MateConf has been replaced by GSettings in MATE >= 1.5
#
# Conditional build:
%bcond_with	gtk3		# use GTK+ 3.x instead of 2.x
%bcond_without	static_libs	# don't build static libraries

Summary:	Editor for the MateConf configuration system
Summary(pl.UTF-8):	Edytor dla systemu konfiguracji MateConf
Name:		mate-conf-editor
Version:	1.4.0
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz
# Source0-md5:	e750e3b0bec139912d5cc695afef1347
URL:		http://wiki.mate-desktop.org/mate-conf
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-glib-devel >= 0.74
BuildRequires:	gettext-devel >= 0.10.40
BuildRequires:	glib2-devel >= 2.0
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2:2.18.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0.0}
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libtool
BuildRequires:	mate-conf-devel >= 1.1.0
BuildRequires:	mate-doc-utils
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	rpmbuild(macros) >= 1.526
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	gtk-update-icon-cache
Requires(post,preun):	mate-conf >= 1.1.0
Requires:	%{name}-libs = %{version}-%{release}
%{!?with_gtk3:Requires:	gtk+2 >= 2:2.18.0}
%{?with_gtk3:Requires:	gtk+3 >= 3.0.0}
Requires:	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	mateconf_schema_install() \
	umask 022; \
	MATECONF_CONFIG_SOURCE="xml:readwrite:/etc/mateconf/mateconf.xml.defaults" /usr/bin/mateconftool-2 --makefile-install-rule /etc/mateconf/schemas/%{?1}%{!?1:*.schemas} > /dev/null ; \
	%{nil}

%define mateconf_schema_uninstall() \
	if [ $1 = 0 -a -x /usr/bin/mateconftool-2 ]; then \
		umask 022; \
		MATECONF_CONFIG_SOURCE="xml:readwrite:/etc/mateconf/mateconf.xml.defaults" /usr/bin/mateconftool-2 --makefile-uninstall-rule /etc/mateconf/schemas/%{?1} > /dev/null \
	fi ; \
	%{nil}

%description
An editor for the MateConf configuration system. It's a fork of
gconf-editor.

%description -l pl.UTF-8
Edytor dla systemu konfiguracji MateConf. Jest to odgałęzienie pakietu
gconf-editor.

%prep
%setup -q

%build
mate-doc-prepare --copy --force
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	MATECONFTOOL=/usr/bin/mateconftool-2 \
	%{!?with_static_libs:--disable-static} \
	%{?with_gtk3:--with-gtk=3.0} \
	--with-mateconf-defaults-source=xml:merged:%{_sysconfdir}/mateconf/mateconf.xml.defaults

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# mate-conf-editor gettext domain, mateconf-editor mate/help and omf files
%find_lang %{name} --with-mate --with-omf --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%mateconf_schema_install mateconf-editor.schemas

%preun
%mateconf_schema_uninstall mateconf-editor.schemas

%postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mateconf-editor
%{_datadir}/mateconf-editor
%{_sysconfdir}/mateconf/schemas/mateconf-editor.schemas
%{_desktopdir}/mateconf-editor.desktop
%{_iconsdir}/hicolor/48x48/apps/mateconf-editor.png
%{_mandir}/man1/mateconf-editor.1*

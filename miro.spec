Summary:	Miro Player
Name:		miro
Version:	3.5
Release:	0.3
License:	GPL v2+
Group:		X11/Applications/Multimedia
URL:		http://www.getmiro.com/
Source0:	ftp://ftp.osuosl.org/pub/pculture.org/miro/src/%{name}-%{version}.tar.gz
# Source0-md5:	6e15d2d6ce086b0fe943a6cbea3c363c
BuildRequires:	ImageMagick
BuildRequires:	gtk-webkit-devel
BuildRequires:	python-Pyrex
BuildRequires:	python-pygobject-devel
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
Requires:	desktop-file-utils
Requires:	gstreamer-plugins-good
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	python-dbus
Requires:	python-gnome-gconf
Requires:	python-gstreamer
Requires:	python-libtorrent-rasterbar
Requires:	python-pycurl
Requires:	python-pygtk-gtk
Requires:	python-pywebkitgtk
Requires:	shared-mime-info
Provides:	democracy
Obsoletes:	democracy
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Internet TV player with integrated RSS and BitTorrent functionality.

%prep
%setup -q -n %{name}-%version

%build
cd linux
CFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags}" \
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
cd linux
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
cd ..

%py_postclean

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/ckb
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/lb

%find_lang miro

%{__sed} -i -e 's,miro-72x72.png,%{name},g' $RPM_BUILD_ROOT%{_desktopdir}/*.desktop

%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/miro/test

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache_post hicolor
%update_mime_database

%postun
%update_desktop_database_postun
%update_icon_cache hicolor
%update_mime_database

%files -f miro.lang
%defattr(644,root,root,755)
%doc README CREDITS
%attr(755,root,root) %{_bindir}/miro
%attr(755,root,root) %{_bindir}/miro.real
%{_datadir}/miro
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%{_pixmapsdir}/*.xpm
%{_mandir}/man1/miro.1*
%{_mandir}/man1/miro.real.1*
%{_datadir}/mime/packages/*.xml
%dir %{py_sitedir}/miro
%{py_sitedir}/miro/*.py[co]
%{py_sitedir}/miro/dl_daemon
%{py_sitedir}/miro/frontends
%{py_sitedir}/miro/plat/frontends
%{py_sitedir}/miro/plat/renderers
%{py_sitedir}/miro/plat/*.py[co]
%attr(755,root,root) %{py_sitedir}/miro/plat/xlibhelper.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/miro-%{version}-*.egg-info
%endif

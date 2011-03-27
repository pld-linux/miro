Summary:	Miro Player
Name:		miro
Version:	3.5.1
Release:	0.9
License:	GPL v2+
Group:		X11/Applications/Multimedia
URL:		http://www.getmiro.com/
Source0:	ftp://ftp.osuosl.org/pub/pculture.org/miro/src/%{name}-%{version}.tar.gz
# Source0-md5:	c4f22333da18bba48eadc65b9b05bfcc
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

rm -f $RPM_BUILD_ROOT%{_mandir}/man1/miro.real.1*
mv -f $RPM_BUILD_ROOT%{_bindir}/miro{.real,}

%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/miro/test
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/miro/resources/testdata

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
%{_datadir}/miro
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%{_pixmapsdir}/*.xpm
%{_mandir}/man1/miro.1*
%{_datadir}/mime/packages/*.xml
%dir %{py_sitedir}/miro
%{py_sitedir}/miro/*.py[co]
%{py_sitedir}/miro/dl_daemon
%dir %{py_sitedir}/miro/frontends
%{py_sitedir}/miro/frontends/*.py[co]
%dir %{py_sitedir}/miro/frontends/widgets
%{py_sitedir}/miro/frontends/widgets/*.py[co]
%dir %{py_sitedir}/miro/frontends/widgets/gtk
%{py_sitedir}/miro/frontends/widgets/gtk/*.py[co]
%attr(755,root,root) %{py_sitedir}/miro/frontends/widgets/gtk/pygtkhacks.so
%attr(755,root,root) %{py_sitedir}/miro/frontends/widgets/gtk/webkitgtkhacks.so
%{py_sitedir}/miro/frontends/cli
%{py_sitedir}/miro/frontends/shell
%dir %{py_sitedir}/miro/plat
%{py_sitedir}/miro/plat/*.py[co]
%attr(755,root,root) %{py_sitedir}/miro/plat/xlibhelper.so
%{py_sitedir}/miro/plat/frontends
%{py_sitedir}/miro/plat/renderers
%if "%{py_ver}" > "2.4"
%{py_sitedir}/miro-%{version}-*.egg-info
%endif

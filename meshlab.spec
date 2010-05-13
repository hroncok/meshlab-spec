Summary:	A system for processing and editing unstructured 3D triangular meshes
Name:		meshlab
Version:	1.2.2
Release:	4%{?dist}
URL:		http://meshlab.sourceforge.net/

Source0:	http://downloads.sourceforge.net/%{name}/MeshLabSrc_v122.tar.gz
Source1:	meshlab-48x48.xpm

# Fedora-specific patches to use shared libraries, and to put plugins and
# shaders in appropriate directories
Patch0:		meshlab-sharedlib.patch
Patch1:		meshlab-plugin-path.patch
Patch2:		meshlab-shader-path.patch

# patch to fix C++ namespace conflict
# http://sourceforge.net/tracker/?func=detail&aid=2872526&group_id=149444&atid=774731
Patch3:		meshlab-vcglib-namespace.patch

License:	GPLv2+ and BSD
Group:		Applications/Multimedia
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	bzip2-devel
BuildRequires:	glew-devel
BuildRequires:	levmar-devel
BuildRequires:	lib3ds-devel
BuildRequires:	muParser-devel
BuildRequires:	qhull-devel
BuildRequires:	qt-devel
BuildRequires:	ImageMagick
BuildRequires:	desktop-file-utils

%description
MeshLab is an open source, portable, and extensible system for the
processing and editing of unstructured 3D triangular meshes.  The
system is aimed to help the processing of the typical not-so-small
unstructured models arising in 3D scanning, providing a set of tools
for editing, cleaning, healing, inspecting, rendering and converting
these kinds of meshes.

%prep
%setup -q -n meshlab-snapshot-svn3524
%patch -P 0 -p1 -b .sharedlib
%patch -P 1 -p1 -b .plugin-path
%patch -P 2 -p1 -b .shader-path
%patch -P 3 -p1 -b .vcglib-namespace

# Turn of execute permissions on source files to avoid rpmlint
# errors and warnings for the debuginfo package
find . \( -name *.h -o -name *.cpp -o -name *.inl \) -a -executable \
	-exec chmod -x {} \;

# Remove bundled library sources, since we use the Fedora packaged
# libraries
rm -rf vcglib/wrap/system

%build
# Build instructions from the wiki:
#   http://meshlab.sourceforge.net/wiki/index.php/Compiling_V122
# Note that the build instructions in README.linux are out of date.

cd meshlab/src
%{_qt4_qmake} -recursive meshlabv12.pro
make %{?_smp_mflags} CFLAGS="%{optflags}" \
	DEFINES="-D__DISABLE_AUTO_STATS__ -DPLUGIN_DIR=\\\"%{_libdir}/%{name}\\\""

# process icon
convert %{SOURCE1} meshlab.png

# create desktop file
cat <<EOF >meshlab.desktop
[Desktop Entry]
Name=meshlab
GenericName=MeshLab 3D triangular mesh processing and editing
Exec=meshlab
Icon=meshlab
Terminal=false
Type=Application
Categories=Graphics;
EOF

# convert doc files from ISO-8859-1 to UTF-8 encoding:
cd ../docs
for f in contrib_Gangemi_Vannini.txt contrib_Buzzelli_Mazzanti.txt
do
  iconv -fiso88591 -tutf8 $f >$f.new
  touch -r $f $f.new
  mv $f.new $f
done

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_bindir}
install -p -m 755 meshlab/src/meshlab/meshlab \
		  meshlab/src/meshlabserver/meshlabserver \
		  %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_mandir}/man1
install -p -m 644 meshlab/docs/meshlab.1 \
		  meshlab/docs/meshlabserver.1 \
		  %{buildroot}%{_mandir}/man1
install -d -m 755 %{buildroot}%{_libdir}/meshlab/plugins
install -p -m 755 meshlab/src/meshlab/plugins/*.so \
		  %{buildroot}%{_libdir}/meshlab/plugins
install -d -m 755 %{buildroot}%{_datadir}/meshlab/shaders
install -p -m 644 meshlab/src/meshlab/shaders/*.{frag,gdp,vert} \
		  %{buildroot}%{_datadir}/meshlab/shaders
install -d -m 755 %{buildroot}%{_datadir}/meshlab/shadersrm
install -p -m 644 meshlab/src/meshlab/shadersrm/*.rfx \
		  %{buildroot}%{_datadir}/meshlab/shadersrm
install -d -m 755 %{buildroot}%{_datadir}/meshlab/textures
install -d -m 755 %{buildroot}%{_datadir}/pixmaps
install -p -m 644 meshlab/src/meshlab.png \
		  %{buildroot}%{_datadir}/pixmaps
install -d -m 755 %{buildroot}%{_datadir}/applications
install -p -m 644 meshlab/src/meshlab.desktop \
		  %{buildroot}%{_datadir}/applications
desktop-file-validate %{buildroot}%{_datadir}/applications/meshlab.desktop

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/meshlab
%{_bindir}/meshlabserver
%{_libdir}/meshlab/
%{_datadir}/meshlab/
%{_mandir}/man1/*.1.*
%doc meshlab/docs/contrib_Buzzelli_Mazzanti.txt
%doc meshlab/docs/contrib_Gangemi_Vannini.txt
%doc meshlab/docs/contrib_Latronico_Venturi.txt
%doc meshlab/docs/contrib_Mochi_Portelli_Vacca.txt
%doc meshlab/docs/gpl.txt
%doc meshlab/docs/history.txt
%doc meshlab/docs/privacy.txt
%doc meshlab/docs/README.linux
%doc meshlab/docs/readme.txt
%doc meshlab/docs/ToDo.txt
%doc meshlab/src/meshlab/shaders/3Dlabs-license.txt
%doc meshlab/src/meshlab/shaders/LightworkDesign-license.txt
%doc meshlab/src/meshlabplugins/filter_poisson/license.txt
%{_datadir}/applications/meshlab.desktop
%{_datadir}/pixmaps/meshlab.png

%changelog
* Mon May  3 2010 Eric Smith <eric@brouhaha.com> - 1.2.2-4
- in prep, remove bundled getopt library sources, to ensure
  that we're using the system library instead
- include doc tag for poisson filter license.txt
- add BSD to license tag
- correct typo in comment in spec

* Wed Apr  7 2010 Eric Smith <eric@brouhaha.com> - 1.2.2-3
- updates based on pre-review comments by Jussi Lehtola

* Tue Apr  6 2010 Eric Smith <eric@brouhaha.com> - 1.2.2-2
- updates based on pre-review comments by Martin Gieseking

* Tue Feb  2 2010 Eric Smith <eric@brouhaha.com> - 1.2.2-1
- initial version
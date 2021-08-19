Name:            libisoburn
Version:         1.4.8
Release:         9
Summary:         Library to enables creation and expansion of ISO-9660 filesystems
License:         GPLv2+
URL:             http://libburnia-project.org/
Source0:         http://files.libburnia-project.org/releases/%{name}-%{version}.tar.gz
BuildRequires:   libburn-devel >= %{version}, libisofs-devel >= %{version}
BuildRequires:   gcc gcc-c++

%description
Libisoburn is a frontend for libraries libburn and libisofs which
enables creation and expansion of ISO-9660 filesystems on all CD/
DVD/BD media supported by libburn. This includes media like DVD+RW,
which do not support multi-session management on media level and
even plain disk files or block devices. The price for that is thorough
specialization on data files in ISO-9660 filesystem images. So
libisoburn is not suitable for audio (CD-DA) or any other CD layout
which does not entirely consist of ISO-9660 sessions. 

%package devel
Summary:         Development files for libisoburn
Group:           Development/Libraries
Requires:        %{name} = %{version}-%{release}, pkgconfig
BuildRequires: doxygen, graphviz

%description devel
The libisoburn-devel package contains libraries and header files for
developing applications that use libisoburn.

%package -n xorriso
Summary:         ISO-9660 and Rock Ridge image manipulation tool
Group:           Applications/Archiving
URL:             http://scdbackup.sourceforge.net/xorriso_eng.html
Requires:        %{name} = %{version}-%{release}
Requires:        kde-filesystem >= 4
Requires:        chkconfig, coreutils
Provides:        %{name}-doc = %{version}-%{release}
Obsoletes:       %{name}-doc < %{version}-%{release}

%description -n xorriso
Xorriso is a program which copies file objects from POSIX compliant
filesystems into Rock Ridge enhanced ISO-9660 filesystems and allows
session-wise manipulation of such filesystems. It can load management
information of existing ISO images and it writes the session results
to optical media or to filesystem objects. Vice versa xorriso is able
to copy file objects out of ISO-9660 filesystems.

Filesystem manipulation capabilities surpass those of mkisofs. Xorriso
is especially suitable for backups, because of its high fidelity of
file attribute recording and its incremental update sessions. Optical
supported media: CD-R, CD-RW, DVD-R, DVD-RW, DVD+R, DVD+R DL, DVD+RW,
DVD-RAM, BD-R and BD-RE. 

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}
doxygen doc/doxygen.conf

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' install

# Don't install any libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}.la

# Clean up for later usage in documentation
rm -rf $RPM_BUILD_ROOT%{_defaultdocdir}

# Symlink xorriso as mkisofs (like in cdrkit)
ln -sf xorriso $RPM_BUILD_ROOT%{_bindir}/mkisofs

# Some file cleanups
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# Don't ship proof of concept for the moment
rm -f $RPM_BUILD_ROOT%{_bindir}/xorriso-tcltk

%check
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$RPM_BUILD_ROOT%{_libdir}"
cd releng
./run_all_auto -x ../xorriso/xorriso || (cat releng_generated_data/log.*; exit 1)

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n xorriso
/sbin/install-info %{_infodir}/xorrecord.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/xorriso.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/xorrisofs.info.gz %{_infodir}/dir || :

link=`readlink %{_bindir}/mkisofs`
if [ "$link" == "xorriso" ]; then
  rm -f %{_bindir}/mkisofs

%{_sbindir}/alternatives --install %{_bindir}/mkisofs mkisofs %{_bindir}/xorriso 50 \
  --slave %{_mandir}/man1/mkisofs.1.gz mkisofs-mkisofsman %{_mandir}/man1/xorrisofs.1.gz
fi

%preun -n xorriso
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/xorrecord.info.gz %{_infodir}/dir || :
  /sbin/install-info --delete %{_infodir}/xorriso.info.gz %{_infodir}/dir || :
  /sbin/install-info --delete %{_infodir}/xorrisofs.info.gz %{_infodir}/dir || :

fi

%files
%license COPYING
%doc AUTHORS COPYRIGHT README ChangeLog
%{_libdir}/%{name}*.so.*

%files devel
%doc doc/html
%{_includedir}/%{name}
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}*.pc

%files -n xorriso
%doc doc/html/
%ghost %{_bindir}/mkisofs
%{_bindir}/osirrox
%{_bindir}/xorrecord
%{_bindir}/xorriso
%{_bindir}/xorrisofs
%{_mandir}/man1/xorrecord.1*
%{_mandir}/man1/xorriso.1*
%{_mandir}/man1/xorrisofs.1*
%{_infodir}/xorrecord.info*
%{_infodir}/xorriso.info*
%{_infodir}/xorrisofs.info*

%changelog
* Wed Aug 04 2021 chenyanpanHW <chenyanpan@huawei.com> - 1.4.8-9
- DESC: delete BuildRequires gdb

* Mon Jun 28 2021 panxiaohe <panxiaohe@huawei.com> - 1.4.8-8
- Add gcc and gcc-c++ to BuildRequires

* Tue Sep 1 2020 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 1.4.8-7
- Fix a removal issue of xorriso

* Mon Mar 16 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.4.8-6
- Add help info to xorriso

* Fri Mar 13 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.4.8-5
- Add build requires of gdb

* Tue Mar 3 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.4.8-4
- Package init

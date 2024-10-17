# libpython is used by tdb, tdb is used by pulseaudio,
# pulseaudio is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

# Not really -- but python's build system enables lto in its own
# different way, no need for 2 conflicting approaches
%define _disable_lto 1

# Barfs on supposed-to-fail parts of the testsuite
%define _python_bytecompile_build 0

# Python modules aren't linked to libpython%{dirver}
%global _disable_ld_no_undefined 1

%define docver %{version}
%define dirver %(echo %{version} |cut -d. -f1-2)
%define familyver 3

%define api %{dirver}
%define major 1
%define libname %mklibname python %{api} %{major}
%define devname %mklibname python39 -d
%define lib32name %mklib32name python %{api} %{major}
%define dev32name %mklib32name python39 -d

%define pre %{nil}

%ifarch %{ix86} %{x86_64} ppc
%bcond_without valgrind
%else
%bcond_with valgrind
%endif

# weird stuff
# pip not available if python package built with pip
# * build without pip files lead to good package
# * but next package lead to unpackaged pip files 
# let's disable pip
%bcond_with pip

Summary:	An interpreted, interactive object-oriented programming language
Name:		python39
Version:	3.9.19
%if "%{pre}" != ""
Release:	0.%{pre}.1
%else
Release:	2
%endif
License:	Modified CNRI Open Source License
Group:		Development/Python
Url:		https://www.python.org/
Source0:	http://www.python.org/ftp/python/%{version}/Python-%{version}%{pre}.tar.xz
Source1:	http://www.python.org/ftp/python/doc/%{docver}/python-%{docver}-docs-html.tar.bz2
Source2:	python3.9.macros
Source3:	pybytecompile.macros
Source100:	%{name}.rpmlintrc
Patch0:		python-3.6.1-module-linkage.patch
Patch1:		https://src.fedoraproject.org/rpms/python3.9/raw/rawhide/f/00001-rpath.patch
Patch2:		https://src.fedoraproject.org/rpms/python3.9/raw/rawhide/f/00111-no-static-lib.patch
Patch3:		https://src.fedoraproject.org/rpms/python3.9/raw/rawhide/f/00189-use-rpm-wheels.patch
Patch4:		https://src.fedoraproject.org/rpms/python3.9/raw/rawhide/f/00251-change-user-install-location.patch
Patch5:		https://src.fedoraproject.org/rpms/python3.9/raw/rawhide/f/00328-pyc-timestamp-invalidation-mode.patch
Patch6:		https://src.fedoraproject.org/rpms/python3.9/raw/rawhide/f/00353-architecture-names-upstream-downstream.patch

Patch7:		Python-select-requires-libm.patch
Patch8:		python-3.3.0b1-test-posix_fadvise.patch
Patch9:		python-3.6.2-clang-5.0.patch
Patch10:	Python-3.8.0-c++.patch
Patch11:	python-3.7.1-dont-build-testembed-with-c++.patch
Patch12:	python-3.8.0-c++atomics.patch
Patch13:	0005-Improve-distutils-C-support.patch
Patch179:	00179-dont-raise-error-on-gdb-corrupted-frames-in-backtrace.patch
Patch184:	00201-fix-memory-leak-in-gdbm.patch
# (tpg) ClearLinux patches
Patch500:	0002-Skip-tests-TODO-fix-skips.patch

BuildRequires:	autoconf
BuildRequires:	autoconf-archive
BuildRequires:	blt
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	db-devel
BuildRequires:	gdbm-devel
BuildRequires:	gmp-devel
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(libffi) >= 3.1
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(uuid)
#BuildRequires:	python2
%if %{with valgrind}
BuildRequires:	valgrind-devel
%endif
BuildConflicts:	python-pyxml
%ifnarch %{riscv}
BuildRequires:	clang
%endif
Obsoletes:	python3 < %{EVRD}
Provides:	python3 = %{EVRD}
Provides:	python3.9 = %{EVRD}
Provides:	python(abi) = %{dirver}
Provides:	/usr/bin/python%{dirver}mu
Conflicts:	tkinter3 < %{EVRD}
Conflicts:	%{libname}-devel < 3.1.2-4
Conflicts:	%{devname} < 3.2.2-3
Conflicts:	python-pyxml
%if %{with compat32}
BuildRequires:	devel(libexpat)
BuildRequires:	devel(libffi)
BuildRequires:	devel(libz)
BuildRequires:	devel(libbz2)
BuildRequires:	devel(libncursesw)
%endif

# Used to be separate packages, bundled with core now
%rename	python-ctypes
%rename	python-elementtree
%rename	python-base
%if %{with pip}
%rename	python-setuptools
%rename	python-pkg-resources
Provides:	python3egg(setuptools)
Provides:	python3egg(distribute)
%endif

%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC).

Programmers can write new built-in modules for Python in C or C++.
Python can be used as an extension language for applications that
need a programmable interface. This package contains most of the
standard Python modules, as well as modules for interfacing to the
Tix widget set for Tk and RPM.

Note that documentation for Python is provided in the python-docs
package.

%package -n %{libname}
Summary:	Shared libraries for Python %{version}
Group:		System/Libraries
Obsoletes:	%{_lib}python3.3 < 3.3.2-2

%description -n %{libname}
This packages contains Python shared object library.  Python is an
interpreted, interactive, object-oriented programming language often
compared to Tcl, Perl, Scheme or Java.

%package -n %{devname}
Summary:	The libraries and header files needed for Python development
Group:		Development/Python
Requires:	%{name} = %{EVRD}
Requires:	%{libname} = %{EVRD}
Requires:	python-pkg-resources
Provides:	%{name}-devel = %{EVRD}
Provides:	%{name}3-devel = %{EVRD}
Provides:	pkgconfig(python) = 3

%description -n %{devname}
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install %{devname} if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package docs
Summary:	Documentation for the Python programming language
Group:		Development/Python
Requires:	%{name} = %{EVRD}
Requires:	xdg-utils
BuildArch:	noarch
Obsoletes:	python3-docs < %{EVRD}

%description docs
The python-docs package contains documentation on the Python
programming language and interpreter.  The documentation is provided
in ASCII text files and in LaTeX source files.

Install the python-docs package if you'd like to use the documentation
for the Python language.

%package tkinter
Summary:	A graphical user interface for the Python scripting language
Group:		Development/Python
Requires:	%{name} = %{EVRD}
Requires:	tcl
Requires:	tk
Obsoletes:	tkinter3 < %{EVRD}

%description tkinter
The Tkinter (Tk interface) program is an graphical user interface for
the Python scripting language.

You should install the tkinter package if you'd like to use a graphical
user interface for Python programming.

%package tkinter-apps
Summary:	Various applications written using tkinter
Group:		Development/Python
Requires:	%{name}-tkinter = %{EVRD}
Obsoletes:	tkinter3-apps < %{EVRD}

%description tkinter-apps
Various applications written using tkinter.

%package test
Summary:	The self-test suite for the main python3 package
Group:		Development/Python
Requires:	%{name} = %{EVRD}

%description test
The self-test suite for the Python interpreter.
This is only useful to test Python itself.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Shared libraries for Python %{version} (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
This packages contains Python shared object library.  Python is an
interpreted, interactive, object-oriented programming language often
compared to Tcl, Perl, Scheme or Java.

%package -n %{dev32name}
Summary:	The libraries and header files needed for Python development (32-bit)
Group:		Development/Python
Requires:	%{devname} = %{EVRD}
Requires:	%{lib32name} = %{EVRD}

%description -n %{dev32name}
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install %{dev32name} if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package python32-libs
Summary:	Libraries for use with the 32-bit python interpreter
Group:		Development/Python
Requires:	%{lib32name} = %{EVRD}

%description python32-libs
Libraries for use with the 32-bit python interpreter
%endif

%prep
%autosetup -p1 -n Python-%{version}%{pre}

# docs
mkdir html
tar xf %{SOURCE1} -C html

find . -type f -print0 | xargs -0 sed -i -e 's@/usr/local/bin/python@%{_bindir}/python3.9@'

cat > README.omv << EOF
Python interpreter support readline completion by default.
This is only used with the interpreter. In order to remove it,
you can :
1) unset PYTHONSTARTUP when you login
2) create a empty file \$HOME/.pythonrc.py
3) change %{_sysconfdir}/pythonrc.py
EOF

#   Remove embedded copy of libffi:
for SUBDIR in darwin libffi_osx ; do
  rm -r Modules/_ctypes/$SUBDIR || exit 1 ;
done

# Ensure that internal copies of expat, libffi and zlib are not used.
rm -fr Modules/expat
rm -fr Modules/zlib

%build
# Various violations, including in object.h
# (tpg) https://maskray.me/blog/2021-05-09-fno-semantic-interposition
%global optflags %{optflags} -O2 -fPIC -fno-strict-aliasing -fno-semantic-interposition -Wl,-Bsymbolic
%global build_ldflags %{ldflags} -fno-semantic-interposition -Wl,-Bsymbolic

rm -f Modules/Setup.local

# Python's configure adds -std=c99 even for c++, clang doesn't like that
# combination at all
sed -i -e 's,-std=c99,,' configure.ac

%ifnarch %{ix86}
# Workaround for https://bugs.llvm.org/show_bug.cgi?id=49327
sed -i -e 's,-flto,-flto=thin,g' configure.ac
%endif

# (tpg) Determinism
export PYTHONHASHSEED=0

autoreconf -vfi
# FIXME why is autodetection broken?
export ax_cv_c_float_words_bigendian=no

export CONFIGURE_TOP="$(pwd)"

%if %{with compat32}
mkdir build32
cd build32
%configure32 \
	--without-ensurepip \
	--with-system-expat \
	--with-system-ffi \
	--disable-optimizations \
	--enable-shared \
	--enable-ipv6 \
	--with-ssl-default-suites=openssl \
	--with-computed-gotos
unset CFLAGS CXXFLAGS CPPFLAGS RPM_OPT_FLAGS LDFLAGS RPM_LD_FLAGS
make
cd ..
%endif

# to fix curses module build
# https://bugs.mageia.org/show_bug.cgi?id=6702
export OPT="%{optflags} -g"
export CFLAGS="%{optflags} -D_GNU_SOURCE -fPIC -fwrapv -I/usr/include/ncursesw"
export CPPFLAGS="%{optflags} -D_GNU_SOURCE -fPIC -fwrapv -I/usr/include/ncursesw"
export LDFLAGS="${CFLAGS}"

mkdir build
cd build
%configure \
	--enable-ipv6 \
	--with-dbmliborder=gdbm \
%if %{with pip}
	--with-ensurepip=install \
%else
	--without-ensurepip \
%endif
	--with-platlibdir=%{_lib} \
	--with-system-expat \
	--with-cxx-main=%{__cxx} \
	--with-system-ffi \
	--enable-loadable-sqlite-extensions \
	--enable-shared \
	--with-pymalloc \
	--enable-ipv6=yes \
	--with-lto=16 \
	--with-computed-gotos=yes \
	--with-ssl-default-suites=openssl \
%if %{with valgrind}
	--with-valgrind \
%endif
	--disable-optimizations

# (misc) if the home is nfs mounted, rmdir fails due to delay
export TMP="/tmp" TMPDIR="/tmp"
# This is used for bootstrapping - and we don't want to
# require ourselves
sed -i -e 's,env python,python2,' ../Python/makeopcodetargets.py
%ifarch riscv64
# wipe 11 hours of tests
rm -frv Lib/test/test_*
%endif
%make_build PYTHON=python2 -j1

%check
# (misc) if the home is nfs mounted, rmdir fails
export TMP="/tmp" TMPDIR="/tmp"

# Currently (3.3.0-1), LOTS of tests fail, but python3 seems to work
# quite fine anyway. Chances are something in the testsuite itself is bogus.
#make test TESTOPTS="-w -x test_linuxaudiodev -x test_nis -x test_shutil -x test_pyexpat -x test_minidom -x test_sax -x test_string -x test_str -x test_unicode -x test_userstring -x test_bytes -x test_distutils -x test_mailbox -x test_ioctl -x test_telnetlib -x test_strtod -x test_urllib2net -x test_runpy -x test_posix -x test_robotparser -x test_numeric_tower -x test_math -x test_cmath -x test_importlib -x test_import -x test_float -x test_strtod -x test_timeout"

%install
mkdir -p %{buildroot}%{_prefix}/lib/python%{dirver}

# fix Makefile to get rid of reference to distcc
perl -pi -e "/^CC=/ and s|distcc|%{__cc}|" Makefile

# set the install path
echo '[install_scripts]' >setup.cfg
echo 'install_dir='"%{buildroot}%{_bindir}" >>setup.cfg

# python is not GNU and does not know fsstd
mkdir -p %{buildroot}%{_mandir}
%if %{with compat32}
%make_install -C build32 LN="ln -sf"
mv %{buildroot}%{_includedir}/python%{dirver}/pyconfig.h %{buildroot}%{_includedir}/python%{dirver}/pyconfig-32.h 
%endif
%make_install -C build LN="ln -sf"
%if %{with compat32}
mv %{buildroot}%{_includedir}/python%{dirver}/pyconfig.h %{buildroot}%{_includedir}/python%{dirver}/pyconfig-64.h 
cat >%{buildroot}%{_includedir}/python%{dirver}/pyconfig.h <<'EOF'
#ifdef __i386__
#include "pyconfig-32.h"
#else
#include "pyconfig-64.h"
#endif
EOF
%endif

(cd %{buildroot}%{_libdir}; ln -sf $(ls libpython%{api}*.so.*) libpython%{api}.so)

# install pynche
cat << EOF > %{buildroot}%{_bindir}/pynche
#!/bin/bash
exec %{_libdir}/python%{dirver}/site-packages/pynche/pynche
EOF
rm -f Tools/pynche/*.pyw
cp -r Tools/pynche %{buildroot}%{_libdir}/python%{dirver}/site-packages/

chmod 755 %{buildroot}%{_bindir}/{idle3,pynche}

ln -f Tools/pynche/README Tools/pynche/README.pynche

%if %{with valgrind}
install Misc/valgrind-python.supp -D %{buildroot}%{_libdir}/valgrind/valgrind-python3.supp
%endif

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-tkinter3.desktop << EOF
[Desktop Entry]
Name=IDLE
Comment=IDE for Python3
Exec=%{_bindir}/idle3
Icon=development_environment_section
Terminal=false
Type=Application
Categories=Development;IDE;
EOF

cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-docs.desktop << EOF
[Desktop Entry]
Name=Python documentation
Comment=Python complete reference
Exec=%{_bindir}/xdg-open %{_defaultdocdir}/%{name}-docs/index.html
Icon=documentation_section
Terminal=false
Type=Application
Categories=Documentation;
EOF

# fix non real scripts
#chmod 644 %{buildroot}%{_libdir}/python*/test/test_{binascii,grp,htmlparser}.py*
find %{buildroot} -type f \( -name "test_binascii.py*" -o -name "test_grp.py*" -o -name "test_htmlparser.py*" \) -exec chmod 644 {} \;
# fix python library not stripped
chmod u+w %{buildroot}%{_libdir}/libpython%{api}*.so.1.0 %{buildroot}%{_libdir}/libpython3.so

# drop backup files
find %{buildroot} -name "*~" -delete
find . -name "*~" -delete

# Get rid of DOS batch files:
find %{buildroot} -name \*.bat -delete
# Get rid of EXE files:
find %{buildroot} -name \*.exe -delete

mkdir -p %{buildroot}%{_sysconfdir}/profile.d/

cat > %{buildroot}%{_sysconfdir}/profile.d/30python.sh << 'EOF'
if [ -f $HOME/.pythonrc.py ] ; then
    export PYTHONSTARTUP=$HOME/.pythonrc.py
else
    export PYTHONSTARTUP=/etc/pythonrc.py
fi

export PYTHONDONTWRITEBYTECODE=1
EOF

cat > %{buildroot}%{_sysconfdir}/profile.d/30python.csh << 'EOF'
if ( -f ${HOME}/.pythonrc.py ) then
    setenv PYTHONSTARTUP ${HOME}/.pythonrc.py
else
    setenv PYTHONSTARTUP /etc/pythonrc.py
endif
setenv PYTHONDONTWRITEBYTECODE 1
EOF

cat > %{buildroot}%{_sysconfdir}/pythonrc.py << EOF
try:
    # this add completion to python interpreter
    import readline
    import rlcompleter
    # see readline man page for this
    readline.parse_and_bind("set show-all-if-ambiguous on")
    readline.parse_and_bind("tab: complete")
except:
    pass
# you can place a file .pythonrc.py in your home to overrides this one
# but then, this file will not be sourced
EOF

mkdir -p %{buildroot}%{_sysconfdir}/rpm/macros.d
install -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/rpm/macros.d/
install -m644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/rpm/macros.d/

# Install pathfix.py to bindir
# See https://github.com/fedora-python/python-rpm-porting/issues/24
cp -p Tools/scripts/pathfix.py %{buildroot}%{_bindir}/

# Fix permissions on docs
find html -type d |xargs chmod 0755
find html -type f |xargs chmod 0644

# remove  stuff provided by system python 3
rm -f %{buildroot}%{_bindir}/{2to3,pydoc3,python3,pyvenv,pip3,python3-config}
rm -f %{buildroot}%{_libdir}/pkgconfig/python3.pc %{buildroot}%{_libdir}/pkgconfig/python3-embed.pc
rm -f %{buildroot}%{_mandir}/man1/python3.1*
rm -f %{buildroot}%{_libdir}/libpython3.so

# Barf if an important module required by dnf didn't build
# (e.g. due to broken dependency libraries)
[ -e %{buildroot}%{_libdir}/python*/lib-dynload/_curses.*.so ] || exit 1
[ -e %{buildroot}%{_libdir}/python*/lib-dynload/_lzma.*.so ] || exit 1

%files
%doc README.omv
%{_sysconfdir}/rpm/macros.d/*.macros
%{_sysconfdir}/profile.d/*
%config(noreplace) %{_sysconfdir}/pythonrc.py
%{_includedir}/python*/pyconfig.h
%if %{with compat32}
%{_includedir}/python*/pyconfig-64.h
%endif

%dir %{_libdir}/python*/config-*
%{_libdir}/python*/config*/Makefile
%exclude %{_libdir}/python*/site-packages/pynche
%exclude %{_libdir}/python*/lib-dynload/_tkinter.*.so

# HACK: build fails without this (TODO: investigate rpm)
%dir %{_libdir}/python*
%{_libdir}/python*/LICENSE.txt
%{_libdir}/python%{dirver}/*.py
%{_libdir}/python%{dirver}/__pycache__
%{_libdir}/python%{dirver}/asyncio
%{_libdir}/python%{dirver}/collections
%{_libdir}/python%{dirver}/concurrent
%{_libdir}/python%{dirver}/ctypes
%exclude %{_libdir}/python%{dirver}/ctypes/test
%{_libdir}/python%{dirver}/curses
%{_libdir}/python%{dirver}/dbm
%{_libdir}/python%{dirver}/distutils
%exclude %{_libdir}/python%{dirver}/distutils/tests
%{_libdir}/python%{dirver}/email
%{_libdir}/python%{dirver}/encodings
%{_libdir}/python%{dirver}/ensurepip
%{_libdir}/python%{dirver}/html
%{_libdir}/python%{dirver}/http
%{_libdir}/python%{dirver}/importlib
%{_libdir}/python%{dirver}/json
%{_libdir}/python%{dirver}/lib-dynload
%exclude %{_libdir}/python%{dirver}/lib-dynload/_ctypes_test.*.so
%exclude %{_libdir}/python%{dirver}/lib-dynload/_testbuffer.*.so
%exclude %{_libdir}/python%{dirver}/lib-dynload/_testcapi.*.so
%exclude %{_libdir}/python%{dirver}/lib-dynload/_testimportmultiple.*.so
%{_libdir}/python%{dirver}/lib2to3
%exclude %{_libdir}/python%{dirver}/lib2to3/tests
%{_libdir}/python%{dirver}/logging
%{_libdir}/python%{dirver}/multiprocessing
%{_libdir}/python%{dirver}/pydoc_data
%{_libdir}/python%{dirver}/site-packages
%{_libdir}/python%{dirver}/sqlite3
%exclude %{_libdir}/python%{dirver}/sqlite3/test
%{_libdir}/python%{dirver}/unittest
%exclude %{_libdir}/python%{dirver}/unittest/test
%{_libdir}/python%{dirver}/urllib
%{_libdir}/python%{dirver}/venv
%{_libdir}/python%{dirver}/wsgiref*
%{_libdir}/python%{dirver}/xml
%{_libdir}/python%{dirver}/xmlrpc
%{_libdir}/python%{dirver}/zoneinfo
%{_bindir}/pydoc3*
%{_bindir}/pathfix.py
%{_bindir}/python3*
%{_bindir}/2to3-%{dirver}
%exclude %{_bindir}/python*config
%if %{with valgrind}
%{_libdir}/valgrind/valgrind-python3.supp
%endif
# pip bits
%if %{with pip}
%if "%{_libdir}" != "%{_prefix}/lib"
# In the %{_libdir} == %{_prefix}/lib case, those are caught by
# globs above.
%dir %{_prefix}/lib/python%{dirver}
%dir %{_prefix}/lib/python%{dirver}/site-packages
%{_prefix}/lib/python%{dirver}/site-packages/__pycache__
%{_prefix}/lib/python%{dirver}/site-packages/pkg_resources.py
%{_prefix}/lib/python%{dirver}/site-packages/easy_install.py
%{_prefix}/lib/python%{dirver}/site-packages/pip
%{_prefix}/lib/python%{dirver}/site-packages/setuptools*
%{_prefix}/lib/python%{dirver}/site-packages/_markerlib
%{_prefix}/lib/python%{dirver}/site-packages/pip-*.dist-info
%endif
%{_bindir}/easy_install-%{dirver}
%{_bindir}/pip3
%{_bindir}/pip%{dirver}
%endif

%files -n %{libname}
%{_libdir}/libpython%{api}.so.%{major}*

%files -n %{devname}
%{_libdir}/libpython*.so
%{_includedir}/python*
%{_libdir}/python*/config-%{dirver}*
%{_bindir}/python%{dirver}*-config
%{_libdir}/pkgconfig/python*.pc
%exclude %{_includedir}/python*/pyconfig.h
%if %{with compat32}
%exclude %{_includedir}/python*/pyconfig-32.h
%exclude %{_includedir}/python*/pyconfig-64.h
%endif
%exclude %{_libdir}/python*/config*/Makefile

%files docs
%doc html/*/*
%{_datadir}/applications/mandriva-%{name}-docs.desktop
%{_mandir}/man*/*

%files tkinter
%{_libdir}/python*/tkinter/
%exclude %{_libdir}/python%{dirver}/tkinter/test
%{_libdir}/python%{dirver}/turtledemo
%{_libdir}/python*/idlelib
%{_libdir}/python*/site-packages/pynche
%{_libdir}/python*/lib-dynload/_tkinter.*.so

%files tkinter-apps
%{_bindir}/idle3*
%{_bindir}/pynche
%{_datadir}/applications/mandriva-tkinter3.desktop

%files test
%{_libdir}/python*/test/
%{_libdir}/python%{dirver}/ctypes/test
%{_libdir}/python%{dirver}/distutils/tests
%{_libdir}/python%{dirver}/sqlite3/test
%{_libdir}/python%{dirver}/lib-dynload/_ctypes_test.*.so
%{_libdir}/python%{dirver}/lib-dynload/_testbuffer.*.so
%{_libdir}/python%{dirver}/lib-dynload/_testcapi.*.so
%{_libdir}/python%{dirver}/lib-dynload/_testimportmultiple.*.so
%{_libdir}/python%{dirver}/lib2to3/tests
%{_libdir}/python%{dirver}/tkinter/test
%{_libdir}/python%{dirver}/unittest/test

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libpython%{api}.so.%{major}*

%files -n %{dev32name}
%{_includedir}/python*/pyconfig-32.h
%{_prefix}/lib/libpython*.so
%{_prefix}/lib/pkgconfig/python*.pc

%files python32-libs
%{_prefix}/lib/python%{dirver}/lib-dynload
%dir %{_prefix}/lib/python%{dirver}
%{_prefix}/lib/python%{dirver}/LICENSE.txt
%{_prefix}/lib/python%{dirver}/*.py
%{_prefix}/lib/python%{dirver}/__pycache__
%{_prefix}/lib/python%{dirver}/asyncio
%{_prefix}/lib/python%{dirver}/collections
%{_prefix}/lib/python%{dirver}/concurrent
%{_prefix}/lib/python%{dirver}/ctypes
%{_prefix}/lib/python%{dirver}/curses
%{_prefix}/lib/python%{dirver}/dbm
%{_prefix}/lib/python%{dirver}/distutils
%{_prefix}/lib/python%{dirver}/email
%{_prefix}/lib/python%{dirver}/encodings
%{_prefix}/lib/python%{dirver}/ensurepip
%{_prefix}/lib/python%{dirver}/html
%{_prefix}/lib/python%{dirver}/http
%{_prefix}/lib/python%{dirver}/idlelib
%{_prefix}/lib/python%{dirver}/importlib
%{_prefix}/lib/python%{dirver}/json
%{_prefix}/lib/python%{dirver}/lib2to3
%{_prefix}/lib/python%{dirver}/logging
%{_prefix}/lib/python%{dirver}/multiprocessing
%{_prefix}/lib/python%{dirver}/pydoc_data
%{_prefix}/lib/python%{dirver}/sqlite3
%{_prefix}/lib/python%{dirver}/test
%{_prefix}/lib/python%{dirver}/tkinter
%{_prefix}/lib/python%{dirver}/turtledemo
%{_prefix}/lib/python%{dirver}/unittest
%{_prefix}/lib/python%{dirver}/urllib
%{_prefix}/lib/python%{dirver}/venv
%{_prefix}/lib/python%{dirver}/wsgiref
%{_prefix}/lib/python%{dirver}/xml
%{_prefix}/lib/python%{dirver}/xmlrpc
%{_prefix}/lib/python%{dirver}/zoneinfo
%{_prefix}/lib/python%{dirver}/config-*
%dir %{_prefix}/lib/python%{dirver}/site-packages
%{_prefix}/lib/python%{dirver}/site-packages/README.txt
%endif

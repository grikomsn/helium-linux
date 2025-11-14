# Helium RPM Spec File for Fedora
# Based on ungoogled-chromium-fedora and Fedora Chromium packaging

%global debug_package %{nil}
%global _build_id_links none

Name:           helium
Version:        0.6.5.1
Release:        1%{?dist}
Summary:        A privacy-focused web browser based on Chromium

License:        GPL-3.0 AND BSD-3-Clause
URL:            https://helium.computer/
# Source tarball would be generated from build process or GitHub release
Source0:        %{name}-%{version}.tar.xz
Source1:        helium.desktop

BuildRequires:  bison
BuildRequires:  clang
BuildRequires:  desktop-file-utils
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gperf
BuildRequires:  ImageMagick
BuildRequires:  lld
BuildRequires:  ninja-build
BuildRequires:  nodejs >= 22
BuildRequires:  npm
BuildRequires:  python3
BuildRequires:  python3-jinja2
BuildRequires:  python3-setuptools
BuildRequires:  yasm

# Development libraries
BuildRequires:  alsa-lib-devel
BuildRequires:  atk-devel
BuildRequires:  cairo-devel
BuildRequires:  cups-devel
BuildRequires:  dbus-devel
BuildRequires:  expat-devel
BuildRequires:  flac-devel
BuildRequires:  glib2-devel
BuildRequires:  gtk3-devel
BuildRequires:  hunspell-devel
BuildRequires:  krb5-devel
BuildRequires:  libcap-devel
BuildRequires:  libcurl-devel
BuildRequires:  libdrm-devel
BuildRequires:  libevent-devel
BuildRequires:  libexif-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libva-devel
BuildRequires:  libvpx-devel
BuildRequires:  libwebp-devel
BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXext-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libXi-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXrender-devel
BuildRequires:  libxshmfence-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libxslt-devel
BuildRequires:  libXtst-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  minizip-devel
BuildRequires:  nspr-devel
BuildRequires:  nss-devel
BuildRequires:  opus-devel
BuildRequires:  pam-devel
BuildRequires:  pango-devel
BuildRequires:  pciutils-devel
BuildRequires:  pipewire-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  re2-devel
BuildRequires:  snappy-devel
BuildRequires:  speech-dispatcher-devel
BuildRequires:  systemd-devel
BuildRequires:  zlib-devel

# Runtime dependencies
Requires:       alsa-lib
Requires:       atk
Requires:       cairo
Requires:       cups-libs
Requires:       dbus-libs
Requires:       expat
Requires:       flac-libs
Requires:       glib2
Requires:       gtk3
Requires:       hunspell
Requires:       krb5-libs
Requires:       libcap
Requires:       libcurl
Requires:       libdrm
Requires:       libevent
Requires:       libgcrypt
Requires:       libjpeg-turbo
Requires:       libpng
Requires:       libva
Requires:       libvpx
Requires:       libwebp
Requires:       libX11
Requires:       libxcb
Requires:       libXcomposite
Requires:       libXcursor
Requires:       libXdamage
Requires:       libXext
Requires:       libXfixes
Requires:       libXi
Requires:       libXrandr
Requires:       libXrender
Requires:       libXScrnSaver
Requires:       libXtst
Requires:       mesa-libEGL
Requires:       mesa-libGL
Requires:       mesa-libGLES
Requires:       nspr
Requires:       nss
Requires:       opus
Requires:       pango
Requires:       pulseaudio-libs
Requires:       snappy
Requires:       speech-dispatcher

%description
Helium is a privacy-focused web browser based on Chromium. It includes
enhanced privacy features and removes various Google integrations while
maintaining full web compatibility.

This browser is designed for users who value privacy and want a
de-Googled browsing experience without sacrificing functionality.

%prep
%setup -q

%build
# Build process would be integrated here
# This spec file assumes pre-built binaries from existing build process
# In production, this would invoke scripts/build.sh or similar
echo "Using pre-built Helium binaries"

%install
rm -rf %{buildroot}

# Create directory structure
install -d %{buildroot}%{_libdir}/helium
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/applications
install -d %{buildroot}%{_datadir}/icons/hicolor/256x256/apps

# Install main application files
# These files would come from the build output
cp -a chrome %{buildroot}%{_libdir}/helium/
cp -a chrome_100_percent.pak %{buildroot}%{_libdir}/helium/
cp -a chrome_200_percent.pak %{buildroot}%{_libdir}/helium/
cp -a chrome_crashpad_handler %{buildroot}%{_libdir}/helium/
cp -a chromedriver %{buildroot}%{_libdir}/helium/
cp -a chrome-wrapper %{buildroot}%{_libdir}/helium/
cp -a icudtl.dat %{buildroot}%{_libdir}/helium/
cp -a libEGL.so %{buildroot}%{_libdir}/helium/
cp -a libGLESv2.so %{buildroot}%{_libdir}/helium/
cp -a libqt5_shim.so %{buildroot}%{_libdir}/helium/
cp -a libqt6_shim.so %{buildroot}%{_libdir}/helium/
cp -a libvk_swiftshader.so %{buildroot}%{_libdir}/helium/
cp -a libvulkan.so.1 %{buildroot}%{_libdir}/helium/
cp -a product_logo_256.png %{buildroot}%{_libdir}/helium/
cp -a resources.pak %{buildroot}%{_libdir}/helium/
cp -a v8_context_snapshot.bin %{buildroot}%{_libdir}/helium/
cp -a vk_swiftshader_icd.json %{buildroot}%{_libdir}/helium/
cp -a xdg-mime %{buildroot}%{_libdir}/helium/
cp -a xdg-settings %{buildroot}%{_libdir}/helium/
cp -a locales %{buildroot}%{_libdir}/helium/

# Create wrapper script
cat > %{buildroot}%{_bindir}/helium << 'EOF'
#!/bin/sh
CHROME_WRAPPER="%{_bindir}/helium"
export CHROME_WRAPPER
exec %{_libdir}/helium/chrome "$@"
EOF
chmod 755 %{buildroot}%{_bindir}/helium

# Install desktop file
desktop-file-install \
    --dir=%{buildroot}%{_datadir}/applications \
    %{SOURCE1}

# Install icon
install -m 644 product_logo_256.png \
    %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/helium.png

%post
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license LICENSE
%doc README.md
%{_bindir}/helium
%{_libdir}/helium/
%{_datadir}/applications/helium.desktop
%{_datadir}/icons/hicolor/256x256/apps/helium.png

%changelog
* Thu Nov 14 2024 Helium Team <helium@imput.net> - 0.6.5.1-1
- Initial RPM package for Helium
- Based on Helium 0.6.5.1
- Includes desktop integration and system library dependencies

%global debug_package %{nil}

Name:           helium
Version:        %{version}
Release:        1%{?dist}
Summary:        Privacy-focused Chromium-based web browser

License:        GPL-3.0
URL:            https://helium.computer/
Source0:        helium-%{version}-%{_arch}_linux.tar.xz

BuildArch:      %{_arch}

Requires:       gtk3
Requires:       nss
Requires:       alsa-lib
Requires:       libXScrnSaver
Requires:       liberation-fonts
Requires:       at-spi2-atk
Requires:       libdrm
Requires:       mesa-libgbm

%description
Helium is a privacy-focused Chromium-based web browser that provides
a secure and private browsing experience. It removes Google-specific
integrations and telemetry while maintaining compatibility with the
Chromium ecosystem.

%prep
%setup -q -n helium-%{version}-%{_arch}_linux

%build
# Binary distribution, no build needed

%install
# Create installation directories
install -d %{buildroot}%{_libdir}/%{name}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/applications
install -d %{buildroot}%{_datadir}/icons/hicolor/256x256/apps

# Copy all files to lib directory
cp -r * %{buildroot}%{_libdir}/%{name}/

# Create wrapper script
cat > %{buildroot}%{_bindir}/%{name} << 'EOF'
#!/bin/bash
exec %{_libdir}/%{name}/chrome "$@"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

# Install desktop file
sed 's|Exec=chromium|Exec=%{name}|g' helium.desktop > %{buildroot}%{_datadir}/applications/%{name}.desktop

# Install icon
install -m 0644 product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

%files
%{_libdir}/%{name}/
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

%changelog
* %(date "+%a %b %d %Y") Helium Team <helium@imput.net> - %{version}-1
- Automated build from helium-linux repository

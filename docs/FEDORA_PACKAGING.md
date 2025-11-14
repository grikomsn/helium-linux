# Fedora Packaging and Distribution

## Overview

This document outlines the distribution options for Helium on Fedora systems.

## Current Distribution Methods

Helium for Linux is distributed in multiple formats:
- **RPM packages** - Native Fedora packages for easy installation via dnf
- **AppImage** - Portable, self-contained format that works across all Linux distributions
- **tar.xz archives** - Traditional tarball format for manual installation

All formats are built automatically via GitHub Actions and published to [GitHub Releases](https://github.com/imputnet/helium-linux/releases).

## Installation Options

### 1. RPM Package Installation (Recommended for Fedora)

RPM packages provide the best integration with Fedora systems.

**Pros:**
- ✅ Native package manager integration
- ✅ Automatic desktop integration
- ✅ Easy installation and updates via dnf
- ✅ System-wide installation
- ✅ Familiar for Fedora users

**Installation:**
```bash
# Download the RPM package
wget https://github.com/imputnet/helium-linux/releases/download/VERSION/helium-VERSION-1.fc*.x86_64.rpm

# Install with dnf
sudo dnf install ./helium-VERSION-1.fc*.x86_64.rpm

# Launch from application menu or terminal
helium
```

**Updating:**
```bash
# Download new version
wget https://github.com/imputnet/helium-linux/releases/download/NEW_VERSION/helium-NEW_VERSION-1.fc*.x86_64.rpm

# Update with dnf
sudo dnf update ./helium-NEW_VERSION-1.fc*.x86_64.rpm
```

**Uninstalling:**
```bash
sudo dnf remove helium
```

### 2. Direct AppImage Distribution (Alternative)

AppImage is recommended for users who want a portable installation or are using multiple Linux distributions.

### 2. Direct AppImage Distribution (Alternative)

AppImage is recommended for users who want a portable installation or are using multiple Linux distributions.

**Pros:**
- ✅ Works on Fedora and all other Linux distributions
- ✅ No installation required - download and run
- ✅ Users don't need root access
- ✅ Easy to update and remove
- ✅ Self-contained with all dependencies

**Cons:**
- ⚠️ Less integrated with Fedora's package manager
- ⚠️ Desktop integration requires manual setup or tools like AppImageLauncher

**How to use on Fedora:**
```bash
# Download the AppImage
wget https://github.com/imputnet/helium-linux/releases/download/VERSION/helium-VERSION-x86_64.AppImage

# Make it executable
chmod +x helium-VERSION-x86_64.AppImage

# Run it
./helium-VERSION-x86_64.AppImage
```

For better desktop integration, Fedora users can install AppImageLauncher:
```bash
sudo dnf install appimagelauncher
```

## RPM Package Details

### Architecture Support

RPM packages are provided for:
- **x86_64** (Intel/AMD 64-bit)
- **aarch64** (ARM 64-bit)

### Dependencies

The RPM package requires the following system packages:
- gtk3
- nss
- alsa-lib
- libXScrnSaver
- liberation-fonts
- at-spi2-atk
- libdrm
- mesa-libgbm

These are automatically installed by dnf when you install the Helium RPM.

### Package Contents

The RPM package installs:
- Browser binary and libraries: `/usr/lib64/helium/`
- Launcher script: `/usr/bin/helium`
- Desktop file: `/usr/share/applications/helium.desktop`
- Application icon: `/usr/share/icons/hicolor/256x256/apps/helium.png`

## Building RPM Packages Locally

If you want to build RPM packages yourself:

```bash
# Clone the repository
git clone --recursive https://github.com/imputnet/helium-linux.git
cd helium-linux

# Build using Docker
./scripts/docker-build.sh

# Package (creates tar.xz and AppImage)
./scripts/package.sh

# Build RPM
./package/docker-build-rpm.sh
```

The RPM file will be created in `build/release/`.

## Removed Sections

### RPM Package Wrapping AppImage (Previously Not Recommended)

This section has been removed as we now provide native RPM packages built from the tarball distribution. The RPM packages provide proper system integration without the limitations of wrapped AppImages.

## Future Enhancements

If there's sufficient interest from the Fedora community, the following could be considered:

1. **Copr Repository Setup**
   - Automated builds via GitHub Actions
   - Native RPM packages for Fedora 39, 40, 41+
   - Automatic updates via dnf

2. **Flathub Distribution**
   - Alternative universal Linux packaging
   - Similar benefits to AppImage with better desktop integration
   - Requires maintaining Flatpak manifest

3. **Official Fedora Package**
   - Submit to Fedora repositories
   - Highest level of integration
   - Very high barrier to entry (review process, maintenance requirements)

## Resources

- [Fedora Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/)
- [Fedora AppImage Wiki](https://fedoraproject.org/wiki/AppImage)
- [AppImage Best Practices](https://docs.appimage.org/reference/best-practices.html)
- [Copr Build GitHub Action](https://github.com/marketplace/actions/copr-build)
- [Creating RPM Packages - Fedora Docs](https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/)

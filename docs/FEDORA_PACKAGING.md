# Fedora Packaging and Distribution

## Overview

This document outlines the options for distributing Helium on Fedora systems and explains the current approach.

## Current Distribution Method

Helium for Linux is currently distributed as:
- **AppImage** - Portable, self-contained format that works across all Linux distributions
- **tar.xz archives** - Traditional tarball format for manual installation

Both formats are built automatically via GitHub Actions and published to [GitHub Releases](https://github.com/imputnet/helium-linux/releases).

## Fedora Distribution Options Evaluated

### 1. Direct AppImage Distribution (Current - Recommended)

**Pros:**
- ✅ Works on Fedora and all other Linux distributions
- ✅ No installation required - download and run
- ✅ Users don't need root access
- ✅ Easy to update and remove
- ✅ Self-contained with all dependencies
- ✅ Already implemented and working

**Cons:**
- ⚠️ Less integrated with Fedora's package manager (dnf)
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

### 2. RPM Package Wrapping AppImage (Not Recommended)

Some projects create RPM packages that simply wrap the AppImage for installation via dnf.

**Pros:**
- Desktop integration is automatic
- Familiar installation method for Fedora users

**Cons:**
- ❌ Negates the portability benefits of AppImage
- ❌ Adds packaging complexity and maintenance burden
- ❌ Against AppImage best practices
- ❌ Requires separate packaging workflow
- ❌ Duplicates effort without significant benefit

**Conclusion:** Not recommended. Fedora users who want AppImages can use them directly.

### 3. Native Fedora RPM via Copr (Future Consideration)

Building native RPM packages from source and hosting them in a Fedora Copr repository.

**Pros:**
- ✅ Full Fedora integration
- ✅ Automatic updates via dnf
- ✅ Familiar for Fedora users
- ✅ Can be automated with GitHub Actions

**Cons:**
- ❌ Requires maintaining separate build pipeline
- ❌ Need to build for multiple Fedora versions
- ❌ Chromium builds are extremely resource-intensive
- ❌ Significant ongoing maintenance effort
- ❌ Copr has resource limits for large packages

**Implementation approach (if pursued):**
1. Create RPM spec file for native build
2. Set up Fedora Copr project
3. Use [copr-build GitHub Action](https://github.com/marketplace/actions/copr-build)
4. Automate builds on new releases

**Conclusion:** Could be valuable for Fedora-native users but requires significant resources. Consider if there's sufficient demand from the Fedora community.

## Recommendation

**Continue with current approach: Direct AppImage distribution via GitHub Releases**

This is the most practical solution because:
1. Already implemented and working well
2. Provides maximum compatibility across distributions
3. Minimal maintenance burden
4. Users who want native Fedora packages can create them locally if needed

## For Fedora Users

### Using AppImage on Fedora

The AppImage format is officially supported on Fedora. See the [Fedora AppImage Wiki](https://fedoraproject.org/wiki/AppImage) for details.

**Quick start:**
1. Download the appropriate AppImage for your architecture (x86_64 or arm64)
2. Make it executable: `chmod +x helium-*.AppImage`
3. Run it: `./helium-*.AppImage`

**For desktop integration:**
Install AppImageLauncher which provides automatic integration:
```bash
sudo dnf install appimagelauncher
```

After installing AppImageLauncher, when you run an AppImage for the first time, you'll be prompted to integrate it into your system. This will:
- Add Helium to your application menu
- Associate it with supported file types
- Enable easy updates and removal

### Building Native RPM Locally (Advanced)

If you prefer a native RPM package, you can build it locally. This requires:
1. A powerful machine (Chromium builds need significant resources)
2. Several hours of build time
3. Familiarity with RPM packaging

The build process is the same as documented in the main README:
```bash
# Clone the repository
git clone --recursive https://github.com/imputnet/helium-linux.git
cd helium-linux

# Build using Docker
./scripts/docker-build.sh

# Package
./scripts/package.sh
```

Then create an RPM spec file that packages the built binaries. Contact the maintainers if you need assistance with this approach.

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

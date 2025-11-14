# Fedora RPM Packaging Guide for Helium

This document outlines the approach, requirements, and implementation plan for creating Fedora RPM packages for Helium.

## Overview

Helium is currently distributed as an AppImage for portability across Linux distributions. Adding native Fedora RPM packages would provide better integration with Fedora's package management system (DNF) and improve the user experience for Fedora users.

## Why RPM Packaging?

### Benefits
- **Native Package Management**: Integration with DNF for easy installation, updates, and removal
- **System Integration**: Better integration with system libraries and SELinux policies
- **Dependency Management**: Automatic handling of runtime dependencies
- **Desktop Environment Integration**: Seamless integration with GNOME and KDE on Fedora
- **User Familiarity**: Fedora users are accustomed to installing software via RPM/DNF

### Distribution Options
1. **Fedora Copr** (Selected): Community-driven build system and repository for custom RPM packages
   - Repository: https://copr.fedorainfracloud.org/coprs/griko/helium-browser/
   - No official Fedora approval required
   - Automated builds for multiple Fedora versions and architectures
   - Easy for users to enable and use
   - Ideal for community/unofficial packages
   
2. **Direct Download**: Host RPM files on GitHub releases
   - Simple distribution method
   - Users manually download and install
   - No repository management needed

3. **Official Fedora Repositories** (future consideration)
   - Requires formal package review and approval
   - Highest level of trust and visibility
   - Long-term maintenance commitment

## Technical Requirements

### RPM Spec File Components

A Fedora RPM spec file for Helium must include:

1. **Preamble/Metadata**
   - Name: `helium` (or `helium-browser`)
   - Version: Extracted from `helium-chromium/utils/helium_version.py`
   - Release: Build number with `%{?dist}` macro
   - Summary: Brief description
   - License: GPL-3.0 (per repository LICENSE)
   - URL: https://helium.computer/
   - Source0: Tarball or build output reference

2. **Dependencies**
   - BuildRequires: All packages needed for compilation (mirrors docker/build.Dockerfile)
   - Requires: Runtime dependencies for the browser
   - System libraries should be used where possible (not bundled)

3. **Build Sections**
   - `%prep`: Extract/prepare source
   - `%build`: Compile Helium (may reference existing build.sh logic)
   - `%install`: Install files to buildroot
   - `%files`: List all files included in the package
   - `%post` / `%postun`: Post-install/uninstall scripts (update-desktop-database, etc.)

4. **Changelog**
   - Document version updates and significant changes

### Key Considerations for Chromium-Based Browsers

1. **System Libraries**: 
   - Prefer system libraries over bundled dependencies
   - Reduces package size and improves security maintainability
   - Aligns with Fedora packaging philosophy

2. **Multimedia Codecs**:
   - Fedora excludes patent-encumbered codecs by default
   - H.264, AAC, and other proprietary codecs may need RPM Fusion
   - Document codec limitations clearly

3. **SELinux Integration**:
   - Ensure Helium runs with proper SELinux confinement
   - Test with Fedora's default SELinux policies
   - May require custom policy modules

4. **Desktop Integration**:
   - Install `.desktop` file to `/usr/share/applications/`
   - Install icon to `/usr/share/icons/hicolor/256x256/apps/`
   - Register MIME types for web content
   - Update desktop database in `%post`

5. **File Locations** (FHS compliance):
   - Binary: `/usr/bin/helium` or `/usr/lib64/helium/chrome`
   - Libraries: `/usr/lib64/helium/`
   - Resources: `/usr/share/helium/`
   - Desktop file: `/usr/share/applications/helium.desktop`
   - Icon: `/usr/share/icons/hicolor/256x256/apps/helium.png`

## Implementation Approach

### Phase 1: Create Initial Spec File

Create `fedora/helium.spec` with:
- Basic package metadata
- Dependencies mirroring those in docker/build.Dockerfile
- Build instructions leveraging existing scripts/build.sh
- Installation paths following Fedora guidelines
- Desktop integration files

### Phase 2: RPM Build Script

Create `fedora/build-rpm.sh`:
- Set up RPM build tree structure
- Copy source files to appropriate locations
- Invoke `rpmbuild` with the spec file
- Output RPM to `build/` directory

### Phase 3: Testing

- Build RPM in clean Fedora container (Fedora 40, 41)
- Install RPM and verify:
  - Application launches successfully
  - Desktop integration works (menu entry, icon)
  - MIME type associations
  - No SELinux denials
- Test on both Fedora Workstation and Silverblue

### Phase 4: Distribution Setup

Fedora Copr repository has been set up at: https://copr.fedorainfracloud.org/coprs/griko/helium-browser/

**Copr Setup (Completed):**
1. ✅ Fedora Account System (FAS) account created
2. ✅ Copr project created for Helium
3. Upload spec file and sources to Copr
4. Configure automated builds from GitHub
5. Document installation instructions for users

**Installation for users:**
```bash
sudo dnf copr enable griko/helium-browser
sudo dnf install helium
```

**Alternative: GitHub Releases**
1. Build RPMs for multiple Fedora versions (38, 39, 40, 41)
2. Upload RPM files to GitHub releases alongside AppImage
3. Provide installation instructions in README

### Phase 5: Documentation Updates

Update repository documentation:
- README.md: Add Fedora installation section
- Installation instructions for RPM
- Instructions for enabling Copr repository (if applicable)
- Known limitations and codec information

## Build Dependencies

Based on existing docker/build.Dockerfile, RPM spec file BuildRequires should include:

```spec
BuildRequires: nodejs >= 22
BuildRequires: npm
BuildRequires: python3
BuildRequires: python3-jinja2
BuildRequires: python3-setuptools
BuildRequires: bison
BuildRequires: flex
BuildRequires: gperf
BuildRequires: ninja-build
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: clang
BuildRequires: lld
BuildRequires: yasm
BuildRequires: desktop-file-utils
BuildRequires: ImageMagick
# ... (additional dependencies from build.Dockerfile)
```

## Runtime Dependencies

```spec
Requires: gtk3
Requires: libX11
Requires: libXss
Requires: alsa-lib
Requires: nss
Requires: cups-libs
# ... (additional runtime libraries)
```

## Reference Projects

- **ungoogled-chromium-fedora**: https://github.com/ungoogled-software/ungoogled-chromium-fedora
  - Excellent reference for Chromium-based browser RPM packaging
  - Spec file structure and patch management
  - Build and test workflows

- **Fedora Chromium Package**: https://packages.fedoraproject.org/pkgs/chromium/
  - Official Fedora packaging approach
  - System integration examples

## Resources

- [Fedora Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/)
- [Fedora RPM Guide](https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/)
- [Fedora Copr Documentation](https://docs.pagure.org/copr.copr/)
- [RPM Spec File Reference](https://rpm-packaging-guide.github.io/)

## Next Steps

1. Create initial spec file based on this research
2. Create RPM build script
3. Test build in Fedora container
4. Decide on distribution method (Copr vs. direct download)
5. Document installation instructions for users

## Notes

- This approach leverages existing build infrastructure (scripts/build.sh)
- RPM packaging complements existing AppImage distribution (doesn't replace it)
- Fedora users can choose their preferred installation method
- Consider Silverblue/Kinoite compatibility (rpm-ostree)

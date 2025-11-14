# Fedora RPM Packaging

This directory contains files for creating Fedora RPM packages for Helium.

## Contents

- `helium.spec` - RPM spec file for building Helium packages
- `build-rpm.sh` - Script to build RPM packages
- `README.md` - This file

## Quick Start

### Prerequisites

Install RPM development tools on Fedora:

```bash
sudo dnf install -y rpmdevtools rpmlint fedora-packager
```

### Building the RPM

1. Ensure Helium is built first:
   ```bash
   cd /path/to/helium-linux
   ./scripts/docker-build.sh
   ```

2. Build the RPM:
   ```bash
   cd fedora
   ./build-rpm.sh
   ```

The resulting RPM will be in `~/rpmbuild/RPMS/x86_64/` (or appropriate architecture).

### Installing

```bash
sudo dnf install ~/rpmbuild/RPMS/x86_64/helium-*.rpm
```

## Distribution

### Fedora Copr (Primary Method)

Helium is available via Fedora Copr at: https://copr.fedorainfracloud.org/coprs/griko/helium-browser/

**For Users - Installation:**
```bash
sudo dnf copr enable griko/helium-browser
sudo dnf install helium
```

**For Maintainers - Uploading to Copr:**

1. Build the RPM locally (see "Building the RPM" above)
2. Log in to Copr: https://copr.fedorainfracloud.org/coprs/griko/helium-browser/
3. Upload the built SRPM or configure automated builds
4. Copr will build for all enabled Fedora versions and architectures

### Alternative: GitHub Releases

RPMs can also be distributed via GitHub releases alongside AppImage:

1. Build RPM for target Fedora versions
2. Upload to GitHub releases
3. Users download and install manually:
   ```bash
   sudo dnf install ./helium-0.6.5.1-1.fc40.x86_64.rpm
   ```

### Future: Official Fedora Repositories

For inclusion in official Fedora repositories:

1. Submit package for review: https://docs.fedoraproject.org/en-US/package-maintainers/
2. Address review feedback
3. Maintain package long-term

## Spec File Details

The `helium.spec` file includes:

- **BuildRequires**: All build dependencies from docker/build.Dockerfile
- **Requires**: Runtime library dependencies
- **%install**: Installs files to FHS-compliant locations
- **%files**: Lists all packaged files
- **%post/%postun**: Desktop database and icon cache updates

### File Locations

- Binary wrapper: `/usr/bin/helium`
- Application files: `/usr/lib64/helium/`
- Desktop file: `/usr/share/applications/helium.desktop`
- Icon: `/usr/share/icons/hicolor/256x256/apps/helium.png`

## Testing

Test the RPM in a clean Fedora container:

```bash
# Create test container
podman run -it --rm -v ~/rpmbuild/RPMS:/rpms:ro fedora:40 bash

# Inside container
dnf install -y /rpms/x86_64/helium-*.rpm

# Verify files
rpm -ql helium

# Test launch (requires X11 forwarding or Wayland)
helium --version
```

## Known Limitations

1. **Pre-built binaries**: Current spec file assumes pre-built binaries from existing build process
2. **Codecs**: Patent-encumbered codecs (H.264, AAC) may not be included per Fedora policy
3. **Full rebuild**: Integrating full Chromium rebuild in spec file requires significant work

## Future Improvements

- [ ] Integrate full build process into spec file (may not be practical)
- [x] Set up Copr repository for automated builds (https://copr.fedorainfracloud.org/coprs/griko/helium-browser/)
- [ ] Configure automated builds from GitHub releases
- [ ] Add SELinux policy if needed
- [ ] Support multiple Fedora versions (38, 39, 40, 41)
- [ ] Add RPM signing with GPG key
- [ ] Create SRPM for source distribution

## Resources

- [Fedora Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/)
- [Fedora Copr](https://copr.fedorainfracloud.org/)
- [ungoogled-chromium-fedora](https://github.com/ungoogled-software/ungoogled-chromium-fedora)

## Notes

This RPM packaging is intended to complement, not replace, the existing AppImage distribution. Fedora users can choose their preferred installation method.

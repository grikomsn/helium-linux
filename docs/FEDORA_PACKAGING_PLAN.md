# Fedora Distribution Package - Research and Planning

## Executive Summary

This document presents the research findings and implementation plan for creating Fedora RPM packages for Helium, a privacy-focused Chromium-based web browser.

## Current State

Helium is currently distributed as:
- **AppImage**: Portable, self-contained Linux package
- **tar.xz archive**: Extracted browser files for manual installation

These distribution methods work across all Linux distributions but lack native integration with Fedora's package management ecosystem.

## Research Findings

### 1. Fedora RPM Packaging Requirements

**Key Components Needed:**
- RPM spec file with proper metadata and build instructions
- BuildRequires and Requires dependency declarations
- Installation scripts for desktop integration
- Compliance with Fedora Packaging Guidelines
- FHS (Filesystem Hierarchy Standard) compliant file locations

**Fedora Packaging Philosophy:**
- Prefer system libraries over bundled dependencies
- Follow SELinux security policies
- Integrate properly with desktop environments
- Maintain clear licensing information (SPDX identifiers)
- Include proper changelog documentation

### 2. Distribution Options Analysis

#### Option A: Fedora Copr (Selected)
**Repository:** https://copr.fedorainfracloud.org/coprs/griko/helium-browser/

**Pros:**
- Community-driven build and hosting infrastructure
- Automated builds for multiple Fedora versions/architectures
- Easy for users to enable and use (`dnf copr enable griko/helium-browser`)
- No formal approval process required
- Free hosting and bandwidth
- Integrates with DNF/package management

**Cons:**
- Unofficial/community package (not in main Fedora repos)
- Requires Fedora Account System account (already created)
- Users must explicitly enable the Copr repository
- No official Fedora support/backing

**Status:** ✅ Repository created and ready for package uploads

**Best For:** Community packages, experimental software, rapid iteration

#### Option B: GitHub Releases (Simple Alternative)
**Pros:**
- Simple distribution (just upload RPM files)
- No external service dependencies
- Full control over releases
- Consistent with current AppImage distribution

**Cons:**
- Manual installation required
- No automatic updates via DNF
- Users must download each update manually
- No repository infrastructure
- Must build for each Fedora version separately

**Best For:** Testing, initial releases, supplementary distribution

#### Option C: Official Fedora Repositories (Long-term Goal)
**Pros:**
- Highest trust and visibility
- Included by default on all Fedora installations
- Official Fedora support and infrastructure
- Automatic updates via DNF

**Cons:**
- Requires formal package review process
- Strict packaging guidelines enforcement
- Long-term maintenance commitment
- May require significant spec file modifications
- Chromium-based browsers are complex to package

**Best For:** Mature, stable projects with dedicated maintainers

### 3. Technical Considerations for Chromium-Based Browsers

#### System Integration
- **Libraries**: Fedora prefers using system libraries (GTK, NSS, ALSA, etc.) over bundled versions
- **SELinux**: Must work with Fedora's default enforcing SELinux policies
- **Desktop Files**: Proper MIME type associations and menu integration
- **Icons**: Install to standard icon directories with appropriate sizes

#### Multimedia Codecs
- Fedora excludes patent-encumbered codecs (H.264, AAC) by default
- Users requiring these codecs need RPM Fusion or similar
- Must document codec limitations clearly

#### Build Complexity
- Chromium takes hours to compile (100+ GB disk space)
- Building in spec file may not be practical
- Alternative: Package pre-built binaries from existing build process
- Hybrid approach: Use existing Docker-based build, then package results

### 4. Reference Implementations

**ungoogled-chromium-fedora:**
- Excellent reference for Chromium browser RPM packaging
- Handles complex dependency management
- Includes patch management system
- Active maintenance and CI/CD

**Fedora Chromium Package:**
- Official approach to Chromium packaging
- System library integration examples
- SELinux policy handling

## Implementation Plan

### Phase 1: Initial Infrastructure ✅

**Created Files:**
- `docs/FEDORA_PACKAGING.md` - Comprehensive technical documentation
- `fedora/helium.spec` - Initial RPM spec file template
- `fedora/build-rpm.sh` - Build script for creating RPM packages
- `fedora/README.md` - Quick start guide for RPM building

**Key Decisions:**
- Use pre-built binaries from existing build process (not full rebuild in spec)
- Follow FHS with files in `/usr/lib64/helium/` and wrapper in `/usr/bin/`
- Include all BuildRequires and Requires for proper dependency management
- Desktop integration with `.desktop` file and icon installation

### Phase 2: Testing and Validation (Next Steps)

1. **Build Testing:**
   - Test RPM build process with actual Helium build output
   - Verify all files are included correctly
   - Check desktop file validation
   - Run rpmlint for quality checks

2. **Installation Testing:**
   - Test installation on Fedora 40, 41
   - Verify application launches correctly
   - Check desktop integration (menu entry, icon)
   - Test MIME type associations
   - Verify no SELinux denials

3. **Runtime Testing:**
   - Launch browser and verify functionality
   - Check privacy features work correctly
   - Test on both X11 and Wayland
   - Verify resource loading (icons, locales, etc.)

### Phase 3: Distribution Setup

**Fedora Copr** (Repository Created)

Repository: https://copr.fedorainfracloud.org/coprs/griko/helium-browser/

**Setup Status:**
1. ✅ Fedora Account System (FAS) account created
2. ✅ Copr project created at https://copr.fedorainfracloud.org/coprs/griko/helium-browser/
3. Configure project settings:
   - Project name: `helium-browser`
   - Description: Privacy-focused Chromium-based browser
   - Instructions: Link to helium.computer
   - Enable for Fedora 38, 39, 40, 41
   - Enable for x86_64 and aarch64

4. Set up automated builds:
   - Option A: Upload SRPM manually for each release
   - Option B: Configure Git/GitHub integration for automatic builds
   - Option C: Use Copr CLI for scripted uploads

5. Installation for users:
   ```bash
   sudo dnf copr enable griko/helium-browser
   sudo dnf install helium
   ```

**Alternative: GitHub Releases**

1. Build RPMs for target Fedora versions
2. Upload alongside AppImage in GitHub releases
3. Provide installation instructions:
   ```bash
   # Download RPM from GitHub releases
   sudo dnf install ./helium-0.6.5.1-1.fc40.x86_64.rpm
   ```

### Phase 4: Documentation Updates (Future)

Update repository documentation:

1. **README.md**:
   - Add "Installation on Fedora" section
   - Document Copr repository (if used)
   - Document manual RPM installation
   - Note codec limitations

2. **Release Notes**:
   - Include RPM packages in release notes
   - Provide per-version installation instructions

3. **Website** (if applicable):
   - Add Fedora installation instructions
   - Link to Copr repository

## Recommendations

### Immediate (Phase 1) ✅
- [x] Create initial RPM spec file
- [x] Create build script
- [x] Document approach and findings
- [x] Set up basic infrastructure

### Short-term (Phase 2)
- [ ] Test RPM build process with real build output
- [ ] Validate installation and runtime on Fedora
- [ ] Fix any issues discovered during testing
- [ ] Iterate on spec file based on testing

### Medium-term (Phase 3)
- [x] Copr repository created: https://copr.fedorainfracloud.org/coprs/griko/helium-browser/
- [ ] Upload packages to Copr
- [ ] Configure automated builds from GitHub
- [ ] Create first official RPM release
- [ ] Document installation for users in main README

### Long-term (Phase 4+)
- [ ] Consider official Fedora repository inclusion (requires significant effort)
- [ ] Add support for additional architectures (aarch64)
- [ ] Integrate full build process into spec (if practical)
- [ ] Add RPM signing with GPG key

## Benefits of RPM Packaging

**For Fedora Users:**
- Native package management integration
- Easy installation via DNF
- Automatic dependency resolution
- Better system integration
- Familiar installation method

**For Helium Project:**
- Increased visibility in Fedora community
- Better distribution on RPM-based systems
- Professional packaging approach
- Potential for wider adoption

**For Maintainers:**
- Leverages existing build infrastructure
- Copr provides free automated builds
- Complements existing AppImage distribution
- No disruption to current workflow

## Risks and Mitigation

**Risk: RPM build complexity**
- Mitigation: Use pre-built binaries from existing process
- Spec file focuses on packaging, not building

**Risk: Maintenance burden**
- Mitigation: Copr can auto-build from GitHub tags
- Automated as much as possible

**Risk: User confusion (multiple install methods)**
- Mitigation: Clear documentation for each method
- AppImage remains primary method

**Risk: Fedora-specific issues**
- Mitigation: Testing on multiple Fedora versions
- Community feedback via Copr

## Conclusion

Fedora RPM packaging is feasible and beneficial for Helium. The selected approach is:

1. **Fedora Copr** as the primary distribution method
   - Repository created: https://copr.fedorainfracloud.org/coprs/griko/helium-browser/
   - Users can install via: `sudo dnf copr enable griko/helium-browser && sudo dnf install helium`
2. **GitHub releases** as supplementary distribution
3. **Consider official repos** as a long-term goal

This approach provides:
- Low barrier to entry for users
- Professional distribution method via Copr
- Automated builds and updates
- Improved user experience for Fedora users

The infrastructure created in Phase 1 provides a solid foundation for RPM packaging, with the Copr repository ready for package uploads.

## Next Actions

1. Test the build-rpm.sh script with actual build output
2. Validate the generated RPM on clean Fedora installations
3. Make any necessary adjustments based on testing
4. Upload packages to Copr repository
5. Configure automated builds from GitHub releases
5. Create first official RPM release
6. Update documentation with installation instructions

---

**Document Version:** 1.0  
**Date:** November 14, 2024  
**Status:** Research Complete, Phase 1 Implementation Complete

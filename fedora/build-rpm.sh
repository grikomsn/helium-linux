#!/bin/bash
set -euo pipefail

# Build script for creating Helium RPM packages for Fedora
# This script sets up the RPM build environment and builds the package

_current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
_root_dir="$(cd "${_current_dir}/.." && pwd)"
_build_dir="${_root_dir}/build"
_tarball_dir="${_build_dir}/release"

echo "=== Helium Fedora RPM Build Script ==="
echo ""

# Check if rpmbuild is available
if ! command -v rpmbuild &> /dev/null; then
    echo "ERROR: rpmbuild not found. Please install rpmdevtools:"
    echo "  sudo dnf install -y rpmdevtools rpmlint fedora-packager"
    exit 1
fi

# Check if build output exists
if [ ! -d "${_build_dir}/src/out/Default" ]; then
    echo "ERROR: Build output not found at ${_build_dir}/src/out/Default"
    echo "Please build Helium first using scripts/docker-build.sh"
    exit 1
fi

# Set up RPM build tree
echo "Setting up RPM build tree..."
if [ ! -d ~/rpmbuild ]; then
    rpmdev-setuptree
fi

# Get version from Helium
echo "Detecting Helium version..."
_version=$(python3 "${_root_dir}/helium-chromium/utils/helium_version.py" \
    --tree "${_root_dir}/helium-chromium" \
    --platform-tree "${_root_dir}" \
    --print)

echo "Version: $_version"

# Get architecture
_arch=$(cat "${_build_dir}/src/out/Default/args.gn" \
    | grep ^target_cpu \
    | tail -1 \
    | sed 's/.*=//' \
    | cut -d'"' -f2)

if [ "$_arch" = "x64" ]; then
    _arch="x86_64"
fi

echo "Architecture: $_arch"

# Create source tarball from build output
_tarball_name="helium-${_version}"
_tarball_path=~/rpmbuild/SOURCES/${_tarball_name}.tar.xz

echo "Creating source tarball..."
_temp_dir=$(mktemp -d)
mkdir -p "${_temp_dir}/${_tarball_name}"

# Copy built files to tarball staging
_files="chrome
chrome_100_percent.pak
chrome_200_percent.pak
chrome_crashpad_handler
chromedriver
chrome-wrapper
icudtl.dat
libEGL.so
libGLESv2.so
libqt5_shim.so
libqt6_shim.so
libvk_swiftshader.so
libvulkan.so.1
locales/
product_logo_256.png
resources.pak
v8_context_snapshot.bin
vk_swiftshader_icd.json
xdg-mime
xdg-settings"

for file in $_files; do
    if [ -e "${_build_dir}/src/out/Default/${file}" ]; then
        cp -r "${_build_dir}/src/out/Default/${file}" "${_temp_dir}/${_tarball_name}/"
    else
        echo "WARNING: ${file} not found in build output"
    fi
done

# Copy additional files
cp "${_root_dir}/LICENSE" "${_temp_dir}/${_tarball_name}/"
cp "${_root_dir}/README.md" "${_temp_dir}/${_tarball_name}/"

# Create tarball
echo "Compressing tarball..."
tar -C "${_temp_dir}" -cJf "${_tarball_path}" "${_tarball_name}"
rm -rf "${_temp_dir}"

echo "Tarball created: ${_tarball_path}"

# Copy spec file and update version
echo "Preparing spec file..."
_spec_file=~/rpmbuild/SPECS/helium.spec
cp "${_current_dir}/helium.spec" "${_spec_file}"

# Update version in spec file
sed -i "s/^Version:.*/Version:        ${_version}/" "${_spec_file}"

# Copy desktop file to SOURCES
cp "${_root_dir}/package/helium.desktop" ~/rpmbuild/SOURCES/

# Build the RPM
echo ""
echo "Building RPM package..."
rpmbuild -ba "${_spec_file}"

_rpm_file=~/rpmbuild/RPMS/${_arch}/helium-${_version}-1.*.${_arch}.rpm
_srpm_file=~/rpmbuild/SRPMS/helium-${_version}-1.*.src.rpm

echo ""
echo "=== Build Complete ==="
echo ""
echo "RPM package: ${_rpm_file}"
echo "Source RPM: ${_srpm_file}"
echo ""
echo "To install:"
echo "  sudo dnf install ${_rpm_file}"
echo ""
echo "To check package contents:"
echo "  rpm -qlp ${_rpm_file}"
echo ""
echo "To lint the package:"
echo "  rpmlint ${_rpm_file}"

#!/bin/bash
set -euo pipefail

_current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
_root_dir="$(cd "$_current_dir/.." && pwd)"
_build_dir="$_root_dir/build"
_release_dir="$_build_dir/release"

_app_name="helium"
_version=$(python3 "$_root_dir/helium-chromium/utils/helium_version.py" \
                   --tree "$_root_dir/helium-chromium" \
                   --platform-tree "$_root_dir" \
                   --print)

_arch=$(cat "$_build_dir/src/out/Default/args.gn" \
                | grep ^target_cpu \
                | tail -1 \
                | sed 's/.*=//' \
                | cut -d'"' -f2)

if [ "$_arch" = "x64" ]; then
    _arch="x86_64"
elif [ "$_arch" = "arm64" ]; then
    _arch="aarch64"
fi

_tarball_name="helium-$_version-${_arch}_linux"
_rpm_arch="$_arch"

echo "Building RPM package for Helium $_version ($_rpm_arch)"

# Check if tar.xz exists
if [ ! -f "$_release_dir/$_tarball_name.tar.xz" ]; then
    echo "Error: $_release_dir/$_tarball_name.tar.xz not found"
    echo "Please run scripts/package.sh first to create the tarball"
    exit 1
fi

# Set up RPM build environment
_rpmbuild_dir="$_build_dir/rpmbuild"
mkdir -p "$_rpmbuild_dir"/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Copy tarball to SOURCES
cp "$_release_dir/$_tarball_name.tar.xz" "$_rpmbuild_dir/SOURCES/"

# Copy spec file and substitute variables
sed -e "s/%{version}/$_version/g" \
    -e "s/%{_arch}/$_rpm_arch/g" \
    "$_root_dir/package/helium.spec" > "$_rpmbuild_dir/SPECS/helium.spec"

# Build RPM
echo "Building RPM package..."
rpmbuild --define "_topdir $_rpmbuild_dir" \
         --define "_arch $_rpm_arch" \
         --target "$_rpm_arch" \
         -bb "$_rpmbuild_dir/SPECS/helium.spec"

# Copy RPM to release directory
_rpm_pattern="$_rpmbuild_dir/RPMS/$_rpm_arch/helium-$_version-1.*.rpm"
_rpm_files=($_rpm_pattern)
if [ -f "${_rpm_files[0]}" ]; then
    cp "${_rpm_files[0]}" "$_release_dir/"
    echo "RPM package created: $(basename "${_rpm_files[0]}")"
    ls -lh "$_release_dir/"*.rpm
else
    echo "Error: RPM file not found at $_rpm_pattern"
    exit 1
fi

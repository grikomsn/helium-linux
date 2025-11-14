# Verifying Helium Downloads

## Overview

Starting with the next release, all Helium Linux releases include a `SHA256SUMS` file that allows you to verify the integrity of your downloads.

## Why Verify Downloads?

Verifying downloads ensures that:
1. The file was not corrupted during download
2. The file has not been tampered with
3. You have the authentic Helium release

## How to Verify

### On Linux

After downloading Helium and the `SHA256SUMS` file from a release:

```bash
# Verify a specific file (AppImage, RPM, or tar.xz)
sha256sum -c SHA256SUMS --ignore-missing

# Or verify all files (if you downloaded all of them)
sha256sum -c SHA256SUMS
```

**Expected output:**
```
helium-0.6.5.1-x86_64.AppImage: OK
helium-0.6.5.1-1.fc40.x86_64.rpm: OK
```

### Manual Verification

If you prefer to verify manually:

```bash
# Generate the checksum of your downloaded file
sha256sum helium-*.AppImage
# or
sha256sum helium-*.rpm

# Compare the output with the value in SHA256SUMS
cat SHA256SUMS | grep AppImage
# or
cat SHA256SUMS | grep rpm
```

The two checksums should match exactly.

## Examples

### Verifying AppImage

```bash
# Download files
wget https://github.com/imputnet/helium-linux/releases/download/0.6.5.1/helium-0.6.5.1-x86_64.AppImage
wget https://github.com/imputnet/helium-linux/releases/download/0.6.5.1/SHA256SUMS

# Verify the download
sha256sum -c SHA256SUMS --ignore-missing
```

**Expected output:**
```
helium-0.6.5.1-x86_64.AppImage: OK
```

### Verifying RPM Package

```bash
# Download files
wget https://github.com/imputnet/helium-linux/releases/download/0.6.5.1/helium-0.6.5.1-1.fc40.x86_64.rpm
wget https://github.com/imputnet/helium-linux/releases/download/0.6.5.1/SHA256SUMS

# Verify the download
sha256sum -c SHA256SUMS --ignore-missing
```

**Expected output:**
```
helium-0.6.5.1-1.fc40.x86_64.rpm: OK
```

## What If Verification Fails?

If the verification fails with a message like:
```
helium-0.6.5.1-x86_64.AppImage: FAILED
```

This means:
1. The file may have been corrupted during download
2. The file may have been tampered with
3. You may have downloaded the wrong version

**Action:** Delete the file and download it again. If it still fails, report this to the maintainers immediately.

## GPG Signature Verification

In addition to SHA256 checksums, AppImage files are also GPG signed. The signature is embedded in the AppImage file itself.

To verify the GPG signature:

```bash
# Import the Helium signing key (one time only)
gpg --recv-keys 351601AD01D6378E

# Extract and verify the signature
# (This is done automatically when you run the AppImage)
```

The GPG key fingerprint is:
```
BE67 7C19 89D3 5EAB 2C5F  26C9 3516 01AD 01D6 378E
```

For more information about the signing key, see the [README](../README.md#signature).

## Automated Verification Script

You can create a simple script to automate verification:

```bash
#!/bin/bash
# verify-helium.sh

VERSION=$1
ARCH=${2:-x86_64}

if [ -z "$VERSION" ]; then
    echo "Usage: $0 <version> [arch]"
    echo "Example: $0 0.6.5.1 x86_64"
    exit 1
fi

BASE_URL="https://github.com/imputnet/helium-linux/releases/download/$VERSION"
APPIMAGE="helium-$VERSION-$ARCH.AppImage"

echo "Downloading $APPIMAGE..."
wget -q "$BASE_URL/$APPIMAGE"

echo "Downloading checksums..."
wget -q "$BASE_URL/SHA256SUMS"

echo "Verifying download..."
if sha256sum -c SHA256SUMS --ignore-missing; then
    echo "✓ Verification successful!"
    chmod +x "$APPIMAGE"
    echo "You can now run: ./$APPIMAGE"
else
    echo "✗ Verification failed!"
    echo "The downloaded file may be corrupted or tampered with."
    exit 1
fi
```

Save this as `verify-helium.sh`, make it executable, and use it:

```bash
chmod +x verify-helium.sh
./verify-helium.sh 0.6.5.1 x86_64
```

## Security Best Practices

1. **Always verify downloads** from any source, even official ones
2. **Download from official sources only**:
   - GitHub Releases: https://github.com/imputnet/helium-linux/releases
3. **Check the HTTPS certificate** when downloading
4. **Keep your system updated** to ensure `sha256sum` and `gpg` are secure
5. **Report any verification failures** to the maintainers

## Additional Resources

- [SHA-256 on Wikipedia](https://en.wikipedia.org/wiki/SHA-2)
- [GPG Documentation](https://gnupg.org/documentation/)
- [Fedora: Verifying RPM Packages](https://docs.fedoraproject.org/en-US/quick-docs/verify-rpms/)

#!/bin/bash
set -euo pipefail

_current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
_root_dir="$(cd "$_current_dir/.." && pwd)"

# Use Fedora container for RPM building
docker run --rm \
    -v "$_root_dir:/workspace" \
    -w /workspace \
    fedora:latest \
    bash -c "
        set -euo pipefail
        dnf install -y rpm-build python3 sed
        bash /workspace/scripts/build-rpm.sh
    "

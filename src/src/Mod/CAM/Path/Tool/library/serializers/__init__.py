# SPDX-License-Identifier: LGPL-2.1-or-later

from .camotics import CamoticsLibrarySerializer
from .auracadtl import auracadTLSerializer
from .linuxcnc import LinuxCNCSerializer

all_serializers = CamoticsLibrarySerializer, auracadTLSerializer, LinuxCNCSerializer


__all__ = [
    "CamoticsLibrarySerializer",
    "auracadTLSerializer",
    "LinuxCNCSerializer",
]

# Copyright (c) 2021-2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""WebSocket healthcheck test case."""

from typing import List, Optional

from omni.kit.livestream.websocket.tests import ExtensionSettingsTestCase

from omni.services.streaming.manager import get_stream_manager, StreamInterface, StreamManager


class WebSocketHealthCheckTestCase(ExtensionSettingsTestCase):
    """WebSocket healthcheck test case."""

    def _get_enabled_stream_interface(self) -> Optional[StreamInterface]:
        stream_manager: StreamManager = get_stream_manager()
        enabled_stream_interface_id: Optional[str] = stream_manager.get_enabled_stream_interface_id()

        if enabled_stream_interface_id is not None:
            enabled_stream_interfaces: List[StreamInterface] = stream_manager.get_registered_stream_interfaces()
            for enabled_stream_interface in enabled_stream_interfaces:
                if enabled_stream_interface.id == enabled_stream_interface_id:
                    return enabled_stream_interface

        return None

    async def test_websocket_stream_interface_naming(self) -> None:
        """Validate that the naming of the WebSocket streaming interface matches the expected values."""
        enabled_stream_interface = self._get_enabled_stream_interface()

        self.assertIsNotNone(enabled_stream_interface)
        if enabled_stream_interface is not None:
            self.assertEqual(first="WebSocket", second=enabled_stream_interface.id)
            self.assertEqual(first="WebSocket", second=enabled_stream_interface.menu_label)

    async def test_websocket_stream_interface_health_status(self) -> None:
        """Validate that WebSocket streaming interface reports the extension as healthy when it is enabled."""
        enabled_stream_interface = self._get_enabled_stream_interface()

        self.assertIsNotNone(enabled_stream_interface)
        if enabled_stream_interface is not None:
            is_healthy = await enabled_stream_interface.is_healthy()
            self.assertTrue(is_healthy)

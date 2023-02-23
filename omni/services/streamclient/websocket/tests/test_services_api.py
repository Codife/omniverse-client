# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

from typing import Dict, Union

import carb.settings

from omni.services.client import AsyncClient
from omni.kit.livestream.websocket.tests import ExtensionSettingsTestCase


class ServicesAPITestCase(ExtensionSettingsTestCase):

    async def setUp(self) -> None:
        super().setUp()

        self._settings = carb.settings.get_settings()
        self._websocket_server_port = self._settings.get_as_int("/app/livestream/websocket/server_port")
        self._wss_enabled = self._settings.get_as_bool("/app/livestream/websocket/wss/enabled")
        router_prefix = self._settings.get_as_string("exts/omni.services.streamclient.websocket/routerPrefix")
        http_port = self._settings.get_as_int("/exts/omni.services.transport.server.http/port")
        self._websocket_server_information_endpoint = f"http://localhost:{http_port}{router_prefix}/websocket-server-information"

    async def _get_websocket_server_information(self) -> Dict[str, Union[int, bool]]:
        client = AsyncClient(uri=self._websocket_server_information_endpoint)
        websocket_server_information: Dict[str, Union[int, bool]] = await client.get()
        await client.stop_async()
        return websocket_server_information

    async def test_websocket_server_information_port_matches_settings_value(self) -> None:
        """Validate that the \"port\" in the API response matches the one provided in the extension settings."""
        websocket_server_information = await self._get_websocket_server_information()
        self.assertTrue(
            expr="port" in websocket_server_information,
            msg="Expected to find a \"port\" key in the WebSocket server information"
        )
        self.assertEqual(self._websocket_server_port, websocket_server_information["port"])

    async def test_websocket_server_information_wss_support_matches_settings_value(self) -> None:
        """Validate that the \"supportsSecureConnections\" in the API response matches the one provided in the extension settings."""
        websocket_server_information = await self._get_websocket_server_information()
        self.assertTrue(
            expr="supportsSecureConnections" in websocket_server_information,
            msg="Expected to find a \"supportsSecureConnections\" key in the WebSocket server information"
        )
        self.assertEqual(self._wss_enabled, websocket_server_information["supportsSecureConnections"])

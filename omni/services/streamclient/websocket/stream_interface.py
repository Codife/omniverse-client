# Copyright (c) 2021-2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""WebSocket stream interface."""

import os
from typing import List

import psutil

import carb.settings

from omni.services.streaming.manager import StreamInterface


class WebSocketStreamInterface(StreamInterface):
    """WebSocket stream interface."""

    @property
    def id(self) -> str:
        return "WebSocket"

    @property
    def menu_label(self) -> str:
        return "WebSocket"

    @property
    def module_name(self) -> str:
        return __name__

    @property
    def stream_urls(self) -> List[str]:
        settings = carb.settings.get_settings()
        router_prefix = settings.get_as_string("exts/omni.services.streamclient.websocket/routerPrefix")
        client_url = settings.get_as_string("exts/omni.services.streamclient.websocket/clientUrl")

        return [f"{host}{router_prefix}{client_url}" for host in self.local_hosts]

    async def is_healthy(self) -> bool:
        """
        Check if the streaming server is in a state that is considered healthy (i.e. that the WebSocket server listens
        for connection requests on the configured port).

        While querying the server is the ideal solution (as it would allow to inspect the contents of the response to
        confirm it is a valid MP4 frame), this would have additional overhead due to the creation of threads, along with
        routing of data across all connected clients. This can further result in potential "hitches" in the stream, as a
        single connection would be performed by the healthcheck process at regular interval, which may result in a
        degraded User experience for actual Users.

        Args:
            None

        Returns:
            bool: A flag indicating whether the streaming server is in a healthy state.

        """
        # Confirm if the superclass may have already flagged the stream as being in an unhealthy state, in order to
        # potentially return early:
        is_healthy = await super().is_healthy()
        if not is_healthy:
            return is_healthy

        # Check that the host process has the expected WebSocket server port in a "LISTENING" state by querying its
        # process, rather than issuing an actual request against the server:
        kit_process = psutil.Process(pid=os.getpid())
        expected_server_port = self._get_websocket_port_number()
        is_listening_on_expected_port = False

        for connection in kit_process.connections(kind="tcp"):
            if connection.laddr.port == expected_server_port:
                if connection.status is psutil.CONN_LISTEN:
                    is_listening_on_expected_port = True
                break

        return is_listening_on_expected_port

    def _get_websocket_port_number(self) -> int:
        """
        Return the port number of on which the WebSocket server is expected to receive connection requests.

        Args:
            None

        Returns:
            int: The port number of on which the WebSocket server is expected to receive connection requests.

        """
        settings = carb.settings.get_settings()
        websocket_server_port = settings.get_as_int("app/livestream/websocket/server_port")
        return websocket_server_port

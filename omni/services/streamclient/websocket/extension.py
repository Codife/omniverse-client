# Copyright (c) 2021-2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""WebSocket streaming client service extension."""

import os
from typing import Optional

from fastapi import staticfiles

import carb
import carb.settings

import omni.ext
import omni.kit.app
from omni.services.core import main
from omni.services.streaming.manager import get_stream_manager, StreamManager

from .services.api import router as api_router
from .stream_interface import WebSocketStreamInterface


class WebSocketFrontendServiceExtension(omni.ext.IExt):
    """WebSocket streaming client service extension."""

    def __init__(self) -> None:
        """Constructor."""
        super().__init__()
        self._router_prefix: Optional[str] = None
        self._frontend_path: Optional[str] = None
        self._stream_interface: Optional[WebSocketStreamInterface] = None

    def on_startup(self, ext_id) -> None:
        settings = carb.settings.get_settings()
        frontend_port = settings.get_as_int("exts/omni.services.transport.server.http/port")
        self._router_prefix = settings.get_as_string("exts/omni.services.streamclient.websocket/routerPrefix")
        client_url = settings.get_as_string("exts/omni.services.streamclient.websocket/clientUrl")

        self._frontend_path = f"{self._router_prefix}{client_url}"
        frontend_url = f"http://localhost:{frontend_port}{self._frontend_path}"
        carb.log_info(
            f"Starting up the WebSocket livestream client. The frontend interface is available at {frontend_url}"
        )

        _extension_path = omni.kit.app.get_app_interface().get_extension_manager().get_extension_path(ext_id)
        static_directory = os.path.join(_extension_path, "web")

        main.register_router(router=api_router, prefix=self._router_prefix, tags=["streaming"])
        main.register_mount(
            path=self._frontend_path,
            app=staticfiles.StaticFiles(directory=static_directory, html=True),
            name="livestream-websocket-static",
        )

        self._stream_interface = WebSocketStreamInterface()
        stream_manager: StreamManager = get_stream_manager()
        stream_manager.register_stream_interface(stream_interface=self._stream_interface)
        stream_manager.enable_stream_interface(stream_interface_id=self._stream_interface.id)

    def on_shutdown(self) -> None:
        carb.log_info("Stopping the WebSocket livestream client.")

        main.deregister_router(router=api_router, prefix=self._router_prefix)
        main.deregister_mount(path=self._frontend_path)

        stream_manager: StreamManager = get_stream_manager()
        stream_manager.disable_stream_interface(stream_interface_id=self._stream_interface.id)
        stream_manager.unregister_stream_interface(stream_interface_id=self._stream_interface.id)

        if self._stream_interface:
            self._stream_interface = None

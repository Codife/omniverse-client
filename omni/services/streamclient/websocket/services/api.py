# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""REST API for the WebSocket streaming client service."""

from typing import Optional

from pydantic import BaseModel, Field

import carb.settings

import omni.appwindow
from omni.services.core import routers


class GetWebSocketServerInformationResponseModel(BaseModel):
    """Response to the request to obtain information about the WebSocket server."""

    port: int = Field(
        ...,
        title="WebSocket server port number",
        description="Port number on which the WebSocket server is listening for connection requests.",
    )
    supportsSecureConnections: bool = Field(
        False,
        title="Flag indicating whether the WebSocket server supports \"wss://\" connections",
        description="Flag indicating whether the WebSocket server supports connections over the \"wss://\" protocol.",
    )


class ResizeStreamRequestModel(BaseModel):
    """Request to resize the WebSocket stream."""

    width: int = Field(
        ...,
        title="Width",
        description="Width of the application window to stream (in pixels).",
        gt=0,
    )
    height: int = Field(
        ...,
        title="Height",
        description="Height of the application window to stream (in pixels).",
        gt=0,
    )


class ResizeStreamResponseModel(BaseModel):
    """Response to the request to resize the WebSocket stream."""

    success: bool = Field(
        ...,
        title="Success",
        description="Flag indicating if the request was successful.",
    )
    errorMessage: Optional[str] = Field(
        None,
        title="Error message",
        description="Details about the error that occurred, in case of failure.",
    )


router = routers.ServiceAPIRouter()


@router.post(
    "/resize-stream",
    summary="Resize the WebSocket stream",
    description="Request that the WebSocket stream server change the resolution of the streamed frames.",
    response_model=ResizeStreamResponseModel,
)
def resize_stream(data: ResizeStreamRequestModel) -> ResizeStreamResponseModel:
    try:
        app_window = omni.appwindow.get_default_app_window()
        app_window.resize(data.width, data.height)
        return ResizeStreamResponseModel(success=True)
    except Exception as exc:
        return ResizeStreamResponseModel(success=False, errorMessage=str(exc))


@router.get(
    "/websocket-server-information",
    summary="Return information about the WebSocket server",
    description="Return metadata information about the WebSocket server used to stream frames from the application.",
    response_model=GetWebSocketServerInformationResponseModel,
)
def get_websocket_server_information() -> GetWebSocketServerInformationResponseModel:
    websocket_server_port = carb.settings.get_settings().get_as_int("app/livestream/websocket/server_port")
    supportsSecureConnections = carb.settings.get_settings().get_as_bool("app/livestream/websocket/wss/enabled")

    return GetWebSocketServerInformationResponseModel(
        port=websocket_server_port,
        supportsSecureConnections=supportsSecureConnections,
    )

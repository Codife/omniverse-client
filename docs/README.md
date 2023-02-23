# WebSocket streaming client service [omni.services.streamclient.websocket]

## About

This feature allows you and your Users to interact with Kit-based application over the network as if they were experiencing it locally. This makes it possible to collaborate over the network from a laptop, tablet or phone connected on the same network.

## Usage

After enabling this extension, navigate to this URL to load a single-page web application allowing you to control your application from your web browser:

- From Kit: http://localhost:8011/streaming/client
- From Create: http://localhost:8111/streaming/client
- From Isaac Sim: http://localhost:8211/streaming/client
- From Kaolin: http://localhost:8311/streaming/client

For convenience, the URLs where the web application is exposed are available from the "Streaming > Local Stream URLs" top-level menu, where they can be copied to the clipboard for sharing.

Firefox Users on Linux may have to install additional video codecs for playback on the client browser. Ubuntu Users may wish to install `sudo apt-get install ffmpeg` for simplicity.

## Configuration

For additional information on configuring and using the extension, refer to the documentation of the "omni.kit.livestream.websocket" extension.

Complementary information about the extension and its configuration options can be found online at https://docs.omniverse.nvidia.com/prod_extensions/prod_extensions/ext_livestream/overview.html

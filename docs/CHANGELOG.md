# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.5] - 2022-06-28
### Added
- Added healthcheck implementation to provide information about the status of the streaming extension.

## [1.4.4] - 2022-03-29
### Changed
- Enabled zipping of extension licenses.

## [1.4.3] - 2022-03-28
### Changed
- Updated extension documentation and metadata.

## [1.4.2] - 2022-03-24
### Changed
- Enabled mouse input handling in a similar way to the traditional Native and WebRTC handlers.

## [1.4.1] - 2022-03-23
### Added
- Updated Kit SDK to leverage the `APP_STARTED` event.

## [1.4.0] - 2022-03-05
### Added
- Updated stream interface to include stream URLs in application menu.

## [1.3.0] - 2022-02-20
### Added
- Added support for switching to the WebSocket Secure (`wss://`) schema when serving content over HTTPS to avoid mixed-content issues in web browsers.
- Added API endpoint to query the server for connection information about the WebSocket server, available at `/streaming/websocket-server-information`.
- Added ability to resize the viewport window along with the browser window.
### Removed
- Removed dependency on `Jinja2` for templating, replacing front-end templating with the more flexible `/streaming/websocket-server-information` endpoint which can be queried from other external services.

## [1.2.2] - 2021-12-31
### Added
- Added information container to display the framerate, URL of the WebSocket server and total number of frames received.

## [1.2.1] - 2021-12-12
### Added
- Added ability for clients to specify a desired stream framerate.
### Changed
- Set capture menu behind a flag.

## [1.2.0] - 2021-12-11
### Added
- Added integration into the Stream Manager feature, to ensure only a single streaming extension can be enabled at any given time.

## [1.1.7] - 2021-12-06
### Changed
- Updated extension metadata.

## [1.1.6] - 2021-12-06
### Added
- Added unit tests to validate correct behavior of the WebSocket server extension when enabling the client.

## [1.1.5] - 2021-10-14
### Added
- Added documentation about where to find additional configuration options for the extension.

## [1.1.4] - 2021-09-22
### Fixed
- Fixed mouse offset issues affecting the web player when the resolution of the web client made it so that the height of the `<video>` Element was smaller than the height of the application window.

## [1.1.3] - 2021-09-14
### Changed
- Fix `jinja2` import. Will be further addressed in OM-37643.

## [1.1.2] - 2021-05-20
### Changed
- Fit video stream to the browser window on displays of smaller resolution.

## [1.1.1] - 2021-05-11
### Changed
- Remove externally-hosted front-end libraries, making the experience entirely self-hosted.

## [0.1.0] - 2021-04-21
### Added
- Initial commit

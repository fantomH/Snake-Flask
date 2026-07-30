<!--
+-----------------------------------------------------------------------------+ 
[+] INFO
+-----------------------------------------------------------------------------+
 [Snake-Flask/src/snake_flask/common/README.md]

 Author      : Pascal Malouin (https://github.com/fantomH)
 Created     : 2026-07-29 23:57:06 UTC
 Updated     : 2026-07-29 23:57:06 UTC
 Description : Snake-Flask Common documentation.
+-----------------------------------------------------------------------------+
-->

# snake_flask.common

Flask extension used by the Snake-Flask suite for shared assets.

Extension name: "snake_common"

## Overview

The `snake_flask.common` extension provides:

* snake-common.css for a shared look, altough Snake-Flask still rely heavily on Bootstrap.
* few javascript autonomus files to implement some interactivity and enable feature such as automatic logout.
* a common base.html, if not provided by the main app.
* HTTP error pages.
* Some useful pages that don't fit yet in other extentions, such as a config panel (to come).

## Default configuration

`SNAKE_ACCESS_INACTIVITY_TIMEOUT`

Default: `None`

`SNAKE_COMMON_BASE_TEMPLATE`

Default: `None`

`SNAKE_COMMON_CONFIGURATION_URL_PREFIX`

Default: "/configuration"


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Overview](#overview)
- [Installation](#installation)

<!-- END doctoc generated TOC please keep comment here to allow auto update 

<a href="https://github.com/CiscoDevNet/ydk-py"><img src="https://cloud.githubusercontent.com/assets/17089095/14834057/2e1fe270-0bb7-11e6-9e94-73dd7d71e87d.png" height="240" width="240" ></a>
-->

# Overview

The YANG Development Kit (YDK) is a software development tool, which provides API for building applications based on YANG models.
The YDK allows generate YANG model API and provides services to apply generated API over various communication protocols.
Currently implemented protocols are: Netconf, Restconf, OpenDaylight and gNMI.
YDK provides CRUD and protocol specific services over above protocols.
YDK also provides codec services to translate API models to/from XML and JSON encoded strings.

# Installation

Create a source distribution for YDK:
```
    $ python setup.py sdist
```

Install YDK:
```
    $ pip install dist/ydk-*.tar.gz
```


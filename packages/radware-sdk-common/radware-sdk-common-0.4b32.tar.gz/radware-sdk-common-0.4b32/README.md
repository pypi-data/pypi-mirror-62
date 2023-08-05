
Introduction
=====================

This project implements common SDK functions for Radware device SDK packages.
it defines interfaces for interacting with device management & configuration planes.
the package is intended to be independently reusable in any device project in Python.
right now it offers REST interface for communication, but additional can be added as needed

each implementing device SDK inherit a ConfigurationManager module that offer configuration staging engine, 
dry run , differential update , write on change and config diff (via the abstraction defined by the model)
set of interfaces enable accurate definition of procedure and normalization customization.

each implementing device provide two methods to accomplish object configuration declaration:
- DEPLOY - when applicable it basically delete (if exist) and create new object 
- DIFFERENTIAL - modify current object to reach desire configuration state as reflected in structure, it will change/add/remove accordingly.

the former suitable for "push-all-at-once" automation, the latter is good for "per-object" modifications as it keep external references

the SDK is requires Python >3.6

further details & doc will be added later

Installation
=================

```pycon
pip install radware-sdk-common
```

Design Principles
=================

-	Define the Interfaces for beans, configurators, management 
-	Define device connections API
-	Provide the Backend driver for communication: currently supports REST
-	Define the abstraction base structure and interface
-	Exceptions
-	Translate enums: developer/user can work with string/values/enum
-	It is actually taking care of configuring the device and also provide a Configuration Manager with staging capability:

       - Diff before and after: at the abstraction level
       - Dry run: go down to the lowest code point, right before submitting the REST call.
       - Dry run report of duplicate entries (Differential=False), Identify duplicate entries within a structure
       - Normalizes result for diff: handle order mismatch, necessary for abstract compare (server1 == real2)
       - Differential update: Executes changes only - modify/add/remove, ignore attributes equal to existing. Useful to prevent errors due to conflicts with existing configuration entries
       - Write on change: Executes Alteon write calls only when an actual change has been evaluated. Prevent false apply due to internal index change
       - Translate result 
       - interface for struct-specific normalization
       

Authors
=======

common SDK was created by [Leon Meguira](https://https://github.com/leonmeguira)

Copyright
=======

Copyright 2019 Radware LTD

License
=======

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and



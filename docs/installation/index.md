<!--
===============================================
DeFFcode library source-code is deployed under the Apache 2.0 License:

Copyright (c) 2021 Abhishek Thakur(@abhiTronix) <abhi.una12@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
===============================================
-->

<figure>
  <img src="../assets/images/installation.png" loading="lazy" alt="DeFFcode Installation" class="center"/>
</figure>

&emsp; 

# Installation Notes


## Supported Systems

DeFFcode is well-tested and supported on the following systems(but not limited to), with [python 3.7+](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip) installed:

??? alert ":fontawesome-brands-python: Upgrade your `pip`"

    ==It strongly advised to upgrade to latest [pip](https://pip.pypa.io/en/stable/installing/) before installing deffcode to avoid any undesired installation error(s).==

    There are two mechanisms to upgrade `pip`:

    === "`pip`"

        You can use existing `pip` to upgrade itself:

        ??? info "Install `pip` if not present"

            * Download the script, from https://bootstrap.pypa.io/get-pip.py.
            * Open a terminal/command prompt, `cd` to the folder containing the `get-pip.py` file and run:

            === "Linux/MacOS"

                ```sh
                python get-pip.py
                
                ```

            === "Windows"

                ```sh
                py get-pip.py
                
                ```
            More details about this script can be found in [pypa/get-pip’s README](https://github.com/pypa/get-pip).


        === "Linux/MacOS"

            ```sh
            python -m pip install pip --upgrade
            
            ```

        === "Windows"

            ```sh
            py -m pip install pip --upgrade
            
            ```

    === "`ensurepip`"

        Python also comes with an [`ensurepip`](https://docs.python.org/3/library/ensurepip.html#module-ensurepip) module[^1], which can easily upgrade/install `pip` in any Python environment.

        === "Linux/MacOS"

            ```sh
            python -m ensurepip --upgrade
            
            ```

        === "Windows"

            ```sh
            py -m ensurepip --upgrade
            
            ```

* Any :material-linux: Linux distro released in 2016 or later
* :fontawesome-brands-windows: Windows 7 or later
* :material-apple: MacOS 10.12.6 (Sierra) or later

&thinsp;

## Supported Python legacies

:fontawesome-brands-python: [**Python 3.7+**](https://www.python.org/downloads/) are only supported legacies for installing DeFFcode v0.1.0 and above.

&thinsp;


## Prerequisites

When installing DeFFcode, [**FFmpeg**][ffmpeg] is the only prerequisites you need to install manually, except on Windows :fontawesome-brands-windows::

### FFmpeg 

Must require FFmpeg binaries installed for all core functions. 

!!! tip "You easily install it by following this dedicated [**FFmpeg Installation doc**](../installation/ffmpeg_install/)"

&nbsp;

## Installation

### A. Install using pip (Recommended)


> _Best option for easily getting stable DeFFcode installed._


**Installation is as simple as:**

??? warning ":fontawesome-brands-windows: Windows Installation"

    If you are using Windows, some of the commands given below, may not work out-of-the-box.

    A quick solution may be to preface every Python command with `python -m` like this:

    ```sh
    # Install latest stable release
    python -m pip install -U deffcode
    ```

    And, If you don't have the privileges to the directory you're installing package. Then use `--user` flag, that makes pip install packages in your home directory instead:

    ```sh
    # Install latest stable release
    python -m pip install --upgrade --user deffcode
    ```

    Or, If you're using `py` as alias for installed python, then:

    ```sh
    # Install latest stable release
    py -m pip install --upgrade --user deffcode
    ```

```sh
# Install latest stable release
pip install -U deffcode
```

**And you can also download its wheel (`.whl`) package from our repository's [releases](https://github.com/abhiTronix/deffcode/releases) section, thereby can be installed as follows:**

```sh
# Install latest release
pip install deffcode-0.1.0-py3-none-any.whl
```

&thinsp;

### B. Installation from Source

>  Best option for trying latest patches(maybe experimental), forking for Pull Requests, or automatically installing all prerequisites(with a few exceptions). 

**If you want to checkout the latest beta [`dev`](https://github.com/abhiTronix/deffcode/tree/dev) branch , you can do so with the following commands:**

!!! danger "DO NOT clone or install any other branch other than `dev` unless advised, as it is not tested with CI environments and possibly very unstable or unusable."

??? warning ":fontawesome-brands-windows: Windows Installation"

    If you are using Windows, some of the commands given below, may not work out-of-the-box.

    A quick solution may be to preface every Python command with `python -m` like this:

    ```sh
    # Install latest beta branch
    python -m pip install -U .
    ```

    And, If you don't have the privileges to the directory you're installing package. Then use `--user` flag, that makes pip install packages in your home directory instead:

    ```sh
    # Install latest beta branch
    python -m pip install --upgrade --user .
    ```

    Or, If you're using `py` as alias for installed python, then:

    ```sh
    # Install latest beta branch
    py -m pip install --upgrade --user .
    ```
    

```sh
# clone the repository and get inside
git clone https://github.com/abhiTronix/deffcode.git && cd deffcode

# checkout the dev beta branch
git checkout dev

# Install it
pip install -U .
```

&nbsp;

[^1]: :warning: The `ensurepip` module is missing/disabled on Ubuntu. Use `pip` method only.

[ffmpeg]:https://www.ffmpeg.org/
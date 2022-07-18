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

# FFmpeg Installation Doc

<figure>
  <a href="http://ffmpeg.org/"><img src="../../assets/images/ffmpeg.png" loading="lazy" alt="FFmpeg"/></a>
</figure>

&thinsp;

==:warning: **DeFFcode APIs requires FFmpeg binaries to be installed for all of its core functionality.**==


You can following machine-specific instructions for its installation:

!!! error "DeFFcode APIs will throw **RuntimeError**, if they failed to detect valid FFmpeg executables on your system."
!!! tip "Enable verbose _([`verbose=True`](../params/#verbose))_ for debugging FFmpeg validation process."

&thinsp;

## :material-linux: Linux FFmpeg Installation

All DeFFcode APIs supports _Auto-Detection_ and _Manual Configuration_ methods on a Linux machine:

### A. Auto-Detection 

!!! quote "This is a recommended approach on Linux Machines"

If DeFFcode APIs do not receive any input from the user on [**`custom_ffmpeg`**](../params/#custom_ffmpeg) parameter, then they try to **auto-detect** the required FFmpeg installed binaries through a validation test that employs `subprocess` python module on the Linux OS systems.

**Installation:** You can install easily install official FFmpeg according to your Linux Distro by following [this post ➶](https://www.tecmint.com/install-ffmpeg-in-linux/)


### B. Manual Configuration

* **Download:** You can also manually download the latest Linux Static Binaries(*based on your machine arch(x86/x64)*) from the link below:

    *Linux Static Binaries:* http://johnvansickle.com/ffmpeg/

* **Assignment:** Then, you can easily assign the custom path to the folder containing FFmpeg executables(`for e.g 'ffmpeg/bin'`)  or path of `ffmpeg` executable itself to the [**`custom_ffmpeg`**](../params/#custom_ffmpeg) parameter in the DeFFcode APIs.

    !!! warning "If binaries were not found at the manually specified path, DeFFcode APIs will throw **RuntimeError**!"

&nbsp;

&nbsp;

## :fontawesome-brands-windows: Windows FFmpeg Installation

DeFFcode APIs supports _Auto-Installation_ and _Manual Configuration_ methods on Windows systems.

### A. Auto-Installation

!!! quote "This is a recommended approach on Windows Machines"

If DeFFcode APIs do not receive any input from the user on [**`custom_ffmpeg`**](../params/#custom_ffmpeg) parameter, then they try to **auto-generate** the required FFmpeg Static Binaries from our dedicated [**Github Server**](https://github.com/abhiTronix/FFmpeg-Builds) into the temporary directory(e.g. `C:\Temp`) of your machine on the Windows OS systems.


!!! danger "Active Internet connection is required while downloading required FFmpeg Static Binaries from our dedicated Github Server."

!!! warning Important Information

    * The files downloaded to a temporary directory (e.g. `C:\TEMP`), may get erased if your machine shutdowns/restarts.

    * You can also provide a custom save path for auto-downloading **FFmpeg Static Binaries** through [`-ffmpeg_download_path`](../params/#a-exclusive-parameters) parameter.

    * If binaries were found at the specified path, StreamGear automatically skips the auto-installation step.

    * ==If the required FFmpeg static binary fails to download, extract, or validate during auto-installation, then DeFFcode APIs will exit with **RuntimeError**!==


### B. Manual Configuration

* **Download:** You can also manually download the latest Windows Static Binaries(*based on your machine arch(x86/x64)*) from the link below:
   
      *Windows Static Binaries:* https://ffmpeg.org/download.html#build-windows

*  **Assignment:** Then, you can easily assign the custom path to the folder containing FFmpeg executables(`for e.g 'C:/foo/Downloads/ffmpeg/bin'`) or path of `ffmpeg.exe` executable itself to the [**`custom_ffmpeg`**](../params/#custom_ffmpeg) parameter in the DeFFcode APIs.

    !!! warning "If binaries were not found at the manually specified path, DeFFcode APIs will throw **RuntimeError**!"


&nbsp;

&nbsp;

## :material-apple: MacOS FFmpeg Installation

DeFFcode APIs supports _Auto-Detection_ and _Manual Configuration_ methods on a macOS machine.

### A. Auto-Detection

!!! quote "This is a recommended approach on MacOS Machines"

If DeFFcode APIs do not receive any input from the user on [**`custom_ffmpeg`**](../params/#custom_ffmpeg) parameter, then they try to **auto-detect** the required FFmpeg installed binaries through a validation test that employs `subprocess` python module on the MacOS systems.

**Installation:** You can easily install FFmpeg on your macOS machine by following [this tutorial ➶](https://trac.ffmpeg.org/wiki/CompilationGuide/macOS)

### B. Manual Configuration

* **Download:** You can also manually download the latest macOS Static Binaries(*only x64 Binaries*) from the link below:
  
    *MacOS Static Binaries:* http://johnvansickle.com/ffmpeg/

* **Assignment:** Then, you can easily assign the custom path to the folder containing FFmpeg executables(`for e.g 'ffmpeg/bin'`) or path of `ffmpeg` executable itself to the [**`custom_ffmpeg`**](../params/#custom_ffmpeg) parameter in the DeFFcode APIs.


    !!! warning "If binaries were not found at the manually specified path, DeFFcode APIs will throw **RuntimeError**!"

   
&nbsp;


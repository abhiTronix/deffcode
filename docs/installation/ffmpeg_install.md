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


You can following machine-specific instructions for its configuration/installation:

!!! fail "DeFFcode APIs will throw **RuntimeError**, if they failed to detect valid FFmpeg executables on your system."
!!! tip "Enable verbose ([`verbose=True`](../../reference/ffdecoder/params/#verbose)) for debugging FFmpeg validation process."

&thinsp;

## :material-linux: Linux FFmpeg Installation

DeFFcode APIs supports **Auto-Detection** and **Manual Configuration** methods on a Linux OS machines:

### A. Auto-Detection 

!!! quote "This is a recommended approach on Linux Machines"

If DeFFcode APIs do not receive any input from the user on [**`custom_ffmpeg`**](../../reference/ffdecoder/params/#custom_ffmpeg) parameter, then they try to **auto-detect** the required FFmpeg installed binaries through a validation test that employs `subprocess` python module on the Linux OS systems.

!!! abstract "You can install easily install official FFmpeg according to your Linux Distro by following [this post ➶](https://www.tecmint.com/install-ffmpeg-in-linux/)"


### B. Manual Configuration

* **Download:** You can also manually download the latest Linux Static Binaries(*based on your machine arch(x86/x64)*) from the link below:

    **:material-file-download: Linux Static Binaries:** http://johnvansickle.com/ffmpeg/

* **Assignment:** Then, you can easily assign the custom path to the folder containing FFmpeg executables(`for e.g 'ffmpeg/bin'`)  or path of `ffmpeg` executable itself to the [**`custom_ffmpeg`**](../../reference/ffdecoder/params/#custom_ffmpeg) parameter in the DeFFcode APIs.

    !!! warning "If binaries were not found at the manually specified path, DeFFcode APIs will throw **RuntimeError**!"

&nbsp;

&nbsp;

## :fontawesome-brands-windows: Windows FFmpeg Installation

DeFFcode APIs supports **Auto-Installation** and **Manual Configuration** methods on Windows OS machines:

### A. Auto-Installation

!!! quote "This is a recommended approach on Windows Machines"

If DeFFcode APIs do not receive any input from the user on [**`custom_ffmpeg`**](../../reference/ffdecoder/params/#custom_ffmpeg) parameter, then they try to **auto-generate** the required FFmpeg Static Binaries from our dedicated [**Github Server**](https://github.com/abhiTronix/FFmpeg-Builds) into the temporary directory(e.g. `C:\Temp`) of your machine on the Windows OS systems.


!!! danger "Active Internet connection is required while downloading required FFmpeg Static Binaries from our dedicated [**Github Server**](https://github.com/abhiTronix/FFmpeg-Builds) onto your :fontawesome-brands-windows: Windows machine."

???+ warning "Important Information regarding Auto-Installation"

    * The files downloaded to a temporary directory (e.g. `C:\TEMP`), may get erased if your machine shutdowns/restarts in some cases.

    * You can also provide a custom save path for auto-downloading **FFmpeg Static Binaries** through exclusive [`-ffmpeg_download_path`](../../reference/sourcer/params/#exclusive-parameters) attribute in Sourcer API.

        ??? question "How to use  `-ffmpeg_download_path` attribute in FFdecoder API?"
            
            `-ffmpeg_download_path` is also available in FFdecoder API through the [`-custom_sourcer_params`](../../reference/ffdecoder/params/#b-exclusive-parameters) attribute of its `ffparams` dictionary parameter"

    * If binaries were found at the specified path, DeFFcode APIs automatically skips the auto-installation step.

    * ==If the required FFmpeg static binary fails to download, extract, or validate during auto-installation, then DeFFcode APIs will exit with **RuntimeError**!==


### B. Manual Configuration

* **Download:** You can also manually download the latest Windows Static Binaries(*based on your machine arch(x86/x64)*) from the link below:
   
      **:material-file-download: Windows Static Binaries:** https://ffmpeg.org/download.html#build-windows

*  **Assignment:** Then, you can easily assign the custom path to the folder containing FFmpeg executables(`for e.g 'C:/foo/Downloads/ffmpeg/bin'`) or path of `ffmpeg.exe` executable itself to the [**`custom_ffmpeg`**](../../reference/ffdecoder/params/#custom_ffmpeg) parameter in the DeFFcode APIs.

    !!! warning "If binaries were not found at the manually specified path, DeFFcode APIs will throw **RuntimeError**!"


&nbsp;

&nbsp;

## :material-apple: MacOS FFmpeg Installation

DeFFcode APIs supports **Auto-Detection** and **Manual Configuration** methods on MacOS OS machines:

### A. Auto-Detection

!!! quote "This is a recommended approach on MacOS Machines"

If DeFFcode APIs do not receive any input from the user on [**`custom_ffmpeg`**](../../reference/ffdecoder/params/#custom_ffmpeg) parameter, then they try to **auto-detect** the required FFmpeg installed binaries through a validation test that employs `subprocess` python module on the MacOS systems.

!!! abstract "You can easily install FFmpeg on your MacOS machine by following [this tutorial ➶](https://trac.ffmpeg.org/wiki/CompilationGuide/macOS)"

### B. Manual Configuration

* **Download:** You can also manually download the latest MacOS Static Binaries(*only x64 Binaries*) from the link below:
  
    **:material-file-download: MacOS Static Binaries:** https://ffmpeg.org/download.html#build-mac

* **Assignment:** Then, you can easily assign the custom path to the folder containing FFmpeg executables(`for e.g 'ffmpeg/bin'`) or path of `ffmpeg` executable itself to the [**`custom_ffmpeg`**](../../reference/ffdecoder/params/#custom_ffmpeg) parameter in the DeFFcode APIs.


    !!! warning "If binaries were not found at the manually specified path, DeFFcode APIs will throw **RuntimeError**!"

   
&nbsp;


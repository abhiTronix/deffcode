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

# Release Notes

## v0.2.2 (2022-09-08) :material-new-box:

??? new "New Features"
    - [x] **Sourcer API:**
        * Added support for `-ffprefixes` attribute through Sourcer API's `sourcer_param` dictionary parameter _(similar to FFdecoder API)_.
    - [x] **FFdecoder API:** 
        * Added new `output_frames_pixfmt` metadata property to preview and handle output frames pixel-format.
    - [x] **Docs:**
        * Added separate "Basic" and "Advanced" Recipes markdowns files with self-explanatory text, related usage code, asset _(such as images, diagrams, GIFs, etc.)_, and UI upgrades for bringing standard quality to visual design. 
        * Added separate `index.md` for Basic and Advanced Recipes with introductory text and curated hyperlinks for quick references to various recipes _(separated with sub-categories "Decoding", "Transcoding", and "Extracting Video Metadata")_.
        * Added related admonitions to specify python dependencies as well as other requirements and relevant information required for each of these recipes.
        * Added new Basic Decoding Recipes:
            * Added Decoding Video files with various pixel formats recipes.
            * Added Decoding Live Feed Devices recipes with `source_demuxer` FFdecoder API parameter.
            * Added Decoding Image sequences recipes supporting Sequential, Glob pattern , Single (looping) image.
            * Added Decoding Network Streams recipes.
        * Added new Basic Transcoding Recipes:
            * Added Transcoding Live frames recipes with OpenCV and WriteGear.
            * Added Transcoding Live Simple Filtergraphs recipes with OpenCV.
            * Added Saving Key-frames as Image recipes with different image processing libraries.
        * Added new Basic Extracting Video Metadata Recipes:
            * Added Extracting Video Metadata recipes with FFdecoder and Sourcer APIs.
        * Added new Advanced Decoding Recipes:
            * Added Hardware-Accelerated Video Decoding recipe using NVIDIA's H.264 CUVID Video-decoder(`h264_cuvid`).
            * Added Decoding Live Virtual Sources recipes with many test patterns using `lavfi` input virtual device.
        * Added new Advanced Decoding Recipes:
            * Added lossless Hardware-Accelerated Video Transcoding recipe with WriteGear API.
            * Added Transcoding Live Complex Filtergraphs recipes with WriteGear API.
            * Added Transcoding Video Art with Filtergraphs recipes with WriteGear API for creating real-time artistic generative video art using simple and complex filtergraphs.
        * Added new Advanced Updating Video Metadata Recipes:
            * Added Updating Video Metadata recipes with user-defined as well as source metadata in FFdecoder API.
        * Added new dark and light theme logo support.
        * Added new recipes GIF assets to `gifs` folder.
        * Added new dark logo `deffcode-dark.png` asset to `images` folder.
        * Added new `ffdecoder.png` and `sourcer.png` Image assets to `images` folder.
        * Added new `navigation.tabs` feature.
        * Added Material Announcement-Bar notifying recent changes.

??? success "Updates/Improvements"  
    - [x] Sourcer API:
        * Implemented new validation checks to ensure given `source` has usable video stream available by checking availability of either `video bitrate` or both `frame-size` and `framerate`_ properties in the source metadata.
        * Improved `extract_resolution_framerate` method for making framerate extraction more robust by falling back to extracting `TBR` value when no framerate value available in the source metadata.
    - [x] FFdecoder API:
        * Updated `metadata` property object to validate and override source metadata properties directly by overloading same property object before formulating Frames Decoder Pipeline:
            * Implemented validation checks to verify each validate manually assigned source metadata property against specific datatype before overriding.
            * Updated logging to notify invalid datatype values when assigned through `metadata` property object.
            * Added support for overriding `source_video_resolution` source metadata property to control frame-size directly through metadata.
            * Added support for overriding `output_frames_pixfmt` metadata attribute to be used as default pixel-format, when `frame_format` parameter value is None-type.
            * Improved handling of source metadata keys in metadata property object.
        * Updated `metadata` property object to handle and assign User-defined metadata directly by overloading the same property object:
            * Added new internal `user_metadata` class variable to handle all User-defined metadata information separately.            
            * FFdecoder API's `metadata` property object now returns User-defined metadata information merged with Source Video metadata.
            * Added `tuple` value warning log to notify users `json` module converts Python `tuples` to JSON `lists`.
        * Improved logic to test validity of `-custom_resolution` attribute value through `ffparams` dictionary parameter.
        * Improved handling of FFmpeg pipeline framerate with both user-defined and metadata defined values.
        * Added `tuple` to exception in datatype check for `ffparams` dictionary parameter.
        * Added datatype validation check for `frame_format` parameter.
        * Improved handling of `-framerate` parameter. 
    - [x] Maintenance:
        * Reformatted all Core class and methods text descriptions:
            * Rewritten introductory each API class description.
            * Moved reference block from `index.md` to class description.
            * Fixed missing class and methods parameter description.
            * Fixed typos and context in texts.
            * Reformatted code comments.
        * Simplified `for` loop with `if` condition checking in metadata property object.
        * Updated logging comments.
    - [x] Setup:
          * Updated project description in metadata.
          * Bumped version to `0.2.2`.
    - [x] Docs:
        * Updated Introduction doc:
            * Added new text sections such as "Getting Started", "Installation Notes", "Recipes a.k.a Examples" and "API in a nutshell".
            * Rewritten Introduction(`index.md`) with recent Information, redefined context, UI changes, updated recipe codes, curated hyperlinks to various recipes(separated with categories), and relatable GIFs.
            * Updated spacing in `index.md` using `spacer` class within `<div>` tag and `&nbsp;`.
            * Reformatted and centered DeFFcode Introductory description.
            * Reformatted FFmpeg Installation doc and Issue & PR guidelines.
            * Updated static FFmpeg binaries download URLs in FFmpeg Installation doc.
            * Refashioned text contexts, icons, and recipes codes.
            * Updated Key Features section with reflecting new features.
        * Updated README.md:
            * Updated README.md w.r.t recent changes in Introduction(`index.md`) doc.
            * Simplified and Reformatted text sections similar to Introduction doc. 
            * Imported new "Contributions" and "Donations" sections from VidGear docs.
            * Added collapsible text and output section using `<summary>` and `<detail>` tags.
            * Added experimental note GitHub blockquote to simulate admonition in README.md.
            * Removed tag-line from README.md and related image asset.
            * Simplified and Grouped README URL hyperlinks.
            * Removed Roadmap section.
        * Updated Recipes docs:
            * Revamped DeFFcode Introduction `index.md` with new Information, Context and UI changes, Updated example codes and hyperlinks.
            * Updated Announcement Bar to fix `announcement_link` variable and text.
            * Updated footer note to notify users regarding `tuple` value warning in FFdecoder API.
            * Rewritten recipes w.r.t breaking changes in APIs.
        * Updated Reference docs:
            * Completely revamped API's parameter reference docs.
            * Added new Functional Block Diagrams to FFdecoder and Sourcer API References.
            * Rewritten and Reformatted FFdecoder and Sourcer API's parameter reference docs with new information w.r.t recent changes.
            * Implemented new admonitions explaining new changes, related warnings/errors, usage examples etc.
            * Removed redundant `advanced.md` and `basic.md` docs.
            * Added new abstracts to FFhelper and Utils docs.
        * Updated docs site navigation and titles:
            * Reformatted `index.md` and `installation/index.md`.
            * Renamed `help/index.md` to `help/help.md`.
            * Moved basic and advanced recipes from `example` to `recipes` folder.
            * Imported "Donations" sections from VidGear docs to `help.md`.
            * Added updated page-title and navigation hyperlinks in `mkdocs.yml` to new markdown files incorporated recently.
            * Updated internal navigation hyperlinks in docs and removed old redundant file links.
        * Updated docs UI:
            * Added custom `spacer` class in CSS for custom vertical spacing.
            * Imported new "New", "Advance", "Alert", "Danger" and "Bug" admonitions custom CSS UI patches from vidgear.
            * Updated all admonitions icons with new custom icon SVG+XML URLs.
            * Reformatted `custom.css` and added missing comments.
            * Updated docs fonts:
                * Updated text font to `Heebo`.
                * Updated code font to `JetBrains Mono`.
            * Updated primary and accent colors:
                * Updated primary light color to `light green`.
                * Updated primary dark color to `amber`.
                * Updated accent light color to `green`.
                * Updated accent dark color to `lime`.
            * Replaced admonitions with appropriate ones.
            * Changed Color palette toggle icons.
            * Updated icons in title headings.
        * Updated admonitions messages.
        * Updated `changelog.md`.
    - [x] CI:
        * Pinned `jinja2` version to `<3.1.0`, since `jinja2>=3.1.0` breaks mkdocs (mkdocs/mkdocs#2799).
        * Updated unittests w.r.t recent changes in APIs: 
            * Updated `test_frame_format` unittest to include manually assign output pixel-format via `metadata` property object.
            * Updated `test_metadata` unittest to include new `checks` parameter to decide whether to perform Assertion test on assigned `metadata` properties in FFdecoder API.
            * Added new parametrize attributes in `test_metadata` and `test_seek_n_save` unittests to cover every use-cases.
            * Replaced `IOError` with `ValueError` in Sourcer API unittests.
        * Updated `test_metadata` unittest to verify `tuple` value warning.
        * Updated unittests to increase code coverage significantly.
        

??? danger "Breaking Updates/Changes"
    * **Sourcer API:**
        - [x] :skull_crossbones: Sourcer API's  `retrieve_metadata()` method now returns parsed metadata either as JSON string or dictionary type.
            * Added new `pretty_json` boolean parameter to `retrieve_metadata()`, that is when `True`, returns metadata formatted as JSON string instead of default python dictionary.
        - [x] :skull_crossbones: Changed `IOError` to `ValueError` in Sourcer API, raised when source with no decodable audio or video stream is provided.
    * **FFdecoder API:**
        - [x] :skull_crossbones: Rename `extraparams` dictionary parameter to `ffparams` in FFdecoder API. 
        - [x] :skull_crossbones: The `source` metadata value cannot be altered through `metadata` property object in FFdecoder API. 
        - [x] :skull_crossbones: Removed `-ffpostfixes` attribute support from `ffparams` dictionary parameter in FFdecoder API, since totally redundant in favor of similar `-ffprefixes` and `-clones` attributes.

??? bug "Bug-fixes"
    - [x] FFdecoder API:
        * Fixed `metadata` property object unable to process user-defined keys when any source metadata keys are defined.
        * Fixed `TypeError` bug with string type `-framerate` parameter values.
    - [x] Sourcer API:
        * Fixed Sourcer API throws `IOError` for videos containing streams without both source bitrate and framerate defined _(such as from `lavfi` input virtual device)_.
        * Fixed `AttributeError` bug due to typo in variable name.
    - [x] CI:
        * Fixed support for newer mkdocstring version in DeFFcode Docs Deployer workflow.
            * Added new `mkdocstrings-python-legacy` dependency.
            * Replaced `rendering` variable with `options`.
            * Removed pinned `mkdocstrings==0.17.0` version.
            * Removed redundant variables.
        * Updated `test_metadata` unittest to fix `AssertionError` Bug.
    - [x] Docs:
        * Fixed some admonitions icons not showing bug using `!important` rule in CSS.
        * Fixed `404.html` static page not showing up.
        * Fixed invalid internal navigation hyperlinks and asset paths.
        * Removed `quote/cite/summary` admonition custom UI patches.
        * Removed redundant information texts.
        * Fixed typos in code comments.
        * Fixed typos in example code.
        

??? question "Pull Requests"
    * PR #23

&nbsp; 

&nbsp; 

## v0.2.1 (2022-07-14)

??? new "New Features"
    - [x] **Sourcer API:**
        * Implemented support for extracting metadata from live input devices/sources.
        * Added new `source_demuxer` and `forced_validate` parameters to `validate_source` internal method.
        * Implemented logic to validate `source_demuxer` value against FFmpeg supported demuxers.
        * Rearranged metadata dict.
        * Updated Code comments.
    - [x] **FFdecoder API:** 
        * Implemented functionality to supported live devices by allowing device path and respective demuxer into pipeline.
        * Included `-f` FFmpeg parameter into pipeline to specify source device demuxer.
        * Added special case for discarding `-framerate` value with Nonetype.
    - [x] **CI:**
        * Added new unittest `test_camera_capture()` to test support for live Virtual Camera devices.
        * Added new `v4l2loopback-dkms`, `v4l2loopback-utils` and kernel related APT dependencies. 
    - [x] **Bash Script:**
        * Added new FFmpeg command to extract image datasets from given video on Linux envs.
        * Created live Virtual Camera devices through `v4l2loopback` library on Github Actions Linux envs. 
            * Added `v4l2loopback` modprobe command to setup Virtual Camera named `VCamera` dynamically at `/dev/video2`.
            * Added `v4l2-ctl --list-devices` command for debugging.
            * Implemented FFmpeg command through `nohup`(no hangup) to feed video loop input to Virtual Camera in the background.

??? success "Updates/Improvements"  
    - [x] Sourcer API:
        * Only either `source_demuxer` or `source_extension` attribute can be present in metadata.
        * Enforced `forced_validate` for live input devices/sources in `validate_source` internal method.
    - [x] FFdecoder API:
        * Rearranged FFmpeg parameters in pipeline.
        * Removed redundant code.
        * Updated Code comments.
    - [x] FFhelper API:
        * Logged error message on metadata extraction failure.
    - [x] CI:
        * Restricted `test_camera_capture()` unittest to Linux envs only.
        * Removed `return_generated_frames_path()` method support for Linux envs. 
        * Pinned jinja2 `3.1.0` or above breaking mkdocs. 
            * `jinja2>=3.1.0` breaks mkdocs (mkdocs/mkdocs#2799), therefore pinned jinja2 version to `<3.1.0`.
    - [x] Bash Script:
          * Updated to latest FFmpeg Static Binaries links. 
              * Updated download links to abhiTronix/ffmpeg-static-builds * hosting latest available versions.
              * Updated date/version tag to `12-07-2022`.
              * Removed depreciated binaries download links and code.
    - [x] Setup:
          * Bumped version to 0.2.1.
    - [x] Docs:
          * Updated Changelog.md

??? danger "Breaking Updates/Changes"
    - [x] :skull_crossbones: **Implement support for live input devices/sources.**
        * `source` parameter now accepts device name or path.
        * Added `source_demuxer` parameter to specify demuxer for live input devices/sources.
        * Implemented Automated inserting of `-f` FFmpeg parameter whenever `source_demuxer` is specified by the user.

??? bug "Bug-fixes"
    - [x] Sourcer API:
        * Fixed Nonetype value bug in `source_demuxer` assertion logic.
        * Fixed typos in parameter names.
        * Added missing import.
    - [x] FFhelper API:
        * Logged error message on metadata extraction failure.
        * Fixed bug with `get_supported_demuxers` not detecting name patterns with commas.
        * Removed redundant logging.
    - [x] CI:
        * Fixed critical permission bug causing  `v4l2loopback` to fail on Github Actions Linux envs. 
            * Elevated privileges to `root` by adding `sudo` to all commands(including bash scripts and python commands).
            * Updated vidgear dependency to pip install from its git `testing` branch with recent bug fixes.
            * Replaced relative paths with absolute paths in unit tests.
        * Fixed WriteGear API unable to write frames due to permission errors.
        * Fixed `test_source_playback()` test failing on Darwin envs with OLD FFmpeg binaries.
            * Removed `custom_ffmpeg` value for Darwin envs.
        * Fixed various naming typos.
        * Fixed missing APT dependencies. 

??? question "Pull Requests"
    * PR #17

&nbsp; 

&nbsp; 

## v0.2.0 (2022-03-21)

??? new "New Features"
    - [x] Sourcer API:
        - **Added a new `source_audio_samplerate` metadata parameter:**
            - Re-implemented  `__extract_audio_bitrate` internal function from scratch as `__extract_audio_bitrate_nd_samplerate`.
                - Implemented new algorithm to extract both extract both audio bitrate and samplerate from given source.
                - Updated regex patterns according to changes.
            - Updated `__contains_video` and `__contains_audio` logic to support new changes.
        - **Added metadata extraction support:**
            - Added `retrieve_metadata` class method to Sourcer API for extracting source metadata as python dictionary.
                * Populated private source member values in dictionary with distinct keys.
        - Added new `-force_validate_source` attribute to Sourcer API's `sourcer_params` dict parameter for special cases.
        - Implemented check whether `probe_stream()` called or not in Sourcer API.
    - [x] FFdecoder API:
        - **Added metadata extraction and updation support:**
            - Added `metadata` property object function to FFdecoder API for retrieving source metadata form Sourcer API as dict and return it as JSON dump for pretty printing.
                * Added Operational Mode as read-only property in metadata.
            - Added `metadata` property object with `setter()` method for updating source metadata with user-defined dictionary.
                * Implemented way to manually alter metadata keys and values for custom results.
    - [x] Docs:
        * **Added new comprehensive documentation with Mkdocs:**
            - Added new image assets:
                - Added new Deffcode banner image, logo and tagline
                - Added new icon ICO file with each layer of the favicon holds a different size of the image.
                - Added new png images for best compatibility with different web browsers.
            - Added new docs files: 
                - Added new index.md with introduction to project.
                - Added new changelog.md.
                - Added license.md
                - Added new index.md with instructions for contributing in DeFFcode.
                    - Added `issue.md` with Issue Contribution Guidelines.
                    - Added `PR.md` with PR Contribution Guidelines.
                - Added new `custom.js` to add gitter sidecard support.
                - Added new `custom.css` that brings standard and quality visual design experience to DeFFcode docs.
                    - Added new admonitions `new` and `alert`.
                - Added separate LICENSE(under CC creative commons) and REAME.md for assets.
                - Added new `main.html` extending `base.html` for defining custom site metadata.
                - Added deFFcode banner image to metadata.
                - Added twitter card and metadata.
                - Added version warning for displaying a warning when the user visits any other version.
                - Added footer sponsorship block.
                - Added gitter card official JS script dist.
                - Added new custom `404.html` to handle HTTP status code `404` Not Found.
                    - Implemented custom theming with new CSS style.
                    - Added custom 404 image asset.
                - Added new `index.md` with DeFFcode Installation notes.
                    - Added info about Supported Systems, Supported Python legacies, Prerequisites, Installation instructions.
                    - Added Pip and Source Installation instructions.
                - Added new `ffmpeg_install.md` with machine-specific instructions for FFmpeg installation.
                - Added new `index.md` with different ways to help DeFFcode, other users, and the author.
                    - Added info about Starring and Watching DeFFcode on GitHub, Helping with open issues etc.
                    - Added Tweeter intent used for tweeting `#deffode` hastags easily.
                    - Added Kofi Donation link button.
                    - Added author contact links and left align avatar image.
                - Added new `get_help.md` to get help with DeFFcode.
                    - Added DeFFcode gitter community link.
                    - Added other helpful links.
            - Added new assets folders.
            - Added Basic Recipes with basic.md 
            - Added Advanced Recipes with advanced.md 
            - Added all API References. 
                - Added `mkdocstrings` automatic documentation from sources.
                - Added new `index.md` for FFdecoder API with its description and explaining its API.
                - Added new `index.md` for Sourcer API with its description and explaining its API.
                - Added ffhelper methods API references.
                - Added utils methods API references.
            - Added all API Parameters. 
                - Added new `params.md` for FFdecoder API explaining all its parameters.
                - Added new `params.md` for Sourcer API explaining all its parameters.
                - Added Mkdocs support with mkdocs.yml 
            - Implemented new `mkdocs.yml` with relevant parameters.
                - Added extended material theme with overridden parts.
                - Added site metadata with site_name, site_url, site_author, site_description, repo_name, repo_url, edit_uri, copyright etc.
                - Added navigation under sections for easily accessing each document.
                - Implemented Page tree for DeFFcode docs.
                - Added features like navigation.tracking, navigation.indexes, navigation.top, search.suggest, search.highlight, search.share, content.code.annotate.
                - Added separate palette [default]light(with primary:green accent: dark green) and [slate]dark(with primary:teal accent: light green) mode.
                - Added Color palette toggle switch with icon `material/home-lightning-bolt`.
                - Added support for all pymarkdown-extensions.
                - Added google fonts for text: `Quicksand` and code: `Fira Code`.
                - Added custom logo and icon for DeFFcode.
                - Added support for plugins like search, git-revision-date-localized, minify.
                - Added support for `mkdocstrings` plugin for auto-built API references.
                    * Added python handler for parsing python source-code to `mkdocstrings`.
                    * Improved source-code docs for compatibility with `mkdocstrings`.
                - Added support for extensions like `admonition`, `attr_list`, `codehilite`, `def_list`, `footnotes`, `meta`, and `toc`.
                - Added social icons and links.
                - Added custom `extra_css` and `extra_javascript`.
                - Added support for `en` (English) language.
            - Added new badges to README.md for displaying current status of CI jobs and coverage.
            - Added Roadmap to README.md
    - [x] CI:
        * **Automated CI support for different environments:**
            - Implemented auto-handling of dependencies installation, unit testing, and coverage report uploading.
            - Added GitHub Action workflow for Linux envs:
                - Added and configured `CIlinux.yml` to enable GitHub Action workflow for Linux-based Testing Envs.
                - Added `3.7+` python-versions to build matrix.
                - Added code coverage through `codecov/codecov-action@v2` workflow for measuring unit-tests effectiveness.
                    * Implemented behavior to about coverage upload on timeout(error code `124`) in pytests.
            - Added Appveyor workflow for Windows envs: 
                - Add and configured `appveyor.yml` to enable Appveyor workflow for Windows-based Testing Envs.
                - Added `3.7+` 64-bit python-versions to build matrix.
                - Enabled `fast_finish` to exit immediately on error.
            - Added Azure-Pipelines workflow for MacOS envs: 
                - Add and configured `azure-pipelines.yml` to enable Azure-Pipelines workflow for MacOS-based Testing Envs.
                - Added code coverage through `codecov` workflow for measuring unit-tests effectiveness.
                    * Added online auto validation of `codecov` bash script using `SH256SUM` and `sig` files as recommended.
                - Implemented behavior to about coverage upload on timeout(error code `124`) in pytests.
                - Added `3.7+` python-versions to build matrix.
            - Added automated flake8 testing to discover any anomalies in code.
            - Added `master` branches for triggering CI.
        * **Implement new automated Docs Building and Deployment on `gh-pages` through GitHub Actions workflow:**
            - Added new workflow yaml `docs_deployer.yml` for automated docs deployment.
            - Added different jobs with ubuntu-latest environement to build matrix.
            - Added `actions/checkout@v2` for repo checkout and `actions/setup-python@v2` for python environment.
            - Pinned python version to `3.8` for python environment in docs building.
            - Added `GIT_TOKEN`, `GIT_NAME`, `GIT_EMAIL` environment variables through secrets.
            - Added Mkdocs Material theme related python dependencies and environments.
            - Added push on `master` and `dev` branch `release` with `published` as triggers.
            - Pinned `mkdocstrings==0.17.0`.
        * **Added new Automated Docs Versioning:**
            - Implemented Docs versioning through `mike`.
            - Separate new workflow steps to handle different versions.
            - Added step to auto-create `RELEASE_NAME` environment variable from DeFFcode version file.
            - Update docs deploy workflow to support `latest`, `release` and `dev` builds.
            - Added automatic release version extraction from GitHub events.
        * **Added Skip Duplicate Actions Workflow to DeFFcode Docs Deployer:**
            - Added Skip Duplicate Actions(`fkirc/skip-duplicate-actions@master`) Workflow to DeFFcode Docs Deployer to prevent redundant duplicate workflow-runs.
    - [x] Maintenance: 
        * **New DeFFcode project issue and PR templates:**
            - Added PR template:
                - Added a pull request template(`PULL_REQUEST_TEMPLATE.md`) for project contributors to automatically see the template's contents in the pull request body.
                - Added Brief Description, Requirements / Checklist, Related Issue, Context, Types of changes blocks.
            - Added Proposal, Bug-Report and Question templates:
                - Created an `ISSUE_TEMPLATE` subdirectory to contain multiple issue templates.
                - Add manually-created Proposal(`proposal.md`) and Question(`question.md`) issue template for project contributors to automatically see the template's contents in the issue body.
                    - Added Brief Description, Acknowledgment, Context, Current Environment, Any Other Information like blocks.
                - Add an manually-created Bug Report(`bug_report.md`) issue template to `ISSUE_TEMPLATE` subdirectory for project contributors to automatically see the template's contents in the issue body.
                    - Added Brief Description, Acknowledgment, Context, Current Environment, Expected Behavior, Actual Behavior, Possible Fix, Steps to reproduce, Miscellaneous like blocks.
                - Added YAML frontmatter to each issue template to pre-fill the issue title, automatically add labels and assignees, and give the template a name and description.
                - Added a `config.yml` file to the `.github/ISSUE_TEMPLATE` folder to customize the issue template chooser that people see when creating a new issue.
                - Set `blank_issues_enabled` parameter to `false` to encourage contributors to use issue templates.
                - Added `contact_links` parameter with gitter community link to receive regular issues outside of GitHub.
            - Added new `FUNDING.yml` with ko-fi donation link.
            - Added `.gitattributes` for DeFFcode, that set the default behavior, in case people don't have `core.autocrlf` set.
            - Imported Codecov config(`codecov.yml`) from vidgear to modify coverage parameters.
    - [x] Tests:
        * **Added DeFFcode unit tests with `pytest`:**
            - Added `essential.py` for defining all essential functions necessary for DeFFcode unit tests.
            - Added `return_static_ffmpeg`, `remove_file_safe`, `return_testvideo_path`, return_generated_frames_path, `actual_frame_count_n_frame_size` essential functions.
            - Added `is_windows` global variable.
            - Added related imports and logging.
            - Added `__init__.py`.
            - Moved all files to `test` folder.
            - Added DeFFcode's utils unit tests with pytest. 
                - Added new `test_loggerhandler` and `test_dict2Args` tests.
            - Added DeFFcode's ffhelper unit tests with pytest. 
                - Added new `test_ffmpeg_binaries_download`, `test_validate_ffmpeg`, `test_get_valid_ffmpeg_path`, `test_check_sp_output`, `test_is_valid_url`, `test_is_valid_image_seq`, and `test_validate_imgseqdir` parametrize tests.
            - Added DeFFcode's Sourcer API unit tests with pytest. 
                - Added new `test_source` and `test_probe_stream_n_retrieve_metadata` parametrize tests.
            - Added DeFFcode's FFdecoder API unit tests with pytest. 
                - Added new `test_source_playback`, `test_frame_format`, `test_metadata`, `test_seek_n_save`,  and `test_FFdecoder_params` parametrize unit tests.
            - Added related imports and logging.
            - Added unit test for `delete_file_safe` utils function.
    - [x] Bash: 
        - 🔧 Imported prepare_dataset.sh from vidgear for downloading pytest datasets to `temp` dir.

??? success "Updates/Improvements" 
    - [x] FFdecoder API:
        - Removed redundant forcing `-r` FFmpeg parameter for image sequences as source.
        - Removed redundant checks on `-vf` FFmpeg parameter.
        - FFmpeg parameter `-s` will be discarded in favor of `-custom_resolution` attribute.
        - Replaced `-constant_framerate` with FFmpeg `-framerate` attribute.
        - Replaced `-custom_source_params` with correct `-custom_sourcer_params` attribute.
        - Renamed `operational_mode` metadata parameter to `ffdecoder_operational_mode`.
    - [x] Sourcer API:
        - Converted all Sourcer APIs public available variables into private ones for stability.
          * All Sourcer's publicly accessed variable metadata values in FFdecoder, therefore replaced with dictionary counterparts.
        - Moved FFmpeg path validation and handling to Sourcer from FFdecoder API.
          * Moved `-ffmpeg_download_path` dictionary attribute to Sourcer API's `sourcer_params` parameter.
          * Moved dependencies and related functions.
    - [x] CI:
        - Excluded `dev` branch from triggering workflow on any environment. 
            - Updated yaml files to exclude beta `dev` branch from  triggering workflow on any environment.
            - Restricted codecov  to use only `master` branch.
        - Re-implemented `fkirc/skip-duplicate-actions@master` to Skip individual deploy steps instead of Skip entire jobs
    - [x] Docs:
        - Updated PR.md 
            - Added instructions to download `prepare_dataset.sh` using curl.
            - Updated dependencies for `pytest`.
        - Updated advanced.md 
            - Updated generating Video from Image sequence to save video using OpenCV writer instead of WriteGear API.
              - Added `frame_format="bgr24"`and additional instructions regarding OpenCV writer.
              - Updated example codes with new changes.
            - Rearranged examples placement.
        - Updates to custom.css 
            - Added donation sponsor link in page footer with heart animation.
            - Added bouncing heart animation through pure CSS.
            - Added Bold property to currently highlighted link in Navigation Bar.
            - Updated Navigation Bar title font size.
            - Updated version list text to uppercase and bold.
            - Updated icon for task list unchecked.
            - Added more top-padding to docs heading.
            - Updated Block quote symbol and theming.
            - Updated Custom Button theming to match docs.
            - Added new custom classes to create shadow effect in dark mode for better visibility.
            - Updated dark mode theme "slate" hue to 285.
        - Updated admonitions colors.
        - Updated gitter sidecard UI colors and properties.
        - Reflected recent changes in Sourcer and FFdecoder API's metadata.
        - Updated sample code formatting from `sh` to `json`.
        - Added missing docs for `delete_file_safe` utils function.
        - Updated Download Test Datasets instructions.
        - Updated contribution guidelines and installation docs with related changes.
        - Updated License Notice.
        - Updated code comments.
        - Updated logging messages.
        - Updated Deffcode Logo and Tagline to be dark-mode friendly.
        - Adjusted asset alignment.
        - Updated example code.
        - Updated Installation instructions, Requirements and Roadmap.
        - Corrected links to documents.
        - Updated project description.
        - Updated LICENSE.
        - Updated indentation and code comments
        - Re-aligned text and images in README.md
        - Adjusted image classes and width.
    - [x] Maintenance: 
        - Updated LICENSE notice to add vidgear notice.
        - Bumped version to `0.2.0`
        - Added useful comments for convenience.

??? danger "Breaking Updates/Changes"
    - [x] :skull_crossbones: Sourcer API will now raises Assertion error if `probe_stream()` not called before calling `retrieve_metadata()`.
    - [x] :skull_crossbones: Only `-framerate` values greater than `0.0` are now valid.
    - [x] :skull_crossbones: Renamed `decode_stream` to `probe_stream` in Sourcer API.
    - [x] :skull_crossbones: Any of _video bitrate_ or _video framerate_ are sufficient to validate if source contains valid video stream(s).
    - [x] :skull_crossbones: Any of _audio bitrate_ or _audio samplerate_ are sufficient to validate if source contains valid audio stream(s).

??? bug "Bug-fixes"
    - [x] APIs:
        - Added missing `delete_file_safe` function in utils. 
            - Imported `delete_file_safe` from vidgear to safely deletes files at given path.
        - Fixed forward slash bugs in regex patterns.
        - Fixed IndexError when no bitrate was discovered in given source.
        - Fixed FFmpeg subprocess pipeline not terminating gracefully in FFdecoder API.
        - Fixed `__version__` not defined in DeFFcode's `__init__.py` that throws `AttributeError: module 'deffcode' has no attribute '__version__'` on query.
            - Added necessary import in `__init__.py`.
    - [x] Docs:
        - Fixed missing `"-vcodec": "h264_cuvid"` value in example code.
        - Fixed typos in filenames in utils.py
        - Fixed internal missing or invalid hyperlinks.
        - Fixed improper docs context and typos.
        - Fixed "year" in license notice.
        - Fixed content spacing.
        - Fixed Gitter Community Link in Mkdocs.
        - Fixed typos in README.md.
        - Fixed typos in license notices.
        - Fixed typos in code comments.
        - Fixed typos in example code.
    - [x] CI:
        - Fixed missing FFmpeg dependency bug in GitHub Actions.
        - Fixes typo in Docs Deployer yaml.
        - Fixed if condition skipping when need is skipping
    - [x] Maintenance: 
        - Added missing imports.
        - Fixed redundant conditional logics.
        - Removed or Replaced redundant conditions and definitions.
        - Fixed minor typos in templates.

??? question "Pull Requests"
    * PR #5
    * PR #6
    * PR #8
    * PR #9
    * PR #11
    * PR #12
    * PR #13
    * PR #14

&nbsp; 

&nbsp; 

## v0.1.0 (2022-03-07)

??? new "New Features"
    - [x] **:tada: Open-Sourced DeFFcode under the Apache 2.0 License.**
    - [x] **Added new Classes(APIs):**
        * FFdecoder: Performant Real-time **Video frames Generator** for generating blazingly fast video frames(RGB ndarray by default).
        * Sourcer: Extracts source video metadata _(bitrate, resolution, framerate, nframes etc.)_ using its subprocess FFmpeg output.
    - [x] **Added new Helper functions:**
        * ffhelper: Backend FFmpeg Wrapper that handles all subprocess transactions and gather data.
        * utils: Handles all additional Utilizes required for functioning of DeFFcode.
    - [x] **First PyPi Release:**
        * Released DeFFcode to Python Package Index (PyPI)
        * Added `setup.py` and related metadata.
        * Added `version.py`
    - [x] **Docs:** 
        * Added abstract and related information in README.md
        * Added installation instructions.
        * Added preliminary usage examples.
    - [x] **Maintenance:**
        * Added LICENSE.
        * Added `.gitignore`

??? success "Updates/Improvements"  
    - [x] Maintenance:
        * Bumped version to `0.1.0`
        * Updated LICENSE notice to add vidgear code usage notice.

??? danger "Breaking Updates/Changes"
    - [x] :skull_crossbones: **Fixed support for Python-3.7 and above legacies only.**

??? bug "Bug-fixes"
    - [x] Docs:
        * Fixed hyperlinks in README.
        * Fixed indentation and spacing.
        * Fixed typos and updated context.
        * Removed dead code.

&nbsp; 

&nbsp; 

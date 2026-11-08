#!/bin/sh

# This bash script is based on modified code from vidgear(https://github.com/abhiTronix/vidgear)

# Copyright (c) 2019 Abhishek Thakur(@abhiTronix) <abhi.una12@gmail.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -e # abort on first failing command

# Determine system temp dir (python first: tests use tempfile.gettempdir(), which differs from /tmp on Windows)
TMPFOLDER=$(python3 -c 'import tempfile; print(tempfile.gettempdir())' 2>/dev/null || python -c 'import tempfile; print(tempfile.gettempdir())' 2>/dev/null || true)
[ -z "$TMPFOLDER" ] && TMPFOLDER="${TMPDIR:-/tmp}"
TMPFOLDER="${TMPFOLDER%/}"

# Creating necessary directories
mkdir -p "$TMPFOLDER/temp_images" \
  "$TMPFOLDER/temp_write" \
  "$TMPFOLDER/temp_ffmpeg" \
  "$TMPFOLDER/Downloads/FFmpeg_static" \
  "$TMPFOLDER/Downloads/Test_videos"

# Defining alternate ffmpeg static binaries date/version
ALTBINARIES_DATE="${1:-"12-07-2022"}"

# If the date/version is empty, exit
if [ -z "$ALTBINARIES_DATE" ]; then
  echo "Error: ALTBINARIES_DATE is empty." >&2
  exit 1
fi

# Acknowledging machine OS type
case $(uname -s | tr '[:upper:]' '[:lower:]') in
linux*)
  OS_NAME=linux
  ;;
darwin*)
  OS_NAME=osx
  ;;
msys* | cygwin* | mingw*)
  OS_NAME=windows
  ;;
*)
  echo "Error: unsupported OS: $(uname -s)" >&2
  exit 1
  ;;
esac

# fail on HTTP errors, follow redirects, retry flaky networks
download() { curl -fL --retry 3 "$@"; }

# Download and Configure FFmpeg Static
cd "$TMPFOLDER/Downloads/FFmpeg_static"

# Clean residual artifacts from previous runs
rm -rf ffmpeg ffmpeg-git* ffmpeg-latest*

BASE_URL="https://github.com/abhiTronix/ffmpeg-static-builds/raw/master/$ALTBINARIES_DATE"

if [ "$OS_NAME" = "linux" ]; then

  echo "Downloading Linux Static FFmpeg Binaries..."
  download -O "$BASE_URL/linux/ffmpeg-git-amd64-static.tar.xz"
  # extracted dir name is read from the archive instead of globbing
  EXTRACTED_DIR=$(tar -tf ffmpeg-git-amd64-static.tar.xz | head -n 1 | cut -d/ -f1)
  tar -xJf ffmpeg-git-amd64-static.tar.xz
  rm ffmpeg-git-amd64-static.tar.xz
  mv "$EXTRACTED_DIR" ffmpeg

elif [ "$OS_NAME" = "windows" ]; then

  echo "Downloading Windows Static FFmpeg Binaries..."
  download -O "$BASE_URL/windows/ffmpeg-latest-win64-static.zip"
  unzip -qq ffmpeg-latest-win64-static.zip
  rm ffmpeg-latest-win64-static.zip
  mv ffmpeg-latest-win64-static ffmpeg

else

  echo "Downloading MacOS64 Static FFmpeg Binary..."
  download -O "$BASE_URL/macOS/ffmpeg-latest-macos64-static.zip"
  unzip -qq ffmpeg-latest-macos64-static.zip
  rm ffmpeg-latest-macos64-static.zip
  mv ffmpeg-latest-macos64-static ffmpeg

fi

# Downloading Test Data
cd "$TMPFOLDER/Downloads/Test_videos"

echo "Downloading Test-Data..."
download https://gitlab.com/abhiTronix/Imbakup/-/raw/master/Images/big_buck_bunny_720p_1mb.mp4 -o BigBuckBunny_4sec.mp4
download https://gitlab.com/abhiTronix/Imbakup/-/raw/master/Images/big_buck_bunny_720p_1mb_vo.mp4 -o BigBuckBunny_4sec_VO.mp4
download https://gitlab.com/abhiTronix/Imbakup/-/raw/master/Images/big_buck_bunny_720p_1mb_ao.aac -o BigBuckBunny_4sec_AO.aac
download https://github.com/abhiTronix/Imbakup/releases/download/vid-001/BigBuckBunny.mp4 -o BigBuckBunny.mp4
download https://github.com/abhiTronix/Imbakup/releases/download/vid-001/jellyfish-50-mbps-hd-h264.mkv -o 50_mbps_hd_h264.mkv
download https://github.com/abhiTronix/Imbakup/releases/download/vid-001/jellyfish-90-mbps-hd-hevc-10bit.mkv -o 90_mbps_hd_hevc_10bit.mkv
download https://github.com/abhiTronix/Imbakup/releases/download/vid-001/jellyfish-120-mbps-4k-uhd-h264.mkv -o 120_mbps_4k_uhd_h264.mkv
echo "Done Downloading Test-Data!"

if [ "$OS_NAME" = "linux" ]; then
  echo "Create undeleteable file for testing"
  # clear immutable flag from previous run, else touch fails
  sudo chattr -i undelete.txt 2>/dev/null || true
  touch undelete.txt
  sudo chattr +i undelete.txt
  echo "Preparing images from video"
  ffmpeg -y -i "$TMPFOLDER/Downloads/Test_videos/BigBuckBunny_4sec_VO.mp4" "$TMPFOLDER/temp_images/out%d.png"
  echo "Setting up ffmpeg v4l2loopback"
  sudo modprobe v4l2loopback devices=1 video_nr=0 exclusive_caps=1 card_label='VCamera'
  nohup sudo ffmpeg -hide_banner -loglevel error -re -stream_loop -1 -i "$TMPFOLDER/Downloads/Test_videos/BigBuckBunny_4sec_VO.mp4" -f v4l2 -pix_fmt yuv420p /dev/video0 >/dev/null 2>&1 &
  echo "$(id -un) ALL=NOPASSWD:$(command -v v4l2-ctl)" | (sudo su -c 'EDITOR="tee" visudo -f /etc/sudoers.d/v4l2ctl')
  v4l2-ctl --list-devices
  echo "Done"
fi

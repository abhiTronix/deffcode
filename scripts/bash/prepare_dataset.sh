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

#determining system specific temp directory
TMPFOLDER=$(python -c 'import tempfile; print(tempfile.gettempdir())')

# Creating necessary directories
mkdir -p "$TMPFOLDER"/temp_images # For Generated Images temp path
mkdir -p "$TMPFOLDER"/temp_write  # For testing WriteGear Assets.
mkdir -p "$TMPFOLDER"/temp_ffmpeg # For downloading FFmpeg Static Binary Assets.
mkdir -p "$TMPFOLDER"/Downloads
mkdir -p "$TMPFOLDER"/Downloads/FFmpeg_static
mkdir -p "$TMPFOLDER"/Downloads/Test_videos

# Acknowledging machine architecture
MACHINE_BIT=$(uname -m)

#Defining alternate ffmpeg static binaries date/version
ALTBINARIES_DATE="12-07-2022"

# Acknowledging machine OS type
case $(uname | tr '[:upper:]' '[:lower:]') in
linux*)
  OS_NAME=linux
  ;;
darwin*)
  OS_NAME=osx
  ;;
msys*)
  OS_NAME=windows
  ;;
*)
  OS_NAME=notset
  ;;
esac

#Download and Configure FFmpeg Static
cd "$TMPFOLDER"/Downloads/FFmpeg_static

if [ $OS_NAME = "linux" ]; then

  echo "Downloading Linux Static FFmpeg Binaries..."
  curl -LO https://github.com/abhiTronix/ffmpeg-static-builds/raw/master/$ALTBINARIES_DATE/linux/ffmpeg-git-amd64-static.tar.xz
  tar -xJf ffmpeg-git-amd64-static.tar.xz
  rm *.tar.*
  mv ffmpeg* ffmpeg

elif [ $OS_NAME = "windows" ]; then

  echo "Downloading Windows Static FFmpeg Binaries..."
  curl -LO https://github.com/abhiTronix/ffmpeg-static-builds/raw/master/$ALTBINARIES_DATE/windows/ffmpeg-latest-win64-static.zip
  unzip -qq ffmpeg-latest-win64-static.zip
  rm ffmpeg-latest-win64-static.zip
  mv ffmpeg-latest-win64-static ffmpeg

else

  echo "Downloading MacOS64 Static FFmpeg Binary..."
  curl -LO https://github.com/abhiTronix/ffmpeg-static-builds/raw/master/$ALTBINARIES_DATE/macOS/ffmpeg-latest-macos64-static.zip
  unzip -qq ffmpeg-latest-macos64-static.zip
  rm ffmpeg-latest-macos64-static.zip
  mv ffmpeg-latest-macos64-static ffmpeg

fi

# Downloading Test Data
cd "$TMPFOLDER"/Downloads/Test_videos || exit

echo "Downloading Test-Data..."
curl https://raw.githubusercontent.com/abhiTronix/Imbakup/master/Images/big_buck_bunny_720p_1mb.mp4 -o BigBuckBunny_4sec.mp4
curl https://raw.githubusercontent.com/abhiTronix/Imbakup/master/Images/big_buck_bunny_720p_1mb_vo.mp4 -o BigBuckBunny_4sec_VO.mp4
curl https://raw.githubusercontent.com/abhiTronix/Imbakup/master/Images/big_buck_bunny_720p_1mb_ao.aac -o BigBuckBunny_4sec_AO.aac
curl -L https://github.com/abhiTronix/Imbakup/releases/download/vid-001/BigBuckBunny.mp4 -o BigBuckBunny.mp4
curl -L https://github.com/abhiTronix/Imbakup/releases/download/vid-001/jellyfish-50-mbps-hd-h264.mkv -o 50_mbps_hd_h264.mkv
curl -L https://github.com/abhiTronix/Imbakup/releases/download/vid-001/jellyfish-90-mbps-hd-hevc-10bit.mkv -o 90_mbps_hd_hevc_10bit.mkv
curl -L https://github.com/abhiTronix/Imbakup/releases/download/vid-001/jellyfish-120-mbps-4k-uhd-h264.mkv -o 120_mbps_4k_uhd_h264.mkv
echo "Done Downloading Test-Data!"

if [ $OS_NAME = "linux" ]; then
  echo "Create undeleteable file for testing"
  touch undelete.txt
  sudo chattr +i - v "$TMPFOLDER"/Downloads/Test_videos/undelete.txt
  echo "Preparing images from video"
  ffmpeg -i "$TMPFOLDER"/Downloads/Test_videos/BigBuckBunny_4sec_VO.mp4 "$TMPFOLDER"/temp_images/out%d.png
  echo "Setting up ffmpeg v4l2loopback"
  sudo modprobe v4l2loopback devices=1 video_nr=0 exclusive_caps=1 card_label='VCamera'
  nohup sudo ffmpeg -hide_banner -loglevel error -re -stream_loop -1 -i "$TMPFOLDER"/Downloads/Test_videos/BigBuckBunny_4sec_VO.mp4 -f v4l2 -pix_fmt yuv420p /dev/video0 &
  echo "$USER ALL=NOPASSWD:$(which v4l2-ctl)" | (sudo su -c 'EDITOR="tee" visudo -f /etc/sudoers.d/v4l2ctl')
  v4l2-ctl --list-devices
  echo "Done"
fi

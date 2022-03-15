# AMD INNOVATION SHOWCASE 2022

## Motivation
- Some video streams do not have downloads of their learning material, i.e. pptx, word files.
- Generate a "powerpoint" for videos that don't have powerpoints, but can be split into less frames

## Goal
- Make it easier to learn in an online environment.

## Functionality
- App should automatically screen capture relevant learning material from a video stream, and then insert it into OneNote, or PDF for current, or later consumption.

## Compatibility
- Any streaming platform
  - Microsoft Teams
  - Any video stream in Chrome Browser? (stretch goal)
  - [UofT My Media](https://play.library.utoronto.ca/login)

- Any capturable part of your screen

- Multi-monitor support
  - Enabled through use of [python-mss](https://python-mss.readthedocs.io/examples.html)

- Export formats:
  - Single-frame PNGs
  - PDF
  - PPTX 
  - TXT (OCR) (stretch goal)
  - Directly to onenote for live annotation? [OneNote API](https://developer.microsoft.com/en-us/graph/get-started), [Graph API](https://developer.microsoft.com/en-us/graph/quick-start)
    - Graph API does not work for my school/work account.


## Endnotes


## Ideas

- run a simultaneous stream and pull frames from it, 
before they happen in your browser stream, 
so that they can be exported into your notetaking app BEFORE the stream gets there, 
and so you can annotate them before the stream gets there
This will only work for certain streams, like browser ones
How would this work with teams? it wouldn't. You'd just have to capture live....unless you somehow
could hook into the stream in advance while watching it live?


## TODO

- [x] Grab individual video frames
  - [ ] Grab entire screen first
  - [ ] Use win32 to grab non-primary monitor if screen of interest is not the primary. (PIL can only grab from primary.)
  - [ ] Could grab window of interest first (can be on non-primary monitor), just need to specify title name
    - [ ] Then decide which monitor it is on.
- [x] Compare video frames
    - [ ] Other options
    - [ ] Compare current with previous frame
    - [ ] Compare current frame with a sequence of previous frames
- [ ] Save the minimal # of video frames that best represent the learnable content from the video - unique frames only

- [ ] Crop video to only the part of the screen that changed the most (assume rectangular)
    - [ ] Could even copy only the parts of the screen that have changed (save space)

- [ ] Add other platform compatibility
    - [ ] YouTube (Live and downloadable)
        - [ ] Download accelerator that preprocesses video for unique frames.
    - [ ] Teams (Live)

- [ ] Convert images to PDF slidedeck


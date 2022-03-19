# Slider - AMD Innovation Showcase 2022 Submission

![ISC Innovation Showcase 2022 Banner]('./innovation-showcase-banner.png')  
## Motivation
- Some video streams do not have downloads of their learning material, i.e. pptx, word files.
- Generate a "powerpoint" for videos that don't have powerpoints, but can be split into less frames

## Goal
- Make it easier to learn in an online environment.

## Functionality
- App should automatically screen capture relevant learning material from a video stream, and then insert it into OneNote, or PDF for current, or later consumption.

## Compatibility
- Tested on Windows  
- Any streaming platform
  - Microsoft Teams
  - Any video stream in Chrome Browser? (stretch goal)
  - [UofT My Media](https://play.library.utoronto.ca/login)

- Any capturable part of your screen

- Multi-monitor support
  - Enabled through use of [python-mss](https://python-mss.readthedocs.io/examples.html)

- Export formats:
  - Single-frame PNGs
  - PDF (future)
  - PPTX  (future)
  - TXT (OCR) (stretch goal)
  - Directly to onenote for live annotation? [OneNote API](https://developer.microsoft.com/en-us/graph/get-started), [Graph API](https://developer.microsoft.com/en-us/graph/quick-start)
    - Graph API does not work for my school/work account.


## How to use Slider!
1. Install [Python](https://www.python.org/downloads/) for your OS. Note: slider has only been tested on Windows 10.  
2. `git clone` this repository.
3. `pip install -r requirements.txt`
4. Note: If you are going to use this program with a notetaking app like OneNote, you should open this app before launching the script.
You should also open your video stream prior to launching the script.
5. `python main.py` to run the program. 

## TODO

- [x] Grab individual video frames
  - [x] Could grab window of interest first (can be on non-primary monitor), just need to specify title name
    - [x] Then decide which monitor it is on.
    - [x] Try to use python-MSS to list monitors. 
  - [x] Grab entire screen first
    - [ ] Decide which region(s) of interest to capture (ones that has the most info change as video progresses.)

- Ways of capturing notes of interest:
  - [ ] User selects region with mouse. (future)
    - [ ] Drag to select
    - [ ] Click to select
    - [ ] Could use package like tkinter to provide UI tool to select
  
  - [x] User enters name of window of interest. (current scope)
    - [x] List names of windows (in terminal or UI).
    - [x] i.e. Chrome, Microsoft Teams, Films & TV
    - [x] Hook into window with package like pywinauto
    - [x] The window location from pywinauto should allow use to know which monitor it is on (for python-mss)

- [x] Combine above functionality into OOP model before getting into image comparison
  
- [x] Prompt user to either:
  - [x]  paste/copy images into OneNote/(notetaking application (by selecting app name) (future scope))
  - [x]  save to PNG
  - [ ]  save to PDF

- [x] Compare video frames
    - [x] Compare current with previous frame
    - [ ] Compare current frame with a sequence of previous frames
- [x] Save the minimal # of video frames that best represent the learnable content from the video - unique frames only

- [ ] Crop video to only the part of the screen that changed the most (assume rectangular)
    - [ ] Could even copy only the parts of the screen that have changed (save space)

- [ ] Add other platform compatibility
    - [x] YouTube (Live and (downloadable (future scope)))
        - [ ] Download accelerator that preprocesses video for unique frames.
    - [x] Teams (Live)
    - [ ] Browser: Enable screenshotting even when tab is not active

- [ ] Convert images to PDF slidedeck (future)

## Future Ideas

- run a simultaneous stream and pull frames from it, 
before they happen in your browser stream, 
so that they can be exported into your notetaking app BEFORE the stream gets there, 
and so you can annotate them before the stream gets there
This will only work for certain streams, like browser ones
How would this work with teams? it wouldn't. You'd just have to capture live....unless you somehow
could hook into the stream in advance while watching it live?


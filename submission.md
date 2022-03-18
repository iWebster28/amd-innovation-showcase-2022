# Slider

Give us a brief rundown on what motivated the project, what problem is it solving, and why you feel like a solution to that problem was important. (400 words max).  
## Inspiration 
My inspiration for this project comes from the online classes I took during the pandemic and for work.
## Motivation
Taking notes in class or while self-learning can be an arduous task. There are countless approaches to learning. Should you listen? Should you write down the gist of the idea? Should you solely take pictures? Should you record audio or video?
We all have different learning styles. As such, some types of note-taking are more effective than others.  

However, while everyone learns differently, many professors emphasize the importance of coming to lectures. 
Sometimes the professor explains course content better than the textbook. Sometimes, they hint at specific practice problems to focus on. 
Professors will even tell you what exact questions will be on the exam. All you need to do is attend lectures.  

## Problem being solved
In online class over the pandemic, I found that most professors uploaded videos of them speaking over slides.
The problem is that some professors do not always provide matching slide decks for their recorded videos.  

In a similar fashion, when watching slide-deck style presentations on the internet (e.g. YouTube) or at work, there are not always slide downloads.  

To generalize, the problem is that video-based learning is not effective on its own, and not all learning sources provide slide downloads.

## Why a solution is important?
Taking notes by hand encourages better retention than taking pictures or solely listening [^fn1] [^fn2]  
Video-based learning should be supplemented with note-taking. Notes are easier to take when you have video-based slides for reference.

*slider* summarizes videos into slides for annotation and review, leading to a richer learning experience. It allows you to reduce videos to PDF slide decks that can easily be imported into applications like OneNote.  

[^fn1]: Learning Faster, https://www.entrepreneur.com/article/323450
[^fn2]: Effective Note Taking in Class, https://learningcenter.unc.edu/tips-and-tools/effective-note-taking-in-class/


## Challenges
I encountered a few significant challenges in this project.

Determining how to:
1. Capture desktop windows on any monitor
2. Copy captured image data to the clipboard
3. Detect when video frames "change" enough such that a new snapshot should be taken
4. Comparing images in memory before saving to disk
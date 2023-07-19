# Introducing the Terminal

The main goal here is just to introduce enough UNIX / bash commands so that students can effectively navigate their file directories at the command line, so they can collaborate using Git/the command line for projects without relying on the GitHub GUI (and navigate out of potential merge commit messages or other times they get kicked into vim). Additionally, in this session students are encouraged to create a 'Flatiron' folder to contain all program contents, and thus begin thinking about how best to organize the materials they're cloning down and working on locally (or projects).

## Materials:

- [[Google Slides] The Terminal: Fear Not the Command Line](https://docs.google.com/presentation/d/17k-zjy3D2ES0wV8VQE_88Eeqa96ZKCbIW7XDf96KcDc/edit?usp=sharing)

## Before Lecture Prep

### Prerequisites

The below two points are not deal breakers for students, but are recommended before this session:

- Students using Windows machines should have Git Bash installed
- All students should have a code-focused text editor installed (we recommend VS Code)
    - Students using Mac machines and VS Code will want to set it up so they can open ([instructions for that here](https://code.visualstudio.com/docs/setup/mac))

## Learning Goals

- Utilize bash commands through a terminal interface
- Use the terminal to list, make, move and remove files and directories
- Use the terminal to navigate between files/directories and open Jupyter notebooks or other files
- Edit text files using vim

## Lesson Plan

Expected total time: 45 minutes

### Introduction (5 Mins)

Discuss how bash allows you to perform all kinds of operations quickly - easy to make a joke here about feeling like a hacker. Set the expectation set that this will feel uncomfortable at first, especially for people who have always used graphical interfaces, but they will get practice and get more comfortable with it over time. Be sure to emphasize that students can do things both in the terminal and using a GUI, but should feel comfortable enough with the terminal that they can use it in the instances that there is no GUI - and the hope is that they realize that some things really are faster/easier in the terminal (but they're not failures if that doesn't happen immediately)

### Slides (35 Mins)

Go through the intro slides, on learning goals and discussing the different terms and Flatiron-specific expectations. 

After that, the slides are structured for a **live demo** as you move through the slides. The intention is that the instructor pulls up a terminal window and puts it over the screenshots of the blank terminal - then demos the contents/focus of each slide for students. Each slide has notes with recommended actions or instructions for that demo. 

Highly encourage students to follow along in their own terminal windows - you might consider using the 'Raise Hand' feature on zoom to check when everyone has their terminal open and is ready to follow along.

There are 3 main parts to the slide demo:

1. Introducing basic commands
    - Practice navigation, then creating and deleting new files/directories
2. Distinguishing between absolute and local paths
    - Start the process of students recognizing where another file is _relative to_ where they currently are in their terminal - how can you navigate relatively rather than going back to your root/home directory?
3. Editing text files
    - Demonstrate how to survive vim, but also how to open more user-friendly text editors from the terminal

### Conclusion (5 Mins)

Open Q&A. Tell students: "It's OK if you're not feeling 100% confident with this stuff right now, you will get plenty of practice with it moving forward."

## Extras

### Tips

- Share the slides in advance - while there are some 'answers' in there which students could find in the slide notes, it will also be easier for students who do not have two screens to follow along with the demo if they have the slides as well as the zoom screenshare

### Additional Resources

- The last slide is full of additional resources for students, and the slide notes explain some of why those resources were included

### Potential Additional Activities

- If students have been exposed to cloning down GitHub repositories already, you may want to demo cloning a repo down to the 'wrong' place on their computer, then moving that from the command line to a place that's more organized/more accessible.

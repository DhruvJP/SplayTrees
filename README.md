# Instructions:
1. clone the repository onto your device using `git clone <Repository URL>.
2. cd into the folder containing main.py and requirements.txt.
3. Run pip3 install manim once you are in the appropriate folder.
4. If you get any errors then its primarily due to not establishing your dependencies. To resolve them you need the following: cairo, cmake, ffmpeg, pkgconf.
5. Run <brew install cairo>
6. Run <brew install cmake>
7. Run <brew install ffmpeg>
8. Run <brew install pkgconf>
9. To check if manim was downloaded properly: Run <manim --version>

# Manim Slides Install:
1. Run <pip3 install manim-slides>

# To Run project:
1. Run <manim-slides render main.py SplayTreePresentation>
1. Run <manim-slides convert SplayTreePresentation main.html --open>

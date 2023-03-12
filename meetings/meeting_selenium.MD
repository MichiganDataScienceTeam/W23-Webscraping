# Selenium Day!
Just as a quick recap, so far we have been doing static webscraping. 
We visit websites and look at their html files to scrape out data we want to use. 
For example, when we use beautiful soup, we use the "html.parser" that takes advantage of the tree structure of html files in order to let us programmitically scrape data we want.
Selenium lets us interact with the websites (click buttons, take screenshots, submit forms...)

## Setup
There is a new library to install that has been added to the ```requirements.txt``` file. Make sure this is up to date by running:

```bash
pip install -r requirements.txt
```

You also will need to make use of webdrivers (for this example, I will be using chromedriver) for selenium to run on. Using Homebrew, simply run 
```bash
brew install chromedriver
```
If Homebrew is not working for you, you can manually download what you need [here](https://chromedriver.chromium.org/downloads). Just make sure to move the binary file over to ```/usr/local/bin/chromedriver```


You can check this is installed correctly by doing 
```
which chromedriver
```
which should return ```/usr/local/bin/chromedriver```, indicating a binary file for chromedriver has been added. Likely, if you are on a Mac, you will need to run 
```bash
xattr -d com.apple.quarantine /usr/local/bin/chromedriver
``` 
to give permission for your computer to run this file.


## Intro
Oh nooo I forgot when the Final Expo for MDST is! I am way too lazy to look at [mdst.club/agenda](https://www.mdst.club/agenda), and would be too embarrassed about asking in the Slack! I need a way to get the information from the site easily (and with a contrived sense of minimal effort).

I made a practice file that explains most of what you need to know about Selenium to get started. I recommend you do these things

1. Run (and watch the browser that opens up) when you run
    ```bash
    python selenium_practice.py
    ```
    There are intentional time.sleeps() so just wait until the window closes by itself. Alternatively, you can step through the corresponding jupyter notebook 
    ```selenium_practice.ipynb```

2. Read the output printed to the terminal (and note the screenshots that should have appeared in your directory!)
3. Look through the comments in ```selenium_practice.py``` since you're going to be doing this sort of stuff next. 

## Task
Do something cool on LinkedIn (shameless plug to connect with me :). Then do something cool on other places. I put starter code in ```selenium_starter.ipynb```
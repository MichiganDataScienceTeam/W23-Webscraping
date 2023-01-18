# webscraping
_Winter 2023 MDST Webscraping Project_


## Table of Contents

-   [Introduction](#introduction)
-   [Description](#description)
-   [Goals](#goals)
-   [A Look at the Data](#a-look-at-the-data)
-   [Project Roadmap](#project-roadmap)
-   [Setup](#setup)
-   [Other](#other-relevant-stuff)

## Introduction

Have you ever felt like stalking someone's 📱insta485~~gram~~📱, but were too embarrassed to do it while logged into your account? Maybe you wanted to pull quotes from someone's favorite 🎥movie🎥 so you could ~~annoy~~ serenade him with a random quote every day! Now imagine these kinds of tasks, but on a _much_ larger scale. Some more MDST examples...

- Scraping SEC filings over a quarter to analyze trends of inside traders in the [SEC Insider Trading Project](https://github.com/MichiganDataScienceTeam/insider-trading)
- Scraping metadata about ~9000 movies from IMDB for a dataset to create a [Movie Recommender System](https://github.com/MichiganDataScienceTeam/movie-recommendations)
- Countless lightning talks

## Description
Since there is no _one way_ to scrape websites, we won't have just one project that we work on the entire semester. Instead, we have a few mini projects (one is completely self-guided) to give us experience scraping many different kinds of websites. This should give us some appreciation for the work google does making their [crawlers](https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers) work. 

The culminating project is a unified app that scrapes information about all UofM professors from their websites (and cross references this with relevant reviews from Atlas). One use case of this is to show open research positions professors have, while checking their teacher experience. 


## Goals

1. Design a functional recommender system from scratch and gain insight to their
   mechanics
2. Provide MDST members the opportunity to work with recommender systems that are very
   prevalent in industry
3. Have a user interface (form of a website)
4. Have fun and learn something! 😃


## A Look at the Data

We scrape our data!

## Project Roadmap

Week of **1/29**: Intro to Webscraping

-   Kickoff!
-   Introductions
-   Familiarize ourselves with BeautifulSoup

---

Week of **2/5**: Scrape well-tabulated websites 

-   MLB website
-   Tennis rankings
-   Pretty much any competitive sport 
-   instagram

---

Weeks of **2/12-3/12**: Begin individual projects

-   Sub-teams!
-   Find something to scrape
-   (At some point) Intro to Selenium (interactive webscraping)

---

## **2/25-3/5**: _Spring Break!_

---

Week of **3/19**: Wrap up individual projects

-   Make visualizations of our data
-   

---

Week of **3/26-4/16**: Develop Michigan Web Crawler

-   Plan out application design
-   Flesh out basic API to interact with webpage
-   Test it!

---

Week of **4/16**: Finishing Touches

-   Complete the write-up
-   Prepare for final presentations!

## Setup

First, clone this repo (via ssh)

```bash
git clone git@github.com:MichiganDataScienceTeam/webscraping.git
```

### Virtual Environment

You can choose whether or not to use a virtual environment for this project (though it is recommended). The setup guide shows how to create a venv through pip, but it can also be done via Conda if you want. The important thing is that you can run the commands found in the [Good to go](#good-to-go) section.

We are going to initialize a Python virtual environment with all the required packages. We use a virtual environment here to isolate our development environment from the rest of your computer. This is helpful in not leaving messes and keeping project setups contained.

First create a Python 3.8 virtual environment. The virtual environment creation code for Linux/MacOS is below:

```bash
python3 -m venv venv
```


Now that you have a virtual environment installed, you need to activate it. This may depend on your system, but on Linux/MacOS, this can be done using

```bash
source ./venv/bin/activate
```

Now your computer will know to use the Python installation in the virtual environment rather than your default installation.

After the virtual environment has been activated, we can install the required dependencies into this environment using

```bash
pip install -r requirements.txt
```

### Good to go

If it is set up correctly, you should be able to open a dev server and see the app for some intro webscraping by moving to the "flaskr" directory and then running the app:

```bash
cd flaskr
flask run
```

Open up the server to see if it works! (ctrl + click on http://127.0.0.1:5000)


## Other relevant stuff

[MDST Calendar](https://www.mdst.club/agenda)

### Required Skills

Intermediate Python, Pandas (enough that it won't impede progress)

### Learned Skills

HTML, CSS, BeautifulSoup, Selenium, RegEx

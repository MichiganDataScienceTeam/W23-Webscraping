# First Meeting!

- Icebreakers (ik sorry :))
- Some introduction to html and basic webscraping
- Complete tasks scraping flask stuff

## Tasks using the flask app
Make sure cd to the proper directory and open the dev server for flask
```bash
cd flaskr
flask run
```

I recommend making a notebook or python script in the webscraping folder (as opposed to inside flaskr or utils) to complete these tasks.

server:
http://127.0.0.1:5000/

### Task 1: ```/caesar```
This was a project inspired from my crypto class! I encrypted some words using a *[vigenere cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher) (which I forgot how to spell when I initially coded this, so I just spelled it caesar). 

The decryption key is encoded in one of the attributes for the first three lines of text that look like gibberish. Feel free to make use of stuff I put in the utils folder. 

### Task 2: ```/shuffled_art/\<choice\>```
choose one of:
- elephant
- dogs
- tweetie
- beaver

I recommend looking at the corresponding ascii art endpoint before attempting:
```/art/\<choice\>```

I took the ascii art and performed multiple operations on it.

1. replaced all ' ' with 'H'
2. added attribute tags specifying the row number the text lies on ex. "row_1"
3. shuffled the rows so it is no longer in order

The goal of this task is to unscramble the image and print out the completed image (in editor is fine) of what the ascii art should actually look like. If you did it correctly, your image will look like the corresponding ```/art/\<choice\>``` endpoint.

### Notes
When webscraping it is important to understand the representation and meaning of the data. Be looking out for edge cases I throw in that requires noticing and understanding patterns in the data. 

Next week, we will look into scraping tabulated forms of data (sports statistics)!
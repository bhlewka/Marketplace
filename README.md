# Marketplace

### Requirements
- Latest release of Python3
- Selenium for Python
- Pyautogui
- Geckodriver (by Mozilla, found [here](https://github.com/mozilla/geckodriver/releases))
- Mozilla Firefox
### Instructions
1. Make sure the geckodriver.exe, login.txt, and ads directory are in the same directory as marketplace.exe.

    ```
    Documents\MarketplaceProgram\marketplace.py
    Documents\MarketplaceProgram\geckodriver.exe
    Documents\MarketplaceProgram\ads\couch\...
    Documents\MarketplaceProgram\ads\chair\...
    ```
2. login.txt should have two lines, email and password
    ```
    username@email.com
    password123
    ```

2. Make sure each ad contains an Ad.txt and at least one image

    ```
    Documents\MarketplaceProgram\ads\chair\Ad.txt
    Documents\MarketplaceProgram\ads\chair\chairPicture.jpg
    ```
3. Make sure Ad.txt is properly formatted
    - The first line should be the item name
    - The second line should be the item price
    - Everything else should be the item description
    ```
    Climbing Shoes
    $100
    Never worn, in the packaging
    Size 42, excellent for slab problems
    If interested call or text 123-456-7890
    ```
    
4. Run marketplace.py from a power shell terminal
    - Let your computer sit by itself for around 30 seconds per ad
    - Because the program uses your mouse and keyboard, you cannot use your computer while it runs
    - You will know it is finished when it stops for longer than 10 seconds (When the last ad from the ads folder is posted)
    - Or when the terminal closes
    - You'll figure it out, its not like it does anything cool like shoot fireworks
    
### Possible TODO's / Personal Notes

- ~~Speed up the program from waiting 2 seconds after every action to
on page load~~
    - Using exclusive waits or something? Waiting for the last element to load
    then performing our operations
    - Could also just eliminate unnecessary waits, like waiting after the page is already loaded
    - This also isn't that big of a deal if you just leave this to run overnight,
    but if you really want to pump out as many ads as possible then optimizing for time becomes more important
- Improve the ad input, using CSV or spreadsheet files instead of notepad
    - Alternatively could just make what goes where in the textfile
    more clear
    - Potentially just a single spreadsheet, and a folder full of pictures
    - That way you could just name the pictures in the spreadsheet instead of 0,1,2, etc
- ~~Do some exception handling, so the program won't just die when something
goes wrong~~
    - ~~This isn't that big of a deal, not much should go wrong~~
    - Basically all I might need is if an ad is formatted incorrectly or doens't have a photo to refresh and
    move to the next one
- ~~Hardcoded coordinates for screensize, specifically
for remember password~~
- ~~Issues with some of the ads~~
    - Changing how some of the code worked fixed these issues as far as I can tell
- ~~It seems like a lot of these selected elements could be found just by doing link search
instead of element ID, not that element ID is wrong or doesn't work~~
    - Actually it seems like absolute path is almost necessary for some
- So I think if I made this in a C language it would be an executable with no other requirements? Im not sure though
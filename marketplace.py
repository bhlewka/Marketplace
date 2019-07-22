from selenium import webdriver
import time
import os
import pyautogui
pyautogui.FAILSAFE = True

# These are some global sleep variables, for each of the expected sleep times
# May need to be changed depending how fast or slow a persons computer is
# For now we will pick some conservative times, so things should work out of the box

# For tabbing, arrow keys, and interacting with a single webpage
shortSleep = 0.2

# For all other loading, including file uploads, page refreshes or reloads, etc.
longSleep = 5



# This will get the username and password from a text file
# Supports multiple logins, line separated
# Returns list of username,password
def getCredentials():

    # Open/read the file
    file = open("login.txt")
    file = file.read().splitlines()
    creds = []
    for credentials in file:
        credentials = credentials.split(", ")
        creds.append([credentials[0], credentials[1]])
    return creds

# This will retrieve the relevant info for the ad posting
# Returns title, price, description
def getAdInformation(directory):

    title, price, description = open("ad/"+directory+"/Ad.txt").read().split("\n", 2)
    return title, price, description

# This will return the absolute path to all images
# Returns a list of absolute paths to images
def getAdImagePaths(directory):
    ads = os.getcwd() + "/ads/" + directory
    files = os.listdir(ads)

    # We will go through this list and remove the hidden files as well as Ad.txt
    # This will assume all remaining files are images so make sure they are!
    # Otherwise bad things might happen
    images = []
    for file in files:
        if file[0] != "." and file != "Ad.txt":
            images.append(ads + "/" + file)
    return images

# This retrieves the directory name of each ad
# Returns list of ad folder names
def getAds():
    ads = os.getcwd() + "/ads/"
    ads = os.listdir(ads)
    return ads

# Logs us into facebook
# Returns the browser object
def login(creds):

    # Init the browser, in this case firefox
    # Take us to facebook.com and maximize the window
    browser = webdriver.Firefox()  # (executable_path='geckodriver')
    browser.maximize_window()
    browser.get('http://facebook.com')

    # Login by finding the correct fields by ID
    browser.find_element_by_id('email').send_keys(creds[0])
    browser.find_element_by_id("pass").send_keys(creds[1])
    browser.find_element_by_id('loginbutton').click()

    # Wait for page load
    time.sleep(longSleep)

    # Use this to close the silly remember login details button that appears every time
    pyautogui.press('escape')
    time.sleep(shortSleep)
    return browser

# Post the ad
def postAd(browser, directory):
    title, price, description = getAdInformation(directory)

    # Allow page to load
    time.sleep(longSleep)

    # Click the "Sell Something" button by using the absolute path to the element
    # Allow page to load
    browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div/div[1]/div/div/div/button').click()
    time.sleep(longSleep)

    # Click the "Item for Sale" button using the link text
    # Allow page to load
    browser.find_element_by_link_text("Item for Sale").click()
    time.sleep(longSleep)

    # Click the category field by using the absolute path
    browser.find_element_by_xpath("/html/body/div[6]/div"
                                  "[2]/div/div/div/div/div[2]/div/div/div[1]/div[1]/div/span/span/label/input").click()
    time.sleep(shortSleep)

    # Type the item category, then navigate to the title
    # In the future, this could also be an element in the ad text
    pyautogui.typewrite('Furniture')
    time.sleep(shortSleep)
    pyautogui.press("down")
    time.sleep(shortSleep)
    pyautogui.press('enter')
    time.sleep(shortSleep)
    pyautogui.press('tab')
    time.sleep(shortSleep)
    pyautogui.press('tab')

    # Type the item name, then navigate to the price
    pyautogui.typewrite(title)
    time.sleep(shortSleep)
    pyautogui.press('tab')

    # Type the item price, then navigate to the description
    pyautogui.typewrite(price)
    time.sleep(shortSleep)
    pyautogui.press('tab')
    time.sleep(shortSleep)
    pyautogui.press('tab')

    # Type the item description, then navigate to the add images button
    pyautogui.typewrite(description)
    time.sleep(shortSleep)
    pyautogui.press('tab')
    time.sleep(shortSleep)
    pyautogui.press('tab')
    time.sleep(shortSleep)

    # Select the images button
    # Allow file selection window to load
    # Leave lots of time for slower computers
    pyautogui.press('enter')
    time.sleep(longSleep)

    # Get the image paths from the ad folder
    images = getAdImagePaths(directory)

    # Create the file string and enter it into the image selection window
    # Allow files to be uploaded
    # I think really slow internet could mess this part up, so we will give it some generous load time (5 seconds)
    files = ""
    for imagePath in images:
        files += '"' + imagePath + '" '

    time.sleep(longSleep)
    pyautogui.typewrite(files)
    time.sleep(shortSleep)
    pyautogui.press('enter')
    time.sleep(longSleep)

    # Scroll down so next button is in view to be clicked
    pyautogui.press("pagedown")
    time.sleep(shortSleep)

    # Click next button
    # Allow page to load
    browser.find_element_by_xpath(
        "/html/body/div[6]/div[2]/div/div/div/div/div[2]/div/div/div[3]/div/div[2]/div/div/span/button/span").click()
    time.sleep(longSleep)

    # Press enter on post
    pyautogui.press('enter')

    # Wait for things to finalize before refreshing
    time.sleep(longSleep)

    # Refresh the page
    # I think this helps because the element names/paths get changed each consecutive sell on the same page
    browser.refresh()
    time.sleep(longSleep)



def main():

    credentials = getCredentials()
    # For each username/password provided, post all the ads
    for creds in credentials:
        browser = login(creds)

        # Find and click the marketplace button by ID
        # Allow page to load
        browser.find_element_by_id('navItem_1606854132932955').click()
        time.sleep(5)

        # Click the "Selling" button, to take us to the selling page
        path = '/html/body/div[1]/div[3]/div[1]/div/div/div[1]/div/div/div/div[2]/div/a[3]'
        browser.find_element_by_xpath(path).click()

        # Here is where we could get it to automatically delete all ads we currently have listed
        # Currently must be done by hand

        # Retrieve the name of each ad folder
        ads = getAds()

        # For each ad folder, post the ad
        # Make this a separate function probably soon
        for directory in ads:

            try:
                postAd(browser, directory)
            except:
                # If something goes wrong with the ad, clicking an element, or anything else
                # Just restart and go to the next ad
                browser.refresh()
                time.sleep(longSleep)

        # Here we could either logout and login on the new account
        # But for now we will just close the browser and open a new one and start over
        # Closing a browser shouldn't need a longSleep, but who knows
        browser.close()
        time.sleep(shortSleep)

    print("All ads posted on all accounts, safe to close windows and stuff")

main()
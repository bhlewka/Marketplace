from selenium import webdriver
import time
import os
import pyautogui
pyautogui.FAILSAFE = True

# This will get the username and password from a text file
# Returns username, password
def getCredentials():

    # Open/read the file
    file = open("login.txt")
    file = file.read().splitlines()[0].split(',')
    username = file[0]
    password = file[1]
    return username, password

# This will retrieve the relevant info for the ad posting
# Returns title, price, description
def getAdInformation(directory):

    title, price, description = open("ads\\"+directory+"\\Ad.txt").read().split("\n", 2)
    return title, price, description

# This will return the absolute path to all images
# Returns a list of absolute paths to images
def getAdImagePaths(directory):
    ads = os.getcwd() + "\\ads\\" + directory
    files = os.listdir(ads)

    # We will go through this list and remove the hidden files as well as Ad.txt
    # This will assume all remaining files are images so make sure they are!
    # Otherwise bad things might happen
    images = []
    for file in files:
        if file[0] != "." and file != "Ad.txt":
            images.append(ads + "\\" + file)
    return images

# This retrieves the directory name of each ad
# Returns list of ad folder names
def getAds():
    ads = os.getcwd() + "\\ads\\"
    ads = os.listdir(ads)
    return ads

# Logs us into facebook
# Returns the browser object
def login():
    # Get the username/password from login.txt
    login = getCredentials()

    # Init the browser, in this case firefox
    # Take us to facebook.com and maximize the window
    browser = webdriver.Firefox()  # (executable_path='geckodriver')
    browser.maximize_window()
    browser.get('http://facebook.com')

    # Login by finding the correct fields by ID
    browser.find_element_by_id('email').send_keys(login[0])
    browser.find_element_by_id("pass").send_keys(login[1])
    browser.find_element_by_id('loginbutton').click()

    # Wait for page load
    time.sleep(4)

    # Use this to close the silly remember login details button that appears every time
    pyautogui.press('escape')
    time.sleep(0.1)
    return browser

# Post the ad
def postAd(browser, directory):
    title, price, description = getAdInformation(directory)

    # Allow page to load
    time.sleep(2)

    # Click the "Sell Something" button by using the absolute path to the element
    # Allow page to load
    browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div/div[1]/div/div/div/button').click()
    time.sleep(2)

    # Click the "Item for Sale" button using the link text
    # Allow page to load
    browser.find_element_by_link_text("Item for Sale").click()
    time.sleep(2)

    # Click the category field by using the absolute path
    browser.find_element_by_xpath("/html/body/div[6]/div"
                                  "[2]/div/div/div/div/div[2]/div/div/div[1]/div[1]/div/span/span/label/input").click()
    time.sleep(0.1)

    # Type the item category, then navigate to the title
    # In the future, this could also be an element in the ad text
    pyautogui.typewrite('Furniture')
    time.sleep(0.1)
    pyautogui.press("down")
    time.sleep(0.1)
    pyautogui.press('enter')
    time.sleep(0.1)
    pyautogui.press('tab')
    time.sleep(0.1)
    pyautogui.press('tab')

    # Type the item name, then navigate to the price
    pyautogui.typewrite(title)
    time.sleep(0.1)
    pyautogui.press('tab')

    # Type the item price, then navigate to the description
    pyautogui.typewrite(price)
    time.sleep(0.1)
    pyautogui.press('tab')
    time.sleep(0.1)
    pyautogui.press('tab')

    # Type the item description, then navigate to the add images button
    pyautogui.typewrite(description)
    time.sleep(0.1)
    pyautogui.press('tab')
    time.sleep(0.1)
    pyautogui.press('tab')
    time.sleep(0.1)

    # Select the images button
    # Allow file selection window to load
    pyautogui.press('enter')
    time.sleep(2)

    # Get the image paths from the ad folder
    images = getAdImagePaths(directory)

    # Create the file string and enter it into the image selection window
    # Allow files to be uploaded
    # I think really slow internet could mess this part up, so we will give it some generous load time (5 seconds)
    files = ""
    for imagePath in images:
        files += '"' + imagePath + '" '

    time.sleep(2)
    pyautogui.typewrite(files)
    time.sleep(0.1)
    pyautogui.press('enter')
    time.sleep(5)

    # Scroll down so next button is in view to be clicked
    pyautogui.press("pagedown")
    time.sleep(0.1)

    # Click next button
    # Allow page to load
    browser.find_element_by_xpath(
        "/html/body/div[6]/div[2]/div/div/div/div/div[2]/div/div/div[3]/div/div[2]/div/div/span/button/span").click()
    time.sleep(2)

    # Press enter on post
    pyautogui.press('enter')

    # Wait for things to finalize before refreshing
    time.sleep(5)

    # Refresh the page
    # I think this helps because the element names/paths get changed each consecutive sell on the same page
    browser.refresh()
    time.sleep(5)



def main():

    browser = login()

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
            time.sleep(5)

    print("Ads posted, program completed, safe to do close windows and stuff")

main()
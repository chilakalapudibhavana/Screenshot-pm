from flask import Flask, render_template, request, redirect
import os
import time
import pyautogui
import keyboard
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tkinter import filedialog

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/capture", methods=['POST'])
def capture():
    url = 'https://hyperv-aln:8181/Admin/adeadmin.html?v=1685078514175#/'
    url_password = request.form['url_password']
    user_name = request.form['user_name']
    password = request.form['password']
    
    current_datetime = datetime.datetime.now()
    filename = "Backup "+ current_datetime.strftime("%d%b%Y(%H %M %S)") + ".png"
    
    # Configure Selenium webdriver
    options = Options()
    options.add_argument('--headless')  # Run in headless mode (without opening browser window)
    driver = webdriver.Chrome()
    driver.maximize_window()
    # Open the URL in the webdriver
    driver.get(url)
    pyautogui.typewrite(url_password)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body.ng-scope')))

    pyautogui.typewrite(user_name)
    pyautogui.press('tab')  # Move to the next input field
    pyautogui.typewrite(password)
    pyautogui.press('enter')    # Click the button using pyautogui
     # Wait for the URL to change
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("https://hyperv-aln:8181/Admin/adeadmin.html?v=1685078514175#/home"))
    time.sleep(5)
    screenshot = pyautogui.screenshot()
    destination_folder = filedialog.askdirectory()
    if destination_folder:
        file_path = os.path.join(destination_folder, filename)
        screenshot.save(file_path)
        return "<h1>Captured</h1>"
    else:
        return "<h1>Not Captured</h1>"
    driver.quit()

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    

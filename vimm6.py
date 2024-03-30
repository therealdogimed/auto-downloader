from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Define the path to the Microsoft Edge WebDriver executable
edgedriver_path = r"C:\Users\pspdr\Desktop\python\vimm downloader\msedgedriver.exe"

# Set up the Selenium Edge webdriver with options
options = webdriver.EdgeOptions()
options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"  # Change this to the actual path of Edge executable
options.add_argument("start-maximized")  # Maximize the browser window

# Add capability to accept insecure certs (ignore SSL errors)
options.set_capability('acceptInsecureCerts', True)

# Create the webdriver instance
browser = webdriver.Edge(options=options)

# Load the game data from the text file
game_data = []
with open("games.txt", "r") as file:
    for line in file:
        name, url = line.strip().split(" - ")[0], line.strip().split(" - ")[1]
        game_data.append((name, url))

# Print the available games for user selection
print("Available games:")
for i, (name, _) in enumerate(game_data):
    print(f"{i + 1}. {name}")

# Ask the user to input their selection
selection = input("Enter the numbers of the games you want to download (separated by commas or ranges): ")

# Parse the user input to get the selected games
selected_games = []
for part in selection.split(","):
    if "-" in part:
        start, end = map(int, part.split("-"))
        selected_games.extend(game_data[start - 1:end])
    else:
        selected_games.append(game_data[int(part) - 1])

for name, url in selected_games:
    print(f"Downloading {name}")
    # Flag to indicate if the download started
    download_started = False
    # Attempt to download until it starts
    while not download_started:
        # Open the URL
        browser.get(url)
        # Find the download button using the provided XPath expression
        button = browser.find_element(By.XPATH, "//button[contains(text(), 'Download')]")
        # Click the download button to start the download
        button.click()
        # Check if the download started
        if "download2.vimm.net/download" not in browser.current_url:
            download_started = True
        else:
            time.sleep(60)  # Wait for 1 minute before retrying
            browser.back()  # Navigate back

# Close the browser when done
browser.quit()

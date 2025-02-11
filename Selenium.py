import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random
import string
import base64



def setup():
	username ="sreenadhb"
	authkey ="I304plaCpBxpERvH5roJ6vFuWqLf4lokSJv2Bb1JvgIF0pjqbH"
	hub = "@hub.lambdatest.com/wd/hub"

	chrome_options = webdriver.ChromeOptions()

	def generate_random_string(length=10):
		# Create a string of letters and digits
		characters = string.ascii_letters + string.digits  # Includes both uppercase and lowercase letters and digits
		# Generate a random string
		random_string = ''.join(random.choice(characters) for _ in range(length))
		return random_string
	
	random_string = generate_random_string(12)
	build = os.getenv("LT_BUILD_NAME")
	platform= os.getenv("LT_PLATFORM")
	browser= os.getenv("LT_BROWSER_NAME")
	browserversion= os.getenv("LT_BROWSER_VERSION")
	buildnumber = os.getenv("LT_BUILD_NUMBER")
	tunnelname =os.getenv("LT_TUNNEL_NAME")


	options = {
		"platform": platform,
		"browserName": browser,
		"version": browserversion,
		"build": build,
		"name": buildnumber,
		"plugin": "git-testng",
		"performance": True,
		"network": True,
		"console": True,
		"networkThrottling": "Regular 4G",
		"commandLog": True,
		"systemLog": True,
		"terminal": True,
		"video": True,
		"tags": ["Feature", "Magicleap", "Severe"],
		"tunnel": True
		# "tunnelName": tunnelname
	}

	chrome_options.set_capability("LT:Options", options)

	driver = webdriver.Remote(
		command_executor="https://" + username + ":" + authkey + hub,
		options=chrome_options
	)

	print("tunnelname is :",tunnelname)

	return driver

def test_basic(driver):
	Status = "failed"
	firstFile = ""

	print("Loading Url")
	try:
		# Navigate to the URL
		driver.get("https://lambdatest.github.io/sample-todo-app/")

		# Checking boxes
		print("Checking Box")
		driver.find_element(By.NAME, "li1").click()

		print("Checking Another Box")
		driver.find_element(By.NAME, "li2").click()

		print("Checking Box")
		driver.find_element(By.NAME, "li3").click()

		print("Checking Another Box")
		driver.find_element(By.NAME, "li4").click()

		# Adding new items to the to-do list
		driver.find_element(By.ID, "sampletodotext").send_keys(" List Item 6")
		driver.find_element(By.ID, "addbutton").click()

		driver.find_element(By.ID, "sampletodotext").send_keys(" List Item 7")
		driver.find_element(By.ID, "addbutton").click()

		driver.find_element(By.ID, "sampletodotext").send_keys(" List Item 8")
		driver.find_element(By.ID, "addbutton").click()

		# Checking more boxes
		print("Checking Another Box")
		driver.find_element(By.NAME, "li1").click()

		print("Checking Another Box")
		driver.find_element(By.NAME, "li3").click()

		print("Checking Another Box")
		driver.find_element(By.NAME, "li7").click()

		print("Checking Another Box")
		driver.find_element(By.NAME, "li8").click()

		# Entering text
		print("Entering Text")
		driver.find_element(By.ID, "sampletodotext").send_keys("Get Taste of Lambda and Stick to It")
		driver.find_element(By.ID, "addbutton").click()

		print("Checking Another Box")
		driver.find_element(By.NAME, "li9").click()

		# Asserting the text in the 9th item
		span_text = driver.find_element(By.XPATH, "/html/body/div/div/div/ul/li[9]/span").text
		assert span_text == "Get Taste of Lambda and Stick to It", f"Text does not match: {span_text}"


	except Exception as e:
		print(str(e))
		session_id = driver.session_id
		print(f"Failed test session id: {session_id}")

		raise

	# Additional test steps here...

	Status = "passed"
	driver.execute_script("lambda-status=" + Status)
	driver.quit()

if __name__ == "__main__":
	driver = setup()
	test_basic(driver)

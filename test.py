from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Test cases
test_cases = [
    {"input": "3 3 3", "expected_output": "Equilateral"},
    {"input": "5 5 3", "expected_output": "Isosceles"},
    {"input": "3 4 5", "expected_output": "Scalene"},
    {"input": "1 2 3", "expected_output": "No Triangle"},
    {"input": "3", "expected_output": "Error: Two sides missing"},
    {"input": "3 4", "expected_output": "Error: One side missing"},
    {"input": "3 a 4", "expected_output": "Error: Non-numeric value encountered"},
    {"input": "3 4 5 6", "expected_output": "Error: Too many sides provided"},
    {"input": "Exit", "expected_output": "Application has exited."},
    {"input": "Quit", "expected_output": "Application has exited."},
    {"input": "0 0 0", "expected_output": "No Triangle"},
    # {"input": "-3 -4 -5", "expected_output": "No Triangle"}, - need to handle on the app
    # {"input": "3.0 4.0 5.0", "expected_output": "Scalene"}, - need to handle on the app
]

# path to chromedriver
#downlad from https://googlechromelabs.github.io/chrome-for-testing/#stable
chrome_driver_path = "/Users/karthik1029/Downloads/chromedriver-mac-arm64/chromedriver"

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

try:
    # open the shiny app
    url = "http://127.0.0.1:8000"
    driver.get(url)

    for case in test_cases:
        input_field = driver.find_element(By.ID, "input_string")
        input_field.clear()
        input_field.send_keys(case["input"])
        input_field.send_keys(Keys.RETURN)

        try:
            WebDriverWait(driver, 0.5).until(
                EC.text_to_be_present_in_element((By.XPATH, "//pre[@id='result']"), case["expected_output"])
            )
            result_output = driver.find_element(By.XPATH, "//pre[@id='result']").text
        except:
            result_output = ""

        if result_output != case["expected_output"]:
            try:
                WebDriverWait(driver, 0.5).until(
                    EC.text_to_be_present_in_element((By.XPATH, "//pre[@id='error']"), case["expected_output"])
                )
                result_output = driver.find_element(By.XPATH, "//pre[@id='error']").text
            except:
                result_output = ""

        assert result_output == case["expected_output"], f"Test failed for input {case['input']}: expected {case['expected_output']}, got {result_output}"
        print(f"Test passed for input {case['input']}")

finally:
    driver.quit()

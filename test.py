from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import yaml
import time

with open("test_cases.yaml", "r")as file:
    test_case = yaml.safe_load(file)

# path to chromedriver
#downlad from https://googlechromelabs.github.io/chrome-for-testing/#stable
chrome_driver_path = "/Users/karthik1029/Downloads/chromedriver-mac-arm64/chromedriver"

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

def run_tests(test_cases, category_name):
    total_tests = len(test_cases)
    passed_tests = 0

    for case in test_cases:
        input_field = driver.find_element(By.ID, "input_string")
        input_field.clear()
        input_field.send_keys(case["input"])
        input_field.send_keys(Keys.RETURN)

        start_time = time.time()

        try:
            WebDriverWait(driver, 0.01).until(
                EC.text_to_be_present_in_element((By.XPATH, "//pre[@id='result']"), case["expected_output"])
            )
            result_output = driver.find_element(By.XPATH, "//pre[@id='result']").text
        except:
            result_output = ""

        if result_output != case["expected_output"]:
            try:
                WebDriverWait(driver, 0.01).until(
                    EC.text_to_be_present_in_element((By.XPATH, "//pre[@id='error']"), case["expected_output"])
                )
                result_output = driver.find_element(By.XPATH, "//pre[@id='error']").text
            except:
                result_output = ""

        end_time = time.time()
        response_time = end_time - start_time
        print(f"Response time for input {case['input']}: {response_time:.4f} seconds\n")

        if result_output == case["expected_output"]:
            passed_tests += 1
            print(f"Test passed for input {case['input']}")
        else:
            print(f"Test failed for input {case['input']}: expected {case['expected_output']}, got {result_output}")

    pass_ratio = passed_tests / total_tests * 100
    print(f"\n{category_name} Tests Summary:")
    print(f"Total Test Cases: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Pass Ratio: {pass_ratio:.2f}%\n")
    print(f"################################################")
    return total_tests, passed_tests

try:
    # open the shiny app
    url = "http://127.0.0.1:8000"
    driver.get(url)

    total_tests = 0
    total_passed = 0

    for category, tests in test_case.items():
        cat_total, cat_passed = run_tests(tests, category)
        total_tests += cat_total
        total_passed += cat_passed


    # pass ratio
    overall_pass_ratio = total_passed / total_tests * 100
    print(f"Overall Test Summary:")
    print(f"Total Test Cases: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Overall Pass Ratio: {overall_pass_ratio:.2f}%\n")
    print(f"################################################")

finally:
    driver.quit()

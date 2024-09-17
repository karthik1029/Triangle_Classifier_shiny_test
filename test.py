from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Test case categories
functional_tests = [
    {"input": "3 3 3", "expected_output": "Equilateral"},
    {"input": "5 5 3", "expected_output": "Isosceles"},
    {"input": "3 4 5", "expected_output": "Scalene"},
    {"input": "1 2 3", "expected_output": "No Triangle"},
]

error_cases = [
    {"input": "3", "expected_output": "Error: Two sides missing"},
    {"input": "3 4", "expected_output": "Error: One side missing"},
    {"input": "3 a 4", "expected_output": "Error: Non-numeric value encountered"},
    {"input": "3 4 5 6", "expected_output": "Error: Too many sides provided"},
]

exit_cases = [
    {"input": "Exit", "expected_output": "Application has exited."},
    {"input": "Quit", "expected_output": "Application has exited."},
]

corner_cases = [
    {"input": "0 0 0", "expected_output": "No Triangle"},
    {"input": "-1 -2 -3", "expected_output": "Error: Triangles can't have negative sides"},
    {"input": "-1", "expected_output": "Error: Triangles can't have negative sides"},
    {"input": "-1 -1", "expected_output": "Error: Triangles can't have negative sides"},
]

# Path to ChromeDriver
chrome_driver_path = "/Users/karthik1029/Downloads/chromedriver-mac-arm64/chromedriver"

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Function to run tests and count passes/fails
def run_tests(test_cases, category_name):
    total_tests = len(test_cases)
    passed_tests = 0

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
    # Open the Triangle Classifier web app
    url = "http://127.0.0.1:8000"  # Replace with your app's URL
    driver.get(url)

    # Run each category of tests and gather results
    total_tests = 0
    total_passed = 0

    for category, tests in [("Functional", functional_tests),
                            ("Error", error_cases),
                            ("Exit", exit_cases),
                            ("Corner Case", corner_cases)]:
        cat_total, cat_passed = run_tests(tests, category)
        total_tests += cat_total
        total_passed += cat_passed

    # Overall results
    overall_pass_ratio = total_passed / total_tests * 100
    print(f"Overall Test Summary:")
    print(f"Total Test Cases: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Overall Pass Ratio: {overall_pass_ratio:.2f}%\n")
    print(f"################################################")

finally:
    driver.quit()

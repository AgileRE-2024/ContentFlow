import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

class ContentFlowAnalysis(unittest.TestCase):
    def setUp(self):
        """Setup browser and navigate to analysis URL page."""
        self.driver = webdriver.Chrome()
        self.base_url = "http://127.0.0.1:8000/analysis/"
        self.driver.get(self.base_url)

    def test_successful_analysis(self):
        """Scenario 1: Successful content analysis and recommendations."""
        driver = self.driver
        # Input valid URL
        url_input = driver.find_element(By.NAME, "url")
        url_input.send_keys("https://biz.kompas.com/read/2024/11/05/105203028/transaksi-bisnis-isef-2024-dekati-angka-rp-2-triliun")
        
        # Click the Analyze button
        analyze_button = driver.find_element(By.ID, "analyze-btn")
        analyze_button.click()

        # Verify the results
        result_section = driver.find_element(By.ID, "result-section")
        self.assertIn("Analysis Result", result_section.text)

    def test_empty_url(self):
        """Scenario 2: Empty URL."""
        driver = self.driver
        # Leave URL empty and click the Analyze button
        analyze_button = driver.find_element(By.ID, "analyze-btn")
        analyze_button.click()

        # Verify the error message
        error_message = driver.find_element(By.ID, "error-section")
        self.assertIn("URL tidak boleh kosong", error_message.text)

    def test_access_denied(self):
        """Scenario 3: Access denied (403 Error)."""
        driver = self.driver
        # Input restricted URL
        url_input = driver.find_element(By.NAME, "url")
        url_input.send_keys("https://kumparan.com/kumparannews/testimoni-tertulis-tom-lembong-saksi-tiba-tiba-jadi-tersangka-dan-ditahan-23wtbgPFiYo")
        
        # Click the Analyze button
        analyze_button = driver.find_element(By.ID, "analyze-btn")
        analyze_button.click()

        # Verify the error message
        error_section = driver.find_element(By.ID, "error-section")
        self.assertIn("Gagal mengambil data", error_section.text)

    def tearDown(self):
        """Close the browser after tests."""
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
__author__ = 'Kan!skA & Ashish'

import unittest
import csv
import time
import os
import win32com.client
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

class TTS(unittest.TestCase):
    driver = None

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        time.sleep(11)
        cls.driver.maximize_window()
        cls.driver.get("http://10.240.12.168/tts-HTS/")
        time.sleep(5)
        iSelect = Select(cls.driver.find_element_by_xpath(".//*[@id='AutoNumber1']/tbody/tr[1]/td[2]/select"))
        iSelect.select_by_value("voice4")
        time.sleep(2)

    def test_TTS(self):
        # Change Your Set Number Here
        set = "Set 1"

        # Handling of .csv files
        rows = dict()
        inputFileName = set + '/Paragraph/Paragraphs'
        data_file = open(inputFileName + '.csv', "r", encoding='utf-8')
        reader = csv.reader(data_file)
        lineNum = 1
        lineNumForFile = 1
        for row in reader:
            rows[lineNum] = row
            lineNum += 1
        time.sleep(5)
        errorOutputFileName = inputFileName + '_error'
        error_out_data_file = open(errorOutputFileName + '.csv', "w", encoding='utf-8')
        time.sleep(2)

        for inputLineNum, inputData in rows.items():
            # Click on Clear Button
            self.driver.find_element_by_xpath(".//*[@id='AutoNumber1']/tbody/tr[4]/td/input[1]").click()
            time.sleep(5)
            # Enter Input in the Text Area
            self.driver.find_element_by_xpath(".//*[@id='AutoNumber1']/tbody/tr[7]/td[2]/p/textarea").send_keys(inputData)
            time.sleep(5)
            # Click on Synthesize Button
            self.driver.find_element_by_xpath(".//*[@id='AutoNumber1']/tbody/tr[4]/td/input[2]").click()
            time.sleep(11)
            displayed = self.driver.find_elements_by_xpath(".//*[@id='jsn-page']/center[1]/a").__len__()
            if displayed > 0:
                # Right-Click on Output Link
                download = self.driver.find_element_by_xpath(".//*[@id='jsn-page']/center[1]/a")
                ActionChains(self.driver).context_click(download).key_down(Keys.ARROW_DOWN).perform()
                time.sleep(5)
                shell = win32com.client.Dispatch("WScript.Shell")
                shell.SendKeys('k')
                time.sleep(5)
                # Path for Keeping Output
                str1 = str('\Audio\\' + set + '\Paragraph\P-' + set + '-')
                shell.SendKeys(os.getcwd() + str1 + str(lineNumForFile))
                lineNumForFile += 1
                time.sleep(5)
                shell.SendKeys('{ENTER}')
                time.sleep(11)
            else:
                error_out_data_file.write(str(inputLineNum) + " : " + inputData[0])
                error_out_data_file.writelines('\n')
                time.sleep(3)
            # Click on Back
            self.driver.find_element_by_link_text("GoBack").click()
            time.sleep(5)
        error_out_data_file.close()

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

if __name__ == '__main__':
    unittest.main()

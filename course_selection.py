import time
import tkinter as tk
import threading
from typing import Counter
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException

class System():
    chrome_options = webdriver.ChromeOptions()
    url = "https://courseselection.ntust.edu.tw"
    Working = False
    StudentNumberStr = tk.StringVar
    PasswordStr = tk.StringVar
    driver = WebDriver
    window = tk.Tk()
    count = 0
    flag = True
    courses = None
    courses_counter = 0
    def __init__(self):
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.StudentNumberStr = tk.StringVar(None,"B10815044")
        self.PasswordStr = tk.StringVar(None,"@Skills39")
        self.driver = webdriver.Chrome("./chromedriver.exe", options=self.chrome_options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{
                "source":"""Object.defineProperty(navigator, 'webdriver', {get: () => false})"""
            })
        self.driver.get(self.url)
    def loot(self):
        ID = self.StudentNumberStr.get()
        PASSWORD = self.PasswordStr.get()

        if(self.driver.find_elements(By.NAME, "UserName")):
            self.driver.find_element(By.NAME, "UserName").send_keys(ID)
        if(self.driver.find_elements(By.NAME, "Password")):
            self.driver.find_element(By.NAME, "Password").send_keys(PASSWORD)
        if(self.driver.find_elements(By.ID, "btnLogIn")):
            self.driver.find_element(By.ID, "btnLogIn").click()
        while True:
            try:
                self.driver.find_element(By.CLASS_NAME, "dropdown").click()
                self.driver.find_element(By.PARTIAL_LINK_TEXT, "電腦抽選後選課").click()
                self.Working = True
                break
            except:
                pass
        # if(self.driver.find_elements(By.CLASS_NAME, "addbtn")):
        #     self.courses = self.driver.find_elements(By.CLASS_NAME, "addbtn")
        self.Update()
    
    def initGUI(self):
        self.window.title('window')
        self.window.geometry('900x600')
        mainCanvas = tk.Canvas(self.window,height=400,width=600,bd=0, highlightthickness = 0,background="#dcdcdc")
        mainCanvas.place(x = 150,y = 100)
        StudentNumberLabel = tk.Label(mainCanvas,text="Student Number：", font=('Helvetica', '15'),background="#dcdcdc")
        StudentNumberLabel.place(x=100,y=100)
        
        StudentNumber = tk.Entry(mainCanvas,textvariable=self.StudentNumberStr)
        StudentNumber.place(x=260,y=100,height=30,width=150)
        
        PasswordLabel = tk.Label(mainCanvas,text="Password：", font=('Helvetica', '15'),background="#dcdcdc")
        PasswordLabel.place(x=100,y=150)
        
        Password = tk.Entry(mainCanvas,textvariable=self.PasswordStr,show="*")
        Password.place(x=260,y=150,height=30,width=150)
        
        StartBtn = tk.Button(mainCanvas,text="Start",command=self.loot)
        StartBtn.place(x = 100, y=200,height=30,width=150)
        
        StopBtn = tk.Button(mainCanvas,text="Stop",command=self.Stop)
        StopBtn.place(x = 260, y=200,height=30,width=150)
        
        ResetBtn = tk.Button(mainCanvas,text="Reset",command=self.Reset)
        ResetBtn.place(x = 260, y=250,height=30,width=150)
        self.window.mainloop()
    def Stop(self):
        self.Working = False
    
    
    def Pick(self):
        try:
            self.courses = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "addbtn"))
            )
            self.courses[self.courses_counter].click()
            self.courses_counter = (self.courses_counter+1) % len(self.courses)
        except TimeoutException as exception:
            parent_msg = " and parent locator '{}'".format(self.parent) if self.parent else ''
            msg = "Page element of type '%s' with locator %s%s not found or is not visible after %s seconds"
            self.logger.error(msg, type(self).__name__, self.locator, parent_msg)
            exception.msg += "\n  {}".format(msg % (type(self).__name__, self.locator, parent_msg))
            return True
        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        except NoAlertPresentException:
            print("alert exceprtion")
            return True
        else:
            self.driver.switch_to.alert.accept()
        return False
        # self.courses = self.driver.find_elements(By.CLASS_NAME, "addbtn")
        # if(self.courses):
        #     while self.flag:
        #         try:
        #             self.courses[self.courses_counter].click()
        #             print(self.courses_counter)
        #             self.courses_counter = (self.courses_counter+1) % len(self.courses)
        #         except:
        #             if(EC.alert_is_present()):
        #                 wait = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        #                 self.driver.switch_to.alert.accept()
        #                 self.flag = False
        # else:
        #     self.Reset()
            
    def Reset(self):
        self.driver.find_element(By.CLASS_NAME, "dropdown").click()
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "電腦抽選後選課").click()
        self.Working = True
        
    def Update(self):
        if(self.Working):
            if(self.Pick()):
                self.Reset()
        self.window.after(100,self.Update)

s = System()
s.initGUI()
   
    
        
    
    
    
    
# 歡迎取用 選課之路 有你有我
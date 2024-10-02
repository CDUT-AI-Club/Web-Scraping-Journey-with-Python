from selenium import webdriver
import pickle

# 配置Selenium
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.bilibili.com/")

# 暂停脚本，等待手动登录
input("请手动登录后按Enter继续...")

# 保存Cookies到文件
pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
print("Cookies 已保存")

driver.quit()

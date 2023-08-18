import os
import time
from email.message import EmailMessage

import schedule as schedule
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import smtplib
import ssl
def sendemail(price,email_reciever):
    email_sender = "your email" #use your email
    email_password = "your password"
    subject = 'Price Change'
    body = f"the price has fallen to {price}"
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_reciever
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        if price <= 999.0:
            smtp.sendmail(email_sender, email_reciever, em.as_string())
        else:
            pass
options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
driver = webdriver.Chrome(options=options)
url = "https://www.amazon.in/dp/B09N3ZNHTY/ref=s9_acsd_al_bw_c2_x_0_i?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-3&pf_rd_r=59QZCXVEGNATQJF7BGKC&pf_rd_t=101&pf_rd_p=5a91b7c5-7007-4012-bd0b-35bdd7ae8152&pf_rd_i=1388921031"
driver.get(url)
price = float(driver.find_element(By.XPATH,'//*[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]').text[1:].replace(',',''))
print(price)
driver.quit()
emails = ["your@email.id"] #Enter your email
for i in emails:
    schedule.every(90).minutes.do(sendemail,price,i)
while 1:
    schedule.run_pending()
    time.sleep(1)

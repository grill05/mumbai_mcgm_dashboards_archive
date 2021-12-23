from selenium import webdriver;
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


import os,requests,time,bs4,datetime,csv;
from PIL import Image
import json

if __name__=='__main__':
  
  PROXY='203.115.123.165:9999'
  max_tries=100;tries=0
  
  date=datetime.datetime.now();date_str=date.strftime('%d_%m_%Y');  
  options=webdriver.ChromeOptions();
  options.add_argument('--ignore-certificate-errors');
  options.add_argument('--disable-gpu');
  options.add_argument("--headless")
  options.add_argument("--window-size=1366,768")
  options.add_argument("--proxy-server=socks4://"+PROXY);

  webdriver.DesiredCapabilities.CHROME['proxy'] = {
    "httpProxy": PROXY,
    "ftpProxy": PROXY,
    "sslProxy": PROXY,
    "proxyType": "MANUAL",
    "socksProxy": PROXY,
    "socksVersion":4

}
  
  driver=webdriver.Chrome(chrome_options=options)  
  
  url='https://www.powerbi.com/view?r=eyJrIjoiOTcyM2JkNTQtYzA5ZS00MWI4LWIxN2UtZjY1NjFhYmFjZDBjIiwidCI6ImQ1ZmE3M2I0LTE1MzgtNGRjZi1hZGIwLTA3NGEzNzg4MmRkNiJ9'
  # ~ url='https://apps.bbmpgov.in/Covid19/en/bedstatus.php'
  
  while tries<max_tries:
    try: 
      driver.get(url);
    except:
      print('Failed on try: %d..Retrying' %(tries));
      tries+=1;
  
  time.sleep(5)
  date=datetime.datetime.now();date_str=date.strftime('%d_%m_%Y')
  if not os.path.exists('images/'+date_str+'.png'):
    driver.save_screenshot('images/'+date_str+'.png')
    img=Image.open('images/'+date_str+'.png')
    img.save('images/'+date_str+'.webp')
    print('saved screenshot of bengaluru beds availability dashboard to %s' %('images/'+date_str+'.webp'))
  else:
    print('Image: %s already existed. Skipping!!' %('images/'+date_str+'.png'))
  

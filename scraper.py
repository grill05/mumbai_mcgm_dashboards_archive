import os,requests,json,datetime,csv

if __name__=='__main__':
  date=datetime.datetime.now();date_str=date.strftime('%d_%m_%Y')
  os.system('wget "https://stopcoronavirus.mcgm.gov.in/assets/docs/Dashboard.pdf" -O "mumbai_dashboards/'+date_str+'.pdf"')


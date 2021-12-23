import os,requests,json,datetime,csv

if __name__=='__main__':
  proxy='socks4://203.115.123.165:9999'
  max_tries=100;tries=0

  
  date=datetime.datetime.now();date_str=date.strftime('%d_%m_%Y')
  # ~ os.system('curl -# "https://stopcoronavirus.mcgm.gov.in/assets/docs/Dashboard.pdf" -o "mumbai_dashboards/'+date_str+'.pdf"')

  dashboard_fname="mumbai_dashboards/"+date_str+'.pdf'
  while (not os.path.exists(dashboard_fname)) and (tries<max_tries):    
    cmd='curl  -k -x "'+proxy+'" "https://stopcoronavirus.mcgm.gov.in/assets/docs/Dashboard.pdf" -o "'+dashboard_fname+'"'
    print(cmd)
    os.system(cmd)
    os.system('ls -a mumbai_dashboards/')
    tries+=1


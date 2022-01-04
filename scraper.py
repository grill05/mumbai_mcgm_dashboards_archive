import os,sys,requests,json,datetime,csv
#proxy='socks4://203.115.123.165:9999'
proxy='socks4://157.119.201.231	:1080'

def mumbai_bulletin_parser(bulletin=''):
  #get date
  cmd='pdftotext -x 10 -y 150 -W 200 -H 200 -layout -f 1 -l 1  "'+bulletin+'" t.txt';os.system(cmd)
  b=[i.strip().replace(',','') for i in open('t.txt').readlines() if i.strip()]

  date=[i.replace(',','') for i in b if '2021' in i or '2022' in i]
  if not date: print('could not get date from '+bulletin)
  else: date=datetime.datetime.strptime(date[0],'%b %d %Y');date_str=date.strftime('%Y-%m-%d')
  
  #get cases,tests,symp etc
  cmd='pdftotext -x 0 -y 100 -W 220 -H 320 -layout -f 2 -l 2 "'+bulletin+'" t.txt';os.system(cmd)
  b=[i.strip().replace(',','') for i in open('t.txt').readlines() if i.strip()]
  
  cases=[i for i in b if 'positive' in i.lower()]
  if not cases: print('could not get cases from '+bulletin)
  else: cases=int(cases[0].split()[-1].strip())
  
  active=[i for i in b if 'active' in i.lower()]
  if not active: print('could not get actives from '+bulletin)
  else: active=int(active[0].split()[-1].strip())
  
  asymp=[i for i in b if 'Asymptomatic' in i]
  if not asymp: print('could not get asymp from '+bulletin)
  else: asymp=int(asymp[0].split()[-1].strip())
  
  symp=[i for i in b if 'Symptomatic' in i]
  if not symp: print('could not get symp from '+bulletin)
  else: symp=int(symp[0].split()[-1].strip())
  
  critical=[i for i in b if 'critical' in i.lower()]
  if not critical: print('could not get criticals from '+bulletin)
  else: critical=int(critical[0].split()[-1].strip())
  
  tests=[i for i in b if 'tests' in i.lower()]
  if not tests: print('could not get tests from '+bulletin)
  else: tests=int(tests[0].split()[-1].strip())
  
  #get hospital occupancy
  cmd='pdftotext -x 340 -y 100 -W 95 -H 340 -layout -f 2 -l 2 "'+bulletin+'" t.txt';os.system(cmd)
  b=[i.strip().replace(',','') for i in open('t.txt').readlines() if i.strip()]
  
  if not ('2021' in b[0] or '2022' in b[0]): #means date wasn't at top, parsed wrong
    print('could not parse occupancy numbers')
  else:
    try:
      bc,bo,ba,dc,do,da,oc,oo,oa,ic,io,ia,vc,vo,va=b[1:]
    except:
      print('failed to get occupancy split')
      return b
    gen_beds_cap=int(bc);gen_beds_occupancy=int(bo)
    o2_cap=int(oc);o2_occupancy=int(oo)
    icu_cap=int(ic);icu_occupancy=int(io)
    vent_cap=int(vc);vent_occupancy=int(vo)
 
  row=(date_str,cases,tests,o2_cap,icu_cap,vent_cap,o2_occupancy,icu_occupancy,vent_occupancy,gen_beds_cap,gen_beds_occupancy,active,symp,asymp,critical)
  
  a=open('mumbai.csv');r=csv.reader(a);info=[i for i in r];a.close()
  dates=list(set([i[0] for i in info[1:] if len(i)>0]));dates.sort()
  if date_str in dates:     
    print('----------\n\nData for %s already exists in mumbai.csv!!\nOnly printing, not modifying csv!!\n\n----------\n\n' %(date_str))
  else:
    a=open('mumbai.csv','a');w=csv.writer(a);w.writerow(row);a.close()
  print(row)
  return row


if __name__=='__main__':
  date=datetime.datetime.now();date_str=date.strftime('%d_%m_%Y')
  dashboard_fname="mumbai_dashboards/"+date_str+'.pdf'
  
  if sys.argv[-1].endswith('.pdf'): #parse bulletin
    print('trying to parse '+sys.argv[-1])
    mumbai_bulletin_parser(sys.argv[-1])
  elif sys.argv[-1] in ['parse_today_bulletin']: #parse bulletin
    print('trying to automatically detect and parse bulletin for today')
    if not os.path.exists(dashboard_fname):      print('bulletin for today: %s not found,returning' %(dashboard_fname))
    else:      mumbai_bulletin_parser(dashboard_fname)
  elif sys.argv[-1] in ['download_bulletin']:  
    max_tries=100;tries=0
    if os.path.exists(dashboard_fname): print('todays bulletin already exists.nothing to download')
  
    while (not os.path.exists(dashboard_fname)) and (tries<max_tries):    
      cmd='curl  -k -x "'+proxy+'" "https://stopcoronavirus.mcgm.gov.in/assets/docs/Dashboard.pdf" -o "'+dashboard_fname+'"'
      print(cmd)
      os.system(cmd)
      os.system('ls -a mumbai_dashboards/')
      tries+=1


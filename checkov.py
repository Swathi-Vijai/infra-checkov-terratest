def get_severity_value(url,check_id):
                      if url == None and check_id.startswith("CP"):
                          return("Custom Policy")
                      elif url == None:
                          return("LOW*")
                      else:
                          import requests
                          from bs4 import BeautifulSoup

                          # Making a GET request
                          r = requests.get(url)
                          soup = BeautifulSoup(r.content, 'html.parser')

                          s = soup.find('div', class_='excerpt')
                          if s == None:
                              return("LOW")
                          else:
                              lines = s.find_all('p')
                              st=''
                              for line in lines:
                                  st=st+(line.text)
                              l=st.split('\n')
                              for x in l:
                                  if 'Severity' in x:
                                      return(x[10:1000])

import json
line = "-"*125
divider = ' | '.join(["-"*18 for _ in range(6)])
line_indicator = '%0D%0A'
block_indicator = """```"""
Severity = ["LOW","MEDIUM","HIGH","CRITICAL"]
Skip_Severity = "LOW"
Restricted_Severity = ["HIGH", "CRITICAL"]
hfc=0
flag=0
if Skip_Severity in Severity:
   i= Severity.index(Skip_Severity)
   sl= Severity[0:i]
else:
    sl=[]
print(sl)
o = open("summary.json", "w")
f=open('Checkov-report_json.json')
data=json.load(f)
res = line + line_indicator
if type(data) == list:
  for i in range(len(data)):
      pas=[]
      fail=[]
      skip=[]
      res = res + str('Check Type:     ' +
                                                  data[i]["check_type"]).center(120)
      xdata = data[i]["summary"]
      check_results = data[i]["results"]
      passed_check = (check_results["passed_checks"])
      for j in range(len((check_results["passed_checks"]))):
          sw=str(get_severity_value(passed_check[j]["guideline"], passed_check[j]["check_id"])) 
          print(sw)
          if sw in sl:
              skip.append(((str(sw+ \
                                                  " : " + (passed_check[j]["check_name"]) + " - Resource Name : " + (passed_check[j]["resource"]))))
          else:
              pas.append(((str(get_severity_value(passed_check[j]["guideline"], passed_check[j]["check_id"]))+ \
                                                  " : " + (passed_check[j]["check_name"]) + " - Resource Name : " + (passed_check[j]["resource"]))))
          
      failed_check = (check_results["failed_checks"])
      for j in range(len((check_results["failed_checks"]))):
          if str(get_severity_value(failed_check[j]["guideline"], failed_check[j]["check_id"])) in sl:
              skip.append(((str(get_severity_value(failed_check[j]["guideline"], failed_check[j]["check_id"]))+ \
                                                  " : " + (failed_check[j]["check_name"]) + " - Resource Name : " + (failed_check[j]["resource"]))))
          else:
              if(str(get_severity_value(failed_check[j]["guideline"], failed_check[j]["check_id"]))) in Restricted_Severity:
                  if(hfc==0):
                      flag = 1
                      print(f"##vso[task.setvariable variable=FlagFailedSeverity;]{flag}")
              fail.append((str(get_severity_value(failed_check[j]["guideline"], failed_check[j]["check_id"]))+ \
                                                  " : " + (failed_check[j]["check_name"]) + " - Resource Name : " + (failed_check[j]["resource"])))
      skipped_checks = (check_results["skipped_checks"])
      for j in range(len((check_results["skipped_checks"]))):
          skip.append(((str(get_severity_value(skipped_checks[j]["guideline"], skipped_checks[j]["check_id"]))+ \
                                                  " : " + (skipped_checks[j]["check_name"]) + " - Resource Name : " + (skipped_checks[j]["resource"]))))
     
      xdata['passed']=len(pas)
      xdata['failed'] = len(fail) 
      xdata['skipped']=len(skip)
      o.write(str('Check Type:     ' +
                                                  data[i]["check_type"]))
      o.write('\n')
      o.write(json.dumps(xdata))
      o.write('\n')
     
      res = res + line_indicator + line + line_indicator + ' | '.join(xdata.keys()
                                                                                                  ) + line_indicator + divider + line_indicator + ' | '.join(map(str, xdata.values())) + line_indicator + line
      for _ in check_results:
        name = " ".join(map(lambda z: z.capitalize(), _.split('_')))
        res = res + line_indicator + block_indicator

        res = res + line_indicator + name + ':'
        if _ == "passed_checks":

            for x in pas:

                res = res + line_indicator + x    
            res = res + line_indicator
        elif _ == "failed_checks":

            for x in fail:

                res = res + line_indicator + x    
            res = res + line_indicator
        elif _ == "skipped_checks":

            for x in skip:

                res = res + line_indicator + x    
            res = res + line_indicator
            
        else:
            for j in range(len(check_results[_])):

                res = res + line_indicator + (check_results[_][j])
            res = res + line_indicator
        res = res + line_indicator + block_indicator + \
            line_indicator + line + line_indicator  
else:
    res = res + str('Check Type:     ' + data["check_type"]).center(120)
    xdata = data["summary"]
    res = res + line_indicator + line + line_indicator + ' | '.join(xdata.keys()    ) + line_indicator + divider + line_indicator + ' | '.join(map(str, xdata.values())) + line_indicator + line
#o.write(res) 
#o.close()
print(f"##vso[task.setvariable variable=GhComment;]{res}")
f.close()

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
def format(pa):
    if(len(pa))==0:
      return pa
    else:
        pas=["SEVERITY,CHECK-NAME,RESOURCE-NAME "]
        pas.extend(pa)
        lse=[]
        lsc=[]
        lsr=[]
        for x in pas:
            
            sp=x.split(",")
            lse.append(sp[0])
            lsc.append(sp[1])
            lsr.append(sp[2])
        mc=0
        for x in lsc:
            if(len(x)) > mc:
                mc=len(x)
        mr=0
        for x in lsr:
          if(len(x))  > mr:
             mr=len(x)
        pas=[]
        for i in range(len(lse)):
            s='|'
            if len(lse[i]) != 15:
                s=s + lse[i] + " "*(15-(len(lse[i]))) + '|'
            else:
                s=s+lse[i]+ '|'
            if len(lsc[i]) != mc:
                s=s + lsc[i] + " "*(mc-(len(lsc[i])))+ '|'
            else:
                s=s+lsc[i]+ '|'
            if len(lsr[i]) != mr:
                s=s + lsr[i] + " "*(mr-(len(lsr[i])))+ '|'
            else:
                s=s+lsr[i]+ '|'
            pas.append(s)
        return pas
    

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
lfa=0
lski=0
if Skip_Severity in Severity:
   i= Severity.index(Skip_Severity)
   sl= Severity[0:(i+1)]
else:
    sl=[]

o = open("summary.json", "w")
f=open('Checkov-report_json.json')
xml=f=open("Checkov-report_xml.xml")
import xml.etree.ElementTree as ET
xmlTree = ET.parse(f)
root = xmlTree.getroot()
data=json.load(f)
res = line + line_indicator
if type(data) == list:
  for i in range(len(data)):
      pas=[]
      fail=[]
      skip=[]
      res = res + str('Check Type:     ' +
                                                  data[i]["check_type"]).center(120)
      check_type=data[i]["check_type"]
      xdata = data[i]["summary"]
      check_results = data[i]["results"]
      passed_check = (check_results["passed_checks"])
      for j in range(len((check_results["passed_checks"]))):
          sw=str(get_severity_value(passed_check[j]["guideline"], passed_check[j]["check_id"])) 
          cn=(passed_check[j]["check_name"])
          rn=(passed_check[j]["resource"])
          
          if sw in sl:
              skip.append(((str(sw)+ \
                                                  " , " + (passed_check[j]["check_name"]) + " , " + (passed_check[j]["resource"]))))
          else:
              pas.append(((str(sw)+ \
                                                  " , " + (passed_check[j]["check_name"]) + " , " + (passed_check[j]["resource"]))))
          
      failed_check = (check_results["failed_checks"])
      for j in range(len((check_results["failed_checks"]))):
          sw=str(get_severity_value(failed_check[j]["guideline"], failed_check[j]["check_id"]))
          if sw in sl:
              skip.append(((str(sw)+ \
                                                  " , " + (failed_check[j]["check_name"]) + " , " + (failed_check[j]["resource"]))))
          else:
              if sw in Restricted_Severity:
                  if(hfc==0):
                      flag = 1
                      print(f"##vso[task.setvariable variable=FlagFailedSeverity;]{flag}")
              fail.append((str(sw)+ \
                                                  " , " + (failed_check[j]["check_name"]) + " , " + (failed_check[j]["resource"])))
      skipped_checks = (check_results["skipped_checks"])
      for j in range(len((check_results["skipped_checks"]))):
          skip.append(((str(get_severity_value(skipped_checks[j]["guideline"], skipped_checks[j]["check_id"]))+ \
                                                  " , " + (skipped_checks[j]["check_name"]) + " , " + (skipped_checks[j]["resource"]))))
     
      
      
      for child in root:
          if child.attrib["name"]==check_type:
                child.attrib["failures"] = len(fail)
                child.attrib["skipped"] = len(skip)
      
      lfa=lfa+len(fail)
      lski=lski+len(skip)
      xdata['passed']=len(pas)
      xdata['failed'] = len(fail) 
      xdata['skipped']=len(skip)
      o.write(str('Check Type:     ' +
                                                  data[i]["check_type"]))
      o.write('\n')
      o.write(json.dumps(xdata))
      o.write('\n')
      pas=format(pas)
      fail=format(fail)
      skip=format(skip)
     
      res = res + line_indicator + line + line_indicator + ' | '.join(xdata.keys()
                                                                                                  ) + line_indicator + divider + line_indicator + ' | '.join(map(str, xdata.values())) + line_indicator + line
      for _ in check_results:
        name = " ".join(map(lambda z: z.capitalize(), _.split('_')))
        res = res + line_indicator + block_indicator

        res = res + line_indicator + name + ':'
        if _ == "passed_checks":
            if(len(pas)>0):
                div="-"*len(pas[0])
            for x in pas:
                res = res + line_indicator + div
                res = res  + line_indicator+ x    
            res = res+ line_indicator + div + line_indicator
        elif _ == "failed_checks":
            if(len(fail)>0):
                div="-"*len(fail[0])
            for x in fail:
                res = res + line_indicator + div
                res = res + line_indicator + x    
            res = res + line_indicator+ div + line_indicator
                
        elif _ == "skipped_checks":
            if(len(skip)>0):
                div="-"*len(skip[0])
            for x in skip:
              res = res + line_indicator + div
              res = res + line_indicator + x    
            res = res + line_indicator+ div + line_indicator
            
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
root.attrib["failures"]=lfa
root.attrib["skipped"]=lski
xml.close()
o.close()
print(f"##vso[task.setvariable variable=GhComment;]{res}")
f.close()

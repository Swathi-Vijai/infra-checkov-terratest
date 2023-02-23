import json
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
                elif 'Bridgecrew Severity' in x:
                    return(x[10:1000])
def github_content(data):
    res = line + line_indicator
    if type(data) == list:
        for i in range(len(data)):
            res = res + str('Check Type:     ' +
                            data[i]["check_type"]).center(120)

            xdata = data[i]["summary"]

            res = res + line_indicator + line + line_indicator + ' | '.join(xdata.keys()
                                                                            ) + line_indicator + divider + line_indicator + ' | '.join(map(str, xdata.values())) + line_indicator + line
            # this report file is use to send email for particular users
            report_file.write(str('Check Type:     ' +
                            data[i]["check_type"]))
            report_file.write('\n')
            report_file.write(json.dumps(xdata))
            report_file.write('\n')
            #################################################
            

            check_results = data[i]["results"]

            # The next block of code is to use to get the severity levl of each error
            # Use flag and set FlagFailedSeverity as an variable
            Failed_Severity = []
            Restricted_Severity = ["HIGH", "CRITICAL"] # required to modify based on requirement
            #["HIGH", "CRITICAL", "MEDIUM", "LOW", "Custom Policy"]
            failed_check = (check_results["failed_checks"])
            for j in range(len((check_results["failed_checks"]))):
                Failed_Severity.append(str(get_severity_value(failed_check[j]["guideline"], failed_check[j]["check_id"])))
            flag = 0
            for _ in Failed_Severity:
                if _ in Restricted_Severity:
                    flag = 1
                    break
            print(
                f"##vso[task.setvariable variable=FlagFailedSeverity;]{flag}")
            

            
            # Rest of the code is for getting the require data for Github pull request and store it in res
            # And set GhComment as variable and assign the value as res
            for _ in check_results:
                name = " ".join(map(lambda z: z.capitalize(), _.split('_')))
                res = res + line_indicator + block_indicator

                res = res + line_indicator + name + ':'
                if _ != "parsing_errors":

                    for j in range(len(check_results[_])):

                        res = res + line_indicator + \
                            str(get_severity_value(check_results[_][j]["guideline"], check_results[_][j]["check_id"])) + \
                            " : " + (check_results[_][j]["check_name"]) + " - Resource Name: " + (check_results[_][j]["resource"])
                        # print("=============")
                        # print(check_results[_][j]["severity"])
                        # print("==========================")
                    res = res + line_indicator
                    
                else:
                    for j in range(len(check_results[_])):

                        res = res + line_indicator + (check_results[_][j])
                    res = res + line_indicator
                res = res + line_indicator + block_indicator + \
                    line_indicator + line + line_indicator
        print(res)
    else:
        res = res + str('Check Type:     ' + data["check_type"]).center(120)
        
        xdata = data["summary"]
        res = res + line_indicator + line + line_indicator + ' | '.join(xdata.keys()
        
                                                                        ) + line_indicator + divider + line_indicator + ' | '.join(map(str, xdata.values())) + line_indicator + line
        report_file.write(str('Check Type:     ' +
                            data["check_type"]))
        report_file.write('\n')
        report_file.write(json.dumps(xdata))
        report_file.write('\n')
        check_results = data["results"]
        Failed_Severity = []
        #print(Failed_Severity)
        Restricted_Severity = ["HIGH", "CRITICAL"]
        #["HIGH", "CRITICAL", "MEDIUM", "LOW"]
        check_results = data["results"]
        failed_check = (check_results["failed_checks"])
        for j in range(len((check_results["failed_checks"]))):
            print(j)
            Failed_Severity.append(
            str(get_severity_value(failed_check[j]["guideline"], failed_check[j]["check_id"])))
        print(Failed_Severity)
        flag = 0
        for _ in Failed_Severity:
            if _ in Restricted_Severity:
                flag = 1
                break
        print(
                f"##vso[task.setvariable variable=FlagFaileSeverity;]{flag}")

        for _ in check_results:
                # spilts_=
            name = " ".join(map(lambda z: z.capitalize(), _.split('_')))
                # print(name)
            res = res + line_indicator + block_indicator

            res = res + line_indicator + name + ':'
            if _ != "parsing_errors":

                for j in range(len(check_results[_])):

                    res = res + line_indicator + \
                        str(get_severity_value(check_results[_][j]["guideline"], check_results[_][j]["check_id"])) + \
                        " : " + (check_results[_][j]["check_name"]) + " - Resource Name: " + (check_results[_][j]["resource"])
                            # print("=============")
                            # print(check_results[_][j]["severity"])
                            # print("==========================")
                    res = res + line_indicator
                        
            else:
                for j in range(len(check_results[_])):

                    res = res + line_indicator + (check_results[_][j])
                res = res + line_indicator
            res = res + line_indicator + block_indicator + \
                        line_indicator + line + line_indicator
    return res

reading_file='aws_checkov_report.json'
writing_file='summary.json'
with open(writing_file, 'w') as report_file:
    print("The empty json file is created")
    line = "-"*125
    divider = ' | '.join(["-"*18 for _ in range(6)])
    line_indicator = '\n'
    block_indicator = """```"""
    with open(reading_file) as f:
        
        data = json.load(f)
        res = line + line_indicator
        res = github_content(data)
    print(f"##vso[task.setvariable variable=GhComment;]{res}")

# this is an example of a bad script to get work done quickly
# the contest logic is derived from https://github.com/nishanthvijayan/CoderCalendar
# the rest is just the fate of experimentation without version control
import requests
from bs4 import BeautifulSoup
import json
from time import strptime,strftime,mktime,gmtime,localtime
import sys
import os
#sys.stdout = open('codecheflogs.txt', 'w')
count={0:[], 1:[], 2:[], 3:[],"others":[] }
def get_problem(contest_code,problem_code):
    contest_code=contest_code.split('?')[0]
    #works on the fact that sample io will be inside pre tag and if more than 1 sample than more than 1 pre tag
    url="https://www.codechef.com/api/contests/"+contest_code+"/problems/"+problem_code
    try:
        r = requests.get(url)
        j= json.loads(r.text)
    except BaseException as e:
         print(e)
         print("error in fetching url "+url)
    else:
         try:
             os.makedirs(contest_code+"/"+problem_code)
         except:
             pass   
         open(contest_code+"/"+problem_code+"/.problem", "w").write(json.dumps(j,indent=4))
         
             
        #try:
        #    count[len(soup.find_all('pre'))].append(contest_code+"/"+problem_code)
        #except:
        #    count["others"].append(contest_code+"/"+problem_code)
            # sample_input=str(sampleio.b.next_sibling).strip()+"\n"
            # sample_output=str(sampleio.b.next_sibling.next_sibling.next_sibling).strip()+"\n"
            # if(sample_input[0] is ":"):
            #     sample_input=sample_input[1:].strip()+"\n"
            # if(sample_output[0] is ":"):
            #     sample_output=sample_output[1:].strip()+"\n"
            # print("input\n"+sample_input)
            # print("output\n"+sample_output)
            # #TODO create a log of the exception
            # print("error get testcase")
            # continue
    sys.stdout.flush()

'''
exceptions to above
https://www.codechef.com/IOIPRAC/problems/INOI1201
see codecheflogs.txt
'''

def get_contest(contest_code):
    try:
        os.makedirs(contest_code)
    except:
        pass
    contest_code=contest_code.split('?')[0]
    url="https://www.codechef.com/api/contests/"+contest_code
    try:
        r = requests.get(url)
        j= json.loads(r.text)
        open(contest_code+"/.contest","w").write(json.dumps(j, indent=4))
    except:
        print("error in fetching url:\n" + url)
    else:
        if("child_contests" in j):
            get_contest(contest_code+'A')
            get_contest(contest_code+'B')
            return
        problems=j["problems"]
        for problem in problems:
            print(contest_code,problems[problem]["code"],problems[problem]["name"],str(problems[problem]["successful_submissions"]))
            try:
                get_problem(contest_code,problems[problem]["code"])
            except BaseException as e:
                print(e)
                print("error geting problem",problems[problem]["code"])


#The following function is derived from CoderCalender
#https://github.com/nishanthvijayan/CoderCalendar
#published under GNU GPL 3.0

def get_duration(duration):
    days = duration/(60*24)
    duration %= 60*24
    hours = duration/60
    duration %= 60
    minutes = duration
    ans=""
    if days==1: ans+=str(days)+" day "
    elif days!=0: ans+=str(days)+" days "
    if hours!=0:ans+=str(hours)+"h "
    if minutes!=0:ans+=str(minutes)+"m"
    return ans.strip()

#The following function is derived from CoderCalender
#https://github.com/nishanthvijayan/CoderCalendar
#published under GNU GPL 3.0
#functionality for past contests is added.
#now using problem code instead of url

def  get_contest_list():
    url="http://www.codechef.com/contests"
    page = requests.get(url)
    print("got the list")
    soup = BeautifulSoup(page.text, "html.parser")

    posts= {"ongoing":[] , "upcoming":[], "past":[]}
    statusdiv = soup.findAll("table", attrs = {"class": "dataTable"})
    headings = soup.findAll("h3")
    contest_tables = {"Future Contests": [], "Present Contests": [],"Past Contests":[]}
    for i in range(len(headings)):
        contest_tables[headings[i].text] = statusdiv[i].findAll("tr")[1:]

    for upcoming_contest in contest_tables["Future Contests"]:
        details = upcoming_contest.findAll("td")
        start_time = strptime(details[2].text, "%d %b %Y %H:%M:%S")
        end_time = strptime(details[3].text, "%d %b %Y %H:%M:%S")
        duration = get_duration(int((mktime(end_time) - mktime(start_time)) / 60))
        posts["upcoming"].append({"Name":  details[1].text,
                                  "code":  details[1].a["href"][1:],
                                  "StartTime": strftime("%a, %d %b %Y %H:%M", start_time),
                                  "EndTime": strftime("%a, %d %b %Y %H:%M", end_time),
                                  "Duration": duration,
                                  "Platform": "CODECHEF"})
        print("contest "+details[1].a["href"][1:].split('?')[0])
        #get_contest(str(details[1].a["href"][1:]))

    for present_contest in contest_tables["Present Contests"]:
        details = present_contest.findAll("td")
        start_time = strptime(details[2].text, "%d %b %Y %H:%M:%S")
        end_time = strptime(details[3].text, "%d %b %Y %H:%M:%S")
        posts["ongoing"].append({"Name":  details[1].text,
                                 "code":  details[1].a["href"][1:],
                                 "StartTime": strftime("%a, %d %b %Y %H:%M", start_time),
                                 "EndTime": strftime("%a, %d %b %Y %H:%M", end_time),
                                 "Platform": "CODECHEF"})
        print("contest "+details[1].a["href"][1:].split("?")[0])
        try:
            get_contest(str(details[1].a["href"][1:].split('?')[0]))
        except:
            print("error get contest",str(details[1].a["href"][1:].split('?')[0]))

    for past_contest in contest_tables["Past Contests"]:
        details = past_contest.findAll("td")
        start_time = strptime(details[2].text, "%d %b %Y %H:%M:%S")
        end_time = strptime(details[3].text, "%d %b %Y %H:%M:%S")
        posts["past"].append({"Name":  details[1].text,
                                 "code":  details[1].a["href"][1:],
                                 "StartTime": strftime("%a, %d %b %Y %H:%M", start_time),
                                 "EndTime": strftime("%a, %d %b %Y %H:%M", end_time),
                                 "Platform": "CODECHEF"})
        print("contest "+details[1].a["href"][1:].split('?')[0])
        try:
            get_contest(str(details[1].a["href"][1:].split('?')[0]))
        except:
             print("error get contest",str(details[1].a["href"][1:].split('?')[0]))

        #print(posts["past"])

get_contest_list()
print("0 count\n",count[0])
print("1 count\n",count[1])
print("2 count\n",count[2])
print("3 count\n",count[3])
print("rest\n",count["others"])
sys.stdout.flush()
time.sleep(100)

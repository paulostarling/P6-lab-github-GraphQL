import requests
import csv
import matplotlib.pyplot
from datetime import datetime
from datetime import date
import numpy as np


api_token = 'place_your_token_here'

headers = {'Authorization': 'token %s' % api_token}

def save_data_to_file(data):
  # open the file in the write mode
  f = open('data.csv', 'a', newline='')
  writer = csv.writer(f)
  for repository in data:
    row = []
    row.append(repository['node']['name'])
    row.append(repository['node']['createdAt'])
    row.append(repository['node']['pushedAt'])
    row.append(repository['node']['stargazers']['totalCount'])
    row.append(repository['node']['pullRequests']['totalCount'])
    row.append(repository['node']['releases']['totalCount'])
    if repository['node']['primaryLanguage'] == None:
      row.append('None')
    else: 
      row.append(repository['node']['primaryLanguage']['name'])
    row.append(repository['node']['open']['totalCount'])
    row.append(repository['node']['closed']['totalCount'])
    writer.writerow(row)
  f.close()

def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.
query = """
{
  search(query: "is:public stars:>100 sort:stars-desc", type: REPOSITORY, first: 10, after:null) {
    repositoryCount
    pageInfo {
      endCursor
      startCursor
    }
    edges {
      node {
        ... on Repository {
          name
          createdAt
          pushedAt
          stargazers {
            totalCount
          }
          pullRequests(states:MERGED) {
            totalCount
          }
          releases {
            totalCount
          }
          primaryLanguage{
            name
          }
          open: issues(states:OPEN) {
            totalCount
          }
          closed: issues(states:CLOSED) {
            totalCount
          }
        }
      }
    }
  }
}
"""

header = ['name', 'createdAt', 'pushedAt', 'stargazers', 'pullRequests', 'releases', 'primaryLanguage', 'open_issues', 'closed_issues']
f = open('data.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(header)
f.close()

query_result = run_query(query) # Execute the query
print(query_result['data']['search']['edges'])
save_data_to_file(query_result['data']['search']['edges'])
end_cursor = '"' + query_result['data']['search']['pageInfo']['endCursor'] + '"'
query = query.replace('null', end_cursor)
old_end_cursor = end_cursor
for x in range(1,100):
  query_result = run_query(query)
  save_data_to_file(query_result['data']['search']['edges'])
  new_end_cursor = '"' + query_result['data']['search']['pageInfo']['endCursor'] + '"'
  query = query.replace(old_end_cursor, new_end_cursor)
  old_end_cursor = new_end_cursor

#RQ 01. Sistemas populares são maduros/antigos?

today = date.today()
with open('data.csv', newline='') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
  next(spamreader)
  delta_array = []
  for row in spamreader:
    create_date = row[0].split(',')[1]
    split_string = create_date.split("T", 1)
    datetime_object = datetime.strptime(split_string[0], '%Y-%m-%d').date()
    delta = today - datetime_object  
    delta_array.append(delta.days/360)
median = np.median(delta_array)
fig1, ax1 = matplotlib.pyplot.subplots()
ax1.set_title('Ano do repositório')
ax1.boxplot(delta_array)
matplotlib.pyplot.show()

#RQ 04. Sistemas populares são atualizados com frequência?

today = date.today()
with open('data.csv', newline='') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
  next(spamreader)
  delta_array = []
  for row in spamreader:
    date_last_push = row[0].split(',')[2]
    split_string = date_last_push.split("T", 1)
    datetime_object = datetime.strptime(split_string[0], '%Y-%m-%d').date()
    delta = today - datetime_object  
    delta_array.append(delta.days)

fig1, ax1 = matplotlib.pyplot.subplots()
ax1.set_title('Atualização do repositório')
ax1.boxplot(delta_array)
matplotlib.pyplot.show()

# RQ 05. Sistemas populares são escritos nas linguagens mais populares?

famous_languages = ['JavaScript', 'Python', 'Java', 'TypeScript', 'C#', 'PHP', 'C++', 'Shell', 'C', 'Ruby']
with open('data.csv', newline='') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
  next(spamreader)
  is_famous_language_counter = 0
  is_not_famous_language_counter = 0
  for row in spamreader:
    language_name = row[0].split(',')[6]
    found = 0
    for idx, data in enumerate(famous_languages):
        if famous_languages[idx] == language_name:
           is_famous_language_counter += 1
           found = 1
           break
    if found == 0:
      is_not_famous_language_counter += 1


chart_label = ['Is famous language', 'Is NOT famous language']
chart_value = [is_famous_language_counter, is_not_famous_language_counter]

matplotlib.pyplot.pie(chart_value,labels = chart_label, autopct='%1.2f%%')
matplotlib.pyplot.show()

# RQ 06. Sistemas populares possuem um alto percentual de issues fechadas?

with open('data.csv', newline='') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
  next(spamreader)
  closed_issues_total = 0
  open_issues_total = 0
  total_issues = 0
  for row in spamreader:
    if not row [0]:
      continue
    open_issues = row[0].split(',')[7]
    closed_issues = row[0].split(',')[8]
    closed_issues_total += int(closed_issues)
    open_issues_total += int(open_issues)


chart_labels = ['Closed issues', 'Open issues']
chart_values = [closed_issues_total, open_issues_total]
matplotlib.pyplot.pie(chart_values, labels = chart_labels, autopct='%1.2f%%')
matplotlib.pyplot.show()
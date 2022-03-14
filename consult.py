import requests
import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime

api_token = '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'

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

# A simple function to use requests.post to make the API call. Note the json= section.


def run_query(query):
    request = requests.post('https://api.github.com/graphql',
                            json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, query))


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

header = ['name', 'createdAt', 'pushedAt', 'stargazers', 'pullRequests',
          'releases', 'primaryLanguage', 'open_issues', 'closed_issues']

f = open('data.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(header)
f.close()

query_result = run_query(query)  # Execute the query
#  print(query_result['data']['search']['edges'])

save_data_to_file(query_result['data']['search']['edges'])
end_cursor = '"' + \
    query_result['data']['search']['pageInfo']['endCursor'] + '"'
query = query.replace('null', end_cursor)
old_end_cursor = end_cursor

for x in range(1, 100):
    query_result = run_query(query)
    save_data_to_file(query_result['data']['search']['edges'])
    new_end_cursor = '"' + \
        query_result['data']['search']['pageInfo']['endCursor'] + '"'
    query = query.replace(old_end_cursor, new_end_cursor)
    old_end_cursor = new_end_cursor

dataframe = pd.DataFrame(index=header)
dataframe = pd.read_csv('data.csv')

total_pull_requests = dataframe['pullRequests']
#  print(total_pull_requests)


def mediana(dataframe):
    mediana_dataframe = dataframe.median()
    return mediana_dataframe


mediana_total_pull_requests = mediana(total_pull_requests)
print(f'A mediana total dos pull request eh: {mediana_total_pull_requests}')


def requisito_dois(dataframe):
    colunas_selecionadas = ['name', 'pullRequests']
    dataframe_com_name_pullRequests = dataframe.filter(
        items=colunas_selecionadas)
    return dataframe_com_name_pullRequests


rq_dois = requisito_dois(dataframe)
# print(rq_dois)


def plt_requisito_dois(dataframe):
    boxplot = dataframe.boxplot(column=['pullRequests'])
    boxplot.plot()
    return plt.show()


# plt_requisito_dois(rq_dois)


def requisito_tres(dataframe):
    colunas_selecionadas = ['name', 'releases']
    dataframe_com_name_realease = dataframe.filter(
        items=colunas_selecionadas)
    return dataframe_com_name_realease


rq_tres = requisito_tres(dataframe)
# print(rq_tres)


def plt_requisito_tres(dataframe):
    boxplot = dataframe.boxplot(column=['releases'])
    boxplot.plot()
    return plt.show()


total_release = dataframe['releases']
mediana_total_release = mediana(total_release)
print(f'A mediana total dos release eh: {mediana_total_release}')
# plt_requisito_tres(rq_tres)

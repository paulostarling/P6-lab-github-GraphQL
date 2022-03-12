import requests
import csv
import pandas as pd
import matplotlib.pyplot as plt

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
print(pd.read_csv('data.csv'))

# An example to get the remaining rate limit using the Github GraphQL API.

import requests
from datetime import datetime
from datetime import date


api_token = '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'

headers = {'Authorization': 'token %s' % api_token}

def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.
query = """
{
  search(query: "is:public stars:>100 sort:stars-desc", type: REPOSITORY, first: 100) {
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
        }
      }
    }
  }
}
"""

query_result = run_query(query) # Execute the query
print(query_result)
results = []
results.append(query_result['data']['search']['edges'])
end_cursor = '"' + query_result['data']['search']['pageInfo']['endCursor'] + '"'
for x in range(1,10):
  query = """
  {
    search(query: "is:public stars:>100 sort:stars-desc", after:""" + end_cursor + """, type: REPOSITORY, first: 100) {
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
            primaryLanguage {
              name
            }
          }
        }
      }
    }
  }
  """
  query_result = run_query(query)
  results.append(query_result['data']['search']['edges'])
  end_cursor = '"' + query_result['data']['search']['pageInfo']['endCursor'] + '"'

today = date.today()
total_days = 0
total_mr = 0
total_releases = 0
for result in results:
  for repository in result:
    # Calcula numero total de dias dos 1000 repos
    createdAt = repository['node']['createdAt']
    split_string = createdAt.split("T", 1)
    datetime_object = datetime.strptime(split_string[0], '%Y-%m-%d').date()
    delta = today - datetime_object
    total_days += delta.days

    # Calcula total de MR
    repository_mr_count = repository['node']['pullRequests']['totalCount']
    total_mr += repository_mr_count

    # Calcula total de releases
    repository_releases = repository['node']['releases']['totalCount']
    total_releases += repository_releases

media_anos = total_days/360/1000
media_mr = total_mr/1000
media_total_releases = total_releases/1000
print('Media de anos dos repos', media_anos)
print('Media de merge requests aceitos', media_mr)
print('Media total de releases', media_total_releases)
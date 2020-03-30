import os

from dotenv import load_dotenv
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

# Change this variable for different components
COMPONENT = 'fft'

if __name__ == "__main__":
    load_dotenv()

    sample_transport = RequestsHTTPTransport(
        url='https://api.github.com/graphql',
        use_json=True,
        headers={
            'Authorization': 'bearer ' + os.getenv("GITHUB_ACCESS_TOKEN"),
        },
        verify=False
    )

    client = Client(
        transport=sample_transport,
        fetch_schema_from_transport=True,
    )

    queryString = """
{
  repository(owner: "numpy", name: "numpy") {
    pullRequests(states: MERGED, last: 100, labels: "component: numpy.""" + COMPONENT + """") {
      edges {
        node {
          title
          mergedBy {
            login
          }
          comments(first: 100) {
            edges {
              node {
                author {
                  login
                }
              }
            }
          }
          participants(first: 100) {
            totalCount
            edges {
              node {
                login
              }
            }
          }
        }
      }
    }
  }
}
"""
    print(queryString)

    query = gql(queryString)

    res = client.execute(query)

    PRDict = res['repository']['pullRequests']['edges']

    commentAuthorDict = {}

    for PR in PRDict:
        for comment in PR['node']['comments']['edges']:
            comment_author = comment['node']['author']['login']
            if comment_author not in commentAuthorDict.keys():
                commentAuthorDict[comment_author] = 1
            else:
                commentAuthorDict[comment_author] += 1

    print(res)

    print(commentAuthorDict)

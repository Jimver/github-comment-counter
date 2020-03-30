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
    query = gql('''
{
  repository(owner: "numpy", name: "numpy") {
    pullRequests(states: MERGED, last: 100, labels: "component: numpy.{component}") {
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


    '''.format(component=COMPONENT))

    res = client.execute(query)

    print(res)

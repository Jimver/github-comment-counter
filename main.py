import csv
import os

import click
from dotenv import load_dotenv
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from collections import Counter, Set


# Get a dictionary of (github username, count) pairs with count the amount of comments of that user in pull requests
# with the given label with the given graphQL client.
def getPRCommentCount(client, repo_name, repo_owner, label):
    queryString = """
        {
          repository(owner: \"""" + repo_owner + """", name: \"""" + repo_name + """") {
            pullRequests(states: MERGED, last: 100, labels: \"""" + label + """") {
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
    query = gql(queryString)
    res = client.execute(query)

    PRList = res['repository']['pullRequests']['edges']
    PRcommentAuthorDict = Counter()
    for PR in PRList:
        for comment in PR['node']['comments']['edges']:
            comment_author = comment['node']['author']['login']
            if comment_author not in PRcommentAuthorDict.keys():
                PRcommentAuthorDict[comment_author] = 1
            else:
                PRcommentAuthorDict[comment_author] += 1
    return PRcommentAuthorDict


# Return a dict of (github username, count) key value pairs for where count is the amount of comments that user posted
# on issues with label 'label' with the given graphQL client.
def getIssueCommentCount(client, repo_name, repo_owner, label):
    queryString = """
        {
          repository(name: \"""" + repo_name + """", owner: \"""" + repo_owner + """") {
            id
            issues(orderBy: {field: CREATED_AT, direction: ASC}, last: 100, labels: \"""" + label + """") {
              edges {
                node {
                  title
                  createdAt
                  comments(first: 100) {
                    edges {
                      node {
                        author {
                          login
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
    """
    query = gql(queryString)
    res = client.execute(query)

    IssueList = res['repository']['issues']['edges']
    IssueCommentDict = Counter()
    for issue in IssueList:
        comments = issue['node']['comments']['edges']
        for comment in comments:
            comment_author = comment['node']['author']['login']
            if comment_author not in IssueCommentDict.keys():
                IssueCommentDict[comment_author] = 1
            else:
                IssueCommentDict[comment_author] += 1
    return IssueCommentDict


@click.command()
@click.option("--repo_name", "-n", prompt="Name of the repository", help="The name of the repository to analyse",
              required=True)
@click.option("--repo_owner", "-o", prompt="Owner of the repository", help="The owner of the repository to analyse",
              required=True)
@click.option("--label", "-l", multiple=True, prompt="The label to filter on in the pull requests/issues",
              help="The label(s) to filter on in the pull requests/issues", default=[])
@click.option("--issues/--no-issues", "-i/-ni", default=True, prompt="Whether to include issue comments or not",
              help="Whether to include issue comments in the analysis")
@click.option("--pull_requests/--no-pull_requests", "-p/-np", default=True,
              prompt="Whether to include pull request comments or not",
              help="Whether to include pull request comments in the analysis")
def main_method(repo_name, repo_owner, label, issues, pull_requests):
    load_dotenv()

    labels = list(label)

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

    PR_And_Issue_Counts = []

    authors = set()

    label_num = len(labels)
    for i in range(0, label_num):
        PR_And_Issue_Count = Counter()
        if pull_requests:
            PRCommentCount = getPRCommentCount(client, repo_name, repo_owner, labels[i])
            PR_And_Issue_Count += PRCommentCount
            click.echo("Following dict is PR comment count for label: " + labels[i])
            click.echo(PRCommentCount)
        if issues:
            IssueCommentCount = getIssueCommentCount(client, repo_name, repo_owner, labels[i])
            PR_And_Issue_Count += IssueCommentCount
            click.echo("Following dict is issue comment count for label: " + labels[i])
            click.echo(IssueCommentCount)
        PR_And_Issue_Counts.append(PR_And_Issue_Count)
        for author in PR_And_Issue_Count.keys():
            authors.add(author)
        click.echo("Following dict is total comments combined for label: " + labels[i])
        click.echo(PR_And_Issue_Count)

    csv_header = ['username'] + labels
    csv_rows = []

    for author in authors:
        csv_row = [author]
        for i in range(0, label_num):
            csv_row.append(PR_And_Issue_Counts[i][author])
        csv_rows.append(csv_row)

    with open("result.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
        writer.writerows(csv_rows)
        f.flush()

    click.echo(csv_rows)


if __name__ == "__main__":
    main_method()

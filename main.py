from gql import gql, Client
from graphql import build_ast_schema, parse
from dotenv import load_dotenv

load_dotenv()

with open('path/to/schema.graphql') as source:
    document = parse(source.read())

schema = build_ast_schema(document)

client = Client(schema=schema, headers={'Authorization': os.getenv("GITHUB_ACCESS_TOKEN")})
query = gql('''
    {
      hello
    }
''')

client.execute(query)

if __name__ == "__main__":


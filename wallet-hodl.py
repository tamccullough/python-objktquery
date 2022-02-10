#!/usr/bin/env python
# twitter->@tamccullough

import json
import pandas as pd
import re
from gql import gql, Client

from gql.transport.requests import RequestsHTTPTransport

_transport = RequestsHTTPTransport(
    url='https://api.objkt.com/v1/graphql',
    use_json=True,
)

client = Client(
    transport=_transport,
    fetch_schema_from_transport=True,
)

# using user input
#***************************
wallet = input('enter the wallet of the creator: ')#'tz1gE27FWHXzisp1SgkuupZ44g4t8mETafMG'
value = input('enter the query (ex."Basqunks %"): ')#'Who Needs the Moon 8'
amount = input('enter the minimum number of tokens to own: ')#'1'

# or alternatively enter something statically and simply double click the .py file
#wallet = 'tz1gE27FWHXzisp1SgkuupZ44g4t8mETafMG'
#value = 'Who Needs the Moon 8'
#amount = '1'

query = gql (
    '''
    query GetFod {
      token(where: {creator_id: {_eq: "'''+wallet+'''"},
      title: {_ilike: "'''+value+'''"}}) {
        id
        creator_id
        title
        token_holders(where: {quantity: {_gte: "'''+amount+'''"}}) {
          holder_id
          quantity
        }
        metadata
      }
    }
    '''
)

tokens = client.execute(query)['token']

a = []
t = 0
for k in tokens:
    for i in k['token_holders']:
        if i['quantity'] > 0:
            if i['holder_id'] in ['KT1HbQepzV1nVGg8QVznG7z4RcHseD5kwqBn','tz1burnburnburnburnburnburnburjAYjjX','KT1FvqJwEDWb1Gwc55Jd1jjTHRVWbYKUUpyq']:
                pass
            else:
                num = i['quantity']
                while num > 0:
                    a.append(i['holder_id'])
                    num-=1
                    t+=1

df = pd.DataFrame(a,columns=['wallet'])
print(df)
df.to_csv('wallets.csv',index=False,header=False)

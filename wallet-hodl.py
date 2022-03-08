#!/usr/bin/env python
# twitter->@tamccullough

import json
import pandas as pd
import re
from gql import gql, Client

from gql.transport.requests import RequestsHTTPTransport

_transport = RequestsHTTPTransport(
    # old url='https://api.objkt.com/v1/graphql',
    url='https://api.objkt.com/v2/graphql',
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
    query MyQuery {
      token(where: {creators: {creator_address: {_eq: "'''+wallet+'''"}}, name: {_ilike: "%'''+value+'''%"}}) {
        token_id
        name
        holders(where: {quantity: {_gte: "'''+amount+'''"}}) {
          holder_address
          quantity
        }
        supply
        lowest_ask
      }
    }
    '''
)

tokens = client.execute(query)['token']

a,b,c = [],[],[]
for k in tokens:
    for i in k['holders']:
        if i['quantity'] > 0:
            if i['holder_address'] in ['tz1gE27FWHXzisp1SgkuupZ44g4t8mETafMG','tz1XQ7QFCbNZiv6efCyLKhcfyQA4pG54jaoT','KT1HbQepzV1nVGg8QVznG7z4RcHseD5kwqBn','tz1burnburnburnburnburnburnburjAYjjX','KT1FvqJwEDWb1Gwc55Jd1jjTHRVWbYKUUpyq']:
                pass
            else:
                num = i['quantity']
                while num > 0:
                    a.append(i['holder_address'])
                    b.append(k['name'])
                    num-=1
                if k['lowest_ask']:
                    c.append(k['lowest_ask']/1000000)
                else:
                    c.append(0)

df = pd.DataFrame(a,columns=['wallet'])
df['title'] = b
df['price'] = c
print(df)
df.to_csv('wallets.csv',index=False,header=False)

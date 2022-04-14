#!/usr/bin/env python
# twitter->@tamccullough

import json
import pandas as pd
import re
from gql import gql, Client

from gql.transport.requests import RequestsHTTPTransport

_transport = RequestsHTTPTransport(
    url='https://data.objkt.com/v2/graphql',
    use_json=True,
)

client = Client(
    transport=_transport,
    fetch_schema_from_transport=True,
)

# using user input
#***************************
wallet = input('enter the wallet of the creator: ')#'tz1gE27FWHXzisp1SgkuupZ44g4t8mETafMG'
query = input('enter the query (ex."Basqunks %"): ')#'Who Needs the Moon 8'
amount = input('enter the minimum number of tokens to own: ')#'1'
skipped_wallets = ['KT1HbQepzV1nVGg8QVznG7z4RcHseD5kwqBn','tz1burnburnburnburnburnburnburjAYjjX','KT1FvqJwEDWb1Gwc55Jd1jjTHRVWbYKUUpyq']
skipped_wallets.append(wallet)

# or alternatively enter something statically and simply double click the .py file
#wallet = 'tz1gE27FWHXzisp1SgkuupZ44g4t8mETafMG'
#value = 'Who Needs the Moon 8'
#amount = '1'

query = gql (
    '''
    query MyQuery {
              token(where: {creators: {creator_address: {_eq: "'''+wallet+'''"}}, name: {_ilike: "%'''+query+'''%"}}) {
                name
                lowest_ask
                holders(where: {quantity: {_gte: "'''+amount+'''"}}) {
                  holder_address
                  quantity
                }
              }
            }
    '''
)

tokens = client.execute(query)['token']

a,b,c = [],[],[]
for keys in tokens:
        for key in keys['holders']:
            if key['quantity'] > 0:
                if key['holder_address'] in skipped_wallets:
                    pass
                else:
                    num = key['quantity']
                    while num > 0:
                        a.append(key['holder_address'])
                        b.append(keys['name'])
                        if keys['lowest_ask']:
                            c.append(keys['lowest_ask']/1000000)
                        else:
                            c.append(0)
                        num-=1

df = pd.DataFrame(a,columns=['wallet'])
df['name'] = b
df['price'] = c
print(df)
df.to_csv('wallets.csv',index=False,header=False)

'''
    Making 100 times HTTP request and save the response to Mongo DB .
    This file takes number of http request to https://httpbin.org/uuid and get a random uuid which later save into mongo db.
'''
import asyncio
from aiohttp import ClientSession
from mongoengine import Document,StringField,connect # driver for cooncet python to mongodb

connect("database_name")

# connect(  # mongodb database connection by URI
#     db="DATABASE_NAME",
#     username=DATABASE_USERNAME',
#     password='DATABASE_PASSWORD',
#     host='DATABASE_HOST'
# )
url = "https://httpbin.org/uuid"

class RandomData(Document):
    '''
    Mongo db collection creation
    '''
    uuid = StringField(required=True)


async def save_data_to_db(data) -> None: 
    '''
    save the fetched data from url to the database
    params :
        data : unique identifier
    returns:
        None
    '''
    RandomData(uuid=data).save()

async def fetch_data(session,url) -> None:
    '''
    fetch the data from the url
    params :
        session : aiohttp client session
        url : URL
    returns:
        None
    '''
    async with session.get(url) as response:
        json_response = await response.json()
        await save_data_to_db(json_response['uuid'])

async def main() -> None:
    async with ClientSession() as session:
        tasks = [fetch_data(session,url) for _ in range(100)] # 100 times http request. 
        await asyncio.gather(*tasks)



if __name__ == "__main__":
    asyncio.run(main())
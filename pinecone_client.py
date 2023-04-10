from pinecone.core import Client
from pinecone.exceptions import PineconeException

pinecone_api_key = 'YOUR_API_KEY_HERE'
pinecone_index_name = 'YOUR_INDEX_NAME_HERE'
pinecone_client = Client(api_key=pinecone_api_key)

try:
    pinecone_index = pinecone_client.create_index(index_name=pinecone_index_name)
except PineconeException as e:
    if e.status == 409:
        pinecone_index = pinecone_client.index(index_name=pinecone_index_name)
    else:
        raise e

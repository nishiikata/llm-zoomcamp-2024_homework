from datetime import datetime
from typing import Dict, List, Tuple, Union

import numpy as np
from elasticsearch import Elasticsearch

from mage_ai.data_preparation.variable_manager import set_global_variable

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def elasticsearch(
    documents: List[Dict[str, Union[Dict, List[int], np.ndarray, str]]], *args, **kwargs,
) -> str:
    """
    Exports document data to an Elasticsearch database.
    """

    connection_string = kwargs.get('connection_string', 'http://localhost:9200')
    
    # First, let's change the line where we read the index name:
    index_name = kwargs.get('index_name', 'documents')
    # To index_name_prefix - we will parametrize it with the day and time we run the pipeline
    index_name_prefix = kwargs.get('index_name', 'documents')
    current_time = datetime.now().strftime("%Y%m%d_%M%S")
    index_name = f"{index_name_prefix}_{current_time}"
    print("index name:", index_name)
    # We will need to save the name in a global variable, so it can be accessible in other code blocks
    set_global_variable("llm_zoomcamp_hw5", 'index_name', index_name)
    
    
    number_of_shards = kwargs.get('number_of_shards', 1)
    number_of_replicas = kwargs.get('number_of_replicas', 0)
    vector_column_name = kwargs.get('vector_column_name', 'embedding')

    dimensions = kwargs.get('dimensions')
    if dimensions is None and len(documents) > 0:
        document = documents[0]
        dimensions = len(document.get(vector_column_name) or [])

    es_client = Elasticsearch(connection_string)

    print(f'Connecting to Elasticsearch at {connection_string}')

    # index_settings = dict(
    #     settings=dict(
    #         number_of_shards=number_of_shards,
    #         number_of_replicas=number_of_replicas,
    #     ),
    #     mappings=dict(
    #         properties=dict(
    #             chunk=dict(type='text'),
    #             document_id=dict(type='text'),
    #             embedding=dict(type='dense_vector', dims=dimensions),
    #         ),
    #     ),
    # )
    #
    # Replace index settings with the settings we used previously:
    index_settings = {
        "settings": {
            "number_of_shards": number_of_shards,
            "number_of_replicas": number_of_replicas
        },
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "section": {"type": "text"},
                "question": {"type": "text"},
                "course": {"type": "keyword"},
                "document_id": {"type": "keyword"}
            }
        }
    }

    if not es_client.indices.exists(index=index_name):
        es_client.indices.create(index=index_name)
        print('Index created with properties:', index_settings)
        print('Embedding dimensions:', dimensions)

    print(f'Indexing {len(documents)} documents to Elasticsearch index {index_name}')
    for document in documents:
        print(f'Indexing document {document["document_id"]}')

        # Remove the embeddings line:
        # if isinstance(document[vector_column_name], np.ndarray):
        #     document[vector_column_name] = document[vector_column_name].tolist()

        es_client.index(index=index_name, document=document)
    
    print(document)

    print("Q4 Answer: The last document id is {}".format(document["document_id"]))

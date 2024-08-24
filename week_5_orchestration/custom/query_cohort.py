from elasticsearch import Elasticsearch

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def query_cohort(*args, **kwargs):
    connection_string = kwargs.get('connection_string', 'http://localhost:9200')
    index_name = kwargs.get("index_name")

    es_client = Elasticsearch(connection_string)

    search_results = elastic_search(
        query="When is the next cohort?",
        es_client=es_client,
        index_name=index_name,
    )

    print("\n\nSearch results:")
    for idx, item in enumerate(search_results):
        print(idx, item, "\n")

    print(f"Using index_name {index_name}")
    print("Q5 Answer: The ID of the top matching result is {}".format(search_results[0]["document_id"]))


    return search_results


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'


def elastic_search(
    query: str,
    es_client: "Elasticsearch",
    index_name: str,
):
    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields"
                    }
                },
                # "filter": {
                #     "term": {
                #         "course": "data-engineering-zoomcamp"
                #     }
                # }
            }
        }
    }

    response = es_client.search(index=index_name, body=search_query)
    
    result_docs = []
    
    for hit in response['hits']['hits']:
        result_docs.append(hit['_source'])
    
    return result_docs

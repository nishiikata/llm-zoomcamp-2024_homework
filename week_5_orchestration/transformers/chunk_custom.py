import hashlib

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data: list[dict] | dict, *args, **kwargs):
    if type(data) is dict:
        data = [data]

    documents = []

    for course_dict in data:
        for doc in course_dict["documents"]:
            doc['course'] = course_dict['course']
            # previously we used just "id" for document ID
            doc['document_id'] = generate_document_id(doc)
            documents.append(doc)

    print("Q3 Answer: There were {} documents (chunks) in the output".format(len(documents)))
    return documents


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'


def generate_document_id(doc):
    combined = f"{doc['course']}-{doc['question']}-{doc['text'][:10]}"
    hash_object = hashlib.md5(combined.encode())
    hash_hex = hash_object.hexdigest()
    document_id = hash_hex[:8]
    return document_id
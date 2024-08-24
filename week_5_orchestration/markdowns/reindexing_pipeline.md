# reindexing_pipeline

## Notes for Q6. Reindexing

You can run the entire pipeline with different LLM FAQ version ids using the terminal.

To run the pipeline with the version 1 google docs id:
```bash
mage run llm llm_zoomcamp_hw5 --runtime-vars '{"connection_string": "http://elasticsearch:9200", "google_docs_id": "1qZjwHkvP0lXHiE4zdbWyUXSVfmVGzougDD6N37bat3E"}'
```

To run the pipeline with the version 1 google docs id:
(This is required in order to solve Q6. Reindexing)
```bash
mage run llm llm_zoomcamp_hw5 --runtime-vars '{"connection_string": "http://elasticsearch:9200", "google_docs_id": "1T3MdwUvqCL3jrh3d3VCXQ8xE0UqRzI3bfgpfBq3ZWG0"}'
```

For the v1 document the answer should be:
Q5 Answer: The ID of the top matching result is bf024675

For the v2 document the answer should be:
Q5 Answer: The ID of the top matching result is b6fa77f3

Note:
The v2 command might require a second rerun or a restart of the mage instance in order to work properly.
Elasticsearch might try to recycle the index used for the v1 command run instead of creating a new index meant for the v2 command run.
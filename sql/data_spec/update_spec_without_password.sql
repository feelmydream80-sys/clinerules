UPDATE tb_data_spec
SET data_name = %s,
    description = %s,
    api_url = %s,
    provider = %s,
    keywords = %s,
    reference_doc_url = %s,
    updated_at = CURRENT_TIMESTAMP
WHERE id = %s;

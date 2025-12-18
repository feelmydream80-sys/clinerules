SELECT id, data_name, description, api_url, provider, keywords, reference_doc_url, created_at, updated_at, password
FROM tb_data_spec
WHERE id = %s;

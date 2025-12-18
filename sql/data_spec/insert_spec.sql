INSERT INTO tb_data_spec (data_name, description, api_url, provider, keywords, reference_doc_url, password)
VALUES (%s, %s, %s, %s, %s, %s, %s)
RETURNING id;

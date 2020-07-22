from google.cloud import bigquery
from google.oauth2 import service_account

def entries_to_remove(entries, the_dict):
    for key in entries:
        if key in the_dict:
            the_dict.pop(key)
            
def insert_rows_to_tables(credentials,
                          project_id,
                          dataset_id,
                          table_id,
                          insert_rows):
    '''
    insert_rows has to be a list of tuples.
    '''
    # Instantiates a client
    bigquery_client = bigquery.Client(credentials= credentials,project=project_id)

    query = f"""
            INSERT INTO {DATASET_ID}.{TABLE_ID}
            VALUES {insert_rows}
            """

    query_job = client.query(query)

def insert_rows_to_tables_new(credentials,
                          project_id,
                          dataset_id,
                          table_id,
                          insert_rows):
    '''
    insert_rows has to be a list of tuples.
    '''
    # Instantiates a client
    bigquery_client = bigquery.Client(credentials= credentials,project=project_id)

    # Prepares a reference to the dataset
    dataset_ref = bigquery_client.dataset(dataset_id)

    table_ref = dataset_ref.table(table_id)
    table = bigquery_client.get_table(table_ref)  # API call

    rows_to_insert = insert_rows
    errors = bigquery_client.insert_rows(table, rows_to_insert)  # API request
    assert errors == []
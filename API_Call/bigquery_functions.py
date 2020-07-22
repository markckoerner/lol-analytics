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
    client = bigquery.Client(credentials= credentials,project=project_id)

    query = f"""
            INSERT INTO {dataset_id}.{table_id}
            VALUES {insert_rows}
            """

    query_job = client.query(query)

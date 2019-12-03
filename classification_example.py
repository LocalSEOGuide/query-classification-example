
# coding: utf-8

# In[ ]:


import pandas as pd
from pandas.io import gbq
import gspread as gs # library used to work with gsheets
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

# GBQ query to get unique terms from the query database
term_query = "SELECT distinct(query) FROM `{project_id}.google_reporting_data.gsc_mom_query`"

# gets query data into a dataframe with 1 column labeled 'query'
query_data = pd.read_gbq(term_query, project_id='{project_id}', dialect='standard')

rubric_gsheet_id = '{sheet_id_from_gsheets}' # ID for rubric used to categorize results

def auth_with_gsheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gs.authorize(creds)
    return(client)

def get_rubric_dataframe(rubric_gsheet_id): 
    # spreadsheet with a row of headers as the categories and the associated columns with strings related to that category
    gc = auth_with_gsheets()
    workbook = gc.open_by_key(rubric_gsheet_id)
    sh = workbook.worksheet('classification_rubric') # create a sheet object
    dataframe = get_as_dataframe(sh).fillna(0) # fill blank values with '0'
    
    return(dataframe)

rubric_df = get_rubric_dataframe().astype(str) # get the rubric DF we'll use to clasify the queries

rubric_dict = {} # get the rubric DF into a dict
for column in rubric_df.columns:
    rubric_dict.update({column : rubric_df[column][rubric_df[column] != '0'].to_list()}) # removes NA results, creates a list
    
    
def categorize_item(text_string):
    cat_list = list() # initiate the output list

    for key in rubric_dict: # check the string based on the rubric dict
        if any(x in text_string for x in rubric_dict[key]) == True:
            cat_list.append(str(key))
            
    return(cat_list)

# categorize the queries
query_data['categories'] = query_data['query'].apply(lambda x: categorize_item(x)) 

# get the number of categories identified for each query
query_data['cat_len'] = query_data['categories'].apply(lambda x: len(x)) 

# drop uncategorized items
query_data = query_data[query_data.cat_len > 0].reset_index(drop=True) 

# explode the category list into invidual rows for queries with multiple categories
query_data = query_data[['query', 'categories']].explode('categories').reset_index(drop=True)

# outputs the data
query_data.to_csv('output_data.csv')


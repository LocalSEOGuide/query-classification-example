# Query Classification Example
This is an example script that uses a gsheet with a header row of categories, with each associated column comprised of strings associated with that 'category' with the sheet named 'classification_rubric'.  

## Example of Rubric Gsheet:
category 1 | category 2 | category 3 | ... | category 999
-----------|------------|------------|-----|----------------
cat-1 string | cat-2 string | cat-3 string | ... | cat-999 string

By default it pulls from Google Big Query to get the query list, but this can easily be changed to a simple csv using pandas `pd.read_csv('csv_name.csv')` with a single column labeled 'query'. 

With the output of this script you can then join on your query data to classify all the terms that have a classification, once you've fed the output into a GBQ table. 

## Example: 

        WITH classification_data as (
          SELECT 
            query as r_query,
            categories
          FROM `{project_id}.query_classification.raw_classification_data`)
        SELECT
          query,
          clicks,
          impressions,
          ctr, 
          position,
          month_pulled,
          location,
          categories
        FROM `{project_id}.google_reporting_data.gsc_mom_query`
        JOIN classification_data ON r_query = query

If you've got a GBQ table of query data already you'll need to update `{project_id}` to your project ID and associated table name. If you've got questions please feel free to reach out to [@hecklerponics](https://twitter.com/hecklerponics) on Twitter. 

Happy classifying! 

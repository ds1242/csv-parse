# CSV Parsing 
This takes a command line argument path to the csv file.  It should check that it is a valid pathway.  If the path is valid it will then transfer the data into a sqlite db table.  If it the first script was successful it will execute the second script and start a Flask server at http://127.0.0.1:5000.  At the endpoint /batch_jobs it will actually display all of the data.  Refer to the API response section below for filtering of the data.  

#### Example Data

The example batch job record dataset is contained in this repo in the `example_batch_records.csv` file.

Each batch job record occupies one line of the file, and each line contains up to (3) comma-delimited attributes for the record, in this order:

  * `batch_number` (*integer*) - A number assigned to the batch job by the batch scheduler
  * `submitted_at` (*ISO 8601 datetime*) - The time the batch job was submitted
  * `nodes_used` (*integer*) - The number of nodes the batch job used

The data are well-formatted, but some attribute values could be missing entirely.

#### API Endpoint:

`GET http://localhost/batch_jobs`

#### API Endpoint Filtering

`GET http://localhost/batch_jobs?filter[submitted_after]='2018-02-28T15:00:00+00:00'&filter[submitted_before]='2018-03-01T15:00:00+00:00'&filter[min_nodes]=2&filter[max_nodes]=20`

#### API Response

The expected response is a [JSON-API](http://jsonapi.org/format/#fetching-resources) document (string) representing an array of objects, one object per record. For example, parsing the API response string should yield something like:

```
{
  "links": {
    "self": "http://localhost/batch_jobs?filter[max_nodes]=20"
  },
  "data": [
    { "type": "batch_jobs",
      "id": "1",
      "attributes": {
        "batch_number": 945,
        "submitted_at": "2018-03-30T15:00:00+00:00",
        "nodes_used": 8
      }
    }, {
      "type": "batch_jobs",
      "id": "2",
      "attributes": {
        "batch_number": 946,
        "submitted_at": "2018-03-30T15:07:01+00:00",
        "nodes_used": 20
      }
    }, ...
  ]
}
```

All filter parameters are optional. All filters should be inclusive (e.g. `filter[min_nodes]=2&filter[max_nodes]=4` should return records that used 2, 3, or 4 nodes).

#### Filter Keywords

  * `[submitted_after]=` (*ISO 8601 datetime*) - return only records submitted on or after the given date
  * `[submitted_before]=` (*ISO 8601 datetime*) - return only records submitted on or before the given date
  * `[min_nodes]=` (*integer*) - return only records that used at least the given number of nodes
  * `[max_nodes]=` (*integer*) - return only records that used at most the given number of nodes
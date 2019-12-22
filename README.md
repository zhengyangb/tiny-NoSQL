# tiny NoSQL
A tiny implementation of NoSQL database with RESTful API support.

## Install

## Getting Started

### Python Interface

```
from nosql import Database
```
**Database**
- **Create a database**: `db = Database('./YOUR_DATABASE_DIRECTORY/')`
- **Show collections in database**: `db.show_collections()`
- **Create a new collection**: `db.create_collection(NEW_NAME)`
- **Get the collection object from a database**: `col = db.get_collection(NAME)`
  - Alternatively, you can also call a collection as an attribute. For example, `db.main` will return the collection with name `main`.
- **Delete a collection from a database**: `db.drop_collection(NAME)` 
- **Close and save database**: `db.close()`

**Collection**
- **Return all documents from collection**: `col.all()`
- **CRUD Operations**: Please see CRUD section

### RESTful API

Start the nosql.py with corresponding argument. By default the database will run on `localhost:9020`, and the examples below are based on this.

## CRUD Operations

Suppose there exists a collection named `fruits`.

### Insert New Documents


<table>

<tr><td>Python</td><td><code>col.insert({'type':'banana', 'price': 10})</code></td>
</tr>

<tr><td>RESTful</td><td>
<code>curl -X "POST" "http://localhost:9020/fruits/_insert?type=banana&price=10"</code>
</td></tr>

<tr><td>RESTful <sub>JSON</sub></td><td><pre><code>
curl -X "POST" "http://localhost:9020/fruits/_insert" \
     -H 'Content-Type: application/json' \
     -d $'{
  "type": "banana",
  "price": 10
}'
</code></pre>
</td>
</tr>
</table>

Supported document types: a JSON object or Python dictionary is acceptable. The valid types include float, integer, string and nested array or object.


### Find all

To retrieve all documents in a collection. 

<table>

<tr><td>Python</td><td><code>col.all()</code></td>
</tr>

<tr><td>RESTful</td><td>
<code>
curl "http://localhost:9020/fruits/_all"
</code></td></tr>
</table>





### Find with document ID
A UUID-format document ID will be generated every time a document is inserted. The document ID will be returned after the insertion. 
<table>

<tr><td>Python</td><td><code>col.find({'_id': DOC_ID})</code></td>
</tr>

<tr><td>RESTful</td><td>
<code>
curl "http://localhost:9020/fruits/DOC_ID"
</code></td></tr>

<tr><td>RESTful <sub>JSON</sub></td><td><pre>
<code>
curl "http://localhost:9020/fruits/_find" \
     -H 'Content-Type: application/json' \
     -d $'{
  "_id": "DOC_ID"
}'
</code></pre>
</td>
</tr>

</table>

### Find with criterion

<table>
<tr><td>Python</td><td><code>col.find({'type': 'banana'})</code></td>
</tr>

<tr><td>RESTful</td><td>
<code>curl "http://localhost:9020/fruits/_find?type=banana"</code>
</td></tr>

<tr><td></td><td></td>
</tr>

<tr><td>RESTful <sub>JSON</sub></td><td><pre>
<code>curl "http://localhost:9020/fruits/_find" 
     -H 'Content-Type: application/json' 
     -d $'{
  "type": "banana"
}'
</code></pre>
</td>
</tr>
</table>

### Supported query criteria
The query criteria must be a query string, JSON object, or Python dictionary. Below are examples of JSON object criteria.
* `_id`: UUID string. Specify document id to find the exact document.
* Equal: Use field/value pair to find all documents with field matching the value.
* Contain: Use field/value pair to find all documents with lists containing the value.
    * e.g. `{"type": "orange", "taste": ["sweet", "sour"]}` will be matched with criterion `{"taste": "sweet"}`
* Advanced search
    * `_eq`: equal. E.g. `{"_eq": {"taste": "sour"}}` will only match documents with taste equal to sour.
    * `_lt`, `_le`: less than, less or equal to.
    * `_gt`, `_ge`: greater than, greater or equal to. 
    * `_ne`: not equal to.
    * `_in`: is in.
    * `_nin`: is not in.

### Update with criterion
For example, if you want to add 1 dollars to all products with price lower than 10 dollars, this contains a query (find all documents with price <10), and an update operation (increase price by 1 ).
The JSON needs to contain to object: `"criteria"` and `"operation"`.

<table>
<tr><td>Python</td><td><code>col.update({"price":{"_lt":100}}, {"_increment": ["price"]})</code></td>
</tr>

<tr><td>RESTful <sub>JSON</sub></td><td><pre>
<code>
curl -X "PUT" "http://localhost:9020/fruits/_update" \
     -H 'Content-Type: application/json' \
     -d $'{
  "operation": {
    "_increment": [
      "price"
    ]
  },
  "criteria": {
    "price": {
      "_lt": 10
    }
  }
}'
</code></pre>
</td>
</tr>
</table>
It will return a list of document id of all documents updated. You can also update a sepecific document by using document id as the criteria.

#### Supported Update Operations
* `_set`: key/value paris of fields to update and new values
* `_unset`: list of fields to be deleted
* `_increment`: list of fields to increase by one. Need to be numeric values. 
* `_append`: key/value paris of fields and values to be appended

### Remove documents

<table>
<tr><td>Python</td><td><code>col.remove({'type': 'banana'})</code></td>
</tr>

<tr><td>RESTful</td><td>
<code>curl -X "DELETE" "http://localhost:9020/fruits/_remove?type=banana"</code>
</td></tr>

<tr><td></td><td></td>
</tr>

<tr><td>RESTful <sub>JSON</sub></td><td><pre>
<code>curl -X "DELETE" "http://localhost:9020/fruits/_remove" \
     -H 'Content-Type: application/json' \
     -d $'{
  "operation": {
    "_increment": [
      "price"
    ]
  },
  "criteria": {
    "price": {
      "_lt": 100
    }
  }
}'

</code></pre>
</td>
</tr>
</table>

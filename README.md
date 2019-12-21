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

### Find all

To retrieve all documents in a collection.

|      |      |
| ---- | ---- |
|  Python |    `col.all()`  |
|    RESTful (Parameters)|  `curl`  |
| RESTful (JSON)  |  GET `localhost:9020/fruits/_all` ```asd```  |


### Find with document ID

<table>
<thead><td></td><td></td></thead>

<tr><td>Python</td><td><code>col.find({'_id': DOC_ID})</code></td>
</tr>

<tr><td></td><td></td>
</tr>

<tr><td></td><td></td>
</tr>

<tr><td>RESTful</td><td>
<code>
curl "http://localhost:9020/fruits/DOC_ID"
</code>
</td>
</tr>
</table>

### Find with criterion

<table>
<thead><td></td><td></td></thead>

<tr><td>Python</td><td><code>col.find({'type': 'banana'})</code></td>
</tr>

<tr><td>RESTful</td><td>
<code>curl "http://localhost:9020/fruits/_find?type=banana"</code>
</td></tr>

<tr><td></td><td></td>
</tr>

<tr><td>RESTful</td><td>
<code>curl "http://localhost:9020/fruits/_find" 
     -H 'Content-Type: application/json' 
     -d $'{
  "type": "banana"
}'
</code>
</td>
</tr>
</table>




# TODO

-[x] Database and Table modules
-[ ] Cache
-[x] RESTful
-[ ] Publish
-[ ] JavaScript Module
-[ ] Index

## Reference


# Ronin Finances BI

Glueing together Python, Postgres, and Metabase.

## Setup

Don't forget to delete `postgres-data/` if you want to wipe everything and start fresh.



## Questions

- Transform data from multiple sources into a single source

- Idempotent ingestion of data from sources

  Fetch by month:
    1. Drop all data from that month from that source
    2. Re-import data
    3. Re-clean/transform data

- Data model? What should a raw[_umcu]_transaction -> transaction flow look like? What's the end goal data model?
```yml
Transaction:
  id: int
  account: str (or id)
  person: str (or id)
  amount: num
  new_balance: num
  date: datetime
  description:  # str
    second_party: str
    
```


## Plan


### 0. Workflow or Orchestrate
Apache Airflow to schedule these as discrete steps
Or just run them manually for now.


### 1. Scrape Transactions
Will need custom scrapers for each source.
End result will either be in-memory data, JSON, or CSV.


### 2. Unify Transactions
Translate data into a common format.
Must determine specification of data model.

```csv
# Transaction Sources
Id, SourceName, AccountName, Account#, AccountType
```

```csv
# Transactions
Id, SourceId, Date, Description, Amount, Balance, Note, Raw_Description, CategoryId
```

```csv
# Category
Id, ParentCategoryId, Name
```


#### 2a. Clean Transactions
If the input data has extra jargon, try to remove the noise here.
<ul>
  <details>
    <summary>
    For Example: "Purchase TST* QUARANTINOS 555-555-5555 MI Date 05/06/24 12345678901234567890123 5555 %% Card 52 #4321 MEMO Balance Change -$37.48"...
    </summary>

    ...Should be reduced to something like "Purchase TST* QUARANTINOS 555-555-5555 MI"

    * Date is already tracked in `"Date"` column
    * Long numbers are not relevant (What are they?)
    * Card Info should not be duplicated on each transaction.
      * This info could be stored more efficiently in a separate account/card info table.
    * Balance Change is already tracked in `"Amount"` column
  </details>
</ul>


### 3. Store Transactions
Save the cleaned data to a store.


### 4. Categorize Transactions
Manually
Or ML?
Or Rules-based? (regex, keywords, etc.)


```csv
# Category Rules
Id, RuleJsonBlob
```

```json-schema
// RuleJsonBlob JSONSchema
{
  "type": "object",
  "properties": {
    "Name": {"type": "string"},
    "Description": {"type": "string"},
    "CategoryId": {"type": "integer"}
    "Rule": {
      "type": "object",
      "properties": {
        "Type": {"type": "string", "enum": ["regex", "keyword"]},
        "Value": {"type": "string"},
      },
    },
  }
}
```


### 5. Analyze Transactions
Metabase or Apache Superset or Others


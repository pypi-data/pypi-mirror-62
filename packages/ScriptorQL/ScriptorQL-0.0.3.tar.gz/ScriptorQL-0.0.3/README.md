# Purpose
Generates an SQL insert script based on data.
Useful when developing databases and an insert script should be defined as post-deploy step.


```python
from ScriptorQL.script import df_to_SQL_insert

# Define a dataframe
# Table example:
# SchemaName.TableName
#
#   col1  |  col2  |  col3
# --------------------------
#   abc  |  val1  |  1
#   def  |  val2  |  2
#   hij  |  val3  |  3
#
# See pandas data frame

sql_script = df_to_SQL_insert(df, table="TableName", schema="SchemaName")
print(sql_script)
```
Result:

```sql
INSERT INTO SchemaName.TableName(col1, col2, col3)
VALUES  ('abc','val1','1'),
        ('def','val2','2'),
        ('hij','val3','3')
```

# To Do

-   Better documentation
-   Recognize datatypes (Always quoted right now)

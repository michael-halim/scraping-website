# AER Sharp Web Scraping

### Runtime

**0:01:06.191526**

### Entry Point File

- main.py

### Partial Dataset Location

- front_page.py

### Complete Dataset Location

- all_data.py

### Product Attribute

|     Attribute     | Status |
| :---------------: | :----: |
|       name        |   ✅   |
|        pic        |   ✅   |
|      address      |   ✅   |
|   contact_phone   |   ✅   |
|       price       |   ✅   |
|       link        |   ✅   |
|    description    |   ✅   |
|       tags        |   ✅   |
|  additional_desc  |   ✅   |
|     material      |   ✅   |
|      weight       |   ✅   |
|    weight_unit    |   ✅   |
|       color       |   ✅   |
| dimension_length  |   ✅   |
|  dimension_width  |   ✅   |
| dimension_height  |   ✅   |
|  dimension_unit   |   ✅   |
|     isProduct     |   ✅   |
| furnitureLocation |   ✅   |

### File Explanation

- front_page.py contains data from the front side of the website
- all_data.py contains all data from a product/item
- testing.py is a file to testing a small batch of program

### Flow

1. main.py get all links from navbar
2. Get all data that can be extracted from just the front page of the website
3. Save that file to front_page.py
4. Open front_page.py and get all the detail about a product and extract all data
5. Combine data from front_page and the data extracted from detail page and save it to all_data.py

### Get Dimension Algorithm

Find value of <td> tag that says 'ukuran barang'

### Get Material Algorithm

Find value of <td> tag that says 'material'

### Get Color Algorithm

Find value of <td> tag that says 'warna'

### Get Weight Algorithm

Find value of <td> tag that says 'berat'

### Remove Excess Whitespace in Middle of String Algorithm

Regex Pattern <br/>

```
\s{2,}
```

- `\s{2,}` Match whitespace with 2 or more

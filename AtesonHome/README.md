# Ateson Home Web Scraping

### Runtime

**0:20:42.164044**

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
|  contact_number   |   ✅   |
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

- links.py contains links from navbar include with title
- front_page.py contains data from the front side of the website
- all_data.py contains all data from a product/item
- testing.py is a file to testing a small batch of program

### Flow

1. main.py get all links from navbar
2. Navbar contains title, link, child_title, and child_link
3. First get all title, link, child_title, and child_link to get corresponding furnitureLocation and tags/category
4. After that, extract the file from links.py and get all the corresponding link
5. Get all data that can be extracted from just the front page of the website
6. Save that file to front_page.py
7. Open front_page.py and get all the detail about a product and extract all data
8. Combine data from front_page and the data extracted from detail page and save it to all_data.py

### Get Dimension Algorithm

Regex Pattern
Regex Pattern for Getting Dimension is 3 times with different regex for its different patterns

```
(\d+)\s?(\d+)\s?(\d+)\s?([a-z]+)
```

- `(\d+)` Match 12,2 or 12.2 or 12 or 12-13
- `\s?`
- `([a-z]+)`

### Get Weight Algorithm

Regex Pattern

```
(\d+)\s?([a-z]+)
```

- `(\d+)`
- `\s?`
- `([a-z]+)`

### Remove Excess Whitespace in Middle of String Algorithm

Regex Pattern

```
\s{2,}
```

- `\s{2,}` Match whitespace with 2 or more

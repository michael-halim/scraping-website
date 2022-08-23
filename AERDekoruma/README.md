# AER Dekoruma Web Scraping

### Runtime

**0:19:57.549275**

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

Regex Pattern
Regex Pattern for Getting Dimension is 3 times with different regex for its different patterns

```
[Uu]kuran\s?[bB]arang\s?([\d.,]+)\s?(cm|m)?\s?[xX]?\s?([\d.,]+)\s?(cm|m)?\s?[xX]?\s?([\d.,]+)\s?(cm|m)
```

- `[Uu]kuran\s?[bB]arang` Match ukuranBarang or ukuran Barang or Ukuran Barang or ukuranbarang, etc
- `([\d.,]+)` Match digit with ,. like 1.2 or 1,2 or 12
- `\s?` match whitespace or not
- `(cm|m)?` Match cm or m or neither
- `[Xx]` Match x or X

### Get Material Algorithm

Regex Pattern <br/>

```
[mM]aterial\s?[^\n]+
```

- `[mM]aterial` Match material or Material
- `\s?` Match whitespace or not
- `[^\n]+` Select all but \n, basically means match everything until found \n

### Get Color Algorithm

Regex Pattern <br/>

```
[wW]arna\s?[^\n]+
```

- `[wW]arna` Match warna or Warna
- `\s?` Match whitespace or not
- `[^\n]+` Select all but \n, basically means match everything until found \n

### Get Weight Algorithm

Regex Pattern <br/>

```
[bB]erat\s?([\d.]+)\s?(\w+)
```

- `[bB]erat` Match berat or Berat
- `\s?` Match whitespace or not
- `([\d.]+)` Match digit with . like 1.2 or 12
- `(\w+)` Match a word

### Remove Excess Whitespace in Middle of String Algorithm

Regex Pattern <br/>

```
\s{2,}
```

- `\s{2,}` Match whitespace with 2 or more

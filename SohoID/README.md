# Soho ID Web Scraping

### Runtime

**0:11:45.896166**

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
|  additional_desc  |   ❌   |
|     material      |   ✅   |
|      weight       |   ❌   |
|    weight_unit    |   ❌   |
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

Regex Pattern <br/>
This Pattern can Select following

1. P 10 cm L 23 cm T 56 cm
2. P 10 cmL 23 cmT 56 cm
3. Panjang 10 cm Kedalaman 23 cm Tinggi 56 cm
4. Panjang 10 cmKedalaman 23 cmTinggi 56 cm
5. P 10 L 23 T 56

```
\bP(?:anjang)?\s([\d-]+)\s(?:cm|m)?(?:\s)?(?:L|Kedalaman)?\s([\d-]+)\s(?:cm|m)?(?:\s)?T(?:inggi)?\s([\d-]+)\s(?:cm|m)?\b
```

<br/>

- `(?:)` non-capturing group
- `\b ` A word boundary to prevent a partial word match
- `P(?:anjang)?` Match P and optionally anjang
- `\s` is whitespace
- `([\d-]+)` Match 123 or 123-456
- `(?:cm|m)?` Match cm or m or nothing
- `(?:\s)?` Match Whitespace or nothing
- `(?:L|Kedalaman)?` Match L or Kedalaman
- `T(?:inggi)?` Match T and optionally inggi

### Get Material Algorithm

Regex Pattern <br/>

```
\b(?:[dD]ibuat|[bB]ahan)[^.]+\b
```

<br/>

- `(?:)` non-capturing group
- `\b ` A word boundary to prevent a partial word match
- `(?:[dD]ibuat|[bB]ahan)` Match 'dibuat' or 'Dibuat' or 'bahan' or 'Bahan'
- `[^.]+` Select all but '.'

### Remove Excess Whitespace in Middle of String Algorithm

Regex Pattern <br/>

```
\s{2,}
```

<br/>

- `\s{2,}` Match whitespace with 2 or more

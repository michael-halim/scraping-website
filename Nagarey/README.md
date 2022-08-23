# Nagarey Web Scraping

### Runtime

**0:13:05.764946**

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

Regex Pattern
Regex Pattern for Getting Dimension is 3 times with different regex for its different patterns

```
\b(?:[dD]ime....ns?|Ukuran)\s?([\d.,]+)\s?[Xx]\s?([\d.,]+)\s?[Xx]\s?([\d.,]+).+\b
```

- `(?:)` non-capturing group
- `\b ` A word boundary to prevent a partial word match
- `[dD]ime....ns?|Ukuran)` Match dimension, Dimension, dimensions, Dimensions. .... is built to avoid typo or Ukuran
- `\s?` match whitespace or not
- `([\d.,]+)` Match 12,2 or 12.2 or 12
- `[Xx]` Match x or X
- `.+` Match Whitespace or nothing

```
\b(?:[dD]ime....ns?|Ukuran)?\s?[A-Z]?([\d.,]+)\s?(?:cm)?\s?[xX]\s?[A-Z]?\s?([\d.,]+)\s?(?:cm)?\s?[xX]\s?[A-Z]?\s?([\d.,]+)\b
```

- `(?:)` non-capturing group
- `\b ` A word boundary to prevent a partial word match
- `[dD]ime....ns?|Ukuran)` Match dimension, Dimension, dimensions, Dimensions. .... is built to avoid typo or Ukuran
- `[A-Z]?` match A to Z or not
- `([\d.,]+)` Match 12,2 or 12.2 or 12
- `(?:cm)?` Match cm or not
- `[Xx]` Match x or X

```
\b(?:[dD]ime....ns?|Ukuran)?(?:DIA)?[A-Z]?\s?([\d,.-]+)\s?(?:cm)?\s?[Xx]?\s?[A-Z]?\s?([\d,.-]+)\b
```

- `(?:)` non-capturing group
- `\b ` A word boundary to prevent a partial word match
- `[dD]ime....ns?|Ukuran)` Match dimension, Dimension, dimensions, Dimensions. .... is built to avoid typo or Ukuran
- `(?:DIA)?` Match DIA or not
- `[A-Z]?` match A to Z or not
- `([\d,.-]+)` Match 12,2 or 12.2 or 12 or 12-13
- `[Xx]` Match x or X
- `(?:cm)?` Match cm or not

### Get Material Algorithm

Regex Pattern <br/>
Try #1

```
\b(?:[bB]ahan|[Mm]at....ls?)\s[^\n]+\b
```

- `\b ` A word boundary to prevent a partial word match
- `(?:)` non-capturing group
- `(?:[bB]ahan|[Mm]at....ls?)` Match 'bahan' or 'Bahan' or materials or Materials. .... is between is to avoid typo
- `\s` whitespace
- `[^\n]+` Select all but \n, basically means match everything until found \n

Try #2

```
[^a-z(),\s]*
```

- `[^a-z(),\s]*` Match all but 'a' to 'z' and ( and ) and ',' and whitespace, match 0 or more

Try #3

```
(?:\(|\)|\(\)|\(\w+\)|\(\w+|\w+\))
```

- `(?:)` non-capturing group
- `\(|\)|\(\)` Match ( or ) or ()
- `|` or
- `\(\w+\)` Match (lorem ipsum)
- `\(\w+` Match (Lorem ipsum
- `\w+\)` Match Lorem ipsum)

### Get Color Algorithm

Regex Pattern

```
[^a-z,\s]*
```

- `[^a-z,\s]*` Match all but 'a' to 'z' and ',' and whitespace, match 0 or more

```
\s[xX]\s
```

- `\s[xX]\s` Match all but whitespace and (x or X) and whitespace

### Remove Excess Whitespace in Middle of String Algorithm

Regex Pattern

```
\s{2,}
```

- `\s{2,}` Match whitespace with 2 or more

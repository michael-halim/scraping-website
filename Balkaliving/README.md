# Balkaliving Web Scraping

### Runtime

**0:05:57.765584**

### Entry Point File

- main.py

### Partial Dataset Location

- front_page.py

### Dataset Location

- all_data.py

### Product Attribute

|     Attribute     | Status |
| :---------------: | :----: |
|       name        |   ✅   |
|        pic        |   ✅   |
|      address      |   ✅   |
|     phone_num     |   ✅   |
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
-

### Flow

1. main.py get all the item from a website with certain pages
2. Then it save first for efficient and tolerate fail if things went south
3. The file that it save is in front_page.py with dictionary formatting
4. After that, extract the file from front_page.py and get all the corresponding link
5. Get all detail for every link
6. For every attribute, it is cleaned and formatted in dict and appended to copied dataset
7. Then, the complete dataset is saved to a file called 'all_data.py'

### Get Material Algorithm

- Split all additional desc into list
- After found specific word such as "bahan" or "material", append the next word until it founds ',' or 'dimensi'

### Get Dimension Algorithm

- Split all additional_information into list
- Loop every info if found 'weight' append the next one and two
- Loop every info if found 'dimension' append the next 1 and 3, check if next 4 is 'cm' or 'm'.
- Loop every info if found 'color' append the next until end

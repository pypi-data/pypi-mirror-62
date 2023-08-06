# pygrocydm
[![Build Status](https://travis-ci.com/BlueBlueBlob/pygrocydm.svg?branch=master)](https://travis-ci.com/BlueBlueBlob/pygrocydm)
[![CodeFactor](https://www.codefactor.io/repository/github/blueblueblob/pygrocydm/badge)](https://www.codefactor.io/repository/github/blueblueblob/pygrocydm)
[![Coverage Status](https://coveralls.io/repos/github/BlueBlueBlob/pygrocydm/badge.svg?branch=master)](https://coveralls.io/github/BlueBlueBlob/pygrocydm?branch=master)
[![PyPI](https://img.shields.io/pypi/v/pygrocydm.svg)](https://pypi.org/project/pygrocydm/)
[![Automated Release Notes by gren](https://img.shields.io/badge/%F0%9F%A4%96-release%20notes-00B2EE.svg)](https://github-tools.github.io/github-release-notes/)
[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/BlueBlueBlob/pygrocydm/?ref=repository-badge)

## Installation

`pip install pygrocydm`

## Managed Entities (WIP)

- products
- chores
- locations
- batteries
- shopping_list
- shopping_lists
- quantity_units
- quantity_unit_conversions
- tasks
- task_categories
- product_groups
- equipment
- userfields
- userentities
- userobjects


Check [Grocy API](https://demo.grocy.info/api#/Generic%20entity%20interactions)

## Documentation

https://blueblueblob.github.io/pygrocydm/

## Usage
Import the package: 
```python
from pygrocydm import GrocyDataManager
```

Obtain a grocy data manager instance:
```python
gdm = GrocyDataManager("https://example.com", "GROCY_API_KEY")
```
or
```python
gdm = GrocyDataManager("https://example.com", "GROCY_API_KEY", port = 9192, verify_ssl = True)
```

Product list :
```python
products = gdm.products()
products_list = products.list
for product in products_list:
    print(vars(product))
    if product.name == "Cookies":
        product.delete()
    if product.name == "Chocolate":
        data = {}
        data['name'] = "Choco"
        product.edit(data)
else:
    new_product = {}
    new_product['name'] = 'Cookies'
    new_product['location_id'] = 1
    new_product['qu_id_purchase'] = 1
    new_product['qu_id_stock'] = 1
    new_product['qu_factor_purchase_to_stock'] = 1
    new_product_id = products.add(new_product)
```

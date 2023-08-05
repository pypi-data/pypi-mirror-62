# Canonical Phone
## Purpose
Convert given phone number into a string with hiphenated phone number with country code.
Default is assumed to be Indonesian number.

## Installation
```bash
pip install canonical-phone==0.0.6
```

## How to use?
### When country code is unknown
```python
from canonical_phone.phone import canonical_number
phone_no = canonical_number(phone) # If invalid, returns False
if not phone_no:
    raise Exception("invalid phone number")
```
### With country code
```python
from canonical_phone.phone import canonical_number
phone_no = canonical_number(phone, has_country_code=True) # If invalid, returns False
if not phone_no:
    raise Exception("invalid phone number")
```
## Input/Output Combinations
```python
    [
        {
            "input": "62-8734878374",
            "output": "62-8734878374",
        },
        {
            "input": "628734878374",
            "output": "62-8734878374",
        },
        {
            "input": "8734878374",
            "output": "62-8734878374",
        },
        {
            "input": "84-8734878374",
            "output": "84-8734878374",
        },
        {
            "input": "91-8734878374",
            "output": "91-8734878374",
        },
        {
            "input": "848734878374",
            "output": "62-848734878374",
        },
        {
            "input": "848734878374",
            "output": "84-8734878374",
            "has_country_code": True,
        },
        {
            "input": "848734878374",
            "output": "62-848734878374",
            "has_country_code": False,
        },
        {
            "input": "91848734878374",
            "output": "91-848734878374",
            "has_country_code": True,
        }
    ]
```

## Important Notes
* Supports only two digit country codes as of now
* Mobile number max length supported is 8-15 characters without country code
* Please add any test cases you want to add to the input output list and create a PR
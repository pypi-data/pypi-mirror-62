# flashgeotext

## Usage
see also: [flashgeotext/examples](https://github.com/iwpnd/flashgeotext/tree/documentation/examples)

### Basic usage

```python
from flashgeotext.geotext import GeoText

geotext = GeoText(use_demo_data=True)

input_text = '''Shanghai. The Chinese Ministry
                of Finance in Shanghai said that
                China plans to cut tariffs on
                $75 billion worth of goods that
                the country imports from the US.
                Washington welcomes the decision.'''

geotext.extract(input_text=input_text, span_info=True)
>> {
    'cities': {
        'Shanghai': {
            'count': 2,
            'span_info': [(0, 8), (45, 53)]
            },
        'Washington, D.C.': {
            'count': 1,
            'span_info': [(175, 185)]
            }
        },
    'countries': {
        'China': {
            'count': 1,
            'span_info': [(64, 69)]
            },
        'United States': {
            'count': 1,
            'span_info': [(171, 173)]
            }
        }
    }
```

### Bring your own data

```python
from flashgeotext.geotext import GeoText
from flashgeotext.lookup import LookupData

districts = {
    'Friedrichshain-Kreuzberg': [
        'Friedrichshain',
        'Kreuzberg',
        'Friedrichshain-Kreuzberg'
        ]
}

text = """
Friedrichshain-Kreuzberg is the second borough
of Berlin, formed in 2001 by merging the former
East Berlin borough of Friedrichshain and
the former West Berlin borough of Kreuzberg.
The historic Oberbaum Bridge, formerly a Berlin
border crossing for pedestrians, links both districts
across the river Spree as the new borough's
landmark (as featured in the coat of arms).
"""

lookup_districts = LookupData(
    name="berlin_districts",
    data=districts)

geotext = GeoText(use_demo_data=False)
geotext.add(lookup_districts)

print(len(geotext.pool))
>> 1

geotext.extract(text, span_info=False)

>> {
    "berlin_districts": {
        "Friedrichshain-Kreuzberg: {
            "count": 3
        }
    }
}
```

### Data handling

#### add data to pool

```python
from flashgeotext.geotext import GeoText
from flashgeotext.lookup import LookupData

districts = {
    'Friedrichshain-Kreuzberg': [
        'Friedrichshain',
        'Kreuzberg',
        'Friedrichshain-Kreuzberg'
        ]
}

lookup_districts = LookupData(
    name="berlin_districts",
    data=districts)

geotext = GeoText(use_demo_data=True)
geotext.add(lookup_districts)

print(len(geotext.pool))
>> 3

print(geotext.pool)

>> {
    'cities': <flashtext.keyword.KeywordProcessor at 0x10b1691d0>,
    'countries': <flashtext.keyword.KeywordProcessor at 0x10acca250>,
    'berlin_districts': <flashtext.keyword.KeywordProcessor at 0x10acc1337>
    }

```

#### remove data from pool

```python
from flashgeotext.geotext import GeoText

geotext = GeoText()

print(geotext.pool)

>> {
    'cities': <flashtext.keyword.KeywordProcessor at 0x10b1691d0>,
    'countries': <flashtext.keyword.KeywordProcessor at 0x10acca250>
    }

print(len(geotext.pool))

>> 2

geotext.remove(lookup_to_remove="cities")

print(len(geotext.pool))

>> 1

print(geotext.pool)

>> {
    'countries': <flashtext.keyword.KeywordProcessor at 0x10acca250>
    }
```

#### remove all data from pool

```python
from flashgeotext.geotext import GeoText

geotext = GeoText()
print(len(geotext.pool))
>> 2

geotext.remove_all()

print(len(geotext.pool))
>> 0
```

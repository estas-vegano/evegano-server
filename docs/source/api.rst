# Evegano API documentation

### Localization
```
    Accept-Language: <en|ru|...>
```

### Possible product types
VEGAN, VEGETARIAN, LACTOVEGETARION, FISH, MEAT

### Api requests
#### `[GET] /api/v1.0/check`
##### request params
```
code=<string>
type=<barcode|qrcode>
```
##### response
```
{
    "id": 1,
    "title": "Some good",
    "info": "vegan",
    "photo": "http://example.com/some.png",
    "producer": {
	"title": "Microsoft",
	"ethical": bool
    },
    "category": {
        "id": "category",
        "title": "Some sub category",
        "sub_category": {
            "id": "subcategory",
            "title": "Some sub category"
        }
    }
}
```
---
#### `[POST] /api/v1.0/add`
##### request body
```
{
    "title": "Some good",
    "info": "vegan",
    "producer": "Microsoft",
    "category": {
        "id": "category",
        "title": "Some sub category",
        "sub_category": {
            "id": "subcategory",
            "title": "Some sub category"
        }
    }
}
```
##### response
```
{
    "id": 1,
    "title": "Some good",
    "info": "vegan",
    "producer": "Microsoft",
    "category": {
        "id": "category",
        "title": "Some sub category",
        "sub_category": {
            "id": "subcategory",
            "title": "Some sub category"
        }
    }
}
```
---
#### `[POST|MULTIPART] /api/v1.0/add/<productId>/image`
##### response
```
{
    "photo":"http://example.com/some.png"
}
```
---
#### `[POST] /api/v1.0/<productId>/complain`
##### request body
```
{
    "message":"VI VSIE VRETE"
}
```

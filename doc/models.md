# Models

Appier has a data layer used to abstract the user from the underlying data source. 
Currently, the data layer only supports [MongoDB](http://www.mongodb.org/), so be
sure to install it before trying to add models to your app.

A database will be created automatically in MongoDB with name of the app, 
and collections will be created with the name of the models. Therefore, if a ``Cat``
model is defined in a app called ``HelloApp``, a database named ``hello`` will be
created in MongoDB with a collection named ``cat`` inside it.

Model attributes can configured by adding keywords to their declaration:

```python
class Cat(appier.Model):
    
    id = appier.field(
        type = int,
        index = True,
        increment = True
    )
    
    name = appier.field(
        type = unicode,
        index = True
    )
```

An attribute can be one of the following types:

* `str` - String (this is the default type)
* `unicode` - Unicode (eg: `Eyjafjallajökull`)
* `int` - Integer (eg: `5`)
* `bool` - Boolean (eg: `True`)
* `float` - Float (eg: `1.3`)
* `list` - List of values (eg: `["a"]`)
* `dict` - Key-value dictionary (eg: `{"a": 1}`)
* `appier.File` - Python file object
* `appier.Files` - List of Python file objects
* `appier.ImageFile` - Specialized type file for images (allows resizing, etc.)
* `appier.ImageFiles` - Sequence based data type for the image type
* `appier.reference` - Non relational equivalent of the foreigh reference/key
* `appier.references` - Multiple items (to many) version of the reference type

The following keywords can be added to configure the attribute further:

* `index` - Boolean indicating if an index should be created for this attribute in 
the data source (faster searches)
* `increment` - Flag indicating if the value should be automatically generated on 
persistence by adding 1 to the previously generated value
* `default` - Indicates that the attribute is the default representation for the model
(useful for search operations to be able to decide which attribute to search by default)
* `safe` - Safe attributes cannot be set automatically with the `apply` operation
* `private` - Private attributes are not retrieved in `get` or `find` operations (useful
to keep passwords safe for example). This behaviour can be bypassed by passing 
`rules = False` to these methods
* `immutable` - Immutable attributes cannot be modified, they can only be set at creation time

### Persistence

To create a cat just do:

```python
cat = Cat()
cat.name = "garfield"
cat.save()
```

Once the cat is saved, a value will be set in its ``id`` attribute, due to the
``increment`` flag being set in the model definition (eg: ``1``, ``2``). To update the 
cat, just make the changes and call ``save`` again. 

To create the cat and have form data be automatically set do this:

```python
cat = Cat.new()
cat.save()
```

Creating a cat this way, will make a form data attribute named ``name``,
be applied to the ``name`` model attribute. The same form mapping behaviour can 
also be performed on a cat that already exists:

```python
cat.apply()
```

Deleting the cat is completely straightforward:

```python
cat.delete()
```

### Retrieval

You can retrieve cats whose name is ``garfield`` by doing the following:

```python
cats = Cat.find(name = "garfield")
```

Or cats whose text is not ``garfield``:

```python
cats = Cat.find(name = {"$ne" : "garfield"})
```

You can retrieve cats whose text is ``garfield`` or ``felix``:

```python
cats = Cat.find(name = {"$in" : ("garfield", "felix")})
```

Or cats whose text is not ``garfield`` nor ``felix``:

```python
cats = Cat.find(name = {"$nin" : ("garfield", "felix")})
```

* `equals` - 
* `not_equals` -
* `like` -
* `llike` -
* `rlike` -
* `greater` -
* `greater_equal` -
* `lesser` -
* `lesser_equal` -
* `is_null` -
* `is_not_null` -
* `contains` -

## Referencing the App

In order to invoke methods that belong to the App object, one can access it through
the ``owner`` attribute. For example, to resolve the URL for a route within a model:

```python
class Cat(appier.Model):
    
    id = appier.field(
        type = int,
        index = True,
        increment = True
    )
    
	def get_show_url(self):
		url = self.owner.url_for("cats.show", id = self.id)
		return url
```

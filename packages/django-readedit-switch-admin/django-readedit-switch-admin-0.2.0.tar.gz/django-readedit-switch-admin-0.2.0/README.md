# django-readedit-switch-admin

Read item detail first, and click the Edit switch button to turn to edit view.


## Install

```shell
pip install django-readedit-switch-admin
```

## Usage

**pro/settings.py**

```python

INSTALLED_APPS = [
    ...
    'django_readedit_switch_admin',
    ...
]
```

**app/admin.py**

```python
from django.contrib import admin
from .models import Category
from .models import Book

from django_readedit_switch_admin.admin import DjangoReadEditSwitchAdminMixin


class BookInline(admin.TabularInline):
    model = Book

class CategoryAdmin(DjangoReadEditSwitchAdminMixin, admin.ModelAdmin):
    list_display = ["pk", "name"]
    list_editable = ["name"]
    inlines = [
        BookInline
    ]

admin.site.register(Category, CategoryAdmin)

```

## Releases

### v0.2.0 2020.02.26

- App rename to django_readedit_switch_admin.

### v0.1.2 2020.02.24

- Don't check is_edit_view in getting add and delete permissions.

### v0.1.1 2020.02.20

- Fix add/change/delete permission problem in changelist view. Changelist view should obey the real permission.

### v0.1.0 2020.02.04

- First release.

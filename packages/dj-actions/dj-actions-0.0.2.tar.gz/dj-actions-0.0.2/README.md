# DJ Actions

A pattern + tooling to enable a standardized way to interact with and mutate data on a Django model

## Getting started

### Add actions to your Django app

#### 1. Create an actions module in your app:

DJActions convention is to isolate each action into it's own module.
A typical file layout might look something like this:

```python
[app]
  |_ [actions]
        |_ action_registry.py
        |_ [some_action]
        |_ [some_other_action]
```

#### 2. Create your action registry

The action registry is how we tell DJActions how to route to our actions. The action registry will also be responsible for generating your documentation endpoints

**Here is an example registry:**

```python
from actions.util import (
    STATUS,
    ACTION_TYPE,
    # get_action_docs,
    enrich_actions
)

action_list = []
## -- START ACTION REGISTRY -- ##
action_list.append(('mark_done', ACTION_TYPE.INSTANCE.value, STATUS.ALPHA.value))
## -- END ACTION REGISTRY -- ##

# this is the abolsute path to the base of your app:
# dj-actions uses this to locate your action directory
base = '/code/example_app/'

# convention over configuration
# this will load your actions configurations from
initial_registry = { "resource": "todo", "basepath": "/todos/", "actions": {} }
ACTIONS = enrich_actions(
    base,
    initial_registry,
    action_list
)
```

Now you need to mixin `actions.ActionViews` into your ViewSet:

```python
from rest_framework import routers, serializers, viewsets

from actions.mixins import ActionMixin
from actions.actions.action_registry import ACTIONS
from actions.models import EventAction


class EventActionViewSet(ActionMixin, viewsets.ModelViewSet):
    queryset = EventAction.objects.all()
    serializer_class = TodoSerializer
    action_registry = ACTIONS


router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet)

```

## Configuration

* `DJACTION_TRACK_ACTIONS` if `True` will store action info in the db (default: `True`)
* `DJACTION_TTL_MINUTES` actions older than this will be archived (default 1 day (60*24))

## Features

* Reliable, simple pattern to execute complex logic
* Self documenting

## Tooling

This library provides you with some tools and tasks which might be useful:

### Stream,io (WIP)

> Push action information into stream.io

### Airflow (WIP)

> Push downstream work to an airflow task




## Concepts

### Task Registry

The Task Registry provides a means of defining tasks in a self documenting way.
Based on the meta-data provided in the task registry, tasks will be exposed in various different ways


==========
GFK Models
==========

It's simple and handy way to extend your exiting models functionality.


Quick start
-----------

1. Add "gfk_models" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'gfk_models.gfk_base',
        'gfk_models.qna',
        'gfk_models.like',
        'gfk_models.review',
        'gfk_models.screenshot',
    ]

2. Attach through the url required functionality:

    target_request_attr - what value from current request will be selected for model instance retrieving
    target_retrieve_attr - tells us what variable name should we choose for model instance retrieving

    In the abstract it's looks like:

    Game.objects.get({% target_retrieve_attr %}, {% target_request_attr__value %})

    '''Q&A module example:'''

    ''Attach Q&A to concrete model:''
    ```
    url(r'^game/(?P<slug>[\w\-]+)/', include('gfk_models.qna.urls', namespace='qna'),
        {
            'target_model': models.Game,
            'target_request_attr': 'slug',
            'target_retrieve_attr': 'slug',
            'parent_urls_namespace': 'game'
        }),
    ```

    ''Attach Q&A globally:''

    ```
    url(r'^', include('gfk_models.qna.urls_global', namespace="qna")),
    ```

    '''Like module example:'''

    url(r'^', include('gfk_models.like.urls')),

    Now you have endpoint to add/delete likes/dislikes on any model in your project :

    /likes/add/(?P<target_id>[\d]+)/(?P<target_ct>[\d]+)

    /likes/add/1/2?v=like # add like to object with id=1 and content_type_id=2
    /likes/add/1/2?v=dislike # add like to object with id=1 and content_type_id=2

    If you add like/dislike twice it would be deleted.


3. Run `python manage.py migrate`
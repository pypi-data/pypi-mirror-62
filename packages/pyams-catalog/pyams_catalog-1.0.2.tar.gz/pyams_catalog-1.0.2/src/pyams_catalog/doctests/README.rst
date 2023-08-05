=====================
PyAMS_catalog package
=====================


Introduction
------------

This package is composed of a set of utility functions, usable into any Pyramid application.

    >>> from pyramid.testing import setUp, tearDown, DummyRequest
    >>> config = setUp()
    >>> config.registry.settings['zodbconn.uri'] = 'memory://'

    >>> from pyramid_zodbconn import includeme as include_zodbconn
    >>> include_zodbconn(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)
    >>> from pyams_site import includeme as include_site
    >>> include_site(config)
    >>> from pyams_i18n import includeme as include_i18n
    >>> include_i18n(config)
    >>> from pyams_catalog import includeme as include_catalog
    >>> include_catalog(config)

NLTK library must first be initialized before using text indexes:

    >>> import nltk
    >>> status = nltk.download('punkt') and nltk.download('snowball_data')
    >>> status
    True


Site generations
----------------

PyAMS_catalog package provides a site generation utility which is automatically checking for
a persistent catalog utility into local site manager:

    >>> from pyams_site.generations import upgrade_site
    >>> request = DummyRequest()
    >>> app = upgrade_site(request)
    Upgrading PyAMS timezone to generation 1...
    Upgrading PyAMS I18n to generation 1...
    Upgrading PyAMS catalog to generation 1...

    >>> from zope.traversing.interfaces import BeforeTraverseEvent
    >>> from pyramid.threadlocal import manager
    >>> from pyams_utils.registry import handle_site_before_traverse
    >>> handle_site_before_traverse(BeforeTraverseEvent(app, request))
    >>> manager.push({'request': request, 'registry': config.registry})

    >>> 'Catalog' in app.getSiteManager()
    True

    >>> from hypatia.interfaces import ICatalog
    >>> from pyams_utils.registry import get_utility
    >>> catalog = get_utility(ICatalog)

We have a catalog, we can now create an index:

    >>> from pyams_catalog.testing import IContentInterface, MyContent

    >>> from pyams_catalog.index import FieldIndexWithInterface
    >>> from pyams_catalog.generations import check_required_indexes
    >>> REQUIRED_INDEXES = [('content.value', FieldIndexWithInterface,
    ...                      {'interface': IContentInterface, 'discriminator': 'value'}), ]
    >>> check_required_indexes(app, REQUIRED_INDEXES)
    >>> 'content.value' in catalog
    True
    >>> index = catalog['content.value']
    >>> list(index.unique_values())
    []


Indexing contents
-----------------

The index is created, we can now create and index contents:

    >>> content = MyContent()
    >>> content.value = 'Test value'

    >>> from zope.lifecycleevent import ObjectAddedEvent, ObjectModifiedEvent, ObjectRemovedEvent
    >>> app['content1'] = content
    >>> config.registry.notify(ObjectAddedEvent(content, app))
    >>> list(index.unique_values())
    ['Test value']

If we try to index another object which doesn't implement index interface, the index is not updated
even if the object provides the same attribute:

    >>> from pyams_catalog.testing import MyOtherContent
    >>> content2 = MyOtherContent()
    >>> app['content2'] = content2
    >>> config.registry.notify(ObjectAddedEvent(content2, app))
    >>> list(index.unique_values())
    ['Test value']


Catalog queries
---------------

We have to be able to query catalog contents; the CatalogResultSet is a wrapper around an
Hypatia query which iterates over database objects instead of internal IDs references:

    >>> from hypatia.catalog import CatalogQuery
    >>> from hypatia.query import Query, Eq
    >>> from pyams_catalog.query import CatalogResultSet

    >>> params = Eq(index, 'Test value')
    >>> result = next(iter(CatalogResultSet(CatalogQuery(catalog).query(params))))
    >>> result is content
    True


Updating contents
-----------------

    >>> content.value = 'Modified value'
    >>> config.registry.notify(ObjectModifiedEvent(content))
    >>> params = Eq(index, 'Modified value')
    >>> result = next(iter(CatalogResultSet(CatalogQuery(catalog).query(params))))
    >>> result is content
    True
    >>> list(index.unique_values())
    ['Modified value']


I18n text indexes
-----------------

PyAMS_catalog allows to define special indexes to handle I18n attributes as defined into PyAMS_i18n
packages; you have to create a dedicated index for each language:

    >>> from hypatia.text.lexicon import Lexicon
    >>> from pyams_catalog.nltk import NltkFullTextProcessor
    >>> from pyams_catalog.testing import II18nContentInterface

    >>> def get_fulltext_lexicon(language):
    ...     return Lexicon(NltkFullTextProcessor(language=language))

    >>> from pyams_catalog.i18n import I18nTextIndexWithInterface
    >>> REQUIRED_INDEXES = [('content.i18n:en', I18nTextIndexWithInterface,
    ...                      {'language': 'en',
    ...                       'interface': II18nContentInterface,
    ...                       'discriminator': 'i18n_value',
    ...                       'lexicon': lambda: get_fulltext_lexicon('english')}), ]
    >>> check_required_indexes(app, REQUIRED_INDEXES)
    >>> 'content.i18n:en' in catalog
    True
    >>> i18n_index = catalog['content.i18n:en']
    >>> i18n_index.word_count()
    0

    >>> from pyams_catalog.testing import I18nContent

    >>> i18n_content = I18nContent()
    >>> i18n_content.i18n_value = {'en': 'I18n text value'}
    >>> app['i18n_content'] = i18n_content
    >>> config.registry.notify(ObjectAddedEvent(i18n_content, app))

    >>> i18n_index.word_count()
    3


Deleting contents
-----------------

Let's now delete these indexed contents:

    >>> del app['content1']
    >>> config.registry.notify(ObjectRemovedEvent(content, app))
    >>> list(index.unique_values())
    []

    >>> del app['i18n_content']
    >>> config.registry.notify(ObjectRemovedEvent(i18n_content, app))
    >>> i18n_index.word_count()
    0


Reindexing database contents
----------------------------

It is always possible to reindex all database contents into the catalog; this feature is used
by the *pyams_index* command line script:

    >>> from pyams_catalog.utils import index_site
    >>> request = DummyRequest(context=app)
    >>> index_site(request, autocommit=False)
    Indexing: <pyams_site.site.BaseSiteRoot object at 0x... oid 0x1 in <Connection at ...>>
    <pyams_site.site.BaseSiteRoot object at 0x... oid 0x1 in <Connection at ...>>


Tests cleanup:

    >>> tearDown()

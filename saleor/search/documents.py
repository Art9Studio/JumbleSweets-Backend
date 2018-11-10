from django_elasticsearch_dsl import DocType, Index, fields
from elasticsearch_dsl import analyzer, token_filter

from ..account.models import User
from ..order.models import Order
from ..product.models import Product, Category

storefront = Index('storefront')
storefront.settings(number_of_shards=1, number_of_replicas=0)

partial_words = token_filter(
    'partial_words', 'edge_ngram', min_gram=3, max_gram=15)
title_analyzer = analyzer(
    'title_analyzer',
    tokenizer='standard',
    filter=[partial_words, 'lowercase'])
email_analyzer = analyzer('email_analyzer', tokenizer='uax_url_email')


@storefront.doc_type
class ProductDocument(DocType):
    title = fields.StringField(analyzer=title_analyzer)
    category = fields.ObjectField(properties={
        'name': fields.StringField(analyzer=title_analyzer),
    })

    def prepare_title(self, instance):
        return instance.name

    class Meta:
        model = Product
        fields = ['name', 'description', 'is_published']
        related_models = [Category]

    def prepare_category_with_related(self, product, related_to_ignore):
        if (product.category is not None and product.category !=
            related_to_ignore):
            return {
                'name': product.category.name,
            }
        return {}

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in one sql request"""
        return super(ProductDocument, self).get_queryset().select_related(
            'category')

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Car instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, Category):
            return related_instance.products.all()


users = Index('users')
users.settings(number_of_shards=1, number_of_replicas=0)


@users.doc_type
class UserDocument(DocType):
    user = fields.StringField(analyzer=email_analyzer)
    first_name = fields.StringField()
    last_name = fields.StringField()

    def prepare_user(self, instance):
        return instance.email

    def prepare_first_name(self, instance):
        address = instance.default_billing_address
        if address:
            return address.first_name
        return None

    def prepare_last_name(self, instance):
        address = instance.default_billing_address
        if address:
            return address.last_name
        return None

    class Meta:
        model = User
        fields = ['email']


orders = Index('orders')
orders.settings(number_of_shards=1, number_of_replicas=0)


@orders.doc_type
class OrderDocument(DocType):
    user = fields.StringField(analyzer=email_analyzer)

    def prepare_user(self, instance):
        if instance.user:
            return instance.user.email
        return instance.user_email

    class Meta:
        model = Order
        fields = ['user_email', 'discount_name']

from rest_framework.serializers import Serializer, HyperlinkedIdentityField, ValidationError
from rest_framework.relations import PrimaryKeyRelatedField

from netbox.api import ChoiceField, WritableNestedSerializer
from dcim.api.nested_serializers import NestedSiteSerializer
from tenancy.api.nested_serializers import NestedTenantSerializer
from extras.api.nested_serializers import NestedTagSerializer


try:
    from extras.api.customfields import CustomFieldModelSerializer
except ImportError:
    from netbox.api.serializers import CustomFieldModelSerializer

from apbr.models import Apbr, ApbrStatusChoices


class TaggedObjectSerializer(Serializer):
    tags = NestedTagSerializer(many=True, required=False)

    def create(self, validated_data):
        tags = validated_data.pop('tags', None)
        instance = super().create(validated_data)

        if tags is not None:
            return self._save_tags(instance, tags)
        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        # Cache tags on instance for change logging
        instance._tags = tags or []

        instance = super().update(instance, validated_data)
        if tags is not None:
            return self._save_tags(instance, tags)
        return instance

    def _save_tags(self, instance, tags):
        if tags:
            instance.tags.set(*[t.name for t in tags])
        else:
            instance.tags.clear()
        return instance


class SerializedPKRelatedField(PrimaryKeyRelatedField):
    def __init__(self, serializer, **kwargs):
        self.serializer = serializer
        self.pk_field = kwargs.pop('pk_field', None)
        super().__init__(**kwargs)

    def to_representation(self, value):
        return self.serializer(value, context={'request': self.context['request']}).data


class ApbrSerializer(TaggedObjectSerializer, CustomFieldModelSerializer):
    status = ChoiceField(choices=ApbrStatusChoices, required=False)
    site = NestedSiteSerializer(required=False, allow_null=True)
    tenant = NestedTenantSerializer(required=False, allow_null=True)

    def validate(self, attrs):
        try:
            number = attrs['number']
            tenant = attrs.get('tenant')
        except KeyError:
            # this is patch
            return attrs
        if Apbr.objects.filter(number=number, tenant=tenant).exists():
            raise ValidationError(
                {'error': 'Asn with this Number and Tenant already exists.'}
            )
        return attrs

    class Meta:
        model = Apbr
        fields = ['number', 'id', 'display', 'status', 'description', 'custom_fields', 'site', 'tenant', 'tags']


class NestedApbrSerializer(WritableNestedSerializer):
    url = HyperlinkedIdentityField(view_name='plugins:apbr:asn')

    class Meta:
        model = Apbr
        fields = ['id', 'url', 'number', 'description']

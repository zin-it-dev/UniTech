from rest_framework import serializers


class BaseMixinSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        fields = ["date_created", "date_updated", "slug", "is_active"]

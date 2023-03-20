import re

from rest_framework import serializers


def username_check(username):
    if username == 'me':
        raise serializers.ValidationError(
            {'username': 'Нельзя использовать me'})
    if not re.match(r'^[\w.@+-]+\Z', username):
        raise serializers.ValidationError(
            {'username': 'Required. 150 characters or fewer.'
                         'Letters, digits and @/./+/-/_ only.'}
        )

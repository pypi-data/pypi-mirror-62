from comet import models
from aristotle_mdr.contrib.serializers.concept_serializer import SubSerializer


class IndicatorNumeratorSerializer(SubSerializer):

    class Meta:
        model = models.IndicatorNumeratorDefinition
        exclude = ('indicator',)


class IndicatorDenominatorSerializer(SubSerializer):

    class Meta:
        model = models.IndicatorNumeratorDefinition
        exclude = ('indicator',)


class IndicatorDisaggregationSerializer(SubSerializer):

    class Meta:
        model = models.IndicatorNumeratorDefinition
        exclude = ('indicator',)


class IndicatorInclusionSerializer(SubSerializer):

    class Meta:
        model = models.IndicatorInclusion
        exclude = ('indicator',)

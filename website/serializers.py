from website.models import Goal
from rest_framework import serializers
from rest_framework import routers
from rest_framework import viewsets

class GoalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Goal
        fields = ('number', 'title', 'target_amount', 'current_amount')



class GoalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer


router = routers.DefaultRouter()
router.register(r'goals', GoalViewSet)

from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout

# Defensive serializer to ensure ObjectId values are converted to strings
try:
    from bson import ObjectId
except Exception:
    ObjectId = None

class BaseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)

        def convert(obj):
            # Convert ObjectId instances to their string representation
            if ObjectId is not None and isinstance(obj, ObjectId):
                return str(obj)
            if isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [convert(v) for v in obj]
            return obj

        return convert(data)

class UserSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TeamSerializer(BaseSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class ActivitySerializer(BaseSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class LeaderboardSerializer(BaseSerializer):
    class Meta:
        model = Leaderboard
        fields = '__all__'

class WorkoutSerializer(BaseSerializer):
    class Meta:
        model = Workout
        fields = '__all__'

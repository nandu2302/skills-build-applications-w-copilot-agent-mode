from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data. Some earlier records may lack primary keys
        # which causes Django's collector to raise TypeError when deleting.
        # Use a safe delete with a fallback to raw collection deletion.
        def safe_clear(qs, model_name):
            try:
                print(f"Clearing {model_name} via ORM delete")
                qs.delete()
            except TypeError:
                # Fallback for malformed records: try to use model's collection accessor
                print(f"TypeError while deleting {model_name} via ORM, attempting raw collection delete")
                try:
                    # djongo may expose _get_collection() on the model
                    coll = qs.model._get_collection()
                    coll.delete_many({})
                except Exception:
                    # Last resort: delete records that do have valid primary keys
                    print(f"Raw collection access failed for {model_name}; deleting records with primary keys only")
                    qs.model.objects.filter(pk__isnull=False).delete()

        safe_clear(Activity.objects.all(), 'Activity')
        safe_clear(Leaderboard.objects.all(), 'Leaderboard')
        safe_clear(User.objects.all(), 'User')
        safe_clear(Team.objects.all(), 'Team')
        safe_clear(Workout.objects.all(), 'Workout')

        # Create Teams
        marvel = Team.objects.create(name='marvel', description='Marvel Superheroes')
        dc = Team.objects.create(name='dc', description='DC Superheroes')

        # Create Users
        users = [
            User(email='ironman@marvel.com', name='Iron Man', team='marvel'),
            User(email='captain@marvel.com', name='Captain America', team='marvel'),
            User(email='batman@dc.com', name='Batman', team='dc'),
            User(email='superman@dc.com', name='Superman', team='dc'),
        ]
        for user in users:
            user.save()

        # Create Workouts
        workouts = [
            Workout(name='Pushups', description='Do 20 pushups', difficulty='easy'),
            Workout(name='Running', description='Run 5km', difficulty='medium'),
            Workout(name='Deadlift', description='Deadlift 100kg', difficulty='hard'),
        ]
        for workout in workouts:
            workout.save()

        # Create Activities
        Activity.objects.create(user=users[0], type='Pushups', duration=10, date=timezone.now().date())
        Activity.objects.create(user=users[1], type='Running', duration=30, date=timezone.now().date())
        Activity.objects.create(user=users[2], type='Deadlift', duration=45, date=timezone.now().date())
        Activity.objects.create(user=users[3], type='Pushups', duration=15, date=timezone.now().date())

        # Create Leaderboard
        Leaderboard.objects.create(team=marvel, points=200)
        Leaderboard.objects.create(team=dc, points=180)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))

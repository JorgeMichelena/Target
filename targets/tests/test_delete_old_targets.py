from targets.factory import TopicFactory, TargetFactory
from users.factory import UserFactory
from rest_framework.test import APITestCase
from targets.models import Target
from target.tasks import delete_one_week_old_targets
import datetime


class DeleteOldTargetsTest(APITestCase):
    def setUp(self):
        user = UserFactory()
        user.save()
        topic = TopicFactory()
        topic.save()
        self.target_today = TargetFactory(user=user, topic=topic)
        self.target_six_days = TargetFactory(user=user, topic=topic)
        target_one_week = TargetFactory(user=user, topic=topic)
        target_two_weeks = TargetFactory(user=user, topic=topic)
        six_days_ago = datetime.date.today() - datetime.timedelta(days=6)
        one_week_ago = datetime.date.today() - datetime.timedelta(days=7)
        two_weeks_ago = datetime.date.today() - datetime.timedelta(days=14)
        self.target_six_days.save()
        target_one_week.save()
        target_two_weeks.save()
        self.target_six_days.creation_date = six_days_ago
        target_one_week.creation_date = one_week_ago
        target_two_weeks.creation_date = two_weeks_ago
        self.target_six_days.save()
        target_one_week.save()
        target_two_weeks.save()
        self.target_today.save()

    def test_delete_one_week_old_targets(self):
        delete_one_week_old_targets()
        targets = Target.objects.all()
        self.assertEqual(len(targets), 2)
        self.assertCountEqual(targets, [self.target_today, self.target_six_days])

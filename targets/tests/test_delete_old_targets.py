from targets.factory import TopicFactory, TargetFactory
from users.factory import UserFactory
from rest_framework.test import APITestCase
from targets.models import Target
from target.tasks import delete_one_week_old_targets
import datetime


class DeleteOldTargetsTest(APITestCase):
    def setUp(self):
        six_days_ago = datetime.date.today() - datetime.timedelta(days=6)
        one_week_ago = datetime.date.today() - datetime.timedelta(days=7)
        two_weeks_ago = datetime.date.today() - datetime.timedelta(days=14)
        targets = TargetFactory.create_batch(4)
        self.target_today = targets[0]
        self.target_six_days = targets[1]
        self.target_six_days.creation_date = six_days_ago
        targets[2].creation_date = one_week_ago
        targets[2].save()
        targets[3].creation_date = two_weeks_ago
        targets[3].save()

    def test_delete_one_week_old_targets(self):
        number_before_method = Target.objects.count()
        delete_one_week_old_targets()
        targets_after_method = Target.objects.all()
        self.assertEqual(number_before_method, 4)
        self.assertEqual(len(targets_after_method), 2)
        self.assertCountEqual(targets_after_method, [self.target_today, self.target_six_days])

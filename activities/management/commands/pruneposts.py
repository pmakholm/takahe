import datetime
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from activities.models import Post


class Command(BaseCommand):
    help = "Prunes posts that are old, not local and have no local interaction"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            "-n",
            type=int,
            default=5000,
            help="The maximum number of posts to prune at once",
        )

    def handle(self, number: int, *args, **options):
        # Find a set of posts that match the initial criteria
        print(f"Running query to find up to {number} old posts...")
        posts = Post.objects.filter(
            local=False,
            created__lt=timezone.now()
            - datetime.timedelta(days=settings.SETUP.REMOTE_PRUNE_HORIZON),
        ).exclude(interactions__identity__local=True)[:number]
        post_ids_and_uris = dict(posts.values_list("object_uri", "id"))
        print(f"  found {len(post_ids_and_uris)}")

        # Fetch all of their replies and exclude any that have local replies
        print("Excluding ones with replies...")
        replies = Post.objects.filter(
            in_reply_to__in=post_ids_and_uris.keys()
        ).values_list("in_reply_to", flat=True)
        for reply in replies:
            if reply:
                del post_ids_and_uris[reply]

        # Delete them
        print(f"  down to {len(post_ids_and_uris)} to delete")
        number_deleted, _ = Post.objects.filter(
            id__in=post_ids_and_uris.values()
        ).delete()
        print(f"Deleted {number_deleted} posts")
        if number_deleted == 0:
            sys.exit(1)

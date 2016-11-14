from django.core.management.base import BaseCommand, CommandError
from website.models import Project

class Command(BaseCommand):
    help = 'Reorders'

    def handle(self, *args, **options):
        projects = Project.objects.all().order_by('?')
        
        for count, project in enumerate(projects):
            project.order = count
            project.save()

        self.stdout.write(self.style.SUCCESS('Successfully reordered projects'))
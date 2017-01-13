from django.core.management.base import BaseCommand, CommandError
from website.models import Project, Grant, Match
import datetime
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

class Command(BaseCommand):
    help = 'Matches'

    def handle(self, *args, **options):
        today = datetime.datetime.today()
        grants = Grant.objects.filter(deadline__gte=today)
        projects = Project.objects.all().order_by('?')
        
        for grant in grants:
            for project in projects:
                
                # matching first attempt - projects with less text ended up matching more
                # similarity = similar(
                #     grant.name + " " + grant.organization.name + " " + grant.comments + " " + grant.tags, 
                #     project.name + " " + 
                #     project.slug + " " + 
                #     project.description + " " + 
                #     project.tags + " " + 
                #     (project.problem and project.problem or "") + 
                #     ''.join([group.name+ " " for group in project.group_set.all()]) + 
                #     ''.join([benefit.name+ " " for benefit in project.benefit_set.all()]) + 
                #     ''.join([barrier.name+ " " for barrier in project.barrier_set.all()]) + 
                #     ''.join([collaborator.name+ " " for collaborator in project.collaborator_set.all()]) 
                # )
                
                # matching second attempt, matching is more even, however more relavant projects are not matching with appropriate grants
                # similarity = similar(
                #     grant.name + " " + grant.organization.name + " " + grant.comments + " " + grant.tags, 
                #     project.name + " " + 
                #     project.description
                # )

                similarity = similar(
                    grant.corpus, 
                    project.description
                )

                similarity = fuzz.token_set_ratio(
                    project.description + " " + 
                    project.tags + " " + 
                    (project.problem and project.problem or "") + 
                    ''.join([group.name+ " " for group in project.group_set.all()]) + 
                    ''.join([benefit.name+ " " for benefit in project.benefit_set.all()]) + 
                    ''.join([barrier.name+ " " for barrier in project.barrier_set.all()]) + 
                    ''.join([collaborator.name+ " " for collaborator in project.collaborator_set.all()])
                    , grant.corpus)

                print project, grant, similarity
                match, created = Match.objects.update_or_create(
                    project=project, grant=grant, defaults={'score': similarity or 0})
                

        self.stdout.write(self.style.SUCCESS('Successfully matched projects'))
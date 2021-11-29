from django.shortcuts import render
from django.views.generic import View
from .models import ApbrProfile

class RandomApbrProfileView(View):
    """
    Display a randomly-selected ApbrProfile.
    """
    def get(self, request):
        profile = ApbrProfile.objects.order_by('?').first()
        return render(request, 'apbr/profile.html', {
            'profile': profile,
        })

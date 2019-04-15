from .models import Profile
from django.shortcuts import render, redirect
import logging

logger = logging.getLogger('logger')


def check_profile(*args, **kwargs):
    ''' check that the user have an existing profile '''
    logger.info('check if user profile exists')
    user = kwargs.get('user')
    details = kwargs.get('details')
    # logger.info(kwargs)
    profile, is_new = Profile.objects.get_or_create(user=kwargs.get('user'), 
                        first_name=details['first_name'],
                        last_name=details['last_name'], age=22, balance=100)
    return {
        'profile': profile
    }
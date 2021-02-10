import datetime
from django.core.exceptions import ValidationError, ObjectDoesNotExist, EmptyResultSet
from django.db.models import Q
from django.shortcuts import render
from .models import Alias

# Create your views here.

# Alias.objects.create(alias='useful-object', target='types-slug-023xf',
# start=timezone.now() - timedelta(days=50), end=None)
# alias_obj = Alias.objects.filter(alias='useful-object', end=None)
# referred_obj_slug = alias_obj.target
# aliases = get_aliases(target='types-slug-023xf', from=<datetime 2020-02-01
# 00:00:00.000000>, to=<datetime 2020-05-01 05:23:47.657264)


def referred_obj_slug(alias):
    alias_obj = Alias.objects.filter(alias=alias)
    if alias_obj:
        return [i.target for i in alias_obj]
    return 'Alias is not found'



'''
we are getting aliases which were running at the specific time frame.
Aliases may start before from_time or end after to_time.
Here we only care about aliases with overlapping running time.
Even one microsecond of overlap counts as running alias at that time
'''


def get_aliases(target, from_time, to_time):
    if (type(from_time) is datetime.datetime) and (type(to_time) is datetime.datetime):
        alias_unfiltered = Alias.objects.filter(target=target)
        if alias_unfiltered:
            if Alias.objects.filter(Q(target=target), Q(start__lte=to_time), Q(end__gte=from_time)).exists() \
                    or Alias.objects.filter(Q(target=target), Q(start__lte=to_time), Q(end__isnull=True)).exists():
                alias_list = [i.alias for i in alias_unfiltered]
                return f"Targeted aliases are: {alias_list}"
            else:
                return f'Alias with {target} target was not running at that time frame'
        else:
            return f"This alias object doesn't exist"
    raise TypeError("from_time or to_time parameters are not in DateTime format")



'''
replacing an existing alias with a new one at a specific time point.
That is, something like:
alias_replace(existing_alias, replace_at, new_alias_value)​ 
that, when called, will set ​end​ for the ​existing_alias​ to ​replace_at​ moment, 
create a new Alias with alias=new_alias_value​ and ​start=replace_at, end=None​.

'''

    # return Alias.objects.filter(Q(target=target), Q(start__lte=to_time))

# return aliases_array if aliases_array else print(f'This alias was not running between {from_time} to {to_time}')


# if end >= alias.start and start <=alias.end OR end >=alias.start and alias.end==None
# if to_time <= alias.start:
# aliases_array = Alias.objects.filter(target=target, start=from_time, end=to_time)


# try:
#     aliases_array = Alias.objects.filter(target=target, start=from_time, end=to_time)
# except Alias.DoesNotExist:
#     raise ValidationError('No aliases found')
# return aliases_array




#isinstance(from, datetime.datetime) & isinstance(to, datetime.datetime)
import datetime
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Alias, Object


def referred_obj_slug(alias, end=None):
    """ referred_obj_slug() - gets list of slugs for particular alias.
        Limitation on particular end period is optional.

    Args:
        alias (`str`): The first parameter. Required.
        end (:obj:`DateTime`, optional): Defaults to None.

    Returns:
        list: List with slugs.
        Example: ['types-slug-023xf', 'types-slug-025xf']

    Raises:
        ValidationError: when alias object is not found

    Example:
        alias_obj = Alias.objects.filter(alias='useful-object', end=None)
    """

    alias_obj = Alias.objects.filter(alias=alias)
    if alias_obj:
        if end is not None:
            # returns slug of currently running Alias objects
            return [i.target.name for i in alias_obj.filter(end__lte=end)]
        else:
            # returns slug of all finished Alias objects active before [end]
            return [i.target.name for i in alias_obj.filter(end__isnull=True)]
    raise ValidationError("Alias is not found")


def get_aliases(target, from_time, to_time):
    """ get_aliases() - gets objects' ``alias`` which were running at the specific time.
            Aliases may start before ``from_time`` or end after ``to_time``.
            Here we only care about aliases with overlapping running time.
            Even one microsecond of overlap counts as running alias.

    Args:
        target (`str`): The first parameter. Name of the object/slug. Required.
        from_time (:obj:`DateTime`): The second parameter. Required.
        to_time (:obj:`DateTime`): The third parameter. Required.

    Returns:
        list: List with aliases running at specific time.
        Example: ['useful-object', 'useful-object2']

    Raises:
        Object.DoesNotExist: when target object is not found,
        TypeError: when ``from_time`` or ``to_time`` are not DateTime objects
        ValidationError: when alias object is not found,
        ValidationError: when no aliases with ``target`` were active

    Example:
        get_aliases(target='types-slug-023xf',
        from=<datetime 2020-02-01 00:00:00.000000>,
        to=<datetime 2020-05-01 05:23:47.657264>)
    """
    try:
        target_obj = Object.objects.get(name=target)
    except Object.DoesNotExist:
        raise Object.DoesNotExist(f"Targeted object - {target} - does not exist")

    else:
        if (type(from_time) is datetime.datetime) \
                and (type(to_time) is datetime.datetime):
            alias_unfiltered = Alias.objects.filter(target=target_obj.id)
            if alias_unfiltered.exists():
                if (Alias.objects.filter(Q(target=target_obj.id),
                                         Q(start__lte=to_time),
                                         Q(end__gte=from_time)).exists()
                        or Alias.objects.filter(Q(target=target_obj.id),
                                                Q(start__lte=to_time),
                                                Q(end__isnull=True)).exists()):
                    alias_list = [i.alias for i in alias_unfiltered]
                    return f"Targeted aliases are: {alias_list}"
                raise ValidationError(f"No aliases with {target} target"
                                      f" were active at that time")
            raise ValidationError(f"Alias objects with {target} don't exist")
        raise TypeError(f"from_time ({from_time}) or to_time ({to_time})"
                        f" parameters are not in DateTime format")


def replace_alias(existing_alias_id, replace_at, new_alias_value):
    """ replace_alias() - replaces an existing alias with a new one
            at a specific time point. When called,
            sets end​ of the ​existing_alias​ to ``​replace_at​ moment``,
            creates a new Alias with alias=new_alias_value​, ​
            start=replace_at, end=None​.

        Args:
            existing_alias_id (`int`): The first parameter. Existing alias ID.
            replace_at (:obj:`DateTime`): The second parameter.
            new_alias_value (`str`): The third parameter - name of new alias.

        Returns:
            int: ID of the new alias
            Example: 8

        Raises:
            TypeError: when ``replace_at`` is not DateTime object
            ValidationError: when alias.start greater or equal ``replace_at``

        Example:
            replace_alias(4, <datetime 2021-02-10 05:23:47.657264>,
                            'Vingardium Leviosa');
    """

    if type(replace_at) is datetime.datetime:
        alias = Alias.objects.get(id=existing_alias_id)
        if alias.start.replace(tzinfo=None) >= replace_at:
            raise ValidationError(
                f"Replacement of {alias.id} with {alias.start} is impossible: "
                f"start time is greater than replace_at"
            )
        else:
            # Updating existing Alias
            Alias.objects.filter(pk=alias.pk).update(end=replace_at)
            alias.refresh_from_db()
            print(f"Alias object updated: {alias.__dict__}")

            # Creating new Alias
            new_alias = Alias.objects.create(
                alias=new_alias_value, target=alias.target, start=replace_at)
            print(f"New alias object created:{new_alias.__dict__}")
            return f"Done! New alias id is {new_alias.id}"

    raise TypeError(f"replace_at ({replace_at}) parameter "
                    f"is not in DateTime format")

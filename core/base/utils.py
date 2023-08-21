from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, Page
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.db.models import ManyToOneRel


def covert_date_to_string(date):
    date_str = date.strftime('%b. %d, %Y, %I:%M ')
    if date.hour < 12:
        date_str += "a.m."
    else:
        date_str += "p.m."
    return date_str


def model_to_dict_with_fk(obj):
    print(obj.seen_details.all(), '5555'*200)
    ''' Convert a model instance to a dictionary, including
        foreign key constraints '''
    data = model_to_dict(obj)
    for field in obj._meta.get_fields():
        print(field, 'f'*500)
        if isinstance(field, ManyToOneRel):
            print('yeah'*150)
            data[field.name] = list(getattr(obj, field.name).all())
    return data


def get_page_obj(request, queryset):
    paginator = Paginator(queryset, request.GET.get('per_page', 2))
    try:
        page_obj = paginator.page(request.GET.get('page', 1))
    except PageNotAnInteger:
        page_obj = paginator.page(request.GET.get('page', 1))
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


def page_serializer(page: Page, obj_list_name):
    obj_list = [model_to_dict_with_fk(model) for model in page]
    print(obj_list, 'iiiiiiii'*200)
    for obj in obj_list:
        user_obj = User.objects.get(id=obj['sent_by'])
        obj['sent_by'] = {'username': user_obj.username, 'id': user_obj.id}
    print(obj_list, 'obj'*150)
    for model in page:
        print('x'*500)
        print(model.seen_details)
        # obj_list['seen_details'] = model.seen_details

    for model in obj_list:
        # print(model.seen_details)
        for i, seen_detail in enumerate(model['seen_details']):
            model['seen_details'][i] = {'username': seen_detail.user.username,
                                        'id': seen_detail.user.id,
                                        'is_recieved': seen_detail.is_recieved,
                                        'seen_at': covert_date_to_string(
                                            seen_detail.created_at)}
    print(obj_list[::-1], '**&&'*250)
    return {
        'number': page.number,
        'has_previous': page.has_previous(),
        'has_next': page.has_next(),
        obj_list_name: obj_list[::-1],
        'total_pages': page.paginator.num_pages,
        'next_page_number': page.next_page_number() if page.has_next() else None
    }

from django import template
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

register = template.Library()

@register.simple_tag
def update_query_params(request, field, value):
    value = str(value)

    # Parse the current query string into a dictionary
    query_dict = parse_qs(urlparse(request.get_full_path()).query, keep_blank_values=True)

    # If the field and value already exist, remove the value
    if field in query_dict and value in query_dict[field]:
        query_dict[field].remove(value)
    else:
        if field == "tag":
            # Manage tags as a list
            tags = query_dict.get('tag', [])
            if value not in tags:
                tags.append(value)
            query_dict['tag'] = tags
        else:
            query_dict[field] = [value]

    # Rebuild the query string
    new_query_string = urlencode(query_dict, doseq=True)

    # Rebuild the full URL with the updated query string
    url_parts = list(urlparse(request.get_full_path()))
    url_parts[4] = new_query_string  # url_parts[4] is the query string

    return urlunparse(url_parts)
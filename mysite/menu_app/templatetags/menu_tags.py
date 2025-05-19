from django import template
from django.urls import reverse, NoReverseMatch
from django.template.loader import render_to_string
from ..models import MenuItem

register = template.Library()

def build_menu_tree(menu_items):
    """
    Builds a nested tree structure from a flat list of menu items.
    """
    tree = {}
    for item in menu_items:
        if item.parent is None:
            tree[item.id] = {'item': item, 'children': []}
        else:
            # Find the parent in the tree and add the item as a child
            # This assumes a valid parent_id exists in the input list
            parent_id = item.parent.id
            if parent_id in tree:
                tree[parent_id]['children'].append({'item': item, 'children': []})
    return list(tree.values())

def is_active(menu_item, request):
    """
    Checks if a menu item's URL matches the current request path.
    """
    try:
        if menu_item.named_url:
            url = reverse(menu_item.named_url)
        else:
            url = menu_item.url
    except NoReverseMatch:
        return False

    return url == request.path

def is_expanded(menu_item, request, menu_tree):
    """Checks if a menu item should be expanded."""
    # Expanded if it's an ancestor of the active item or the active item itself.
    if is_active(menu_item['item'], request):
        return True

    # Check if any child is active and should be expanded.
    # We need to traverse the original menu_items to check for ancestors

    # Check if any child is active
    for child in menu_item.get('children', []):
        if is_expanded(child, request, menu_tree):
            return True

    return False

def add_expansion_status(menu_tree, request):
    """
    Recursively adds 'is_expanded_node' key to each node in the menu tree.
    """
    for node in menu_tree:
        node['is_expanded_node'] = is_expanded(node, request, menu_tree)
        if node['children']:
            add_expansion_status(node['children'], request)
    return menu_tree

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    """
    Template tag to draw a menu by name.
    """
    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')
    menu_tree = build_menu_tree(menu_items)
    request = context['request']

    return render_to_string('menu_app/menu_tree.html', {
        'menu_tree': add_expansion_status(menu_tree, request),
        'request': request,
        'is_active': is_active,
    })
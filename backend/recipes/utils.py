from django.conf import settings 
from django.http import HttpResponse


def convert_txt(shop_list):
    file_name = settings.SHOPPING_CART_FILE_NAME
    lines = []
    for ing in shop_list:
        lines.append(f'{ing[0]} ({ing[1]}) - {shop_list[ing]}')
    lines.append('\nFoodGram Service')
    lines.append('   (＠＾◡＾)')
    content = '\n'.join(lines)
    content_type = settings.SHOPPING_LIST_CONTENT_TYPE
    response = HttpResponse(content, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response

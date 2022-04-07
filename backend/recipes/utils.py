from django.http import HttpResponse


def convert_txt(shop_list):
    file_name = 'shopping_list.txt'
    lines = []
    for ing in shop_list:
        lines.append('{0} ({1}) - {2}'.format(ing[0], ing[1], shop_list[ing]))
    lines.append('\nFoodGram Service')
    lines.append('   (＠＾◡＾)')
    content = '\n'.join(lines)
    response = HttpResponse(content, content_type="text/plain,charset=utf8")
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response

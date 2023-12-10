import mimetypes
from pathlib import Path
from urllib.parse import urlparse

import weasyprint
from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.core.files.storage import default_storage
from django.template.loader import get_template
from django.urls import get_script_prefix
from weasyprint import HTML

from config import settings


def url_fetcher(url, *args, **kwargs):
    if url.startswith('file:'):
        mime_type, encoding = mimetypes.guess_type(url)
        url_path = urlparse(url).path
        data = {
            'mime_type': mime_type,
            'encoding': encoding,
            'filename': Path(url_path).name,
        }

        default_media_url = settings.MEDIA_URL in ('', get_script_prefix())
        if not default_media_url and url_path.startswith(settings.MEDIA_URL):
            media_root = settings.MEDIA_ROOT
            if isinstance(settings.MEDIA_ROOT, Path):
                media_root = f'{settings.MEDIA_ROOT}/'
            path = url_path.replace(settings.MEDIA_URL, media_root, 1)
            data['file_obj'] = default_storage.open(path)
            return data

        elif settings.STATIC_URL and url_path.startswith(settings.STATIC_URL):
            path = url_path.replace(settings.STATIC_URL, '', 1)
            data['file_obj'] = open(find(path), 'rb')
            return data

    return weasyprint.default_url_fetcher(url, *args, **kwargs)


def create_pdf(context, template_name):
    template = get_template(template_name)
    html_template = template.render(context).encode(encoding='utf-8')
    return HTML(string=html_template, base_url='.', url_fetcher=url_fetcher).write_pdf(presentational_hints=True)

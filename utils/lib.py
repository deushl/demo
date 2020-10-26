from django.contrib.sessions.models import Session
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from utils.responses import MISSING_PARAMETERS, BAD_REQUEST, UNSUPPORTED_TYPE

import json


class BaseView(View):
    body = None
    fields_required = None
    files_required = None
    content_type = None
    get_params = None
    data_required = False

    def parse_get_params(self, request):
        if not self.get_params:
            return None
        try:
            data = {}
            for param in self.get_params:
                data[param] = request.GET.get(param)

        except Exception as e:
            print(e)
            return JsonResponse(BAD_REQUEST, status=400)

        return data

    def parse_data(self, request):
        if not self.data_required:
            return None

        try:
            if self.body is None:
                data = json.loads(request.body.decode('utf8'))
            else:
                data = json.loads(request.POST.get(self.body))

            if data is None:
                return JsonResponse(MISSING_PARAMETERS, status=422)
        except json.decoder.JSONDecodeError:
            return JsonResponse(BAD_REQUEST, status=400)

        if self.fields_required is not None and not all(field in data for field in self.fields_required):
            return JsonResponse(MISSING_PARAMETERS, status=422)

        return data

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        print()
        if self.content_type is not None and request.content_type is not self.content_type:
            return JsonResponse(UNSUPPORTED_TYPE, status=415)

        data = self.parse_data(request)
        if isinstance(data, JsonResponse):
            return data

        get_data = self.parse_get_params(request)
        if isinstance(get_data, JsonResponse):
            return get_data

        return super().dispatch(request, data=data, get_data=get_data, *args, **kwargs)

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList


class CustomJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        data_dict = {
            'status': 'success',
            'message': "Data Retrieved Successfully",
            'data': data
        }
        response = renderer_context['response']
        if type(data) in (ReturnList, list):
            if len(data) > 0 and (response.status_code >=200 and response.status_code <=299):
                data_dict['message'] = 'Data Retrieved Successfully'
            else:
                data_dict['message'] = "No Data Found"
        # Change status checking status code  
        if response.status_code >=200 and response.status_code <=299:
            data_dict['status'] = 'success'
            data_dict['message'] = 'Data Retrieved Successfully'
        else:
            data_dict['status'] = 'failure'
            data_dict['message'] = "No Data Found"
        return super(CustomJSONRenderer, self).render(data_dict, accepted_media_type, renderer_context)
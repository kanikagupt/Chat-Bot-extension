import json
from django.views import View
from django.http import JsonResponse
from core.Interfaces.CursorInterface import CursorInterface
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class CursorView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.interface = CursorInterface()

    def get(self, request, chat_id):
        res = self.interface.get_chats(chat_id)
        data = {
            "chat_id": chat_id,
            "messages": res
        }
        return JsonResponse(data)

    def post(self, request, chat_id):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        thread_id = data.get('thread_id')
        query = data.get('query')

        if not thread_id or not query:
            return JsonResponse({'error': 'thread_id and query are required'}, status=400)

        result = self.interface.chat_cursor(thread_id, query)
        return JsonResponse({'result': result})
    
class CursorChatListing(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.interface = CursorInterface()
    
    def get(self, request):
        res = self.interface.get_chat_ids()
        data = {
            "result": res
        }
        return JsonResponse(data)

    


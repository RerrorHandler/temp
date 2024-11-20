from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TempData, HumidityData
import json
from django.core.serializers import serialize
from datetime import datetime, timedelta
from django.db.models import Q
from django.utils.timezone import make_aware
from django.utils import timezone
from django.db.models import Avg
from django.views.decorators.http import require_GET
from django.core.serializers.json import DjangoJSONEncoder




@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        board_name = data.get('board_name', 'Arduino')

        TempData.objects.create(board_name=board_name, measure='temperature', data=temperature)
        HumidityData.objects.create(board_name=board_name, measure='humidity', data=humidity)

        return JsonResponse({'status': 'success'}, status=201)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def home(request):
    return render(request, 'home.html')



@require_GET
def temperature_data_api(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if start_date_str and end_date_str:
        start_date = datetime.fromisoformat(start_date_str)
        end_date = datetime.fromisoformat(end_date_str)

        board_names = TempData.objects.values_list('board_name', flat=True).distinct()
        temperature_data = []

        for board_name in board_names:
            board_data = TempData.objects.filter(board_name=board_name, created_at__range=(start_date, end_date)) \
                                         .annotate(avg_temp=Avg('data')) \
                                         .order_by('created_at')

            timestamps = [data.created_at.isoformat() for data in board_data]
            temperatures = [data.avg_temp if data.avg_temp else 'null' for data in board_data]
            
            temperature_data.append({
                'board_name': board_name,
                'timestamps': timestamps,
                'temperatures': temperatures,
            })

        return JsonResponse({'temperature_data': temperature_data})

    return JsonResponse({'error': 'Invalid request parameters'})

@require_GET
def humidity_data_api(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if start_date_str and end_date_str:
        start_date = datetime.fromisoformat(start_date_str)
        end_date = datetime.fromisoformat(end_date_str)

        board_names = HumidityData.objects.values_list('board_name', flat=True).distinct()
        humidity_data = []

        for board_name in board_names:
            board_data = HumidityData.objects.filter(board_name=board_name, created_at__range=(start_date, end_date)) \
                                             .annotate(avg_humidity=Avg('data')) \
                                             .order_by('created_at')

            timestamps = [data.created_at.isoformat() for data in board_data]
            humidities = [data.avg_humidity if data.avg_humidity else 'null' for data in board_data]
            
            humidity_data.append({
                'board_name': board_name,
                'timestamps': timestamps,
                'humidities': humidities,
            })

        return JsonResponse({'humidity_data': humidity_data})

    return JsonResponse({'error': 'Invalid request parameters'})

def latest_measurements(request):
    
    latest_temp_MRT = TempData.objects.filter(board_name='MRT').order_by('-created_at').first()
    latest_humidity_MRT = HumidityData.objects.filter(board_name='MRT').order_by('-created_at').first()
    
    
    MRT = {
        'temperature_MRT': latest_temp_MRT.data if latest_temp_MRT else None,
        'humidity_MRT': latest_humidity_MRT.data if latest_humidity_MRT else None,
        'temp_timestamp_MRT': latest_temp_MRT.created_at if latest_temp_MRT else None,
        'humidity_timestamp_MRT': latest_humidity_MRT.created_at if latest_humidity_MRT else None,
        'board_name_MRT': 'MRT'
    }

    latest_temp_resident = TempData.objects.filter(board_name='resident').order_by('-created_at').first()
    latest_humidity_resident = HumidityData.objects.filter(board_name='resident').order_by('-created_at').first()   

    resident = {
        'temperature_resident': latest_temp_resident.data if latest_temp_resident else None,
        'humidity_resident': latest_humidity_resident.data if latest_humidity_resident else None,
        'temp_timestamp_resident': latest_temp_resident.created_at if latest_temp_resident else None,
        'humidity_timestamp_resident': latest_humidity_resident.created_at if latest_humidity_resident else None,
        'board_name_resident': 'resident'
    }

    
    return render(request, 'latest_measurements.html', {'MRT': MRT, 'resident': resident})

def latest_measurements_data(request):
    # Get your latest measurements data
    temperature_MRT_data = TempData.objects.filter(board_name='MRT').order_by('-created_at').first()  # Assuming this is how you get your data
    humidity_MRT_data = HumidityData.objects.filter(board_name='MRT').order_by('-created_at').first()  # Adjust based on your model structure
    
    temperature_resident_data = TempData.objects.filter(board_name='resident').order_by('-created_at').first()
    humidity_resident_data = HumidityData.objects.filter(board_name='resident').order_by('-created_at').first()

    return JsonResponse({
        'temperature_MRT': temperature_MRT_data.data if temperature_MRT_data else None,
        'humidity_MRT': humidity_MRT_data.data if humidity_MRT_data else None,
        'temp_timestamp_MRT': temperature_MRT_data.created_at.strftime("%B %d, %Y, %H:%M:%S") if temperature_MRT_data else None,
        'humidity_timestamp_MRT': humidity_MRT_data.created_at.strftime("%B %d, %Y, %H:%M:%S") if humidity_MRT_data else None,
        'temperature_resident': temperature_resident_data.data if temperature_resident_data else None,
        'humidity_resident': humidity_resident_data.data if humidity_resident_data else None,
        'temp_timestamp_resident': temperature_resident_data.created_at.strftime("%B %d, %Y, %H:%M:%S") if temperature_resident_data else None,
        'humidity_timestamp_resident': humidity_resident_data.created_at.strftime("%B %d, %Y, %H:%M:%S") if humidity_resident_data else None,
    })

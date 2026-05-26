from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, ProductView, Design, RenderJob
from .tasks import process_customization_request
import json

def index(request):
    """Simple UI to test the flow"""
    products = Product.objects.all()
    return render(request, 'customizer/index.html', {'products': products})

@csrf_exempt
def upload_design(request):
    """API endpoint to upload design and start render job"""
    if request.method == 'POST':
        product_view_id = request.POST.get('product_view_id')
        image_file = request.FILES.get('design_image')
        
        if not product_view_id or not image_file:
            return JsonResponse({'error': 'Missing product_view_id or design_image'}, status=400)
            
        try:
            pv = ProductView.objects.get(id=product_view_id)
        except ProductView.DoesNotExist:
            return JsonResponse({'error': 'Invalid product_view_id'}, status=400)
            
        # Create Design
        design = Design.objects.create(image=image_file)
        
        # Create Render Job
        job = RenderJob.objects.create(
            design=design,
            product_view=pv,
            status='pending'
        )
        
        # Trigger celery task
        process_customization_request.delay(job.id)
        
        return JsonResponse({
            'message': 'Job started',
            'job_id': job.id
        })
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def check_status(request, job_id):
    """API endpoint to check job status"""
    try:
        job = RenderJob.objects.get(id=job_id)
        return JsonResponse({
            'job_id': job.id,
            'status': job.status,
            'result_image': job.result_image.url if job.result_image else None,
            'error_message': job.error_message
        })
    except RenderJob.DoesNotExist:
        return JsonResponse({'error': 'Job not found'}, status=404)


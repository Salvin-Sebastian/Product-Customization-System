from celery import shared_task
from .models import RenderJob
from .services.image_processor import process_customization
import os
from django.conf import settings
import traceback

@shared_task
def process_customization_request(job_id):
    try:
        job = RenderJob.objects.get(id=job_id)
        job.status = 'processing'
        job.save()

        pv = job.product_view
        design = job.design

        base_image_path = pv.base_image.path
        design_image_path = design.image.path
        
        # Output file logic
        filename = f"result_{job_id}.jpg"
        output_rel_path = os.path.join('results', filename)
        output_abs_path = os.path.join(settings.MEDIA_ROOT, output_rel_path)

        # Call OpenCV processing
        process_customization(
            base_image_path=base_image_path,
            design_image_path=design_image_path,
            print_x=pv.print_area_x,
            print_y=pv.print_area_y,
            print_w=pv.print_area_width,
            print_h=pv.print_area_height,
            output_path=output_abs_path
        )

        job.result_image.name = output_rel_path
        job.status = 'completed'
        job.save()

    except Exception as e:
        if 'job' in locals():
            job.status = 'failed'
            job.error_message = str(e) + "\n" + traceback.format_exc()
            job.save()
        raise e

import cv2
import numpy as np
import os

def process_customization(base_image_path, design_image_path, print_x, print_y, print_w, print_h, output_path):
    """
    Overlays a design onto a base product image with displacement mapping and realistic blending.
    """
    # Load images
    # We load base with alpha if it exists, though usually it's RGB
    base_img = cv2.imread(base_image_path)
    if base_img is None:
        raise ValueError(f"Could not load base image from {base_image_path}")
    
    # Load design with alpha channel
    design_img = cv2.imread(design_image_path, cv2.IMREAD_UNCHANGED)
    if design_img is None:
        raise ValueError(f"Could not load design image from {design_image_path}")

    # Ensure design has alpha channel
    if design_img.shape[2] == 3:
        design_img = cv2.cvtColor(design_img, cv2.COLOR_BGR2BGRA)

    # 1. Perspective Alignment (Scale to fit the print area)
    # Calculate scale preserving aspect ratio
    design_h, design_w = design_img.shape[:2]
    scale = min(print_w / design_w, print_h / design_h)
    new_w = int(design_w * scale)
    new_h = int(design_h * scale)
    
    resized_design = cv2.resize(design_img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Calculate padding to center it within the print area
    pad_x = (print_w - new_w) // 2
    pad_y = (print_h - new_h) // 2

    # Create a blank overlay the size of the base image
    base_h, base_w = base_img.shape[:2]
    overlay = np.zeros((base_h, base_w, 4), dtype=np.uint8)

    # Paste the resized design into the overlay at the correct coordinates
    start_x = print_x + pad_x
    start_y = print_y + pad_y
    overlay[start_y:start_y+new_h, start_x:start_x+new_w] = resized_design

    # 2. Displacement Mapping (Fabric Conformation)
    # Convert base image to grayscale to act as a displacement map
    base_gray = cv2.cvtColor(base_img, cv2.COLOR_BGR2GRAY)
    
    # Smooth the grayscale map slightly to avoid sharp noise displacements
    displacement_map = cv2.GaussianBlur(base_gray, (5, 5), 0)
    
    # Calculate gradients
    grad_x = cv2.Sobel(displacement_map, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(displacement_map, cv2.CV_32F, 0, 1, ksize=3)
    
    # Normalize gradients to create a shift map
    strength = 3.0 # Displacement strength
    map_x, map_y = np.meshgrid(np.arange(base_w), np.arange(base_h))
    
    map_x_32 = map_x.astype(np.float32) + (grad_x * strength / 255.0)
    map_y_32 = map_y.astype(np.float32) + (grad_y * strength / 255.0)
    
    # Warp the overlay based on the folds of the base image
    distorted_overlay = cv2.remap(overlay, map_x_32, map_y_32, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_TRANSPARENT)

    # 3. Realistic Blending (Multiply Blend)
    result = base_img.copy()
    
    # Multiply blend the distorted overlay onto the base image
    # Extract alpha mask
    alpha = distorted_overlay[:, :, 3] / 255.0
    
    for c in range(3):
        # Multiply blend formula: (Base * Overlay) / 255
        # Since overlay RGB values might be pre-multiplied or normal, we blend:
        # Base * (1 - Alpha) + (Base * Overlay / 255) * Alpha
        overlay_color = distorted_overlay[:, :, c]
        blended_color = (base_img[:, :, c].astype(np.float32) * overlay_color.astype(np.float32)) / 255.0
        
        result[:, :, c] = (base_img[:, :, c] * (1 - alpha) + blended_color * alpha).astype(np.uint8)

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the result
    cv2.imwrite(output_path, result)
    return output_path

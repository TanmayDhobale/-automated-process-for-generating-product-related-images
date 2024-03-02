import cv2
import os

def apply_design(product_path, design_path, output_path):
    # Load the product and design images
    product_image = cv2.imread(product_path)
    design = cv2.imread(design_path, cv2.IMREAD_UNCHANGED)  # Include alpha

    # Assume the design needs to be resized; change as needed
    design_resized = cv2.resize(design, (100, 100))  # Adjust based on the product

    # For simplicity, place the design on the center of the product
    x_offset = (product_image.shape[1] - design_resized.shape[1]) // 2
    y_offset = (product_image.shape[0] - design_resized.shape[0]) // 2

    for c in range(0,3):
        product_image[y_offset:y_offset+design_resized.shape[0], x_offset:x_offset+design_resized.shape[1], c] = \
            design_resized[:,:,c] * (design_resized[:,:,3]/255.0) +  product_image[y_offset:y_offset+design_resized.shape[0], x_offset:x_offset+design_resized.shape[1], c] * (1.0 - design_resized[:,:,3]/255.0)

    # Save the result
    cv2.imwrite(output_path, product_image)

# Example usage
if __name__ == "__main__":
    product_path = '../products/tshirt.png'
    design_path = '../designs/design1.png'
    output_path = 'tshirt_with_design.png'

    apply_design(product_path, design_path, output_path)
    print("Design applied and image saved to output folder.")

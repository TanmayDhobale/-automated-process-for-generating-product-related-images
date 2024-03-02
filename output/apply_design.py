import cv2
import os

def apply_design(product_path, design_path, output_path, new_width, new_height):
    print(f"Loading images... \nProduct: {product_path} \nDesign: {design_path}")
    
    # Check if the files exist
    if not os.path.exists(product_path):
        print(f"Product image not found at {product_path}")
        return
    if not os.path.exists(design_path):
        print(f"Design image not found at {design_path}")
        return

    product_img = cv2.imread(product_path)
    design_img = cv2.imread(design_path, -1)  # Load with transparency

    if product_img is None or design_img is None:
        print("Error loading images. Please check the paths.")
        return
    else:
        print("Images loaded successfully.")

    # Resize the design image
    design_resized = cv2.resize(design_img, (new_width, new_height))
    print(f"Design resized to {new_width}x{new_height}")

    # Calculate the center position
    x_offset = (product_img.shape[1] - new_width) // 2
    y_offset = (product_img.shape[0] - new_height) // 2
    print(f"Applying design at position: {x_offset}, {y_offset}")

    # Apply the design
    for c in range(0, 3):
        alpha = design_resized[:, :, 3] / 255.0  # Alpha channel from the design
        product_img[y_offset:y_offset+design_resized.shape[0], x_offset:x_offset+design_resized.shape[1], c] = \
            alpha * design_resized[:, :, c] + \
            product_img[y_offset:y_offset+design_resized.shape[0], x_offset:x_offset+design_resized.shape[1], c] * (1 - alpha)

    # Save the output
    if cv2.imwrite(output_path, product_img):
        print(f"Design applied and image saved to: {output_path}")
    else:
        print("Failed to save the image. Check the output path and permissions.")

# Example usage
if __name__ == "__main__":
    product_path = '../products/tshirt.png'  # Adjust this path if necessary
    design_path = '../designs/design1.png'  # Adjust this path if necessary
    output_path = 'tshirt_with_design.png'  # This is where the output will be saved

    # Example resizing parameters
    new_width = 200
    new_height = 200

    apply_design(product_path, design_path, output_path, new_width, new_height)

    print("Design applied and image saved to output folder.")

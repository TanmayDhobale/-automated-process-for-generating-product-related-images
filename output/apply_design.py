import cv2
import numpy as np

def apply_design_and_remove_background(product_path, design_path, output_path, new_width, new_height):
    product_img = cv2.imread(product_path)
    design_img = cv2.imread(design_path, -1)  # Load with transparency

    if product_img is None or design_img is None:
        print("Error loading images. Please check the paths.")
        return


    hsv_img = cv2.cvtColor(product_img, cv2.COLOR_BGR2HSV)

  
    lower_val = np.array([0, 0, 0])
    upper_val = np.array([0, 0, 255])

 
    mask = cv2.inRange(hsv_img, lower_val, upper_val)
    mask_inv = cv2.bitwise_not(mask)

    
    product_img_bg_black = cv2.bitwise_and(product_img, product_img, mask=mask_inv)

    # Resize and apply the design onto the t-shirt
    design_resized = cv2.resize(design_img, (new_width, new_height))
    x_offset = (product_img.shape[1] - new_width) // 2
    y_offset = (product_img.shape[0] - new_height) // 2

    for c in range(0, 3):
        alpha = design_resized[:, :, 3] / 255.0
        product_img_bg_black[y_offset:y_offset+design_resized.shape[0], x_offset:x_offset+design_resized.shape[1], c] = \
            alpha * design_resized[:, :, c] + \
            product_img_bg_black[y_offset:y_offset+design_resized.shape[0], x_offset:x_offset+design_resized.shape[1], c] * (1 - alpha)

    # Save the result
    cv2.imwrite(output_path, product_img_bg_black)
    print("Design applied with background removed. Image saved to:", output_path)


if __name__ == "__main__":
    product_path = '../products/tshirt.png'  
    design_path = '../designs/design1.png' 
    output_path = 'tshirt_with_design.png'  

    new_width = 200
    new_height = 200

       
    apply_design_and_remove_background(product_path, design_path, output_path, new_width, new_height)

import cv2
import numpy as np
import pandas as pd

def closest_color_name(r, g, b, colors_df):
    distances = np.sqrt((colors_df['r'] - r) ** 2 + (colors_df['g'] - g) ** 2 + (colors_df['b'] - b) ** 2)
    return colors_df.loc[distances.idxmin(), 'name']

def show_color(event, x, y, flags, param):
    global display_image, image, colors_df

    if event == cv2.EVENT_LBUTTONDOWN:
        display_image = image.copy()
        b, g, r = image[y, x]
        r, g, b = int(r), int(g), int(b)
        name = closest_color_name(r, g, b, colors_df)

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 1

        name_text = name.upper()
        rgb_text = f"({r},{g},{b})"

        (name_w, name_h), _ = cv2.getTextSize(name_text, font, font_scale, thickness)
        (rgb_w, rgb_h), _ = cv2.getTextSize(rgb_text, font, font_scale, thickness)

        box_size = 40
        padding = 10
        box_w = padding * 3 + box_size + max(name_w, rgb_w)
        box_h = padding * 2 + max(name_h + rgb_h + 10, box_size)

        box_x = x + 10
        box_y = y - box_h // 2

        if box_x + box_w > image.shape[1]:
            box_x = x - box_w - 10
        if box_y < 0:
            box_y = 0
        if box_y + box_h > image.shape[0]:
            box_y = image.shape[0] - box_h

        
        cv2.rectangle(display_image, (box_x - 1, box_y - 1), (box_x + box_w + 1, box_y + box_h + 1), (0, 0, 0), -1)
        
        cv2.rectangle(display_image, (box_x, box_y), (box_x + box_w, box_y + box_h), (255, 255, 255), -1)
        
        color_box_x = box_x + padding
        color_box_y = box_y + padding
        cv2.rectangle(display_image, (color_box_x, color_box_y), (color_box_x + box_size, color_box_y + box_size), (b, g, r), -1)
        cv2.rectangle(display_image, (color_box_x, color_box_y), (color_box_x + box_size, color_box_y + box_size), (0, 0, 0), 1)

        
        cv2.circle(display_image, (x, y), 3, (0, 0, 0), -1)

       
        text_x = color_box_x + box_size + padding
        text_y = color_box_y + 15
        cv2.putText(display_image, name_text, (text_x, text_y), font, font_scale, (0, 0, 0), thickness)
        cv2.putText(display_image, rgb_text, (text_x, text_y + 20), font, font_scale, (0, 0, 0), thickness)

def main():
    global display_image, image, colors_df

    
    colors_df = pd.read_csv(r"C:\Users\Mayada AbouZeid\Pictures\colors.csv") # CSV file contains all colors with RGB

    image_path = input("Enter full path of image: ").strip()
    image = cv2.imread(image_path)

    if image is None:
        print("Image not found. Check the path.")
        return

    image = cv2.resize(image, (640, 480))
    display_image = image.copy()

    print("Left click anywhere on the image to detect color. Press ESC to exit.")
    cv2.namedWindow("Color Detection")
    cv2.setMouseCallback("Color Detection", show_color)

    while True:
        cv2.imshow("Color Detection", display_image)
        if cv2.waitKey(1) & 0xFF == 27:  

            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

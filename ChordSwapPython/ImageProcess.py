import cv2
import os
import Modify as mo
import Transpose as tr

def process_image(image_path, ocr_result, half_steps, save_directory='chord_image'):
    img = cv2.imread(image_path)
    roi_img = img.copy()
    font_italic = cv2.FONT_ITALIC

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    for field in ocr_result['images'][0]['fields']:
        text = field['inferText']
        first_char = text[0] if len(text) > 0 else ''

        if first_char.isupper() and first_char in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
            vertices_list = field['boundingPoly']['vertices']
            pts = [tuple(vertice.values()) for vertice in vertices_list]
            topLeft = [int(_) for _ in pts[0]]
            bottomRight = [int(_) for _ in pts[2]]

            fill_img = cv2.rectangle(roi_img, tuple(topLeft), tuple(bottomRight), (255, 255, 255), thickness=-1)
            modified_text = mo.modify_text(text)
            transposed_chord = tr.transpose_chord(modified_text, half_steps)
            
            new_code = cv2.putText(fill_img, transposed_chord, (topLeft[0], topLeft[1] + 10), font_italic, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

            crop_img = img[topLeft[1]:bottomRight[1], topLeft[0]:bottomRight[0]]
            file_name = f"{save_directory}/{transposed_chord}.png"
            cv2.imwrite(file_name, crop_img)

    return roi_img

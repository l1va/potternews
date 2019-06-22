import numpy as np
import cv2
import imageio

templates_folder = 'templates/'
animations_folder = 'animations/'
gifs_folder = 'results/gifs/'
template_name = 'template3_cropped.jpg'
animation_name = 'telka.mp4'
gif_name = 'newspaper.gif'

scale_factor = 4
if template_name == 'template4.jpg':
    position = [230, 430]
    desired_size = [580, 380]
elif template_name == 'template3_cropped.jpg':
    position = [200, 300]
    desired_size = [400, 200]

position = [int(x/scale_factor) for x in position]
desired_size = [int(x/scale_factor) for x in desired_size]
cv2.namedWindow("output", cv2.WINDOW_NORMAL)
cv2.namedWindow("template", cv2.WINDOW_NORMAL)

# Load an color image in grayscale
template = cv2.imread('{}{}'.format(templates_folder,
                                    template_name), cv2.IMREAD_COLOR)
cv2.imshow('template', template)
cv2.waitKey(0)
cv2.destroyAllWindows()

template = cv2.resize(template, None, fx=1/scale_factor, fy=1/scale_factor)


print(template.shape)
cap = cv2.VideoCapture('{}{}'.format(animations_folder,
                                     animation_name))

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video stream or file")
else:
    anim_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    anim_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

images = []
# Read until video is completed
with imageio.get_writer('{}{}'.format(gifs_folder,
                                      gif_name), mode='I', fps=25) as writer:
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            output = template.copy()
            anim_frame = cv2.resize(
                frame, tuple(desired_size))
            anim_shape = anim_frame.shape
            anim_h, anim_w = anim_shape[1], anim_shape[0]
            output[position[0]:position[0]+anim_w,
                   position[1]: position[1]+anim_h] = anim_frame

            # output_resized = cv2.resize(output, None, fx=0.25, fy=0.25)
            output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
            cv2.imshow('output', output)
            writer.append_data(output)
            # Press Q to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

# When everything done, release the video capture object
cap.release()

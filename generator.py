from PIL import Image, ImageDraw

from Box import Box


# Define the size of the image in inches
width_inches = 8.5
height_inches = 11

height = 1.75
thickness = .25

outer_width = 4
outer_length = 6


# Define the DPI of the image
dpi = 300

inner_dimensions = (outer_width,outer_length,height,thickness)


t = thickness

total_length = 2*(.5 + inner_dimensions[2])+inner_dimensions[1]
total_width = 2*(.5 + inner_dimensions[2])+inner_dimensions[0]

margin_length = height_inches-total_length
margin_width = width_inches-total_width

recommended_width = width_inches-2*height-1
recommended_length = height_inches-2*height-1

recommended_height_w = (width_inches-inner_dimensions[0]-1)/2
recommended_height_l = (height_inches-inner_dimensions[1]-1)/2

recommended_height = min(recommended_height_w,recommended_height_l)


print(f"  Total Paper Width:                   {total_width:.2f} ({margin_width:.2f}) \
      \n  Total Paper Length:                  {total_length:.2f} ({margin_length:.2f}) \
      \n  Box Dimensions (W x L x H):          {inner_dimensions[0]:.2f} X {inner_dimensions[1]:.2f} X {inner_dimensions[2]:.2f}\
      \n  Recommended Max (W x L) for {inner_dimensions[2]:.2f}:    {recommended_width:.2f} x {recommended_length:.2f} \
      \n  Recommended Max (H) for {inner_dimensions[0]:.2f} X {inner_dimensions[1]:.2f}:    {recommended_height}")

box = Box(width_inches,height_inches,dpi,inner_dimensions,t)
box.image_create()
box.draw_solid_box()
box.draw_wrap()



box.img.show()

# # Save the image as a PNG file
box.img.save("output.png", dpi=(dpi, dpi))


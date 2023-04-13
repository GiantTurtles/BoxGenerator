from PIL import Image, ImageDraw
import math
from points import point_collection

class Box():
    def __init__(self, width,height,dpi,inner_dimensions,t):
      
      # Calculate the size of the image in pixels
      self.digital_width = int(width * dpi)
      self.digital_height = int(height * dpi)

      self.center = (self.digital_width/(2*dpi),self.digital_height /(2*dpi))
      self.dpi = dpi
      self.inner_width = inner_dimensions[0]
      self.inner_length = inner_dimensions[1]
      self.inner_height = inner_dimensions[2]
      self.t = t

      self.flap_width = .5
      self.inset_flap = self.flap_width/2

      self.arc_length = 1.52*t


    def image_create(self):
      # Create a new image with a white background
      self.img = Image.new("RGB", (self.digital_width, self.digital_height), "white")

      # Set the DPI of the image
      self.img.info["dpi"] = (self.dpi, self.dpi)

      # Create a drawing context
      self.draw = ImageDraw.Draw(self.img)

    def draw_solid_box(self):
      inner_box,_ = self.compile_box("inner")
      solids = line_to_pixel(inner_box,self.dpi)

      # Draw the lines
      for line in solids:
          self.draw.line(line, fill="black", width=2)

    def draw_wrap(self):
      wrap,incision = self.compile_box("outer")
      dashes = line_to_pixel(wrap,self.dpi)



      # Draw the lines
      for line in dashes:
          draw_dashed(self.draw,line)
          # self.draw.line(line, fill="black", width=2)

      incision = double_mirror(self.center,[incision])
      incisions = line_to_pixel(incision,self.dpi)
      for cut in incisions:
        self.draw.line(cut, fill="black", width=5)

      # all_circles = double_mirror(self.center,circle_points)

      # for circle_points in all_circles:
      #   draw_circle(self.draw,circle_points,self.dpi)


    def compile_box(self,line_type):
      points = {}
      box_points = []
      circle_points = []
      

      points,out_points,circle_points = point_collection(line_type,self.center,self.inner_width,self.inner_height,self.inner_length,self.t,self.inset_flap,self.flap_width)


      box_points = multi_mirror_points(self.center,points)
      out_points = double_mirror(self.center,out_points)
    
      box_points = box_points + out_points

      return box_points,circle_points
    
def double_mirror(center,points):
  output = []
  for pair in points:
    dy_0 = abs(pair[0][1]-center[1])
    dx_0 = abs(pair[0][0]-center[0])

    dy_1 = abs(pair[1][1]-center[1])
    dx_1 = abs(pair[1][0]-center[0])
    output.append([(center[0]+dx_0,pair[0][1]),(center[0]+dx_1,pair[1][1])])
    output.append([(pair[0][0],center[1]+dy_0),(pair[1][0],center[1]+dy_1)])
    output.append([(center[0]+dx_0,center[1]+dy_0),(center[0]+dx_1,center[1]+dy_1)])
  return points + output


def mirror_points(center,initial_point,direction):
    if direction == "h":
      final_point = (initial_point[0]+2*(center[0]-initial_point[0]),initial_point[1])
    elif direction == "v":
      final_point = (initial_point[0],initial_point[1]+2*(center[1]-initial_point[1]))

    return [initial_point,final_point]

def line_to_pixel(lines,dpi):
   # Convert the line coordinates to pixels
  pixel_lines = []
  for line in lines:
      pixel_line = []
      for point in line:
          pixel_point = (int((point[0]) * dpi), int((point[1]) * dpi))  # Convert from inches to pixels
          pixel_line.append(pixel_point)
      pixel_lines.append(pixel_line)
  return pixel_lines

def multi_mirror_points(center,points):
    mirrored_points = []

    for point in points.items():
      if "horizontal" in point[0]:
        mirrored_points = mirrored_points + [mirror_points(center,point[1],"h")]
      elif "vertical" in point[0]:
        mirrored_points = mirrored_points + [mirror_points(center,point[1],"v")]
    return mirrored_points



def draw_dashed(draw,line, dashlen=10, ratio=2,width=2): 
    x0 = line[0][0]
    y0 = line[0][1]
    x1 = line[1][0]
    y1 = line[1][1]

    dx=x1-x0 # delta x
    dy=y1-y0 # delta y
    # check whether we can avoid sqrt

    if dy==0: len=dx
    elif dx==0: len=dy
    else: len=math.sqrt(dx*dx+dy*dy) # length of line
    xa=dx/len # x add for 1px line length
    ya=dy/len # y add for 1px line length
    step=dashlen*ratio # step to the next dash
    a0=0

    if len > 0:
      while a0<len:
          a1=a0+dashlen
          if a1>len: a1=len
          draw.line((x0+xa*a0, y0+ya*a0, x0+xa*a1, y0+ya*a1), fill = (0,0,0),width=width)
          a0+=step 
    else:
      while a0>len:
          a1=a0-dashlen
          if a1<len: a1=len
          draw.line((x0+xa*a0, y0+ya*a0, x0+xa*a1, y0+ya*a1), fill = (0,0,0),width=width)
          a0-=step 
    

def draw_circle(draw,circle_points,dpi):
        circle_points = [[int(x*dpi) for x in y] for y in circle_points]

        a = circle_points[0][0]
        b = circle_points[0][1]
        c = circle_points[1][0]
        d = circle_points[1][1]

        if a < c:
           circle_points[0][0] = a
           circle_points[1][0] = c
        elif c < a:
           circle_points[0][0] = c
           circle_points[1][0] = a

        if b < d:
           circle_points[0][1] = b
           circle_points[1][1] = d
        elif d < b:
           circle_points[0][1] = d
           circle_points[1][1] = b

        draw.ellipse((circle_points[0][0],circle_points[0][1],circle_points[1][0],circle_points[1][1]),fill = 'grey',outline='black')
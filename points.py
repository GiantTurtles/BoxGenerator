def point_collection(line_type,center,inner_width,inner_height,inner_length,t,inset_flap,flap_width):
    points = {}
    out_points = []
    incision = []

    if line_type == 'inner':
        points['horizontal_big_top'] = (center[0] - inner_width/2,center[1] - inner_length/2)
        points['horizontal_big_bottom'] = (center[0] - inner_width/2,center[1] + inner_length/2)
        points['horizontal_small_top'] = (center[0] - inner_width/2,center[1] - inner_length/2 - inner_height)
        points['horizontal_small_bottom'] = (center[0] - inner_width/2,center[1] + inner_length/2 + inner_height)

        long_side_1 = (center[0] - inner_width/2-inner_height,center[1] - inner_length/2+t)
        long_side_2 = (center[0] - inner_width/2,center[1] - inner_length/2+t)

        points['vertical_small_left'] = (center[0] - inner_width/2-inner_height,center[1] + inner_length/2-t)
        points['vertical_small_right'] = (center[0] + inner_width/2+inner_height,center[1] - inner_length/2+t)
        points['vertical_big_left'] = (center[0] - inner_width/2,center[1] - inner_length/2 - inner_height)
        points['vertical_big_right'] = (center[0] + inner_width/2,center[1] + inner_length/2 + inner_height)

        out_points.append([long_side_1,long_side_2])
    else:
        points['horizontal_big_top'] = (center[0] - inner_width/2-inner_height-1.2*t,center[1] - inner_length/2)
        points['horizontal_big_bottom'] = (center[0] - inner_width/2-inner_height-1.2*t,center[1] + inner_length/2)
        points['vertical_big_left'] = (center[0] - inner_width/2,center[1] - inner_length/2 - inner_height-1.2*t)
        points['vertical_big_right'] = (center[0] + inner_width/2,center[1] + inner_length/2 + inner_height+1.2*t)

        # points['horizontal_base_top'] = (center[0] - inner_width/2-t,center[1] - inner_length/2 - t)
        # points['horizontal_base_bottom'] = (center[0] - inner_width/2-t,center[1] + inner_length/2 + t)
        vertical_base_left = (center[0] - inner_width/2,center[1] - inner_length/2 )
        vertical_base_right = (center[0] + inner_width/2+t,center[1] + inner_length/2 )

        points['horizontal_top_top'] = (vertical_base_left[0]-(.5-t)/2-t, center[1] - inner_length/2  - inner_height)
        points['horizontal_bottom_bottom'] = (center[0] - inner_width/2-t, center[1] + inner_length/2  + inner_height)
        points['vertical_left_left'] = (center[0] - inner_width/2-inner_height, center[1] - inner_length/2)
        points['vertical_right_right'] = (center[0] + inner_width/2+inner_height, center[1] + inner_length/2)

        points['horizontal_flap_top'] = (center[0] - inner_width/2+inset_flap,center[1] - inner_length/2  - inner_height-flap_width)
        points['horizontal_flap_bottom'] = (center[0] - inner_width/2+inset_flap,center[1] + inner_length/2  + inner_height+flap_width)
        points['vertical_flap_left'] = (center[0] - inner_width/2-inner_height-flap_width,center[1] - inner_length/2+inset_flap)
        points['vertical_flap_right'] = (center[0] + inner_width/2+inner_height+flap_width,center[1] + inner_length/2-inset_flap)

        #WRAP Full Mirror
        main_diag_in = (vertical_base_left[0]-t,vertical_base_left[1])
        main_diag_out =  (points['horizontal_top_top'][0],vertical_base_left[1]-(.5-t)/2)

        short_perp_bottom = main_diag_out
        short_perp_top = (short_perp_bottom[0],points['horizontal_top_top'][1])



        short_long_diag = (points['horizontal_flap_top'],points['vertical_big_left'])

        long_long_diag = [points['vertical_flap_left'],points['horizontal_big_top']]

        incision = (main_diag_in,vertical_base_left)


        out_points.append([main_diag_in,main_diag_out])
        out_points.append([short_perp_bottom,short_perp_top])

        out_points = out_points + [long_long_diag,short_long_diag]

    return points,out_points,incision
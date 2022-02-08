import cv2
import matplotlib.pyplot as plt
import numpy as np
import constants
import colors


def ConnectedCompFunction(image):

    numlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(image, 4, cv2.CV_32S)
    cX=[]
    cY=[]
    # loop over the number of unique connected component labels
    for i in range(1, numlabels):
        area = stats[i, cv2.CC_STAT_AREA]
        # return the index of the largest area component except the 1st

        # print(stats[i,cv2.CC_STAT_AREA])
        if (centroids.size > 2) and (stats[i, cv2.CC_STAT_AREA] > 80) and (
                stats[i, cv2.CC_STAT_AREA] < 4000) and stats[i, cv2.CC_STAT_WIDTH] < 58 \
                and stats[i,cv2.CC_STAT_HEIGHT]>10 and stats[i,cv2.CC_STAT_HEIGHT]<200:
            (cX2, cY2) = centroids[i]
            cX.append(cX2)
        # else:
        #     cX.append(0)

    for j in reversed(range(0, len(cX))):
        for jj in reversed(range(0, j)):
            if abs(cX[j]-cX[jj]) <= 8:
                del(cX[jj])
                break

    return cX

def extract_bands(list):

    first = sorted_list[0][1]
    second = sorted_list[1][1]
    third = sorted_list[2][1]

    bands = len(sorted_list)
    print("Bands", bands)
    if bands ==3:
        OhmValue = int(str(constants.const[first]['value']) + str(constants.const[second]['value']))\
                       * constants.const[third]['multiply']
        tolerance = "20%"
        print("Colors:", constants.const[first]['name'], constants.const[second]['name'],
              constants.const[third]['name'])

        print("Ohm Value: "+"{:.2e}".format(OhmValue))
        print("Tolerance: \u00B1"+tolerance)
    elif bands == 4:
        fourth = sorted_list[3][1]
        OhmValue = int(str(constants.const[first]['value']) + str(constants.const[second]['value'])) \
                   * constants.const[third]['multiply']
        tolerance = str(constants.const[fourth]['tolerance'])+" %"
        print("Colors:", constants.const[first]['name'], constants.const[second]['name'],
              constants.const[third]['name'], constants.const[fourth]['name'])

        print("Ohm Value: ", "{:.2e}".format(OhmValue))
        print("Tolerance: \u00B1" + tolerance)
    elif bands == 5:
        fourth = sorted_list[3][1]
        fifth = sorted_list[4][1]
        OhmValue = int(str(constants.const[first]['value']) + str(constants.const[second]['value']) +
                       str(constants.const[third]['value'])) * constants.const[fourth]['multiply']
        tolerance = str(constants.const[fifth]['tolerance'])+" %"
        print("Colors:", constants.const[first]['name'], constants.const[second]['name'],
              constants.const[third]['name'], constants.const[fourth]['name'],constants.const[fifth]['name'])
        print("Ohm Value: ", "{:.2e}".format(OhmValue))
        print("Tolerance: \u00B1"+tolerance)
    elif bands == 6:
        fourth = sorted_list[3][1]
        fifth = sorted_list[4][1]
        sixth = sorted_list[5][1]
        OhmValue = int(
            str(constants.const[first]['value']) + str(constants.const[second]['value']) +
            str(constants.const[third]['value'])) * constants.const[fourth]['multiply']
        tolerance = str(constants.const[fifth]['tolerance']) + " %"
        temperature = str(constants.const[sixth]['temp']) + " ppm/K"
        print("Colors:", constants.const[first]['name'], constants.const[second]['name'],
              constants.const[third]['name'], constants.const[fourth]['name'],
              constants.const[fifth]['name'], constants.const[sixth]['name'])
        print("Ohm Value: ", "{:.2e}".format(OhmValue))
        print("Tolerance: \u00B1"+tolerance)
        print("Temperature coeff: "+temperature)
    else:
        print("ERROR: The system deteced wrong number of bands")

def search4colors(im):
    color_loc = []
    resmask = 0
    for i in range(12):
        if i == 2:
            mask = cv2.inRange(median, colors.lows[i], colors.highs[i])
            mask = mask + cv2.inRange(median, colors.red_low2, colors.red_up2)
            resmask = mask + resmask
        elif i==10:
            mask = cv2.inRange(median, colors.lows[i], colors.highs[i])
            a = ConnectedCompFunction(mask)
            if len(a)!=1:
                mask = cv2.inRange(median, colors.gold2_low, colors.gold2_up)

        else:
            mask = cv2.inRange(median, colors.lows[i], colors.highs[i])
            resmask = mask + resmask
        a = ConnectedCompFunction(mask)
        if a:
            for j in a:
                color_loc.append((j, i))
        resmask = mask + resmask
    return color_loc, resmask

def sorting_algorithm(mylist):
    sorted_list = sorted(mylist, key=lambda x: x[0])
    print("Sorted: ", sorted_list)

    nontoler = (0, 3, 4, 9)
    if sorted_list[0][1] >= 10:
        sorted_list = list(reversed(sorted_list))
    elif sorted_list[-1][1] in nontoler:
        sorted_list = list(reversed(sorted_list))
    return sorted_list

# cv2.namedWindow("out/put", cv2.WINDOW_NORMAL)    # Create window with freedom of dimensions
# image = cv2.imread("Images/realR.jpeg")
# image = cv2.imread("Images/r100koms.png")
# image = cv2.imread("Images/resistor-band-code.jpg")
# image = cv2.imread("Images/resistor-band-code2.jpg")
image = cv2.imread("Images/tan-fixed-resistors.jpg")
# image = cv2.imread("Images/resistor-5-color-bands.png")
# image = cv2.imread("Images/Metal_film_resistor.jpg")
# image = cv2.imread("Images/electrical-resistors.jpg")
# image = cv2.imread("Images/download.png")
# image = cv2.imread("Images/Screenshot2.jpg")



rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
median = cv2.medianBlur(hsv, 5)  # Apply a median filter for denoising
# edges = cv2.Canny(median, 50, 150, apertureSize=3)

resmask = cv2.inRange(median, colors.light_blue, colors.dark_blue)
a=ConnectedCompFunction(resmask)
print(a)
#
mylist,resmask=search4colors(median)
print("Color_loc:", mylist)

sorted_list=sorting_algorithm(mylist)
print("After check:",sorted_list)

extract_bands(sorted_list)

plt.subplot(2, 1, 1)
plt.title("mask")
plt.imshow(resmask)
plt.subplot(2, 1, 2)
plt.title("RGB")
plt.imshow(rgb)

plt.show()

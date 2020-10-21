#!/usr/bin/env python3
import cv2
import numpy as np
import cv2
import os
from time import sleep

cap = cv2.VideoCapture(2)

if __name__=='__main__':
    n_splits = int(os.environ['N_SPLITS'])
    print('N_SPLITS set to {}'.format(n_splits))

    colourmap = {'red': [np.array([0,0,0]), np.array([15,255,255]), np.array([155,0,0]), np.array([179,255,255])],
                 'yellow': [np.array([16,0,0]), np.array([42,255,255])],
                 'green': [np.array([42,0,0]), np.array([75,255,255])],
                 'cyan': [np.array([76,0,0]), np.array([105,255,255])],
                 'blue': [np.array([106,0,0]), np.array([125,255,255])],
                 'purple': [np.array([126,0,0]), np.array([154,255,255])]}
    lower_red = np.array([0,0,0])
    upper_red = np.array([30,255,255])

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        #Put here your code!
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            ind = np.arange(0,frame.shape[0],round(frame.shape[0]/n_splits)).tolist()
            ind.append(frame.shape[0])

            for i in range(len(ind)-1):
                ind_start = ind[i]
                ind_end = ind[i+1]
                frame_split = frame[ind_start:ind_end,:,:]
                mask = cv2.inRange(frame_split, lower_red, upper_red)
                
                frame_dim = frame_split.shape[0]*frame_split.shape[1]
                
                colours = {}

                colour_count = 0
                dom_colour = ''
                for c in colourmap:
                    if c=='red':
                        cur_colour_count = np.sum(cv2.inRange(frame_split, colourmap['red'][0], colourmap['red'][1])!=0) \
                        + np.sum(cv2.inRange(frame_split, colourmap['red'][2], colourmap['red'][3])!=0)
                    else:
                        cur_colour_count = np.sum(cv2.inRange(frame_split, colourmap[c][0], colourmap[c][1])!=0)
                    if cur_colour_count > colour_count:
                        colour_count = cur_colour_count
                        dom_colour = c

                print('Segment {} of {}, major colour is {}.'.format(i, len(ind)-2, dom_colour))

        else:
            print('Image read failed! Check that duckiebot-interface is not running.')

        sleep(1)
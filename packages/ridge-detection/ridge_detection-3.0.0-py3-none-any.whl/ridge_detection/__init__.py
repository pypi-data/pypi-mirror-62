__version__ = "3.0.0"

"""
0.0.1 first running version
0.0.2 change the structures of the package
0.0.3 vectorization critical 'convolve_row_gauss' and 'convolve_cols_gauss' and optimized 'convolve_gauss' flow
0.0.4 added function to skeletonize the detected lines
0.0.5 speed up the code precalculating the '_ctable' table of Correct obj in width.py:
      It took 0.002 second per call but it was called for each point found. Now it is called for each lines ( e.g: 80 times instead of 22000)
1.0.0 First stable version and optimized version. Added all the tests
1.0.1 Added a logger . The code generates the 'ridge_detection_X_Y.log' file. Where X=day Y=starting time
1.1.0 Moved the function called and implemented in the main.py in the helper.py to make the package uploadable to pipy 
1.2.0 Add GUI
1.3.0 First stable GUI version
1.3.2 Added info guis
2.0.0 first stable version with GUI
2.0.1 added a way to select the output directory when you save the results
3.0.0 added the posiibility to set the mandatory parameter via optional parameter as specified in the paper
"""

#todo
"""
2) the functionality "estimate width" is high buggy
"""
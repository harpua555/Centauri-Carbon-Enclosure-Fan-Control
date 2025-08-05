# Centauri-Carbon-Enclosure-Fan-Control
Post-processing script to control the CC enclosure/exhaust fan

*** USE AT YOUR OWN RISK, AND ALWAYS VERIFY GCODE OUTPUT SAFETY BEFORE PRINTING! ***

Currently (8/5/25) there is a bug in the CC firmware that causes the enclosure fan to either be forced to 100% or 0% based on material being printed.  Between layer gcode can be used to override this at the start of every layer, however on longer ( >60 sec) layers, the firmware will re-override whatever value was set.

This post-processing script can be added in the slicer (Global -> Others -> Post-processing Scripts) to insert a P3 (enclosure) fan speed instruction every x number of lines.  The default number of lines is 20.

When the script runs, a terminal window will open.  Here, you will enter the fan speed in % as well as the frequency of insertion in lines.  The script will then go through the gcode file and insert M106 P3 S<value> at the selected interval.

The script is set up to ONLY insert these commands between the start of LAYER 0 and the end of LAYER <last>.  For this script to funtion, you MUST have the correct before layer change G-code and Layer change G-code configured in the machine settings of your slicer.

Before layer change must include:
;BEFORE_LAYER_CHANGE
;[layer_z]

Layer change must include:
;LAYER:{layer_num+1}
SET_PRINT_STATS_INFO CURRENT_LAYER={layer_num + 1}




Usage:
To use this script, if you have python set up system-wide you can simply enter the direct path to the python script in the post processing scripts field.  Otherwise, this can be wrapped in a batch file.  I have included the .py and a sample .bat for reference.

*** USE AT YOUR OWN RISK, AND ALWAYS VERIFY GCODE OUTPUT SAFETY BEFORE PRINTING! ***

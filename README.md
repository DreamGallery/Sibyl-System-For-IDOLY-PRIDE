# Generate_Ass_File_For_IDOLY_PRIDE
Auto generate subtitle file of aegisub for IDOLY PRIDE through game file.

Also Using `OPENCV2` to fix timeline of subtitle frame by frame.

This tool is based on `MalitsPlus/HoshimiToolkit`, you need to get the subtitle file in game through `HoshimiToolkit`,<br /> the name of required file will usually be `adv_***.txt`.


# Usage

install requirement
```
pip3 install -r requirements.txt
```

edit `[Info]` in `config.ini` first, put game subtitle file in `ass/txt`, and the `.ass` file will be saved in `adv/ass`.

generate .ass file without time-fix

```
python generate.py
```

to use the time-fix options you should put your video file in `ass/video` , <br />the fps of video should be 30 or 60, and the recommended resolution is 1920x1080 <br />or you can change the `[Font Config]` youself in `config.ini` to fit your video.

generate .ass file with time-fix
```
python main.py
```



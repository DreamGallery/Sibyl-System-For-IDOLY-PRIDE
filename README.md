# Generate_Ass_File_For_IDOLY_PRIDE
Auto generate subtitle file of aegisub for IDOLY PRIDE through game file.

Also Using `CV2` to fix timeline of subtitle frame by frame.

# Usage

install requirement
```
pip3 install -r requirements.txt
```

edit `config.py` first, the `.ass` file will be saved in `adv/ass`

generate .ass file without time-fix

```
python generate.py
```

put video file in `ass/video` and put game subtitle file in `ass/txt`, 

generate .ass file with time-fix
```
python main.py
```



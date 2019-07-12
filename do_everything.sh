cp offline_learn.txt resultado/offline_learn.txt
python online_qtable.py
python offline_qtable.py
yes | ffmpeg -r 60 -i resultado/online_heatmap/im_%04d.png -vcodec libx264rgb resultado/heatmap.mp4 -hide_banner
rm -rf qtables/*

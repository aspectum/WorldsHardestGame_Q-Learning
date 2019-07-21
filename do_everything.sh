cp offline_learn.txt result/offline_learn.txt
python heatmap_online_qtable.py
python heatmap_offline_qtable.py
yes | ffmpeg -r 60 -i result/online_heatmap/im_%04d.png -vcodec libx264rgb result/heatmap.mp4 -hide_banner
rm -rf qtables/*

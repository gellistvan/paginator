if (($# <2)) 
then
	echo "Missing arguments, music, output"
	exit
fi


news=$(ls *.mp3 |cut -d "." -f 1)
bcg=$(echo $1 | cut -d "." -f 1)
touch list.txt
touch lenin.txt

sumlen=0
for x in $news; do
    if [[ $x == $bcg ]]; then
		echo "Skipping background";
	else
	  lenstr=$(./ffmpeg.exe -i $x.mp3 2>&1 | grep Duration| cut -d " " -f 4 |cut -d "." -f 1;)
	  arrIN=(${lenstr//:/ })
	  lenint=$((10#${arrIN[0]}*3600 + 10#${arrIN[1]}*60 + 10#${arrIN[2]} + 10)) 
	  echo "./ffmpeg.exe -loop 1 -framerate 1 -i $x.png -i $x.mp3 -i $1 -ss 0 -t $lenint -filter_complex amix=inputs=2:duration=longest:weights='3 0.82' -c:v libx264 -r 0.1 -movflags +faststart $x.mp4"
	  
	  ./ffmpeg.exe -loop 1 -framerate 1 -i $x.png -i $x.mp3 -i $1 -ss 0 -t $lenint -filter_complex amix=inputs=2:duration=longest:weights='3 0.82' -c:v libx264 -r 0.1 -movflags +faststart $x.mp4
	 
	  lenstr=$(./ffmpeg.exe -i $x.mp4 2>&1 | grep Duration| cut -d " " -f 4 |cut -d "." -f 1;)
	  arrIN=(${lenstr//:/ })
	  lenint=$((10#${arrIN[0]}*3600 + 10#${arrIN[1]}*60 + 10#${arrIN[2]})) 
	  echo $lenstr
	  
	  hour=$(($sumlen/3600))
	  min=$((($sumlen - $hour*3600)/60))
	  sec=$(($sumlen-$hour*3600-min*60))
	  
	  printf "%d:%02d:%02d\n" $hour $min $sec >> lenin.txt
	 # echo "$hour:$min:$sec\r\n" >> lenin.txt
	  sumlen=$(($sumlen + $lenint))
	  echo "file '$x.mp4'" >> list.txt
	fi;
done

$(./ffmpeg.exe -f concat -i list.txt -c copy $2.mp4)


for x in $news; do
    if [[ $x == $bcg ]]; then
		echo "Skipping background";
	#else
		#rm $x.mp4
	fi		
done

rm list.txt
docker run --rm --network=multicast --name ptp1 ptp4l -S -s -i eth0 &
docker run --rm --network=multicast --name ptp2 ptp4l -S -s -i eth0 &

python3 main_opcua.py
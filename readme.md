# Mobile Connect

Automate Mobile Screen Recording

Screen Unlock: Start Recording

Screen Lock: Stop Recording

## Requirements
- Scrcpy
- Adb

## Usage

- Turn Debug mode on from developer options
- Connect mobile with USB
- To use on Wi-Fi, Make sure the devices sharing same network

```` Python
python main.py -i 192.168.1.5

or 

python main.py -i 192.168.1.5 -p 5557
````
IP is your mobile's IP

default port is 5555

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)





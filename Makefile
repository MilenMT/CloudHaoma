all:
	rm -rf CloudHaoma
	git clone https://github.com/abhishekgupta-1/CloudHaoma.git 
	cd CloudHaoma
	sudo apt-get install nodejs nodejs-legacy npm libzmq-dev git
	sudo pip install pyzmq-static
	sudo pip install zmq
	npm install

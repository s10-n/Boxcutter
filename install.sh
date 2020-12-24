pip3 install -r requirements.txt
echo "Python dependencies installed"
chmod +x boxcutter
sudo cp -r boxcutter_resources/ /usr/local/share/boxcutter_resources
echo "Resources placed in /usr/local/share/boxcutter_resources"
sudo cp boxcutter /usr/local/bin
echo "Binary placed in /usr/local/bin"

sudo -i
apt install pip
pip3 install numpy
pip3 install pandas
pip3 install jmespath
wget https://raw.githubusercontent.com/xcgx/office365-cli/main/acc.txt -O acc.txt
wget https://raw.githubusercontent.com/xcgx/office365-cli/main/admin.json -O manifest.json
wget https://raw.githubusercontent.com/xcgx/office365-cli/main/az_cli.py -O az_cli.py
python3 az_cli.py

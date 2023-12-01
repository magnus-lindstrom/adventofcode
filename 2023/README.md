# Python version

Project uses 3.12, which can be installed on Ubuntu with the following commands
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3.12 python3.12-distutils python3.12-venv
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12
```

And then, within a virtual environment:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

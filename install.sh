# Install virtualenv
DIR="$( cd "$( dirname "$0" )" && pwd )"
echo $DIR
echo $1
sudo su # You probably need to be root to do this.
apt-get install python-virtualenv

# Create the directory structure
mkdir -p /www/helloflask.example.org
cd /www/helloflask.example.org
mkdir logs

# Clone the project
git clone https://github.com/Minizza/ghome.git
		

# Initialize virtualenv and install dependencies
virtualenv helloflask
cd helloflask
pip install -r requirements.txt
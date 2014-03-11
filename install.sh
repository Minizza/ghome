#local directory
DIR="$( cd "$( dirname "$0" )" && pwd )"

SERVICE=mongodb

# Install virtualenv
# You probably need to be root to do this.
sudo apt-get install xterm python-virtualenv mongodb
echo "			end install with apt-get"
if ps ax | grep -v grep | grep $SERVICE > /dev/null
then
    echo "$SERVICE service running, everything is fine"
else
    echo "$SERVICE is not running"
fi



# Clone the project
git clone https://github.com/Minizza/ghome.git -b forInstallOnly

echo "			end git cloning"

# Initialize virtualenv and install dependencies
virtualenv ghome
cd ghome
pip install -r script/requirement.txt
mkdir log
touch log/activity.log
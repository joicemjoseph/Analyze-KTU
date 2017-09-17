mkdir ~/.virtualenvs
echo export WORKON_HOME=~/.virtualenvs >> ~/.bashrc
echo ./usr/local/bin/virtualenvwrapper.sh >> ~/.bashrc
mkvirtualenv $1
workon $1
mkdir -p ~/Projects && cd $_
git clone git@gitlab.com:gecw/Analyze-KTU.git Analyzer
cd Analyzer
setvirtualenvproject
pip install -r requirement.txt

echo Done setting up environment

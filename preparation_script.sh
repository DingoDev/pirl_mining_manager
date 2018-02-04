if [ "$(uname)" == "Darwin" ];
then
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    /usr/local/bin/brew install python
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ];
then
    sudo apt-get install python2.7
    sudo apt-get install python-pip
fi

touch mining_ledger.csv
touch mining_ledger.db
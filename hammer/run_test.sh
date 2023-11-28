#!/bin/bash
ls
# Activate the Python
source ~/.bash_profile
#source ~/.profile
#source ~/.zsh_profile
#source ~/.bashrc
# Source pyenv to load it into the shell
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
  eval "$(pyenv virtualenv-init -)"
else
  echo "Error: pyenv is not installed. Please install pyenv and configure it."
  exit 1
fi

# Activate the Python environment
pyenv activate hammer-env2

# Check if the activation was successful
if [ $? -ne 0 ]; then
  echo "Error: Failed to activate the Python environment."
  exit 1
fi

#if ! command -v pyenv &> /dev/null; then
#  echo "Error: pyenv is not installed. Please install pyenv and configure it."
#  exit 1
#fi
pyenv activate hammer-env2
if [ $? -ne 0 ]; then
  echo "Error: Failed to activate the Python environment."
  exit 1
fi

# Define the range of transactions to send
for num_trx in $(seq 4000 1000 10000)
  do
    for type_of_transaction in sequential threaded1 threaded2 threaded3
      do

        # Run tps.py and keep it running
        python tps.py &

        # Run send.py with arguments num_trx and type_of_transaction
        echo "----------------------"
        echo $num_trx
        echo $type_of_transaction
        python send.py $num_trx $type_of_transaction
        echo "----------------------"


        # Wait for tps.py to exit
        wait

        # Save the last_experiment.json with a relevant name
        timestamp=$(date +%Y%m%d%H%M%S)
        mv last-experiment.json "qbft_${num_trx}_${type_of_transaction}_${timestamp}.json"
        echo '###############################################################'
        echo "finished processing $num_trx for $type_of_transaction"
        echo '###############################################################'
  done
done

# Deactivate the Python environment when the test is complete
pyenv deactivate

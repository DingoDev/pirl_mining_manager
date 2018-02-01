Run the preparation script for your setup and file generation
./preparation_script.sh

Then run the pirl_mining_manager to monitor the mining operation, no arguments but do add in your
accounts key, otherwise the API will fail
Do please try to pre install the packages with pip, better to set it than rely on my exception
handling installations
python pirl_mining_manager.py

If you would like the mining ledger to be put into a csv document, run without arguments
python export_mining_ledger.py
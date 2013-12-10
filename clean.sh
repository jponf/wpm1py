#!/usr/bin/env sh
#
# Remove all the .pyc and .pyo files from the specified root directory
# and all its subdirectories
#

cleanDirectory()
{
    
    echo "+++ Cleaning Directory $1"
    removeCompiledPythonFiles $1

    # Look for subdirectories
    for entry in $1/*; do
if [[ -d $entry && $entry != .. ]]; then
cleanDirectory $entry
        fi
done
echo "--- Cleaned Directory $1"
}

removeCompiledPythonFiles()
{
    rm -vf $1/*.pyc
    rm -vf $1/*.pyo
}


#
# Main
if [[ $# -lt 1 || $# -gt 1 ]]; then
echo ""
    echo "Usage: $0 root_directory"
    echo ""
    echo "This script remove all .pyc and .pyo files from root_directory"
    echo "and all the directories under <root_folder>"
else

if [ -d $1 ]; then
echo ""
        echo "### Cleaning... ###"
        echo ""
        cleanDirectory $1
        echo ""
        echo "### Finished ###"
        echo ""
    else
echo "'$1' is not a directory"
    fi
fi


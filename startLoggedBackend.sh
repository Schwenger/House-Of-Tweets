#!/bin/sh

set -e

# 'script' installed?
command -v script >/dev/null 2>&1 || { echo "You don't have 'script' installed.  Install it and try again." ; exit 1 ; }

# Argument looks valid?
case "$1" in
    test_ben)
        echo "Hello, Ben."
        ;;
    test_max)
        echo "Hello, Max."
        ;;
    production_silent)
        echo "Running as SILENT PRODUCTION."
        ;;
    production_responder)
        echo "Running as RESPONDING PRODUCTION."
        ;;
    *)
        echo "Please provide some key, like 'test_max' or something."
        exit 1
        ;;
esac

# Run it
# (In a new block to delimit the effects of 'cd'.)
{
    cd backend
    OUTFILE=$(date +'../log_%Y%m%d_%H%M%S.txt')
    # No need to resolve OUTFILE, 'script' is clever enough.
    echo "View this log interactively by calling:"
    echo "scriptreplay --timing=${OUTFILE}.timing --typescript=${OUTFILE} --maxdelay=10"
    
    if [[ $OSTYPE == darwin* ]]
    then
        script "${OUTFILE}" "./startBackend.py $1"
    else 
        script -c "./startBackend.py $1" --timing="${OUTFILE}.timing" "${OUTFILE}"
    fi
}

#! /bin/bash
export $(grep -v '^#' /main/.env | xargs)

echo "INSALL OPTION:" $INSTALL_OPTION
cd /main/
# all local installs, mapped from host
if [ "$INSTALL_OPTION" == "local-all" ]; then
    for f in lab animal session event deeplabcut; do 
        pip install -e ./element-${f}
    done
    pip install -e ./workflow-deeplabcut
# all except workflow pip installed
else 
    pip install git+https://github.com/${GITHUB_USERNAME}/element-lab.git
    pip install git+https://github.com/${GITHUB_USERNAME}/element-animal.git
    pip install git+https://github.com/${GITHUB_USERNAME}/element-session.git
    pip install git+https://github.com/${GITHUB_USERNAME}/element-event.git
    # only deeplabcut items from local install
    if [ "$INSTALL_OPTION" == "local-dlc" ]; then
        pip install -e ./element-deeplabcut
        pip install -e ./workflow-deeplabcut
    # all from github
    elif [ "$INSTALL_OPTION" == "git" ]; then
        pip install git+https://github.com/${GITHUB_USERNAME}/element-deeplabcut.git
        pip install git+https://github.com/${GITHUB_USERNAME}/workflow-deeplabcut.git
    fi
fi

# If test cmd contains pytest, install 
if [[ "$TEST_CMD" == *pytest* ]]; then
    pip install pytest
    pip install pytest-cov
fi

# additional installs for running DLC
pip install torch
pip install ffmpeg
# all local installs, mapped from host
if [ "$INSTALL_OPTION" == "local-all" ]; then
    for f in $(ls -d ./{ele,work}*); do 
        pip install -e /main/${f}
    done
# all except workflow pip installed
else 
    pip install git+https://github.com/${GITHUB_USERNAME}/element-lab.git
    pip install git+https://github.com/${GITHUB_USERNAME}/element-animal.git
    pip install git+https://github.com/${GITHUB_USERNAME}/element-session.git
    pip install git+https://github.com/${GITHUB_USERNAME}/element-event.git
    # only deeplabcut items from local install
    if [ "$INSTALL_OPTION" == "local-dlc" ]; then
        pip install -e /main/element-deeplabcut
        pip install -e /main/workflow-deeplabcut
    # unless specified, defualts to git install
    else
        pip install git+https://github.com/${GITHUB_USERNAME}/element-deeplabcut.git
        pip install git+https://github.com/${GITHUB_USERNAME}/workflow-deeplabcut.git
    fi
fi

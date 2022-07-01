""" deeplabcut
fresh docker:
    docker run --name wf-dlc -p 3306:3306 -e \
    MYSQL_ROOT_PASSWORD=tutorial datajoint/mysql
dependencies: pip install pytest pytest-cov
run all tests:
    pytest tests/
run one test, debug:
    pytest --pdb tests/tests_name.py -k function_name
"""

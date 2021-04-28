.PHONY: help requirements sync_data_from_drive clean test_environment train predict tests

PROJECT_NAME = houselib
PYTHON_INTERPRETER = python3

include .env

## Install Python Dependencies
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	$(PYTHON_INTERPRETER) -m pip install -r requirements-test.txt

## Download Data from Google-Drive using dvc
sync_data_from_drive:
	dvc pull data/ # TODO

## Delete all compiled Python files recursively in the current directory
clean:
	find . | grep -E "(__pycache__|\.pyc$|\.pyo$)" | xargs rm -rf

## Test python environment is setup correctly
test_environment:
	$(PYTHON_INTERPRETER) test_environment.py

## Train the model on previously created dataset and save logs to Google-Drive
train:
	$(PYTHON_INTERPRETER) src/scripts/train.py \
        	--data_path ${DATA_PATH} \
       		--results_path ${RESULTS_PATH} \
        	--models_path ${MODELS_PATH} \
        	--log_path ${LOG_PATH}
	dvc add -R ${MODELS_PATH}
	dvc add -R ${RESULTS_PATH}
	dvc commit

## Predict using the trained model and save logs to Google-Drive
predict:
	$(PYTHON_INTERPRETER) src/scripts/test.py \
        	--data_path ${DATA_PATH} \
        	--results_path ${RESULTS_PATH} \
        	--models_path ${MODELS_PATH} \
        	--log_path ${LOG_PATH}
	dvc add -R ${RESULTS_PATH}
	dvc commit

## Run all tests by pytest, save reports
tests:
	pytest --cov=houselib \
				 --cov-branch \
				 --cov-report term-missing \
				 --cov-report xml:./results/coverage.xml test \
				 --junitxml=./results/report.xml

.DEFAULT: help
help:
	@echo "make requirements"
	@echo "       Install Python Dependencies"
	@echo "make test_environment"
	@echo "       Test python environment is setup correctly"
	@echo "make clean"
	@echo "       Delete all compiled Python files"
	@echo "make sync_data_from_drive"
	@echo "       Download Data from Google-Drive using dvc"
	@echo "make train"
	@echo "       Train the model on previously created dataset and save logs to Google-Drive"
	@echo "make predict"
	@echo "       Predict using the trained model and save logs to Google-Drive"
	@echo "make tests"
	@echo "       Run all tests by pytest, save reports"

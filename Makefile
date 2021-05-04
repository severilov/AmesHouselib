.PHONY: help requirements sync_data_from_drive pull_data clean test_environment train predict tests

PROJECT_NAME = houselib
PYTHON_INTERPRETER = python3
BUCKET = drive/u/3/folders/1kbww1knOuM-GMIAH3ifN-Zwhwx4oW_2v

include .env

## Test python environment is setup correctly
test_environment:
	$(PYTHON_INTERPRETER) test_environment.py

## Install Python Dependencies
requirements: test_environment
	mkdir -p ${LOG_PATH}
	mkdir -p ${MODELS_PATH}
	$(PYTHON_INTERPRETER) setup.py install
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	$(PYTHON_INTERPRETER) -m pip install -r requirements-test.txt
	$(PYTHON_INTERPRETER) -m pip install dvc
	$(PYTHON_INTERPRETER) -m pip install pydrive2


## Add remote Google-Drive storage
sync_data_from_drive:
	dvc remote add -d storage gdrive://$(BUCKET)

## Download Data from Google-Drive using dvc
pull_data: requirements
	export GOOGLE_APPLICATION_CREDENTIALS=".dvc/opportune-sylph-230917-5abc1b6e125d.json"
	dvc pull

## Delete all compiled Python files recursively in the current directory
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Train the model on previously created dataset and save logs to Google-Drive
train: pull_data
	$(PYTHON_INTERPRETER) src/scripts/train.py \
					--models_path ${MODELS_PATH} \
       		--logs True \
        	--model_type ${MODEL_TYPE} &>${LOG_PATH}/train_log.txt
	dvc add -R ${MODELS_PATH}
	dvc add -R ${LOG_PATH}
	dvc commit
	dvc push

## Predict using the trained model and save logs to Google-Drive
predict: train
	$(PYTHON_INTERPRETER) src/scripts/test.py \
        	--logs True \
        	--model ${MODEL_PATH} &>${LOG_PATH}/test_log.txt
	dvc add -R ${LOG_PATH}
	dvc commit
	dvc push

## Run all tests by pytest, save reports
tests:
	pytest --cov=houselib \
				 --cov-branch \
				 --cov-report term-missing \
				 --cov-report xml:${LOG_PATH}/coverage.xml test \
				 --junitxml=${LOG_PATH}/report.xml
	dvc add -R ${LOG_PATH}
	dvc commit
	dvc push


.DEFAULT: help
help:
	@echo "make requirements"
	@echo "       Install Python Dependencies"
	@echo "make test_environment"
	@echo "       Test python environment is setup correctly"
	@echo "make clean"
	@echo "       Delete all compiled Python files"
	@echo "make sync_data_from_drive"
	@echo "       Add remote Google-Drive storage"
	@echo "make pull_data"
	@echo "       Download Data from Google-Drive using dvc"
	@echo "make train"
	@echo "       Train the model on previously created dataset and save logs to Google-Drive"
	@echo "make predict"
	@echo "       Predict using the trained model and save logs to Google-Drive"
	@echo "make tests"
	@echo "       Run all tests by pytest, save reports"

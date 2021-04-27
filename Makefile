.PHONY: help clean data lint requirements train predict

PROJECT_NAME = houselib
PYTHON_INTERPRETER = python3

include .env

## Install Python Dependencies
requirements: test_environment
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	$(PYTHON_INTERPRETER) -m pip install -r requirements-test.txt


#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Train the model on previously created dataset
train: data
	$(PYTHON_INTERPRETER) src/models/train_model.py \
			--num_epochs ${NUM_EPOCHS} \
        	--run_name ${RUN_NAME} \
        	--data_path ${DATA_PATH} \
       		--results_path ${RESULTS_PATH} \
        	--models_path ${MODELS_PATH} \
        	--log_path ${LOG_PATH}
	dvc add -R ${MODELS_PATH}
	dvc add -R ${RESULTS_PATH}
	dvc commit

## Predict using the trained model
predict: train
	$(PYTHON_INTERPRETER) src/models/predict_model.py \
        	--run_name ${RUN_NAME} \
        	--data_path ${DATA_PATH} \
        	--results_path ${RESULTS_PATH} \
        	--models_path ${MODELS_PATH} \
        	--log_path ${LOG_PATH}
	dvc add -R ${RESULTS_PATH}
	dvc commit




# Makefile variables
VENV_NAME:=venv
PYTHON=${VENV_NAME}/bin/python3


# Include your variables here
RANDOM_SEED:=42
NUM_EPOCHS:=15
INPUT_DIM:=784
HIDDEN_DIM:=128
OUTPUT_DIM:=10

.DEFAULT: help
help:
	@echo "make venv"
	@echo "       prepare development environment, use only once"
	@echo "make lint"
	@echo "       run pylint"
	@echo "make run"
	@echo "       run project"

# Install dependencies whenever setup.py is changed.
venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || python3 -m venv $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -e .
	rm -rf ./*.egg-info
	touch $(VENV_NAME)/bin/activate

lint: venv
	${PYTHON} -m pylint main.py

run: venv
	${PYTHON} main.py --seed $(RANDOM_SEED) --num_epochs $(NUM_EPOCHS) --input_dim $(INPUT_DIM) --hidden_dim $(HIDDEN_DIM) --output_dim $(OUTPUT_DIM)

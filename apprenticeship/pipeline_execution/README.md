# Architecting Pipelines with AWS
##### [Source](https://docs.aws.amazon.com/sagemaker/latest/dg/define-pipeline.html)

**Note:** *This lecture presupposes an adequate [AWS Overview](https://github.com/flatiron-school/DS-Deloitte-07062022-Architecting-Pipelines-with-AWS/blob/main/AWS%20Overview.md). Additionally, it is assumed that the [Pipeline Execution notebook](https://github.com/flatiron-school/DS-Deloitte-07062022-Architecting-Pipelines-with-AWS/blob/main/Pipeline%20Execution.ipynb) content will be discussed at the beginning of the [Pipeline Execution lecture](https://github.com/flatiron-school/DS-Deloitte-07062022-Pipeline-Execution-on-AWS).*

To orchestrate your workflows with Amazon SageMaker Model Building Pipelines, you need to generate a directed acyclic graph (DAG) in the form of a JSON pipeline definition. The following image is a representation of the pipeline DAG that is created using the workflow described in this notebook:

<div>
<img src="images/pipeline-full.png" width="500"/>
</div>

## SageMaker Pipelines

SageMaker Pipelines supports the following activities, which are demonstrated in this notebook:

* Pipelines - A DAG of steps and conditions to orchestrate SageMaker jobs and resource creation.

* Processing job steps - A simplified, managed experience on SageMaker to run data processing workloads, such as feature engineering, data validation, model evaluation, and model interpretation.

* Training job steps - An iterative process that teaches a model to make predictions by presenting examples from a training dataset.

* Conditional execution steps - A step that provides conditional execution of branches in a pipeline.

* Register model steps - A step that creates a model package resource in the Model Registry that can be used to create deployable models in Amazon SageMaker.

* Create model steps - A step that creates a model for use in transform steps or later publication as an endpoint.

* Transform job steps - A batch transform to preprocess datasets to remove noise or bias that interferes with training or inference from a dataset, get inferences from large datasets, and run inference when a persistent endpoint is not needed.

* Fail steps - A step that stops a pipeline execution and marks the pipeline execution as failed.

* Parametrized Pipeline executions - Enables variation in pipeline executions according to specified parameters.

<a id = 'toc'></a>
## Notebook Overview

This notebook shows how to:

* [Define a set of Pipeline parameters](#pipeline-parameters) that can be used to parametrize a SageMaker Pipeline.

* [Define a Processing step that performs cleaning](#processing-step), feature engineering, and splitting the input data into train and test data sets.

* [Define a Training step](#training-step) that trains a model on the preprocessed train data set.

* [Define a Processing step that evaluates the trained model](#processing-step-2)’s performance on the test dataset.

* [Define a Create Model step that creates a model](#create-model-step) from the model artifacts used in training.

* [Define a Transform step that performs batch transformation](#batch-transform-step) based on the model that was created.

* [Define a Register Model step](#register-model-step) that creates a model package from the estimator and model artifacts used to train the model.

* [Define a Conditional step](#condition-step) that measures a condition based on output from prior steps and conditionally executes other steps.

* [Define a Fail step with a customized error message](#fail-step) indicating the cause of the execution failure.

* [Define and create a Pipeline](#create-pipeline-step) definition in a DAG, with the defined parameters and steps.

<!-- * Start a Pipeline execution and wait for execution to complete.

* Download the model evaluation report from the S3 bucket for examination. -->

## A SageMaker Pipeline

The pipeline that you create follows a typical machine learning (ML) application pattern of preprocessing, training, evaluation, model creation, batch transformation, and model registration:

![](images/pipeline-full1.png)

## Prerequisites

###### To run the following tutorial you must do the following:

* Set up your notebook instance as outlined in [Create a notebook instance](https://docs.aws.amazon.com/sagemaker/latest/dg/howitworks-create-ws.html). This gives your role permissions to read and write to Amazon S3, and create training, batch transform, and processing jobs in SageMaker.
* (Optional) Upload and run the "Quick Start" notebook provided in the `sagemaker_upload` folder ([Link](https://github.com/flatiron-school/DS-Deloitte-07062022-Architecting-Pipelines-with-AWS/tree/main/sagemaker_upload)) by following the instructions in the `README`. 

## Set Up Your Environment
Create a new SageMaker session using the following code block. This returns the role ARN for the session.


```python
import boto3
import sagemaker
import sagemaker.session

region = boto3.Session().region_name
sagemaker_session = sagemaker.session.Session()
role = sagemaker.get_execution_role()
default_bucket = sagemaker_session.default_bucket()
model_package_group_name = f"AbaloneModelPackageGroupName"
```

## Create a Pipeline

Run the following steps from your SageMaker notebook instance to create a pipeline including steps for preprocessing, training, evaluation, conditional evaluation, and model registration.

### Step 1: Download the Dataset

This notebook uses the [UCI Machine Learning Abalone Dataset](http://archive.ics.uci.edu/ml). The dataset contains the following features:

* `length` – The longest shell measurement of the abalone.

* `diameter` – The diameter of the abalone perpendicular to its length.

* `height` – The height of the abalone with meat in the shell.

* `whole_weight` – The weight of the whole abalone.

* `shucked_weight` – The weight of the meat removed from the abalone.

* `viscera_weight` – The weight of the abalone viscera after bleeding.

* `shell_weight` – The weight of the abalone shell after meat removal and drying.

* `sex` – The sex of the abalone. One of 'M', 'F', or 'I', where 'I' is an infant abalone.

* `rings` – The number of rings in the abalone shell.

The number of rings in the abalone shell is a good approximation for its age using the formula `age = rings + 1.5`. However, obtaining this number is a time-consuming task. You must cut the shell through the cone, stain the section, and count the number of rings through a microscope. However, the other physical measurements are easier to determine. This notebook uses the dataset to build a predictive model of the variable rings using the other physical measurements.

#### To download the dataset

- Download the dataset into your account's default Amazon S3 bucket:


```python
!mkdir -p data
local_path = "data/abalone-dataset.csv"

s3 = boto3.resource("s3")
s3.Bucket(f"sagemaker-servicecatalog-seedcode-{region}").download_file(
    "dataset/abalone-dataset.csv",
    local_path
)

base_uri = f"s3://{default_bucket}/abalone"
input_data_uri = sagemaker.s3.S3Uploader.upload(
    local_path=local_path, 
    desired_s3_uri=base_uri,
)
print(input_data_uri)
```

    s3://sagemaker-us-east-1-167762637358/abalone/abalone-dataset.csv


- Download a second dataset for batch transformation after your model is created:


```python
local_path = "data/abalone-dataset-batch"

s3 = boto3.resource("s3")
s3.Bucket(f"sagemaker-servicecatalog-seedcode-{region}").download_file(
    "dataset/abalone-dataset-batch",
    local_path
)

base_uri = f"s3://{default_bucket}/abalone"
batch_data_uri = sagemaker.s3.S3Uploader.upload(
    local_path=local_path, 
    desired_s3_uri=base_uri,
)
print(batch_data_uri)
```

    s3://sagemaker-us-east-1-167762637358/abalone/abalone-dataset-batch


[Back to TOC](#toc)
<a id = 'pipeline-parameters'></a>

### Step 2: Define Pipeline Parameters

![](images/pipeline-1.png)

Define Pipeline parameters that you can use to parametrize the pipeline. Parameters enable custom pipeline executions and schedules without having to modify the Pipeline definition.

The supported parameter types include:

* `ParameterString` - represents a str Python type

* `ParameterInteger` - represents an int Python type

* `ParameterFloat` - represents a float Python type

These parameters support providing a default value, which can be overridden on pipeline execution. The default value specified should be an instance of the type of the parameter.

This code block defines the following parameters for your pipeline:

* `processing_instance_count` – The instance count of the processing job.

* `input_data` – The Amazon S3 location of the input data.

* `batch_data` – The Amazon S3 location of the input data for batch transformation.

* `model_approval_status` – The approval status to register the trained model with for CI/CD. For more information, see [Automate MLOps with SageMaker Projects](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects.html).


```python
from sagemaker.workflow.parameters import (
    ParameterInteger,
    ParameterString,
    ParameterFloat,
)

processing_instance_count = ParameterInteger(
    name="ProcessingInstanceCount",
    default_value=1
)
model_approval_status = ParameterString(
    name="ModelApprovalStatus",
    default_value="PendingManualApproval"
)
input_data = ParameterString(
    name="InputData",
    default_value=input_data_uri,
)
batch_data = ParameterString(
    name="BatchData",
    default_value=batch_data_uri,
)
mse_threshold = ParameterFloat(name="MseThreshold", default_value=6.0)
```

[Back to TOC](#toc)
<a id = 'processing-step'></a>

### Step 3: Define a Processing Step for Feature Engineering

![](images/pipeline-2.png)

This section shows how to create a processing step to prepare the data from the dataset for training.

#### To create a processing step

- Create a directory for the processing script:


```python
!mkdir -p abalone
```

- Create a file in the `/abalone` directory named `preprocessing.py` with the following content. This preprocessing script is passed in to the processing step for execution on the input data. The training step then uses the preprocessed training features and labels to train a model, and the evaluation step uses the trained model and preprocessed test features and labels to evaluate the model. The script uses `scikit-learn` to do the following:

    * Fill in missing `sex` categorical data and encode it so it's suitable for training.

    * Scale and normalize all numerical fields except for `rings` and `sex`.

    * Split the data into training, test, and validation datasets.


```python
%%writefile abalone/preprocessing.py
import argparse
import os
import requests
import tempfile
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Because this is a headerless CSV file, specify the column names here.
feature_columns_names = [
    "sex",
    "length",
    "diameter",
    "height",
    "whole_weight",
    "shucked_weight",
    "viscera_weight",
    "shell_weight",
]
label_column = "rings"

feature_columns_dtype = {
    "sex": str,
    "length": np.float64,
    "diameter": np.float64,
    "height": np.float64,
    "whole_weight": np.float64,
    "shucked_weight": np.float64,
    "viscera_weight": np.float64,
    "shell_weight": np.float64
}
label_column_dtype = {"rings": np.float64}

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

if __name__ == "__main__":
    base_dir = "/opt/ml/processing"

    df = pd.read_csv(
        f"{base_dir}/input/abalone-dataset.csv",
        header=None, 
        names=feature_columns_names + [label_column],
        dtype=merge_two_dicts(feature_columns_dtype, label_column_dtype)
    )
    numeric_features = list(feature_columns_names)
    numeric_features.remove("sex")
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]
    )

    categorical_features = ["sex"]
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ]
    )

    preprocess = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features)
        ]
    )
    
    y = df.pop("rings")
    X_pre = preprocess.fit_transform(df)
    y_pre = y.to_numpy().reshape(len(y), 1)
    
    X = np.concatenate((y_pre, X_pre), axis=1)
    
    np.random.shuffle(X)
    train, validation, test = np.split(X, [int(.7*len(X)), int(.85*len(X))])

    pd.DataFrame(train).to_csv(f"{base_dir}/train/train.csv", header=False, index=False)
    pd.DataFrame(validation).to_csv(f"{base_dir}/validation/validation.csv", header=False, index=False)
    pd.DataFrame(test).to_csv(f"{base_dir}/test/test.csv", header=False, index=False)
```

    Overwriting abalone/preprocessing.py


- Create an instance of an `SKLearnProcessor` to pass in to the processing step. 

    Note the `processing_instance_count` parameter used by the processor instance (as defined above in **Step 2**). Also previously-specified was the `framework_version` to use throughout this notebook.


```python
from sagemaker.sklearn.processing import SKLearnProcessor

from sagemaker.workflow.parameters import (
    ParameterInteger,
    ParameterString,
    ParameterFloat,
    ParameterBoolean
)

processing_instance_count = ParameterInteger(
    name="ProcessingInstanceCount",
    default_value=1
)

framework_version = "0.23-1"

sklearn_processor = SKLearnProcessor(
    framework_version=framework_version,
    instance_type="ml.m5.xlarge",
    instance_count=processing_instance_count,
    base_job_name="sklearn-abalone-process",
    role=role,
)
```

- Create a processing step. This step takes in the `SKLearnProcessor`, the input and output channels, and the `preprocessing.py` script that you created. This is very similar to a processor instance's run method in the SageMaker Python SDK. The `input_data` parameter passed into `ProcessingStep` is the input data of the step itself. This input data is used by the processor instance when it runs.

    Note the `"train"`, `"validation"`, and `"test"` channels specified in the output configuration for the processing job. Step `Properties` such as these can be used in subsequent steps and resolve to their runtime values at execution.


```python
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.workflow.steps import ProcessingStep
    
step_process = ProcessingStep(
    name="AbaloneProcess",
    processor=sklearn_processor,
    inputs=[
      ProcessingInput(source=input_data, destination="/opt/ml/processing/input"),  
    ],
    outputs=[
        ProcessingOutput(output_name="train", source="/opt/ml/processing/train"),
        ProcessingOutput(output_name="validation", source="/opt/ml/processing/validation"),
        ProcessingOutput(output_name="test", source="/opt/ml/processing/test")
    ],
    code="abalone/preprocessing.py",
)
```

[Back to TOC](#toc)
<a id = 'training-step'></a>

### Step 4: Define a Training step

![](images/pipeline-3.png)

This section shows how to use the SageMaker [XGBoost Algorithm](https://docs.aws.amazon.com/sagemaker/latest/dg/xgboost.html) to train a logistic regression model on the training data output from the processing steps.

#### To define a training step

- Specify the model path where you want to save the models from training:


```python
model_path = f"s3://{default_bucket}/AbaloneTrain"
```

- Configure an estimator for the XGBoost algorithm and the input dataset. The training instance type is passed into the estimator. A typical training script loads data from the input channels, configures training with hyperparameters, trains a model, and saves a model to `model_dir` so that it can be hosted later. SageMaker uploads the model to Amazon S3 in the form of a `model.tar.gz` at the end of the training job.


```python
from sagemaker.estimator import Estimator

image_uri = sagemaker.image_uris.retrieve(
    framework="xgboost",
    region=region,
    version="1.0-1",
    py_version="py3",
    instance_type="ml.m5.xlarge"
)

xgb_train = Estimator(
    image_uri=image_uri,
    instance_type="ml.m5.xlarge",
    instance_count=1,
    output_path=model_path,
    role=role,
)

xgb_train.set_hyperparameters(
    objective="reg:linear",
    num_round=50,
    max_depth=5,
    eta=0.2,
    gamma=4,
    min_child_weight=6,
    subsample=0.7,
    silent=0
)
```

- Create a `TrainingStep` using the estimator instance and properties of the `ProcessingStep`. In particular, pass in the `S3Uri` of the `"train"` and `"validation"` output channel to the `TrainingStep`. 


```python
from sagemaker.inputs import TrainingInput
from sagemaker.workflow.steps import TrainingStep

step_train = TrainingStep(
    name="AbaloneTrain",
    estimator=xgb_train,
    inputs={
        "train": TrainingInput(
            s3_data=step_process.properties.ProcessingOutputConfig.Outputs[
                "train"
            ].S3Output.S3Uri,
            content_type="text/csv"
        ),
        "validation": TrainingInput(
            s3_data=step_process.properties.ProcessingOutputConfig.Outputs[
                "validation"
            ].S3Output.S3Uri,
            content_type="text/csv"
        )
    },
)
```

[Back to TOC](#toc)
<a id = 'processing-step-2'></a>

### Step 5: Define a Processing Step for Model Evaluation

![](images/pipeline-4.png)

This section shows how to create a processing step to evaluate the accuracy of the model. The result of this model evaluation is used in the condition step to determine which execute path to take.

#### To define a processing step for model evaluation

- Create a file in the `/abalone` directory named `evaluation.py`. This script is used in a processing step to perform model evaluation. It takes a trained model and the test dataset as input, then produces a JSON file containing classification evaluation metrics.


```python
%%writefile abalone/evaluation.py
import json
import pathlib
import pickle
import tarfile
import joblib
import numpy as np
import pandas as pd
import xgboost

from sklearn.metrics import mean_squared_error

if __name__ == "__main__":
    model_path = f"/opt/ml/processing/model/model.tar.gz"
    with tarfile.open(model_path) as tar:
        tar.extractall(path=".")
    
    model = pickle.load(open("xgboost-model", "rb"))

    test_path = "/opt/ml/processing/test/test.csv"
    df = pd.read_csv(test_path, header=None)
    
    y_test = df.iloc[:, 0].to_numpy()
    df.drop(df.columns[0], axis=1, inplace=True)
    
    X_test = xgboost.DMatrix(df.values)
    
    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)
    std = np.std(y_test - predictions)
    report_dict = {
        "regression_metrics": {
            "mse": {
                "value": mse,
                "standard_deviation": std
            },
        },
    }

    output_dir = "/opt/ml/processing/evaluation"
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    evaluation_path = f"{output_dir}/evaluation.json"
    with open(evaluation_path, "w") as f:
        f.write(json.dumps(report_dict))
```

    Overwriting abalone/evaluation.py


- Create an instance of a `ScriptProcessor` that is used to create a `ProcessingStep`:


```python
from sagemaker.processing import ScriptProcessor

script_eval = ScriptProcessor(
    image_uri=image_uri,
    command=["python3"],
    instance_type="ml.m5.xlarge",
    instance_count=1,
    base_job_name="script-abalone-eval",
    role=role,
)
```

- Create a `ProcessingStep` using the processor instance, the input and output channels, and the `evaluation.py` script. In particular, pass in the `S3ModelArtifacts` property from the `step_train` training step, as well as the `S3Uri` of the `"test"` output channel of the `step_process` processing step. This is very similar to a processor instance's `run` method in the SageMaker Python SDK. 


```python
from sagemaker.workflow.properties import PropertyFile

evaluation_report = PropertyFile(
    name="EvaluationReport",
    output_name="evaluation",
    path="evaluation.json"
)
step_eval = ProcessingStep(
    name="AbaloneEval",
    processor=script_eval,
    inputs=[
        ProcessingInput(
            source=step_train.properties.ModelArtifacts.S3ModelArtifacts,
            destination="/opt/ml/processing/model"
        ),
        ProcessingInput(
            source=step_process.properties.ProcessingOutputConfig.Outputs[
                "test"
            ].S3Output.S3Uri,
            destination="/opt/ml/processing/test"
        )
    ],
    outputs=[
        ProcessingOutput(output_name="evaluation", source="/opt/ml/processing/evaluation"),
    ],
    code="abalone/evaluation.py",
    property_files=[evaluation_report],
)
```

[Back to TOC](#toc)
<a id = 'create-model-step'></a>

### Step 6: Define a CreateModelStep for Batch Transformation

![](images/pipeline-5.png)

This section shows how to create a SageMaker model from the output of the training step. This model is used for batch transformation on a new dataset. This step is passed into the condition step and only executes if the condition step evaluates to `true`.

#### To define a CreateModelStep for batch transformation

- Create a SageMaker model. Pass in the `S3ModelArtifacts` property from the `step_train` training step:


```python
from sagemaker.model import Model

model = Model(
    image_uri=image_uri,
    model_data=step_train.properties.ModelArtifacts.S3ModelArtifacts,
    sagemaker_session=sagemaker_session,
    role=role,
)
```

- Define the model input for your SageMaker model:


```python
from sagemaker.inputs import CreateModelInput

inputs = CreateModelInput(
    instance_type="ml.m5.large",
    accelerator_type="ml.eia1.medium",
)
```

- Create your `CreateModelStep` using the `CreateModelInput` and SageMaker `model` instance you defined:


```python
from sagemaker.workflow.steps import CreateModelStep

step_create_model = CreateModelStep(
    name="AbaloneCreateModel",
    model=model,
    inputs=inputs,
)
```

[Back to TOC](#toc)
<a id = 'batch-transform-step'></a>

### Step 7: Define a TransformStep to Perform Batch Transformation

This section shows how to create a `TransformStep` to perform batch transformation on a dataset after the model is trained. This step is passed into the condition step and only executes if the condition step evaluates to `true`.

#### To define a TransformStep to perform batch transformation

- Create a transformer instance with the appropriate compute instance type, instance count, and desired output Amazon S3 bucket URI. Pass in the `ModelName` property from the `step_create_model` `CreateModel` step.


```python
from sagemaker.transformer import Transformer

transformer = Transformer(
    model_name=step_create_model.properties.ModelName,
    instance_type="ml.m5.xlarge",
    instance_count=1,
    output_path=f"s3://{default_bucket}/AbaloneTransform"
)
```

- Create a `TransformStep` using the transformer instance you defined and the `batch_data` pipeline parameter:


```python
from sagemaker.inputs import TransformInput
from sagemaker.workflow.steps import TransformStep

step_transform = TransformStep(
    name="AbaloneTransform",
    transformer=transformer,
    inputs=TransformInput(data=batch_data)
)
```

[Back to TOC](#toc)
<a id = 'register-model-step'></a>

### Step 8: Define a RegisterModel Step to Create a Model Package

This section shows how to construct an instance of `RegisterModel`. The result of executing `RegisterModel` in a pipeline is a model package. A model package is a reusable model artifacts abstraction that packages all ingredients necessary for inference. It consists of an inference specification that defines the inference image to use along with an optional model weights location. A model package group is a collection of model packages. You can use a `ModelPackageGroup` for SageMaker Pipelines to add a new version and model package to the group for every pipeline execution. For more information about model registry, see [Register and Deploy Models with Model Registry](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html).

This step is passed into the condition step and only executes if the condition step evaluates to `true`.

#### To define a RegisterModel step to create a model package

* Construct a `RegisterModel` step using the estimator instance you used for the training step. Pass in the `S3ModelArtifacts` property from the `step_train` training step and specify a `ModelPackageGroup`. SageMaker Pipelines creates this `ModelPackageGroup` for you.


```python
from sagemaker.model_metrics import MetricsSource, ModelMetrics 
from sagemaker.workflow.step_collections import RegisterModel

model_metrics = ModelMetrics(
    model_statistics=MetricsSource(
        s3_uri="{}/evaluation.json".format(
            step_eval.arguments["ProcessingOutputConfig"]["Outputs"][0]["S3Output"]["S3Uri"]
        ),
        content_type="application/json"
    )
)

step_register = RegisterModel(
    name="AbaloneRegisterModel",
    estimator=xgb_train,
    model_data=step_train.properties.ModelArtifacts.S3ModelArtifacts,
    content_types=["text/csv"],
    response_types=["text/csv"],
    inference_instances=["ml.t2.medium", "ml.m5.xlarge"],
    transform_instances=["ml.m5.xlarge"],
    model_package_group_name=model_package_group_name,
    approval_status=model_approval_status,
    model_metrics=model_metrics
)
```

[Back to TOC](#toc)
<a id = 'fail-step'></a>

### Step 9: Define a Fail Step to Terminate the Pipeline Execution and Mark it as Failed

![](images/pipeline-8.png)

This section walks you through the following steps:

* Define a FailStep with customized error message, which indicates the cause of the execution failure.

* Enter the FailStep error message with a Join function, which appends a static text string with the dynamic mse_threshold parameter to build a more informative error message.


```python
from sagemaker.workflow.fail_step import FailStep
from sagemaker.workflow.functions import Join

step_fail = FailStep(
    name="AbaloneMSEFail",
    error_message=Join(on=" ", values=["Execution failed due to MSE >", mse_threshold]),
)
```

[Back to TOC](#toc)
<a id = 'condition-step'></a>

### Step 10: Define a Condition Step to Verify Model Accuracy

![](images/pipeline-6.png)

A `ConditionStep` allows SageMaker Pipelines to support conditional execution in your pipeline DAG based on the condition of step properties. In this case, you only want to register a model package if the accuracy of that model, as determined by the model evaluation step, exceeds the required value. If the accuracy exceeds the required value, the pipeline also creates a SageMaker Model and runs batch transformation on a dataset. This section shows how to define the Condition step.

#### To define a condition step to verify model accuracy

- Define a `ConditionLessThanOrEqualTo` condition using the accuracy value found in the output of the model evaluation processing step, `step_eval`. Get this output using the property file you indexed in the processing step and the respective JSONPath of the mean squared error value, `"mse"`.


```python
from sagemaker.workflow.conditions import ConditionLessThanOrEqualTo
from sagemaker.workflow.condition_step import ConditionStep
from sagemaker.workflow.functions import JsonGet

cond_lte = ConditionLessThanOrEqualTo(
    left=JsonGet(
        step_name=step_eval.name,
        property_file=evaluation_report,
        json_path="regression_metrics.mse.value"
    ),
    right=mse_threshold
)
```

- Construct a `ConditionStep`. Pass the `ConditionEquals` condition in, then set the model package registration and batch transformation steps as the next steps if the condition passes.


```python
step_cond = ConditionStep(
    name="AbaloneMSECond",
    conditions=[cond_lte],
    if_steps=[step_register, step_create_model, step_transform],
    else_steps=[step_fail], 
)
```

[Back to TOC](#toc)
<a id = 'create-pipeline-step'></a>

### Step 11: Create a pipeline

![](images/pipeline-7.png)

Now that you’ve created all of the steps, you can combine them into a pipeline!

#### To create a pipeline

- Define the following for your pipeline: `name`, `parameters`, and `steps`. Names must be unique within an (`account`, `region`) pair.

**Note**: *A step can only appear once* in either the pipeline's step list or the if/else step lists of the condition step. It cannot appear in both.


```python
from sagemaker.workflow.pipeline import Pipeline

pipeline_name = f"AbalonePipeline"
pipeline = Pipeline(
    name=pipeline_name,
    parameters=[
        processing_instance_count,
        model_approval_status,
        input_data,
        batch_data,
        mse_threshold,
    ],
    steps=[step_process, step_train, step_eval, step_cond],
)
```

- (Optional) Examine the JSON pipeline definition to ensure that it's well-formed:


```python
import json

json.loads(pipeline.definition())
```

    No finished training job found associated with this estimator. Please make sure this estimator is only used for building workflow config





    {'Version': '2020-12-01',
     'Metadata': {},
     'Parameters': [{'Name': 'ProcessingInstanceCount',
       'Type': 'Integer',
       'DefaultValue': 1},
      {'Name': 'ModelApprovalStatus',
       'Type': 'String',
       'DefaultValue': 'PendingManualApproval'},
      {'Name': 'InputData',
       'Type': 'String',
       'DefaultValue': 's3://sagemaker-us-east-1-167762637358/abalone/abalone-dataset.csv'},
      {'Name': 'BatchData',
       'Type': 'String',
       'DefaultValue': 's3://sagemaker-us-east-1-167762637358/abalone/abalone-dataset-batch'},
      {'Name': 'MseThreshold', 'Type': 'Float', 'DefaultValue': 6.0}],
     'PipelineExperimentConfig': {'ExperimentName': {'Get': 'Execution.PipelineName'},
      'TrialName': {'Get': 'Execution.PipelineExecutionId'}},
     'Steps': [{'Name': 'AbaloneProcess',
       'Type': 'Processing',
       'Arguments': {'ProcessingResources': {'ClusterConfig': {'InstanceType': 'ml.m5.xlarge',
          'InstanceCount': {'Get': 'Parameters.ProcessingInstanceCount'},
          'VolumeSizeInGB': 30}},
        'AppSpecification': {'ImageUri': '683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:0.23-1-cpu-py3',
         'ContainerEntrypoint': ['python3',
          '/opt/ml/processing/input/code/preprocessing.py']},
        'RoleArn': 'arn:aws:iam::167762637358:role/service-role/AmazonSageMakerServiceCatalogProductsUseRole',
        'ProcessingInputs': [{'InputName': 'input-1',
          'AppManaged': False,
          'S3Input': {'S3Uri': {'Get': 'Parameters.InputData'},
           'LocalPath': '/opt/ml/processing/input',
           'S3DataType': 'S3Prefix',
           'S3InputMode': 'File',
           'S3DataDistributionType': 'FullyReplicated',
           'S3CompressionType': 'None'}},
         {'InputName': 'code',
          'AppManaged': False,
          'S3Input': {'S3Uri': 's3://sagemaker-us-east-1-167762637358/AbaloneProcess-94160e00688e34972e58a18a33ec6342/input/code/preprocessing.py',
           'LocalPath': '/opt/ml/processing/input/code',
           'S3DataType': 'S3Prefix',
           'S3InputMode': 'File',
           'S3DataDistributionType': 'FullyReplicated',
           'S3CompressionType': 'None'}}],
        'ProcessingOutputConfig': {'Outputs': [{'OutputName': 'train',
           'AppManaged': False,
           'S3Output': {'S3Uri': 's3://sagemaker-us-east-1-167762637358/AbaloneProcess-94160e00688e34972e58a18a33ec6342/output/train',
            'LocalPath': '/opt/ml/processing/train',
            'S3UploadMode': 'EndOfJob'}},
          {'OutputName': 'validation',
           'AppManaged': False,
           'S3Output': {'S3Uri': 's3://sagemaker-us-east-1-167762637358/AbaloneProcess-94160e00688e34972e58a18a33ec6342/output/validation',
            'LocalPath': '/opt/ml/processing/validation',
            'S3UploadMode': 'EndOfJob'}},
          {'OutputName': 'test',
           'AppManaged': False,
           'S3Output': {'S3Uri': 's3://sagemaker-us-east-1-167762637358/AbaloneProcess-94160e00688e34972e58a18a33ec6342/output/test',
            'LocalPath': '/opt/ml/processing/test',
            'S3UploadMode': 'EndOfJob'}}]}}},
      {'Name': 'AbaloneTrain',
       'Type': 'Training',
       'Arguments': {'AlgorithmSpecification': {'TrainingInputMode': 'File',
         'TrainingImage': '683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:1.0-1-cpu-py3'},
        'OutputDataConfig': {'S3OutputPath': 's3://sagemaker-us-east-1-167762637358/AbaloneTrain'},
        'StoppingCondition': {'MaxRuntimeInSeconds': 86400},
        'ResourceConfig': {'VolumeSizeInGB': 30,
         'InstanceCount': 1,
         'InstanceType': 'ml.m5.xlarge'},
        'RoleArn': 'arn:aws:iam::167762637358:role/service-role/AmazonSageMakerServiceCatalogProductsUseRole',
        'InputDataConfig': [{'DataSource': {'S3DataSource': {'S3DataType': 'S3Prefix',
            'S3Uri': {'Get': "Steps.AbaloneProcess.ProcessingOutputConfig.Outputs['train'].S3Output.S3Uri"},
            'S3DataDistributionType': 'FullyReplicated'}},
          'ContentType': 'text/csv',
          'ChannelName': 'train'},
         {'DataSource': {'S3DataSource': {'S3DataType': 'S3Prefix',
            'S3Uri': {'Get': "Steps.AbaloneProcess.ProcessingOutputConfig.Outputs['validation'].S3Output.S3Uri"},
            'S3DataDistributionType': 'FullyReplicated'}},
          'ContentType': 'text/csv',
          'ChannelName': 'validation'}],
        'HyperParameters': {'objective': 'reg:linear',
         'num_round': '50',
         'max_depth': '5',
         'eta': '0.2',
         'gamma': '4',
         'min_child_weight': '6',
         'subsample': '0.7',
         'silent': '0'},
        'ProfilerRuleConfigurations': [{'RuleConfigurationName': 'ProfilerReport-1660261695',
          'RuleEvaluatorImage': '503895931360.dkr.ecr.us-east-1.amazonaws.com/sagemaker-debugger-rules:latest',
          'RuleParameters': {'rule_to_invoke': 'ProfilerReport'}}],
        'ProfilerConfig': {'S3OutputPath': 's3://sagemaker-us-east-1-167762637358/AbaloneTrain'}}},
      {'Name': 'AbaloneEval',
       'Type': 'Processing',
       'Arguments': {'ProcessingResources': {'ClusterConfig': {'InstanceType': 'ml.m5.xlarge',
          'InstanceCount': 1,
          'VolumeSizeInGB': 30}},
        'AppSpecification': {'ImageUri': '683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:1.0-1-cpu-py3',
         'ContainerEntrypoint': ['python3',
          '/opt/ml/processing/input/code/evaluation.py']},
        'RoleArn': 'arn:aws:iam::167762637358:role/service-role/AmazonSageMakerServiceCatalogProductsUseRole',
        'ProcessingInputs': [{'InputName': 'input-1',
          'AppManaged': False,
          'S3Input': {'S3Uri': {'Get': 'Steps.AbaloneTrain.ModelArtifacts.S3ModelArtifacts'},
           'LocalPath': '/opt/ml/processing/model',
           'S3DataType': 'S3Prefix',
           'S3InputMode': 'File',
           'S3DataDistributionType': 'FullyReplicated',
           'S3CompressionType': 'None'}},
         {'InputName': 'input-2',
          'AppManaged': False,
          'S3Input': {'S3Uri': {'Get': "Steps.AbaloneProcess.ProcessingOutputConfig.Outputs['test'].S3Output.S3Uri"},
           'LocalPath': '/opt/ml/processing/test',
           'S3DataType': 'S3Prefix',
           'S3InputMode': 'File',
           'S3DataDistributionType': 'FullyReplicated',
           'S3CompressionType': 'None'}},
         {'InputName': 'code',
          'AppManaged': False,
          'S3Input': {'S3Uri': 's3://sagemaker-us-east-1-167762637358/AbaloneEval-19b131b63656129c86bfecbee4904927/input/code/evaluation.py',
           'LocalPath': '/opt/ml/processing/input/code',
           'S3DataType': 'S3Prefix',
           'S3InputMode': 'File',
           'S3DataDistributionType': 'FullyReplicated',
           'S3CompressionType': 'None'}}],
        'ProcessingOutputConfig': {'Outputs': [{'OutputName': 'evaluation',
           'AppManaged': False,
           'S3Output': {'S3Uri': 's3://sagemaker-us-east-1-167762637358/AbaloneEval-19b131b63656129c86bfecbee4904927/output/evaluation',
            'LocalPath': '/opt/ml/processing/evaluation',
            'S3UploadMode': 'EndOfJob'}}]}},
       'PropertyFiles': [{'PropertyFileName': 'EvaluationReport',
         'OutputName': 'evaluation',
         'FilePath': 'evaluation.json'}]},
      {'Name': 'AbaloneMSECond',
       'Type': 'Condition',
       'Arguments': {'Conditions': [{'Type': 'LessThanOrEqualTo',
          'LeftValue': {'Std:JsonGet': {'PropertyFile': {'Get': 'Steps.AbaloneEval.PropertyFiles.EvaluationReport'},
            'Path': 'regression_metrics.mse.value'}},
          'RightValue': {'Get': 'Parameters.MseThreshold'}}],
        'IfSteps': [{'Name': 'AbaloneRegisterModel-RegisterModel',
          'Type': 'RegisterModel',
          'Arguments': {'ModelPackageGroupName': 'AbaloneModelPackageGroupName',
           'ModelMetrics': {'ModelQuality': {'Statistics': {'ContentType': 'application/json',
              'S3Uri': 's3://sagemaker-us-east-1-167762637358/AbaloneEval-19b131b63656129c86bfecbee4904927/output/evaluation/evaluation.json'}},
            'Bias': {},
            'Explainability': {}},
           'InferenceSpecification': {'Containers': [{'Image': '683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:1.0-1-cpu-py3',
              'ModelDataUrl': {'Get': 'Steps.AbaloneTrain.ModelArtifacts.S3ModelArtifacts'}}],
            'SupportedContentTypes': ['text/csv'],
            'SupportedResponseMIMETypes': ['text/csv'],
            'SupportedRealtimeInferenceInstanceTypes': ['ml.t2.medium',
             'ml.m5.xlarge'],
            'SupportedTransformInstanceTypes': ['ml.m5.xlarge']},
           'ModelApprovalStatus': {'Get': 'Parameters.ModelApprovalStatus'}}},
         {'Name': 'AbaloneCreateModel',
          'Type': 'Model',
          'Arguments': {'ExecutionRoleArn': 'arn:aws:iam::167762637358:role/service-role/AmazonSageMakerServiceCatalogProductsUseRole',
           'PrimaryContainer': {'Image': '683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:1.0-1-cpu-py3',
            'Environment': {},
            'ModelDataUrl': {'Get': 'Steps.AbaloneTrain.ModelArtifacts.S3ModelArtifacts'}}}},
         {'Name': 'AbaloneTransform',
          'Type': 'Transform',
          'Arguments': {'ModelName': {'Get': 'Steps.AbaloneCreateModel.ModelName'},
           'TransformInput': {'DataSource': {'S3DataSource': {'S3DataType': 'S3Prefix',
              'S3Uri': {'Get': 'Parameters.BatchData'}}}},
           'TransformOutput': {'S3OutputPath': 's3://sagemaker-us-east-1-167762637358/AbaloneTransform'},
           'TransformResources': {'InstanceCount': 1,
            'InstanceType': 'ml.m5.xlarge'}}}],
        'ElseSteps': [{'Name': 'AbaloneMSEFail',
          'Type': 'Fail',
          'Arguments': {'ErrorMessage': {'Std:Join': {'On': ' ',
             'Values': ['Execution failed due to MSE >',
              {'Get': 'Parameters.MseThreshold'}]}}}}]}}]}



This pipeline definition is ready to submit to SageMaker. During the next lecture, we'll submit this pipeline to SageMaker and [start an execution](https://github.com/flatiron-school/DS-Deloitte-07062022-Architecting-Pipelines-with-AWS/blob/main/Pipeline%20Execution.ipynb)!

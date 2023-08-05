# mlmodels


* Lightweight Functional interface to wrap access to Deep Learning, ML models
and Hyper-Parameter Search, cross platforms such as Tensorflow, Pytorch, Gluon, Keras,...

* Logic follows Scikit Learn API: fit, predict, transform, metrics, save, load

* Goal is to facilitate Jupyter script code to Semi-Prod code with a minimal amount of code refactoring ... *


```
#### Docs here:   https://mlmodels.readthedocs.io/en/latest/  (incomplete docs)
```

######################################################################################
## ① Installation
Install as editable package (ONLY dev branch)

    cd yourfolder
    git clone https://github.com/arita37/mlmodels.git mlmodels
    cd mlmodels
    git checkout dev     
    pip install -e .  --no-deps  

####  Dependencies
    optuna
    tensorflow>=1.14.0
    pytorch>=0.4.0
    keras>=2.0
    gluon
    autogluon
    gluonts
    pandas>=0.24.2
    scipy>=1.3.0
    numexpr>=2.6.8 
    scikit-learn>=0.21.2

#######################################################################################
## ② How to add a new model
### Source code structure as below
- `docs`: documentation
- `mlmodels`: interface wrapper for pytorch, keras, gluon, tf, transformer NLP for train, hyper-params searchi.
    + `model_xxx`: folders for each platform with same interface defined in template folder
    + `dataset`: store dataset files for test runs.
    + `template`: template interface wrapper which define common interfaces for whole platforms
    + `ztest`: testing output for each sample testing in `model_xxx`
- `ztest`: testing output for each sample testing in `model_xxx`

###  How to define a custom model
1. Create a file `mlmodels\model_XXXX\mymodel.py` , XXX: tch: pytorch, tf:tensorflow, keras:keras, ....
- Declare below classes/functions in the created file:

      Class Model()                                                 :   Model definition
            __init__(model_pars)                                    :   
                                  
      def fit(model, data_pars, model_pars, compute_pars, )         : Train the model
      def predict(model, sess, data_pars, compute_pars, out_pars )  : Predict the results
      def metric(ytrue, ypred, yproba, data_pars, compute_pars, out_pars )         : Measure the results

      def get_params()                                              : returnparameters of the model
      def get_dataset(data_pars)                                    : load dataset
      def test()                                                    : example running the model     
      def test2()                                                   : example running the model in global settings  

      def save(model, path)                                         : save the model
      def load(path)                                                : load the trained model


- *Infos* 
     ```
     model :         Model(model_pars), instance of Model() object
     sess  :         Session for TF model.
     model_pars :    dict containing info on model definition.
     data_pars :     dict containing info on input data.
     compute_pars :  dict containing info on model compute.
     out_pars :      dict containing info on output folder.
     ```

2. Write your code and create test() to test your code.

- *Example* 
    https://github.com/arita37/mlmodels/tree/dev/mlmodels/template
    https://github.com/arita37/mlmodels/blob/dev/mlmodels/model_gluon/gluon_deepar.py
    https://github.com/arita37/mlmodels/blob/dev/mlmodels/model_gluon/gluon_deepar.json


3. Create JSON config file inside  /model_XXX/
     mymodel.json



 
#######################################################################################
## ③ CLI tools: package provide below tools
- ml_models
- ml_optim    
### How to use tools

- Lightweight Functional interface to execute models
`ml_models`  :  mlmodels/models.py

```
ml_models --do  
    model_list  :  list all models in the repo                            
    testall     :  test all modules inside model_tf
    test        :  test a certain module inside model_tf
    fit         :  wrap fit generic m    ethod
    predict     :  predict  using a pre-trained model and some data
    generate_config  :  generate config file from code source
```
   
- Lightweight Functional interface to wrap Hyper-parameter Optimization `ml_optim`   :  mlmodels/optim.py

```
ml_optim --do
    test      :  Test the hyperparameter optimization for a specific model
    test_all  :  TODO, Test all
    search    :  search for the best hyperparameters of a specific model
```

- Lightweight Functional interface to run test samples `ml_test`
```
ml_test
```


### Command line tool sample

#### generate config file
    ml_models  --do generate_config  --model_uri model_tf.1_lstm.py  --save_folder "c:\myconfig\"


#### TF LSTM model
    ml_models  --model_uri model_tf/1_lstm.py  --do test


#### Custom  Models
    ml_models --do test  --model_uri "D:\_devs\Python01\gitdev\mlmodels\mlmodels\model_tf\1_lstm.py"


#### PyTorch models
    ml_models  --model_uri model_tch/mlp.py  --do test


#### Model param search test
    ml_optim --do test


#### For normal optimization search method
    ml_optim --do search --ntrials 1  --config_file optim_config.json --optim_method normal
    ml_optim --do search --ntrials 1  --config_file optim_config.json --optim_method prune  ###### for pruning method


#### HyperParam standalone run
    ml_optim --modelname model_tf.1_lstm.py  --do test
    ml_optim --modelname model_tf.1_lstm.py  --do search



###########################################################################################
##④ Interface

models.py 
```
   module_load(model_uri)
   model_create(module)
   fit(model, module, session, data_pars, out_pars   )
   metrics(model, module, session, data_pars, out_pars)
   predict(model, module, session, data_pars, out_pars)
   save(model, path)
   load(model)
```

optim.py
```
   optim(modelname="model_tf.1_lstm.py",  model_pars= {}, data_pars = {}, compute_pars={"method": "normal/prune"}
       , save_folder="/mymodel/", log_folder="", ntrials=2) 

   optim_optuna(modelname="model_tf.1_lstm.py", model_pars= {}, data_pars = {}, compute_pars={"method" : "normal/prune"},
                save_folder="/mymodel/", log_folder="", ntrials=2) 
```

#### Generic parameters 
```
   Define in models_config.json
   model_params      :  Relative to model definition 
   compute_pars      :  Relative to  the compute process
   data_pars         :  Relative to the input data
   out_pars          :  Relative to outout data
```
   Sometimes, data_pars is required to setup the model (ie CNN with image size...)
   

#########################################################################################
##⑤ Code sample
```python
from mlmodels.models import module_load, data_loader, create_model, fit, predict, stats
from mlmodels.models import load #Load model weights

#### Training
model_pars   =  {  "num_layers": 1,
                  "size": ncol_input, "size_layer": 128, "output_size": ncol_output, "timestep": 4,
                }
data_pars    =  {}
compute_pars =  { "learning_rate": 0.001, }

module        =  module_load( model_uri="model_tf.1_lstm.py" )  #Load file definition
model         =  model_create(module, model_pars)    # Create Model instance
model, sess   =  fit(model, module, data_pars)       # fit the model
metrics_val   =  metrics( model, sess, ["loss"])     # get stats
model.save( "myfolder/", model, module, sess,)
```

#### Inference
```python
model = load(folder)    #Create Model instance
ypred = module.predict(model, module, data_pars, compute_pars)     # predict pipeline
```

###############################################################################
## ⑥ Naming convention

### Function naming
```
pd_   :  input is pandas dataframe
np_   :  input is numpy
sk_   :  inout is related to sklearn (ie sklearn model), input is numpy array
plot_

_col_  :  name for colums
_colcat_  :  name for category columns
_colnum_  :  name for numerical columns (folat)
_coltext_  : name for text data
_colid_  : for unique ID columns\

_stat_ : show statistics
_df_  : dataframe
_num_ : statistics

col_ :  function name for column list related.
```

### Argument Variables naming 
```
df     :  variable name for dataframe
colname  : for list of columns
colexclude
colcat : For category column
colnum :  For numerical columns
coldate : for date columns
coltext : for raw text columns
```


##⑦ Conda install
```
conda create -n py36_tf13 python=3.6.5  -y
source activate py36_tf13

pip install tensorflow=1.13.1
pip install  ipykernel spyder-kernels=0.* -y

```











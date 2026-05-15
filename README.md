# Little Alchemy with Children

This code and data can be used to replicate the results from the project "Tiny Alchemists" by Franziska Brändle, Azzurra Ruggeri Silja Keßler, and Eric Schulz.

## Installation

Install the requirements from "requirements.txt".

## Data

The data collected in the main study (exp1) can be found in 'resources/playerdata/data', and the validation experiment (exp2) can be found in 'resources/playerdata_validation'

## Usage

The code for both experiments can be found in the folder "experiments".

To recreate the plots for experiment 1 in the article, go to 'empowermentexploration/resources/playerdata/BehaviorAnalysis_RCode' for the behavioral results and to 'empowermentexploration/regression/ModelComparison_RCode' for the regression results.

To recreate the plots for experiment 2 in the article, go to 'empowermentexploration/resources/playerdata_validation'.



To recreate the different tools used for setting up this project and the analysis, run `python3 -m empowermentexploration.resources.littlealchemy`. Adapt the main file to select the intended tool.

The resulting data files can be found in the folder 'resources/littlealchemy/data'. They can be accessed via the functions in 'utils/data_handle.py'.

For the preprocessing of the raw data, run the pipeline in 'resources/playerdata' with `python3 -m empowermentexploration.resources.playerdata`. Select the corresponding class in the main file first.

For the behavior analysis, also run `python3 -m empowermentexploration.resources.playerdata`. Select the corresponding class in the main file first. The figures are saved in the 'figures' folder. Further analyses can be found in the 'BehaviorAnalysis_RCode' folder. 

The regression methods can be found under 'regression'. Use the R code to evaluate the regression models. Run `python3 -m empowermentexploration.regression` to recreate the regression runs. 

For the analysis of the validation experiment, use the R-Code in the 'resources/playerdata_validation' folder.

Note: The files under 'resources/customgametree/data' are adopted from Brändle et al. (2022).

## Credits

If you have any questions, or for any additional information contact Franziska Brändle via frabraendle@gmail.com.
The code is based of the code used in 'Intrinsically Motivated Exploration as Empowerment' by Brändle et al. (2022) and modified/written by Franziska Brändle and Silja Keßler. This project was created together with Azzurra Ruggeri and Eric Schulz. Thank you for all your support!

MIT © Franziska Brändle, Silja Keßler
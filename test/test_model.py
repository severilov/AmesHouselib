import hypothesis.strategies as s
from hypothesis import given
from statsmodels.stats.diagnostic import normal_ad
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import StandardScaler

from houselib import calculate_results_for_test, get_df


MODEL_PATH = './src/models/model.pkl'
DATA_PATH = './data/processed/ames_prepared.csv'

def test_normal_errors_assumption(modelpath=MODEL_PATH, datapath=DATA_PATH, p_value_thresh=0.05):
    """
    Normality: Assumes that the error terms are normally distributed. If they are not,
    nonlinear transformations of variables may solve this.

    Using Anderson-Darling test
    """
    results = calculate_results_for_test(modelpath, datapath)
    p_value = normal_ad(results['Residuals'])[1]

    assert p_value > p_value_thresh


def test_multicollinearity_assumption(datapath=DATA_PATH):
    """
    Multicollinearity: Assumes that predictors are not correlated with each other. If there is
                       correlation among the predictors, then either remove predictors with high
                       Variance Inflation Factor (VIF) values or perform dimensionality reduction

                       > 10: An indication that multicollinearity may be present
                       > 100: Certain multicollinearity among the variables
    """
    df_0609, df_2010 = get_df(datapath)
    scaler = StandardScaler()
    X_train = df_0609.drop(['SalePrice', 'LnSalePrice'], axis=1)
    features = scaler.fit_transform(X_train)

    VIF = [variance_inflation_factor(features, i) for i in range(features.shape[1])]

    # total cases of possible or definite multicollinearity
    possible_multicollinearity = sum([1 for vif in VIF if vif > 10])
    definite_multicollinearity = sum([1 for vif in VIF if vif > 100])

    # assert possible_multicollinearity == 0
    assert definite_multicollinearity == 0

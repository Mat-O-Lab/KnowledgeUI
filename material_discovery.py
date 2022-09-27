## Materials Discovery
import app
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from scipy.spatial import distance_matrix
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor as SKRFR
from sklearn.ensemble import AdaBoostRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from lolopy.learners import RandomForestRegressor
from sklearn.preprocessing import StandardScaler


class learn():
    y_pred_dtr_mean = None
    y_pred_dtr_std = None
    y_pred_dtr = None

    def __init__(self, dataframe, model, target_df, feature_df, fixed_target_df, strategy, sigma,
                 target_selected_number2, fixedtarget_selected_number2, min_or_max_target, min_or_max_fixedtarget):

        self.dataframe = dataframe
        self.df_final = dataframe
        self.model = model
        self.strategy = strategy
        self.targets = target_df
        self.target_df = self.dataframe[self.targets]
        self.fixed_targets = fixed_target_df
        self.fixed_target_df = self.dataframe[self.fixed_targets]
        self.features = feature_df
        self.feature_df = self.dataframe[self.features]
        self.sigma = sigma
        # self.distance=distance
        self.target_selected_number2 = target_selected_number2
        self.fixedtarget_selected_number2 = fixedtarget_selected_number2
        # print('dic', self.target_selected_number2)
        self.min_or_max_target = min_or_max_target
        self.min_or_max_fixedtarget = min_or_max_fixedtarget
        first_selected_target = self.targets[0]

        # self.PredIdx = pd.DataFrame([first_selected_target])[0] #pd.isnull(self.dataframe[first_selected_target]).to_numpy().nonzero()#[0]
        # self.SampIdx = self.dataframe.index.difference(self.PredIdx)
        # first_selected_target=list(confirm_target(target_selection_application))[0]
        self.PredIdx = pd.isnull(self.dataframe[first_selected_target]).to_numpy().nonzero()[0]
        self.SampIdx = self.dataframe.index.difference(self.PredIdx)
        # print('PRED', self.PredIdx.shape, self.PredIdx)
        # print('Sam', self.SampIdx.shape, self.SampIdx)
        print('self.target_df', self.target_df)

    """
    def scale_data(self):
        dataframe_norm=(self.dataframe-self.dataframe.mean())/self.dataframe.std()
        target_df_norm=(self.target_df-self.target_df.mean())/self.target_df.std()
        features_df_norm=(self.features_df-self.features_df.mean())/self.features_df.std()
        fixed_target_df_norm=(self.fixed_target_df-self.fixed_target_df.mean())/self.fixed_target_df.std()

        self.features_df=features_df_norm
        self.target_df=target_df_norm
        self.dataframe=dataframe_norm
        self.fixed_target_df=fixed_target_df_norm
    """

    def scale_data(self):
        scaler = StandardScaler()
        dataframe_norm = scaler.fit_transform(self.dataframe)
        target_df_norm = scaler.fit_transform(self.target_df)
        features_df_norm = scaler.fit_transform(self.feature_df)
        fixed_target_df_norm = scaler.fit_transform(self.fixed_target_df)

        self.features_df = pd.DataFrame(features_df_norm)
        self.target_df = pd.DataFrame(target_df_norm)
        self.dataframe = pd.DataFrame(dataframe_norm)
        self.fixed_target_df = pd.DataFrame(fixed_target_df_norm)
        # print(self.dataframe)

    def start_learning(self):
        self.dataframe = self.decide_max_or_min(self.min_or_max_target, self.dataframe)
        self.dataframe = self.decide_max_or_min(self.min_or_max_fixedtarget, self.dataframe)
        self.fixed_target_selection_idxs = self.fixed_targets  # confirm_fixed_target(fixed_target_selection_application)
        self.fixed_target_idxs = self.fixed_targets  # confirm_fixed_target(fixed_target_selection_application)

        # self.fixed_target_df=self.dataframe[self.fixed_target_selection_idxs]
        self.target_selection_idxs = self.targets  # confirm_target(target_selection_application)
        self.features_df = self.feature_df  # confirm_features(feature_selector_application)]
        # self.target_df=self.dataframe[self.targets]#confirm_target(target_selection_application)]
        print('feature', self.features_df)
        self.decide_model(self.model)
        if self.strategy == 'MEI (exploit)':
            self.sigma = 0
            self.distance = 0
        elif self.strategy == 'MU (explore)':
            self.sigma = 1
            self.distance = 0
        elif self.strategy == 'MLI (explore & exploit)':
            self.distance = 0

        util = self.update_strategy(self.strategy)
        distance = distance_matrix(self.features_df.iloc[self.PredIdx], self.features_df.iloc[self.SampIdx])
        min_distances = distance.min(axis=1)
        max_of_min_distances = min_distances.max()
        novelty_factor = min_distances * (max_of_min_distances ** (-1))

        df = self.dataframe  # .abs

        df = df.iloc[self.PredIdx].assign(Utility=pd.Series(util).values)
        df = df.loc[self.PredIdx].assign(Novelty=pd.Series(novelty_factor).values)
        print('test df', df, df.columns)
        if (self.Uncertainty.ndim > 1):
            for i in range(len(self.targets)):
                df[self.targets[i]] = self.Expected_Pred[:, i]
                uncertainty_name_column = 'Uncertainty (' + self.targets[i] + ' )'
                df[uncertainty_name_column] = self.Uncertainty[:, i].tolist()
                # df = df.loc[self.PredIdx].assign(Uncertainty=pd.Series(self.Uncertainty[:,i]).values)
                # df=df.rename(columns={"Uncertainty":"Uncertainty  ("+self.targets[i]+")"})
        else:
            df[self.targets] = self.Expected_Pred.reshape(len(self.Expected_Pred), 1)
            uncertainty_name_column = 'Uncertainty (' + self.targets + ' )'
            df[uncertainty_name_column] = self.Uncertainty.reshape(len(self.Uncertainty), 1)
            # df = df.loc[self.PredIdx].assign(Uncertainty=pd.Series(self.Uncertainty[:]).values)
            # df=df.rename(columns={"Uncertainty":"Uncertainty  ("+self.targets+")"})

        show_df = df.sort_values(by='Utility', ascending=False)
        target_list = show_df[self.targets]
        # print('showfxdf', show_df)
        # print('self.target', self.targets)
        # print('targetlist', target_list)
        # print('namenotinsided', show_df.columns)
        if len(self.fixed_target_selection_idxs) > 0:
            target_list = pd.concat((target_list, show_df[self.fixed_target_idxs]), axis=1)
        target_list = pd.concat((target_list, show_df['Utility']), axis=1)

        # print('targetlist', target_list)
        g = sns.PairGrid(target_list, diag_sharey=False, corner=True, hue='Utility')
        g.map_diag(sns.histplot, hue=None, color=".3")
        g.map_lower(sns.scatterplot)
        g.add_legend()
        plt.savefig('static/img.png')

        return show_df

        # display(Markdown(show_df.to_markdown()))

    def weight_fixed_tars(self):
        fixedtarget_weight = []
        for i in self.fixedtarget_selected_number2:
            fixedtarget_weight.append(self.fixedtarget_selected_number2[i])

        fixed_targets_in_prediction = self.fixed_target_df.iloc[self.PredIdx].to_numpy()

        for weights in range(len(fixedtarget_weight)):
            fixed_targets_in_prediction[weights] = fixed_targets_in_prediction[weights] * fixedtarget_weight[weights]
        return fixed_targets_in_prediction.sum(axis=1)

    def weight_Pred(self):

        target_weight = []
        for i in self.target_selected_number2:
            target_weight.append(float(self.target_selected_number2[i]))
        print('target_weight',target_weight)
        print(self.Expected_Pred)
        if (self.Expected_Pred.ndim > 2):
            for weights in range(len(target_weight)):
                self.Expected_Pred[:, weights] = self.Expected_Pred[:, weights] * target_weight[weights]
        else:
            self.Expected_Pred = self.Expected_Pred * (target_weight[0])
            self.Uncertainty = self.Uncertainty * (target_weight[0])

    def updateIndexMEI(self):
        self.weight_Pred()

        Expected_Pred_norm = (self.Expected_Pred - np.array(self.target_df.iloc[self.SampIdx].mean(axis=0))) / np.array(
            self.target_df.iloc[self.SampIdx].std(axis=0))
        # self.scale_data()
        if (len(self.fixed_targets) > 0):
            fixed_targets_in_prediction = self.weight_fixed_tars()
        else:
            fixed_targets_in_prediction = np.zeros(len(self.PredIdx))
        if (len(self.targets) > 1):
            util = fixed_targets_in_prediction.squeeze() + Expected_Pred_norm.sum(axis=1).squeeze()
        else:
            util = fixed_targets_in_prediction.squeeze() + Expected_Pred_norm.squeeze()
        return util

    def decide_max_or_min(self, source, dataframe):
        for s in source:
            if (source[s] == 'min'):
                dataframe[s] = dataframe[s] * (-1)
        return dataframe

    def updateIndexMLI(self):

        self.weight_Pred()
        Uncertainty_norm = self.Uncertainty / np.array(self.target_df.iloc[self.SampIdx].std())
        Expected_Pred_norm = (self.Expected_Pred - np.array(self.target_df.iloc[self.SampIdx].mean())) / np.array(
            self.target_df.iloc[self.SampIdx].std())
        target_weight = []
        for i in self.target_selected_number2:
            target_weight.append(self.target_selected_number2[i])

        if (self.Expected_Pred.ndim >= 2):

            for weights in range(len(target_weight)):
                Expected_Pred_norm[:, weights] = Expected_Pred_norm[:, weights] * target_weight[weights]
                Uncertainty_norm[:, weights] = Uncertainty_norm[:, weights] * target_weight[weights]

        else:

            Expected_Pred_norm = Expected_Pred_norm * target_weight[0]
            Uncertainty_norm = Uncertainty_norm * target_weight[0]
        # self.scale_data()
        if (len(self.fixed_targets) > 0):
            fixed_targets_in_prediction = self.weight_fixed_tars()
        else:
            fixed_targets_in_prediction = np.zeros(len(self.PredIdx))
        if (len(self.targets) > 1):
            util = fixed_targets_in_prediction.squeeze() + Expected_Pred_norm.sum(
                axis=1) + self.sigma * Uncertainty_norm.sum(axis=1)
        else:
            util = fixed_targets_in_prediction.squeeze() + Expected_Pred_norm.squeeze() + self.sigma * Uncertainty_norm.squeeze()
        return util

    def fit_DT_wJK(self):

        td, tl = self.jk_resampling()
        self.y_pred_dtr = []
        for i in range(len(td)):
            dtr = DecisionTreeRegressor()
            dtr.fit(td[i], tl[i])

            self.y_pred_dtr.append(dtr.predict(self.features_df.iloc[self.PredIdx]))
        self.y_pred_dtr = np.array(self.y_pred_dtr)
        self.Expected_Pred = self.y_pred_dtr.mean(axis=0)
        self.Uncertainty = self.y_pred_dtr.std(axis=0)
        return self.Expected_Pred, self.Uncertainty

    def fit_TE_wJK(self):
        td, tl = self.jk_resampling()
        # print('td', td, td.shape)
        # print('tl', tl, tl.shape)
        self.y_pred_dtr = []
        for i in range(len(td)):
            ## alternative Ensamble Learners below:
            dtr = SKRFR(n_estimators=10)
            dtr.fit(td[i], tl[i])
            self.y_pred_dtr.append(dtr.predict(self.features_df.iloc[self.PredIdx]))
        self.y_pred_dtr = np.array(self.y_pred_dtr)
        self.Expected_Pred = self.y_pred_dtr.mean(axis=0)
        self.Uncertainty = self.y_pred_dtr.std(axis=0)

    def fit_RF_wJK(self):
        dtr = RandomForestRegressor()
        self.x = self.features_df.iloc[self.SampIdx].to_numpy()
        self.y = self.target_df.iloc[self.SampIdx].to_numpy()  # .sum(axis=1).to_numpy()
        if self.y.shape[0] < 8:
            self.x = np.tile(self.x, (4, 1))
            self.y = np.tile(self.y, (4, 1))

        dtr.fit(self.x, self.y)
        self.Expected_Pred, self.Uncertainty = dtr.predict(self.features_df.iloc[self.PredIdx], return_std=True)

    #      self.Expected_Pred, self.Uncertainty = dtr.predict(self.features_df.iloc[self.PredIdx].to_numpy(), return_std=True)

    def fit_GP(self):
        for i in range(len(self.targets)):
            kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))

            dtr = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)
            temp = self.targets  # self.target_selection_idxs.tolist()

            # print('target_zero', self.target_df)
            temp_new = filter(lambda x: x != self.targets[i], temp)
            temp_new = list(temp_new)
            var_temp = self.SampIdx[i]
            # print('temp', temp_new)
            # print(self.features_df.iloc[self.SampIdx])
            # target_df = self.dataframe[self.target_df]
            y = self.target_df[temp_new].iloc[self.SampIdx].to_numpy()
            x = self.features_df.iloc[self.SampIdx].to_numpy()
            print('x', x)
            print('y', y)
            dtr.fit(x, y)
            self.Expected_Pred, uncertainty = dtr.predict(self.features_df.iloc[self.PredIdx], return_std=True)

            if (i == 0):
                uncertainty_stacked = uncertainty
            else:
                uncertainty_stacked = np.vstack((uncertainty_stacked, uncertainty))

        self.Uncertainty = uncertainty_stacked.T

    """
    def fit_GP(self):
        self.Uncertainty=np.empty([len(self.PredIdx)])

        kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
        print('feature', (self.features_df.iloc[self.SampIdx]))
        print('target', self.target_df.iloc[self.SampIdx])
        print('len', len(self.target_selection_idxs))

        dtr = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)
        for i in range( len(self.features_df.iloc[self.SampIdx])):
            dtr.fit(self.features_df.iloc[self.SampIdx], self.target_df.iloc[self.SampIdx])
            self.Expected_Pred, uncertainty= dtr.predict(self.features_df.iloc[self.PredIdx], return_std=True)
        uncertainty_stacked= np.vstack((self.Uncertainty,uncertainty))
        self.Uncertainty=uncertainty_stacked.T
    """

    def decide_model(self, model):
        if model == 'lolo Random Forrest (RF)':
            self.fit_RF_wJK()
        elif model == 'Decision Trees (DT)':
            self.fit_DT_wJK()
        elif model == 'Random Forrest (RFscikit)':
            self.fit_TE_wJK()
        elif model == 'Gaussian Process Regression (GPR)':
            self.fit_GP()

    def jk_resampling(self):
        from resample.jackknife import resample as b_resample
        td = [x for x in b_resample(self.features_df.iloc[self.SampIdx])]
        tl = [x for x in b_resample(self.target_df.iloc[self.SampIdx])]
        tl = np.array(tl)
        td = np.array(td)
        return td, tl

    def update_strategy(self, strategy):
        util2=None
        if strategy == 'MEI (exploit)':
            util2 = self.updateIndexMEI()
        # elif strategy=='MU (explore)':
        #    util=self.updateIndexMU()
        elif strategy == 'MLI (explore & exploit)':
            util2 = self.updateIndexMLI()
        # elif strategy=='MEID (exploit)':
        #    util=self.updateIndexMEID()
        else:  # strategy=='MLID (explore & exploit)':
            # util=self.updateIndexMLID()
            print('Thank you ')
        return util2

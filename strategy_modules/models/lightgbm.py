import numpy as np
import os
import lightgbm as lgb
from sklearn import metrics
from common.config import ConfigUtils
from sklearn.metrics import classification_report

class LGB():
    def __init__(self, trn, trn_label, val, val_label, name):
        self.trn = trn
        self.val = val
        self.trn_label = trn_label
        self.val_label = val_label
        self.path = os.path.join(ConfigUtils.get_model("MODELPATH"), name)

        if not os.path.exists(ConfigUtils.get_model("MODELPATH")):
            os.makedirs(ConfigUtils.get_model("MODELPATH"))

        self.param = {
            'num_leaves': 60,
            'n_estimatores': 3000,
            'min_data_in_leaf': 30,
            'objective': 'multiclass',
            'num_class': 21,
            'lambda_l1': 0.1,
            'lambda_l2': 0.2,
            'max_depth': 5,
            'learning_rate': 0.01,
            "min_child_samples": 20,
            "boosting": "gbdt",
            # "feature_fraction": 0.45,
            "bagging_freq": 1,
            "bagging_fraction": 0.8,
            "bagging_seed": 11,
            "nthread": 30,
            'metric': 'multi_logloss',
            "random_state": 1111,
            "verbosity": -1
        }

        # self.params = {
        #       'task': 'train',
        #       'boosting_type': 'gbdt',  # 设置提升类型
        #       'objective': 'regression',  # 目标函数
        #       'metric': {'l2', 'auc'},  # 评估函数
        #       'num_leaves': 31,  # 叶子节点数
        #       'learning_rate': 0.05,  # 学习速率
        #       'feature_fraction': 0.9,  # 建树的特征选择比例
        #       'bagging_fraction': 0.8,  # 建树的样本采样比例
        #       'bagging_freq': 5,  # k 意味着每 k 次迭代执行bagging
        #       'verbose': 1  # <0 显示致命的, =0 显示错误 (警告), >0 显示信息
        # }

    def train(self, num_round=9000):
        trn_data = lgb.Dataset(self.trn, self.trn_label)
        val_data = lgb.Dataset(self.val, self.val_label)
        self.clf = lgb.train(self.param, trn_data, num_round, valid_sets=[trn_data, val_data], verbose_eval=300,
                             early_stopping_rounds=1000)
        self.persist()
        self.validate()


    def validate(self, ):
        oof_lgb = self.clf.predict(self.val, num_iteration=self.clf.best_iteration)
        result = np.argmax(oof_lgb, axis=1)
        print(classification_report(result, self.val_label))

    def persist(self, ):
        self.clf.save_model(self.path)

    def load(self, ):
        self.clf = lgb.Booster(model_file=self.path)
        print('[finish load mode from path: {}]'.format(self.path))

    def predict(self, testX):
        testY = self.clf.predict(testX, num_iteration=self.clf.best_iteration)
        return testY

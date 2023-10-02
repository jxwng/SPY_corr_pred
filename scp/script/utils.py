import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.tools.eval_measures import rmse


def get_forecast(stocks, params, model, window, test, alpha=0.1):
    preds = []
    for t in stocks:
        m = model[t]
        y_pred = m.get_forecast(window).summary_frame(alpha=alpha)
        y_pred['ticker'] = t
        y_pred.index = test.index
        preds.append(y_pred)
        #params[t].update(m.params.to_dict())
        params[t].update({'Test RMSE': rmse(test[t], y_pred['mean'])})
        params[t].update({'Test Mean': test[t].mean()})
    summary = pd.DataFrame(params).T
    return summary, pd.concat(preds, axis=0)


def get_deep_ar_forecast(train_ds, model, window, test, alpha=0.1):
    preds = []
    params = {}
    for item in list(model.predict(train_ds)):
        mean = item.samples.mean(axis=0)
        mean_ci_lower = np.percentile(item.samples, alpha * 100, axis=0)
        mean_ci_upper = np.percentile(item.samples, (1 - alpha) * 100, axis=0)
        dates = pd.date_range(start=item.start_date.to_timestamp(), periods=len(mean), freq='B')
        y_pred = pd.DataFrame(
            {'date': dates, 'ticker': item.item_id, 'mean': mean, 'mean_ci_lower': mean_ci_lower,
             'mean_ci_upper': mean_ci_upper})
        preds.append(y_pred)
        params[item.item_id] = {}
        params[item.item_id].update({'Test RMSE': rmse(test[item.item_id], y_pred['mean'])})
        params[item.item_id].update({'Test Mean': test[item.item_id].mean()})
    summary = pd.DataFrame(params).T
    return summary, pd.concat(preds, ignore_index=True)


def plot_forecast(train, test, preds, mean_col='mean', lower_col='mean_ci_lower', upper_col='mean_ci_upper'):
    stocks = train.columns.values
    fig, axs = plt.subplots(len(stocks), 1, figsize=(15, 15), sharex='all')

    for i, t in enumerate(stocks):
        axs[i].plot(train.index, train[t])
        axs[i].plot(test.index, test[t])
        axs[i].plot(preds.loc[preds.ticker == t, 'date'], preds.loc[preds.ticker == t, mean_col])
        axs[i].fill_between(preds.loc[preds['ticker'] == t, 'date'], preds.loc[preds['ticker'] == t, lower_col],
                            preds.loc[preds['ticker'] == t, upper_col], color='k', alpha=0.1)
        axs[i].set_title(t)

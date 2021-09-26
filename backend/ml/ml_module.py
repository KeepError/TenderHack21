import numpy as np
import pandas as pd
import json

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import warnings

warnings.simplefilter("ignore", UserWarning)
pd.options.mode.chained_assignment = None


def prepare_cte(data):
    data = data[['ID СТЕ', 'Категория', 'Код КПГЗ']].set_index('ID СТЕ')
    data["KPGZ_short"] = data["Код КПГЗ"].apply(str).apply(lambda x: '.'.join(x.split('.')[:3]))
    return data


def format_cte(x):
    jx = json.loads(x)
    sx = set()
    for obj in jx:
        if obj['Id'] is not None:
            sx.add(data_cte.at[obj['Id'], 'KPGZ_short'])
    return sx


def prepare_contracts(data):
    data = data[['Дата публикации КС на ПП',
                 'Дата заключения контракта',
                 'Цена контракта', 'ИНН заказчика',
                 'ИНН поставщика', 'СТЕ']]
    data = data[~data['Дата заключения контракта'].isna()]
    data['СТЕ'] = data['СТЕ'].apply(format_cte).apply(set)
    data = data[data['СТЕ'] != set()]
    data = data[data['Дата публикации КС на ПП'] <= data['Дата заключения контракта']]
    data['ИНН заказчика'] = data['ИНН заказчика'].apply(str)
    data = data.sort_values('Дата публикации КС на ПП')
    return data


def make_data_supplier(data_contracts):
    data_supplier = dict()
    for i in data_contracts.index:
        inn = data_contracts.at[i, 'ИНН поставщика']
        s = set(data_contracts.at[i, 'СТЕ'])
        if inn in data_supplier.keys():
            data_supplier[inn] = data_supplier[inn].union(s)
        else:
            data_supplier[inn] = s
    data_supplier = [(inn, data_supplier[inn]) for inn in data_supplier.keys()]
    data_supplier_df = pd.DataFrame(data_supplier, columns=['inn', 'cats']).set_index('inn')
    data_supplier_df = data_supplier_df[data_supplier_df['cats'] != set()]
    return data_supplier_df


def get_categories(client_inn, order_frequency=2, treshold=.8):
    client_df = data_contracts[data_contracts['ИНН заказчика'] == client_inn]

    cte_freq_dict = dict()
    for cte in client_df["СТЕ"]:
        for e in cte:
            if e in cte_freq_dict.keys():
                cte_freq_dict[e] += 1
            else:
                cte_freq_dict[e] = 1

    new_cte = []
    for cte in client_df["СТЕ"]:
        freq = 0
        cat = ''
        for e in cte:
            if cte_freq_dict[e] > freq:
                freq = cte_freq_dict[e]
                cat = e
        new_cte.append(e)
    client_df["СТЕ"] = new_cte
    unique_cte = client_df['СТЕ'].unique()

    encoder = dict()
    decoder = dict()
    for i, key in enumerate(unique_cte):
        encoder[key] = i + 1
        decoder[i + 1] = key

    client_df['СТЕ'] = client_df['СТЕ'].apply(lambda x: encoder[x])
    client_df = client_df.drop(['ИНН заказчика', 'ИНН поставщика', 'Дата заключения контракта', 'Цена контракта'],
                               axis=1)

    freq_cte = set(client_df["СТЕ"].value_counts()[client_df["СТЕ"].value_counts() >= order_frequency].index)
    client_df = client_df[client_df["СТЕ"].apply(lambda x: x in freq_cte)]
    client_df = client_df.reset_index(drop=True)

    assert not client_df.empty, "Not enough orders to make predictions"

    h_start = client_df.at[0, 'Дата публикации КС на ПП'].value // (10 ** 9 * 60 * 60)
    h_end = client_df.at[client_df.index[-1], 'Дата публикации КС на ПП'].value // (10 ** 9 * 60 * 60)

    freq_d = f'{min(int((h_end - h_start) // (len(client_df) * 1.1)), 48)}h'  # two days at most
    client_df['Дата публикации КС на ПП'] = client_df['Дата публикации КС на ПП'].astype('datetime64').dt.ceil(freq_d)

    r = pd.date_range(start=client_df['Дата публикации КС на ПП'].min(),
                      end=client_df['Дата публикации КС на ПП'].max(), freq=freq_d)
    client_df = client_df.set_index('Дата публикации КС на ПП')
    client_df = client_df[~client_df.index.duplicated()].reindex(r).fillna(0).rename_axis(
        'Дата публикации КС на ПП').reset_index()
    client_df['Дата публикации КС на ПП'] = client_df['Дата публикации КС на ПП'].astype('datetime64').dt.ceil(freq_d)

    client_df['month'] = client_df['Дата публикации КС на ПП'].dt.month
    client_df['day'] = client_df['Дата публикации КС на ПП'].dt.day
    client_df['week_day'] = client_df['Дата публикации КС на ПП'].dt.weekday
    client_df['week_of_month'] = (client_df['Дата публикации КС на ПП'].dt.day - client_df[
        'Дата публикации КС на ПП'].dt.weekday - 2) // 7 + 2
    client_df['weekday_order'] = (client_df['Дата публикации КС на ПП'].dt.day + 6) // 7
    client_df = client_df.set_index('Дата публикации КС на ПП')

    client_df['СТЕ'] = client_df['СТЕ'].astype('int')

    x_train, y_train = client_df.drop(['СТЕ'], axis=1), client_df['СТЕ']
    grid_param = {"n_estimators": range(2, 15, 2),
                  "max_depth": range(2, 15, 2),
                  "class_weight": ['balanced'],
                  "random_state": [42]}
    model = RandomForestClassifier()
    grid = GridSearchCV(estimator=model, param_grid=grid_param,
                        scoring="balanced_accuracy",
                        cv=3, verbose=0, n_jobs=-1)
    grid.fit(x_train, y_train)
    random_forest = grid.best_estimator_
    random_forest.fit(x_train, y_train)

    future_date = pd.date_range(start=client_df.index.max(),
                                end=pd.Timestamp.today().round('1d') + pd.DateOffset(days=30), freq=freq_d)
    future_date_df = pd.DataFrame(future_date, columns=['Дата публикации КС на ПП'])
    future_date_df['Дата публикации КС на ПП'] = future_date_df['Дата публикации КС на ПП'].astype('datetime64[ns]')
    future_date_df['month'] = future_date_df['Дата публикации КС на ПП'].dt.month
    future_date_df['day'] = future_date_df['Дата публикации КС на ПП'].dt.day
    future_date_df['week_day'] = future_date_df['Дата публикации КС на ПП'].dt.weekday
    future_date_df['week_of_month'] = (future_date_df['Дата публикации КС на ПП'].dt.day - future_date_df[
        'Дата публикации КС на ПП'].dt.weekday - 2) // 7 + 2
    future_date_df['weekday_order'] = (future_date_df['Дата публикации КС на ПП'].dt.day + 6) // 7
    future_date_df = future_date_df.set_index('Дата публикации КС на ПП')

    preds = random_forest.predict(future_date_df)
    preds = preds[future_date_df.index + pd.DateOffset(days=30) > pd.Timestamp.today().round('1d')]

    unique, counts = np.unique(preds, return_counts=True)
    ctes = [0 if not i else decoder[i] for i in unique]
    for i, e in enumerate(ctes):
        if e:
            counts[i] *= cte_freq_dict[e]
    res = np.array(sorted(zip(counts, unique)))[::-1]
    res = res[res[:, 0] >= (treshold * res[0, 0])]
    categories = [None if not i else decoder[i] for i in res[:, 1]]
    assert not all(map(lambda x: x is None, categories)), "Not enough orders to make predictions"

    result = []
    for code_kpgz in categories:
        if not code_kpgz is None:
            assert not data_kpgz.index[data_kpgz.kpgzCode == code_kpgz].empty, f"No such code: {code_kpgz}"
            result.append(data_kpgz.at[data_kpgz.index[data_kpgz.kpgzCode == code_kpgz][0], 'kpgzName'])

    return result


def check_tender(data_supplier_df, inn, current_contracts):
    def score(x, total):
        return len(x.intersection(total)) * 100 / len(total)

    res = []
    if inn not in data_supplier_df.index:
        res = [(i, 0) for i in current_contracts.index]
        return res
    for i in current_contracts.index:
        contract_cats = current_contracts.at[i, 'СТЕ']
        if contract_cats != set():
            res.append((i, score(data_supplier_df.at[inn, 'cats'], contract_cats)))
    return sorted(res, key=lambda x: -x[1])


content_path = "ml/content/"
data_contracts_raw = pd.read_excel(content_path + "tenderHack/Контракты.xlsx")
data_cte_raw = pd.read_excel(content_path + "tenderHack/СТЕ.xlsx")
data_kpgz = pd.read_excel(content_path + "kpgz.xlsx")

data_cte = prepare_cte(data_cte_raw)
data_contracts = prepare_contracts(data_contracts_raw)

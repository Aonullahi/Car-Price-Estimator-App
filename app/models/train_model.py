import os
import pickle
import re
import sys
import textwrap

import pandas as pd
import numpy as np
from numpy.random import RandomState
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from app import settings

from ..helpers import files as files_helper
from ..utils import files as files_utils

def process_data(path_to_dataset):

    to_replace = {'venza':'toyota', 'scion':'toyota', 'corolla':'toyota','rx':'lexus','es':'lexus','rex':'lexus','premacy':'mazda',
    'kinglong':'hiace','gl450':'mercedes-benz','a190':'mercedes-benz','accord':'honda','dzire':'suzuki','ertiga':'suzuki','jimny':'suzuki',
    'grand':'suzuki','ciaz':'suzuki','g35x':'infiniti','s-type':'jaguar'}

    data = pd.read_csv(path_to_dataset)
    data.dropna(inplace=True)
    data.drop_duplicates(['car_ID'], inplace=True)
    data.drop(data[data['year']<1980].index, inplace=True)
    data.replace('[\₦,]', '', regex=True,inplace = True )
    data['mileage'].replace('Km', '', regex=True,inplace = True )
    data['price'] = data['price'].apply(int)
    data['mileage'] = data['mileage'].apply(int)
    data['year'] = data['year'].apply(int)
    data['status_rank'] = 1
    data['status_rank'] = np.where(data['sec_status']=='Foreign Used', 2 , data['status_rank'])
    data['status_rank'] = np.where(data['sec_status']=='New', 3 , data['status_rank'])
    data['manufacturer'] = [i.split()[1].lower() for i in data['car_model']]
    data['manufacturer'].replace(to_replace=to_replace, inplace=True)
    data['manuyear'] = data['manufacturer'] + data['year'].astype(str)
    data['price_cat'] = pd.cut(data['price'], bins = 100, labels=list(range(1,101))).astype(int)
    h = data.groupby(['manuyear'])['price_cat'].median().reset_index()
    h.rename(columns={'price_cat':'rank'},inplace=True)
    data = pd.merge(data,h, on ="manuyear", how = "left")
    processed_data =  data.drop(columns = ['_id', 'car_model', 'car_ID', 'sec_status', 'manufacturer', 'manuyear', 'price_cat'])
    return processed_data


def train(path_to_dataset, version_id):
    processed_data = process_data(path_to_dataset)
    # split into training and validation
    training_set, validation_set = _split_dataset(processed_data, 0.25, 1)
    print('training set has %s rows' % len(training_set))
    print('validation set has %s rows' % len(validation_set))

    # train model
    model = LinearRegression()
    model.fit(training_set[['year', 'mileage', 'status_rank', 'rank']], training_set["price"])

    # evaluate model
    validation_predictions = model.predict(validation_set[['year', 'mileage', 'status_rank', 'rank']])

    print(mean_squared_error(validation_set[["price"]], validation_predictions, squared=False))



    filename = files_helper.make_filename(version_id)

    path_to_model_file = settings.MODELS_ROOT + "/" + filename

    _persist_to_disk(model, path_to_model_file)


def _split_dataset(df, validation_percentage, seed):
    state = RandomState(seed)
    validation_indexes = state.choice(df.index, int(len(df.index) * validation_percentage), replace=False)
    training_set = df.loc[~df.index.isin(validation_indexes)].copy()
    validation_set = df.loc[df.index.isin(validation_indexes)].copy()
    return training_set, validation_set


def _persist_to_disk(classifier, path_to_file):

    with open(path_to_file, "wb") as f:
        pickle.dump(classifier, f)

    if os.path.isfile(path_to_file):
        print("Successfully saved model at {}".format(path_to_file))
        return 0
    else:
        print("Something went wrong; failed to persist the trained classifier to disk.")
        return 1


def _validate_args(path, model_version):
    """
    Validation function. Does not return anything, only produces side effects
    in case the passed parameters are not valid.
    :param path: string
    :param model_version: string
    :return: None
    """
    if not os.path.isfile(files_utils.to_abs_path(path)):
        raise ValueError("{} is not a valid path.".format(path))

    if not re.match('^v\d+', model_version):
        raise ValueError("{} is not a valid version id. Valid values: v0,v1,v2, etc.".format(model_version))


if __name__ == '__main__':

    args = sys.argv

    if len(args) != 3:
        help = """
            Train a logistic regression classifier on a parquet dataset.
            
            Usage: python -m app.models.train_model <path-to-parquet-dataset> <model-version>
            
            Example: python -m app.models.train_model path/to/my/model.parquet v2
        """

        print(textwrap.dedent(help))
        sys.exit(1)

    path = args[1]
    model_version = args[2]

    _validate_args(path, model_version)

    path_to_dataset = files_utils.to_abs_path(path)

    print("\nWill train model {} using the file at: {} \n\n".format(model_version, path_to_dataset))

    path_to_models_directory = settings.MODELS_ROOT

    train(path_to_dataset, model_version)

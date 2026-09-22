import os; os.system('clear')
import numpy as np
from scipy import signal
import scipy
from leg.models import train_test_split
import pandas as pd
import leg.parameters as p
from leg.models import features_v1
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt
import joblib



def remove_invalid_windows(features, labels):
    """Remove windows whose features contain NaN or inf (e.g. flat signal)"""
    valid = np.isfinite(features).all(axis=1)
    return features[valid], labels[valid]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Train the contraction/relaxation RF classifier')
    parser.add_argument('files', nargs='+', help='Recording names in recordings/ (without .npy)')
    parser.add_argument('--no-plot', action='store_true', help='Do not show the label plot')
    parser.add_argument('--k', type=int, default=10, help='Number of features kept by ANOVA F-score selection')
    args = parser.parse_args()

    # Load data
    files = args.files

    data = []
    for file in files:
        temp = np.load(f'recordings/{file}.npy')
        print(temp.shape)
        data.append(temp)

    data = np.hstack(data)



    n_points = data.shape[1]
    print(f"Recording time: {n_points/250} s")

    df = pd.DataFrame(data.T, columns=p.CH_NAMES)
    print(df)
    df['labels'] = df['MARKERS']
    print(df)
    print(set(df['labels'].tolist()))
    

    df = df[df['labels'] != 0]
    df['labels'] = df['labels'].apply(lambda x: 1 if x == 2 else 0)

    fig = plt.figure()

    plt.plot(df['labels'].to_numpy(), label='orig')

    # Smooth filter
    kernel_size = 200 
    #df['labels'] = np.convolve(df['labels'].to_numpy(), np.array([1]*kernel_size) / kernel_size, mode='same')
    #df['labels'] = np.convolve(df['labels'].to_numpy(), np.array([1]*kernel_size) / kernel_size, mode='same')
    #df['labels'] = np.convolve(df['labels'].to_numpy(), np.array([1]*kernel_size) / kernel_size, mode='same')

    plt.plot(df['labels'].to_numpy(), label='filter')

    #df['labels'] = df['labels'].apply(lambda x: 1 if x > 0.5 else 0)

    plt.plot(df['labels'].to_numpy(), label='final')
    plt.legend()

    if not args.no_plot:
        plt.show()
    print(df)
    train_data, train_label, test_data, test_label = train_test_split([df], 
                                         columna=['C1', 'C2', 'C3', 'C4'],
                                         window_size=25,
                                         overlap=0, 
                                         test_size=0.2,
                                         random_state=42)
    
    print(train_data.shape, train_label.shape, test_data.shape, test_label.shape)

    # Feature extraction
    train_features = [features_v1(x.T)[0] for x in train_data]
    train_features = np.array(train_features)

    test_features = [features_v1(x.T)[0] for x in test_data]
    test_features = np.array(test_features)

    # Remove invalid windows
    train_features, train_label = remove_invalid_windows(train_features, train_label)
    test_features, test_label = remove_invalid_windows(test_features, test_label)

    print(train_features.shape, test_features.shape)
    print(train_label.shape, test_label.shape)

    # Normalisation -> ANOVA F-score feature selection -> Random Forest.
    # The whole pipeline is saved, so realtime inference still passes all 36 features.
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('select', SelectKBest(f_classif, k=args.k)),
        ('rf', RandomForestClassifier(random_state=42)),
    ])

    param_grid = {
        'rf__n_estimators': [10, 20, 30, 40, 50, 80, 100],
        'rf__max_depth': [None, 10, 20],
        'rf__min_samples_split': [2, 5],
    }

    grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='accuracy')
    grid_search.fit(train_features, train_label)
    best_clf = grid_search.best_estimator_

    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Cross-validation accuracy: {grid_search.best_score_ * 100:.2f}%")

    y_pred = best_clf.predict(test_features)
    print(f"Test accuracy: {accuracy_score(test_label, y_pred) * 100:.2f}%")
    print(confusion_matrix(test_label, y_pred))
    print(classification_report(test_label, y_pred, target_names=['rest', 'contraction']))

    # Selected features, ranked by Random Forest importance
    feature_names = np.array(features_v1(train_data[0].T)[1])
    selected = feature_names[best_clf.named_steps['select'].get_support()]
    importances = best_clf.named_steps['rf'].feature_importances_
    for name, imp in sorted(zip(selected, importances), key=lambda x: -x[1]):
        print(f"  {name:<22} {imp:.3f}")

    # Save the best model
    joblib.dump(best_clf, 'model.pkl')
    print("Saved model.pkl")

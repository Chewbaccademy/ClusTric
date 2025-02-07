import pandas as pd
import constants
from sklearn import preprocessing

def df_to_dict(data:pd.DataFrame, discretize_prog_rate=False) -> dict:
    """Transforms a DataFrame into a Dict
    
    ------------------
    parameters:
    - data: a dataframe containing medical data, the dataframe is assumed to be sorted by patient_id (asc or desc) and visit date (asc)
    - discretize_prog_rate (NOT IMPLEMENTED)

    ------------------
    Input dataframe format :
    
    |index|id_patient|feat1|feat2|feat3|...|                                     |
    |-----|----------|-----|-----|-----|---|-------------------------------------|
    |  0  |     1    | 36  | 40  |  12 |...|-- assumed to be visit 0 of patient 1|
    |  1  |     1    | 36  | 39  |  10 |...|-- assumed to be visit 1 of patient 1|
    |  2  |     1    | 32  | 39  |  9  |...|-- assumed to be visit 2 of patient 1|
    |  3  |     2    | 27  | 32  |  22 |...|-- assumed to be visit 0 of patient 2|
    |  4  |     2    | 26  | 31  |  22 |...|-- assumed to be visit 1 of patient 2|
    ...
    
    --------------------
    Output dict format:
    ```
    {
        1: { # patient_id
            0: { # timepoint
                "feat1": 36,
                "feat2": 40,
                "feat3": 12
                ...
            },
            1: {
                "feat1": 36,
                "feat2": 39,
                "feat3": 10
                ...
            },
            2: {
                "feat1": 32,
                "feat2": 39,
                "feat3": 9
                ...
            }
        },
        2: { # patient_id
            0: { # timepoint
                "feat1": 27,
                "feat2": 32,
                "feat3": 22
                ...
            },
            1: {
                "feat1": 26,
                "feat2": 31,
                "feat3": 22
                ...
            }
        }
    }
    ```



    """

    data_dict = data.to_dict('index')
    final_dict = dict()

    id_paciente_glob = 0
    time_counter = 0
    for k in data_dict.keys():
        ref = data_dict[k][constants.REF_FEATURE]  # Patient ID of the current iteration
        if ref != id_paciente_glob:
            id_paciente_glob = ref
            time_counter = 0

        del data_dict[k][constants.REF_FEATURE]
        if ref not in final_dict:
            final_dict[ref] = {time_counter: data_dict[k]}
        else:
            final_dict[ref][time_counter] = data_dict[k]

        time_counter += 1

    return final_dict

def compute_consecutive_snapshots_n(data:dict, n:int, label:str, yes_label:str='Y') -> dict:
    """Build snapshots of n timepoints

    -------
    parameters:
    - data: is a dict with ALS data with the format returned by `df_to_dict`
    - n: is the number of consecutive snapshots to consider, ie. the size of snapshots set. the size of snapshots set could be defined 
    - label: is the target problem
    - yes_label: symbole used as a positive target
    - strategy (NOT IMPLENTED ):
        - `flexible` (default) - sets of snapshots have a maximum size `n` 
        - `strict` - sets of snapshots have a strict size of `n`

    ------
    output dict format:
    ```
    {
        1: [ # patient_id
            (0, 'Y'), # snapshot_id and target value of the snapshot
            (1, 'Y'),
            ...
        ]
        ...
    }
    ```
    """

    # filters out patient with too few appointments (number of appointments < n)
    #? final is not used ??
    final = dict()
    for (p, t) in data.items(): # loop through patients
        if len(t.keys()) >= n:
            fd = dict()
            for (key, val) in t.items(): # loop through timepoints of the patient
                fd[key] = val
                final[p] = fd #? I think this is one tab too far

    # build snapshots
    snaps = dict()
    for (p, ts) in data.items(): # loop through patients
        for t in ts.keys(): # loop through timepoints of the patient

            size_t = len(ts.keys())
            size_n = n
            if t < size_t - (size_n-1) and all(map(lambda c: c != yes_label, [data[p][t+y][label] for y in range(0, size_n-1)])):
                if p not in snaps:
                    snaps[p] = list()
                snaps[p].append([(t+j, data[p][t+j][label])
                                for j in range(0, size_n)])
    return snaps

def create_matrix_temporal(data:dict, sps:dict, n:int) -> tuple[pd.DataFrame, list]:
    """Je ne sais pas encore

    -----
    parameters:
    - data: is a dict with ALS data with the format returned by `df_to_dict`
    - sps: is a dict of snapshots returned by `compute_consecutive_snapshots_n`
    - n: is the number of consecutive snapshots to consider, ie. the size of snapshots set. the size of snapshots set could be defined 

    -----
    Output format :
    """
    y = list()
    values = list()
    cols = list()
    cols.append("Patient_ID")
    for p in sps.keys():
        tp = data[p]
        for snaps in sps[p]:
            l = list()
            l.append(p)

            for e in snaps:
                i = e[0]
                l.extend([tp[i][feature]
                         for feature in tp[i].keys() if feature != "Evolution"])

            values.append(l)
            y.append(e[1])

    cols.extend([f"{ti}{feature}" for ti in range(n)
                 for feature in tp[i].keys() if feature != "Evolution"])

    mats = pd.DataFrame(data=values,
                        columns=cols)

    return mats, y

def create_matrix_static(data, sps) -> tuple[pd.DataFrame, list]:
    y = list()
    values = list()
    cols = list()
    cols.append("Patient_ID")
    for p in sps.keys():
        tp = data[p]
        for snaps in sps[p]:
            l = list()
            l.append(p)
            i = snaps[0][0]
            l.extend([tp[i][feature]
                      for feature in tp[i].keys() if feature != "Evolution"])

            values.append(l)
            y.append(snaps[-1][1])

    cols.extend([f"{feature}"
                 for feature in tp[i].keys() if feature != "Evolution"])

    mats = pd.DataFrame(data=values,
                        columns=cols)

    return mats, y



def label_encoder_als(wri, features):
    le = preprocessing.LabelEncoder()
    for f in features:
        le.fit(wri[f])
        wri[f] = list(map(lambda a: a+1, le.transform(wri[f])))
    return wri
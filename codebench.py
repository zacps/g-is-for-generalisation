import os
import json
from glob import glob
from json import JSONDecodeError
import pandas as pd
import dateutil
from functools import lru_cache


def parse_codemirror(path):
    components = os.path.normpath(path).split(os.sep)
    student = int(components[-3])
    assign_excercise = components[-1].split('.')[0]
    assignment = assign_excercise.split('_')[0]
    klass = components[-5]
    semester = components[-6]
    
    _, _, deadline = parse_assessment_data(
        path+f"/../../../../assessments/{assignment}.data"
    )
    
    with open(path, encoding='utf-8') as f:
        log = f.readlines()
    events = []
    for line in log:
        if not line.strip():
            continue
        try:
            time, event_type, data = line.split("#", 2)
        except ValueError:
            # Some events skip the data section
            try:
                time, event_type = line.split("#", 2)
            except ValueError:
                # Some lines contain errors in codemirror itself instead of logs,
                # we just ignore them and continue passing what events we can.
                continue
        
        try:
            t = pd.to_datetime(time)
        except dateutil.parser._parser.ParserError:
            continue
        
        time = deadline - t

        event_type_map = {
            "focus": "focus_gained",
            "blur": "focus_lost",
            "paste": "text_paste"
        }
        if event_type == "change":
            try:
                data = json.loads(data.strip() or "{}")
            except AttributeError as e:
                print(line)
                raise e
            except JSONDecodeError:
                continue
            if "".join(data['text']).strip():
                events.append((semester, klass, student, assign_excercise, time, "text_insert"))
            if "".join(data['removed']).strip():
                events.append((semester, klass, student, assign_excercise, time, "text_remove"))
        elif event_type in event_type_map.keys():
            events.append((semester, klass, student, assign_excercise, time, event_type_map[event_type]))
        else:
            pass
    return events


def parse_run_log(path):
    components = os.path.normpath(path).split(os.sep)
    student = int(components[-3])
    assign_excercise = components[-1].split('.')[0]
    assignment = assign_excercise.split('_')[0]
    klass = components[-5]
    semester = components[-6]
    with open(path, encoding='utf-8') as f:
        log = f.readlines()
    filtered = [line[3:].strip().split(maxsplit=1) for line in log if line.startswith("==")]
    
    _, _, deadline = parse_assessment_data(
        path+f"/../../../../assessments/{assignment}.data"
    )
    
    event_type_map = {
        "TEST": "run",
        "SUBMITION": "submit"
    }
    
    return [(
        semester,
        klass,
        student,
        assign_excercise,
        deadline-pd.to_datetime(line[1][1:-1]),
        event_type_map[line[0]]
    ) for line in filtered]


def parse_final_grade(path):
    components = os.path.normpath(path).split(os.sep)
    student = int(components[-3])
    klass = components[-5]
    semester = components[-6]
    try:
        with open(path) as f:
            return (semester, klass, student, float(f.read().strip()))
    except FileNotFoundError:
        return (semester, klass, student, float('nan'))
    
    
@lru_cache
def parse_assessment_data(path):
    components = os.path.normpath(path).split(os.sep)
    assessment = components[-1].split('.')[0]
    with open(path) as f:
        lines = f.readlines()
    start = pd.to_datetime(next(line for line in lines if line.startswith("---- start:"))[12:])
    end = pd.to_datetime(next(line for line in lines if line.startswith("---- end:"))[10:])
    return (assessment, start, end)


def first_assessment_for_class(klass):
    "Get the ID of the first assessment for the class, this is used for all predictions."
    df = pd.DataFrame(
        [parse_assessment_data(path) for path in glob(rf"{klass}/assessments/*.data")], 
        columns=["id", "start", "end"]
    ).sort_values('start')
    
    try:
        return df.iloc[0].id
    except IndexError:
        return None

    
def assessments(klass):
    return glob(rf"{klass}/assessments/*.data")
    

def semesters(root):
    return [sem for sem in glob(rf'{root}/*') if os.path.isdir(sem)]


def classes(semester):
    return glob(rf'{semester}/*')


def users(klass):
    return glob(rf'{klass}/users/*')


def logs_for_user(user, assessment):
    logs = []
    # Some students might not have used codemirror! In this case we only have run/submit logs
    for excercise in glob(f'{user}/codemirror/{assessment}_*.log'):
        logs.extend(parse_codemirror(excercise))
    for excercise in glob(f'{user}/executions/{assessment}_*.log'):
        logs.extend(parse_run_log(excercise))
    return pd.DataFrame(logs, columns=["semester", "class", "student", "assignment_excercise", "time_to_deadline", "event_type"])
import json
from collections import defaultdict

ID_STR = "id"
REPORTS_STR = "reports"
EVENT_ID_STR = "EventID"
END_EVENT_ID_STR = "EndEventID"
PARENT_ID_STR = "ParentEventID"
REAL_PARENT_ID_STR = "RealParentEventID"
START_TIME_STR = "Timestamp"
END_TIME_STR = "end_time"
REL_TIME_STR = "HRT"
OPERATION_STR = "Operation"
DURATION_STR = "Duration"
TAG_STR = "Tag"
TASK_NAME_STR = "Label"
PROCESS_ID_STR = "ProcessID"
THREAD_ID_STR = "ThreadID"
SEPARATOR_STR = ":"
WAITED_OPERATION_STR = "waited"
UNSET_OPERATION_STR = "unset"
SET_OPERATION_STR = "set"
JOIN_OPERATION_STR = "join"
FORK_OPERATION_STR = "fork"

def parse(file_path):
  with open(file_path) as f:
    data = json.load(f)
  events = []
  trace_found = False
  tag_found = False
  count = 0
  for item in data:
    trace_id = item[ID_STR]
    if trace_found:
      print("Multiple Traces found!!!!")
    trace_found = True
    for report in item[REPORTS_STR]:
      event = {}
      event[EVENT_ID_STR] = report[EVENT_ID_STR]
      event[START_TIME_STR] = report[START_TIME_STR]
      event[REL_TIME_STR] = report[REL_TIME_STR]
      event[PARENT_ID_STR] = report[PARENT_ID_STR]
      # if DURATION_STR in report:
      #   print(report[OPERATION_STR])
      # if len(event[PARENT_ID_STR]) > 1:
      #   parent1 = report[PARENT_ID_STR][0]
      #   parent2 = report[PARENT_ID_STR][1]
      #   if 
      #   print(str(len(event[PARENT_ID_STR])) + event[EVENT_ID_STR])
      #   count += 1
      if OPERATION_STR in report:
        event[OPERATION_STR] = report[OPERATION_STR]
      if DURATION_STR in report:
        event[DURATION_STR] = report[DURATION_STR]
      if TAG_STR in report:
        event[TAG_STR] = report[TAG_STR]
        if tag_found:
          print("Multiple tags found!!!!")
        tag_found = True
      event[TASK_NAME_STR] = report[TASK_NAME_STR]
      event[PROCESS_ID_STR] = report[PROCESS_ID_STR]
      event[THREAD_ID_STR] = report[THREAD_ID_STR]
      events.append(event)
  print(count)
  return events

def event_comparator(event):
  return event[START_TIME_STR]

def ids_comparator(event):
  return event[0]

def getProcThreadKey(process_id, thread_id):
  return str(process_id) + SEPARATOR_STR + str(thread_id)

def convertToTrace(file_path):
  events = parse(file_path)
  sorted_events = sorted(events, key=event_comparator)
  proc_thread = defaultdict(list)
  # prev_time = ""
  for index, value in enumerate(sorted_events):
    if (index == 0 and not TAG_STR in value):
      print("Error: Starting event does not contain Tag!!!!!")
      print(value)
    # if prev_time >= value[START_TIME_STR]:
    #   print("WTF")
    #   print(value)
    # prev_time = value[START_TIME_STR]
    # if len(proc_thread[getProcThreadKey(value[PROCESS_ID_STR], value[THREAD_ID_STR])]) != 0:
    #   if proc_thread[getProcThreadKey(value[PROCESS_ID_STR], value[THREAD_ID_STR])][-1][EVENT_ID_STR] != value[PARENT_ID_STR][0]:
    #     print("Woah " + proc_thread[getProcThreadKey(value[PROCESS_ID_STR], value[THREAD_ID_STR])][-1][EVENT_ID_STR] + " " + value[PARENT_ID_STR][0])
    proc_thread[getProcThreadKey(value[PROCESS_ID_STR], value[THREAD_ID_STR])].append(value)
  print("Number of process & threads combos: " + str(len(proc_thread)))
  spans_dict = {}
  spans_end_id_to_start_id = {}
  sorted_ids = []
  unset_id_map = {}
  unset_dict = {}
  for key in proc_thread:
    for index, value in enumerate(proc_thread[key]):
      parent_span_id = value[PARENT_ID_STR][0]
      spans_end_id_to_start_id[value[EVENT_ID_STR]] = parent_span_id
      if OPERATION_STR in value and value[OPERATION_STR] == UNSET_OPERATION_STR:
        # print(value[EVENT_ID_STR])
        unset_dict[value[EVENT_ID_STR]] = 1
        continue
      spans_dict[value[EVENT_ID_STR]] = value
      # if value[EVENT_ID_STR] == "C5ECFEA48148ECD1":
      #   print("FML")
      #   print(value)
      #   print(spans_dict["C5ECFEA48148ECD1"])
  # print("Next")
  for key in proc_thread:
    for index, value in enumerate(proc_thread[key]):
      span = value
      span_id = value[EVENT_ID_STR]
      span_start_time = value[START_TIME_STR]
      parent_span_id = value[PARENT_ID_STR][0]
      # spans_end_id_to_start_id[span_id] = parent_span_id
      # print(value[PARENT_ID_STR])
      if OPERATION_STR in value:
        # End previous span and handle unset case
        if value[OPERATION_STR] == UNSET_OPERATION_STR:
          spans_dict[parent_span_id][END_TIME_STR] = span_start_time
          spans_dict[parent_span_id][END_EVENT_ID_STR] = span_id
          parent = value[PARENT_ID_STR][0]
          real_parent = spans_end_id_to_start_id[parent]
          unset_id_map[span_id] = real_parent
          # print(span_id + " " + real_parent)
          # span[PARENT_ID_STR][0] = real_parent
          # spans_dict[span_id] = span
          # spans_end_id_to_start_id[span_id] = spans_dict[parent_span_id][EVENT_ID_STR]
          continue
        # Handle waited operation case
        if value[OPERATION_STR] == WAITED_OPERATION_STR:
          sorted_ids.append([span_start_time, span_id])
          spans_dict[span_id] = span
          start_duration = float(span_start_time) - (float(value[DURATION_STR])/1000000)
          spans_dict[parent_span_id][END_TIME_STR] = str(start_duration)
          continue
        # Handle set operation case
        if value[OPERATION_STR] == SET_OPERATION_STR:
          sorted_ids.append([span_start_time, span_id])
          spans_dict[span_id] = span
          continue
        # Handle join operation case
        if value[OPERATION_STR] == JOIN_OPERATION_STR:
          parent1 = value[PARENT_ID_STR][0]
          parent2 = value[PARENT_ID_STR][1]
          real_parent1 = spans_end_id_to_start_id[parent1]
          real_parent2 = spans_end_id_to_start_id[parent2]
          span[REAL_PARENT_ID_STR] = []
          span[REAL_PARENT_ID_STR].append(real_parent1)
          span[REAL_PARENT_ID_STR].append(real_parent2)
          # span[PARENT_ID_STR][0] = real_parent1
          # span[PARENT_ID_STR][1] = real_parent2
          # spans_dict[parent_span_id][END_TIME_STR] = span_start_time
          if not parent1 in unset_dict:
          # if not ((not parent1 in unset_dict) and OPERATION_STR in spans_dict[parent1] and (spans_dict[parent1][OPERATION_STR] == UNSET_OPERATION_STR)):
            spans_dict[parent1][END_TIME_STR] = span_start_time
          if not parent2 in unset_dict:
          # if not ((not parent2 in unset_dict) and OPERATION_STR in spans_dict[parent2] and (spans_dict[parent2][OPERATION_STR] == UNSET_OPERATION_STR)):
            spans_dict[parent2][END_TIME_STR] = span_start_time
          sorted_ids.append([span_start_time, span_id])
          spans_dict[span_id] = span
          # if spans_dict[parent1][OPERATION_STR] != UNSET_OPERATION_STR and spans_dict[parent2][OPERATION_STR] != UNSET_OPERATION_STR:
          #   print("problemo")
          #   print(spans_dict[parent1][OPERATION_STR])
          #   print(spans_dict[parent2][OPERATION_STR])
          continue
      # print(parent_span_id)
      if not TAG_STR in value:
        spans_dict[parent_span_id][END_TIME_STR] = span_start_time
      # Add Duration if needed
      # Normal spans done
      sorted_ids.append([span_start_time, span_id])
      spans_dict[span_id] = span
      # if DURATION_STR in value and OPERATION_STR in value and value[OPERATION_STR] == WAITED_OPERATION_STR:
      #   span_start_time += value[DURATION_STR]
  sorted_ids = sorted(sorted_ids, key=ids_comparator)
  sorted_ids.pop()
  print("Processed")
  return sorted_ids, spans_dict, spans_end_id_to_start_id, unset_id_map



def getCPT(file_path):
  sorted_ids, spans_dict, c, unset_id_map = convertToTrace(file_path)
  # print(sorted_ids)
  id_time_spent = {}
  id_time_spent["0"] = 0.0
  # print(unset_id_map)
  for index, value in enumerate(sorted_ids):
    span_id = value[1]
    # print(span_id)
    duration = float(spans_dict[span_id][END_TIME_STR]) - float(spans_dict[span_id][START_TIME_STR])
    # if duration < 0:
      # print("------------------- " + str(duration) + " " + spans_dict[span_id][END_TIME_STR])
    if spans_dict[span_id][PARENT_ID_STR][0] in unset_id_map:
      # print("whynot" + span_id)
      id_time_spent[span_id] = id_time_spent[unset_id_map[spans_dict[span_id][PARENT_ID_STR][0]]] + duration
      continue
    if len(spans_dict[span_id][PARENT_ID_STR]) == 1:
      # print(span_id)
      id_time_spent[span_id] = id_time_spent[spans_dict[span_id][PARENT_ID_STR][0]] + duration
    else:
      # max_duration = id_time_spent[spans_dict[span_id][PARENT_ID_STR][0]]
      max_duration = id_time_spent.get(spans_dict[span_id][PARENT_ID_STR][0], 0)
      # print(span_id)
      for id in spans_dict[span_id][PARENT_ID_STR]:
        if id in unset_id_map:
          max_duration = max(max_duration, id_time_spent[unset_id_map[id]])
        else:
          # max_duration = max(max_duration, id_time_spent[id])
          max_duration = max(max_duration, id_time_spent.get(id, 0))
      id_time_spent[span_id] = max_duration + duration
    # print(id_time_spent[span_id])
  print(id_time_spent)

getCPT("sample-large-xtrace.json")

# -*- coding: utf-8 -*-
from pymongo import MongoClient
from collections import Counter # Keep track of our term counts
import pandas as pd

client = MongoClient('localhost', 27017)

db = client.indeed
collection = db.postings

# -------------------------------------- overall counter for state and skill -------------------------------------
state_frequency = Counter()
doc_frequency = Counter()  # This will create a full counter of our terms.
for item in collection.find({},{'words':1,'state':1}):
    doc_frequency.update(item['words'])
    state_frequency.update([item['state']])
# words = pd.DataFrame(doc_frequency.items(), columns=['Word','Count'])
# words.sort(columns='Count', ascending=False, inplace=True)
# words.to_csv('word.csv')

# ------------------------------ state counter -------------------------------
state_frequency = pd.DataFrame(state_frequency.items(), columns=['State', 'NumPostings'])  # Convert these terms to a
state_frequency.to_csv('state.csv')

# ------------------------------------ words counter ------------------------------------
def words_counter(doc_frequency):
    skills = Counter({'R': doc_frequency['r'], 'Python': doc_frequency['python'], 'Java': doc_frequency['java'],
                      'C++': doc_frequency['c++'], 'Ruby': doc_frequency['ruby'], 'Perl': doc_frequency['perl'],
                      'Matlab': doc_frequency['matlab'], 'JavaScript': doc_frequency['javascript'],
                      'Scala': doc_frequency['scala'], 'Excel': doc_frequency['excel'],
                      'Tableau': doc_frequency['tableau'], 'D3.js': doc_frequency['d3.js'],
                      'SAS': doc_frequency['sas'], 'SPSS': doc_frequency['spss'], 'D3': doc_frequency['d3'],
                      'Hadoop': doc_frequency['hadoop'], 'MapReduce': doc_frequency['mapreduce'],
                      'Spark': doc_frequency['spark'], 'Pig': doc_frequency['pig'], 'Hive': doc_frequency['hive'],
                      'Shark': doc_frequency['shark'], 'Oozie': doc_frequency['oozie'],
                      'ZooKeeper': doc_frequency['zookeeper'], 'Flume': doc_frequency['flume'],
                      'Mahout': doc_frequency['mahout'], 'SQL': doc_frequency['sql'], 'NoSQL': doc_frequency['nosql'],
                      'HBase': doc_frequency['hbase'], 'Cassandra': doc_frequency['cassandra'], 'MongoDB': doc_frequency['mongodb']})
    final_frame = pd.DataFrame(skills.items(),columns=['Term', 'NumPostings'])  # Convert these terms to data frame
    final_frame.NumPostings = (final_frame.NumPostings) * 100 / (sum(final_frame.NumPostings))  # Gives percentage of job postings
    final_frame = final_frame.fillna(0)
    final_frame.sort(columns='NumPostings', ascending=False, inplace=True)
    return final_frame

# ------------------------------ overall skill counter -------------------------------
skill = words_counter(doc_frequency)
skill.to_csv('skill.csv')

# -------------- skill for each state -----------------
for state in state_frequency['State']:
    doc_sub_frequency = Counter()
    for item in collection.find({'state':state}, {'words': 1, 'state': 1}):
        doc_sub_frequency.update(item['words'])
        skill_sub = words_counter(doc_sub_frequency)
        skill_sub.to_csv(state+'.csv')

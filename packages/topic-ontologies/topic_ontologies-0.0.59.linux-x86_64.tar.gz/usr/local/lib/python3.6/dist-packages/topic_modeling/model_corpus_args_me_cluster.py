#docker exec -u befi8957 -it webis-datascience-image-befi8957 bash -l -c 'cd; exec /opt/spark/bin/spark-submit   /home/yamenajjour/git/topic_ontologies/topic_modeling/model_corpus_args_me_cluster.py'
#docker exec -u befi8957 -it webis-datascience-image-befi8957 bash -l -c 'cd; exec /opt/spark/bin/spark-submit --deploy-mode cluster --py-files /home/yamenajjour/git/topic_ontologies/deploy/topic-ontologies-dep.zip --executor-memory 2G --driver-memory 4G /home/yamenajjour/git/topic_ontologies/topic_modeling/model_corpus_args_me_cluster.py'
import sys
sys.path.insert(0,"/home/yamenajjour/git/topic-ontologies/")

from pyspark.sql import SparkSession
import argument_esa_model.esa_all_terms
import argument_esa_model.esa_top_n_terms
import pickle
import codecs
from conf.configuration import *




spark = SparkSession.builder.appName('topic-ontologies').config('master','yarn').getOrCreate()
args_me = spark.read.format('csv').option('header','true').option('delimiter',',')

def dict_to_list(dictionary):
    vector  = []
    for key in sorted(dictionary):
        vector.append(dictionary[key])
    pickled = codecs.encode(pickle.dumps(vector), "base64").decode()
    return pickled


def project_arguments(topic_ontology):
    def project_argument(argument):
        set_cluster_mode()
        path_topic_model = get_path_topic_model('ontology-'+topic_ontology,'esa')
        path_word2vec_model = get_path_topic_model('word2vec','word2vec')
        path_word2vec_vocab = get_path_vocab('word2vec')
        vector = argument_esa_model.esa_all_terms.model_topic(path_topic_model,path_word2vec_model,path_word2vec_vocab,'cos',argument)
        return dict_to_list(vector)

    args_me_arguments_df  = spark.read.format("csv").option("header", "true").option("delimiter", "|", ).option('quote', '"').load('/user/befi8957/topic-ontologies/args-me/corpus-args-me-preprocessed-documents-sample.csv').na.drop()
    arguments = args_me_arguments_df.select("text").rdd.map(lambda r: r[0]).repartition(400)
    ids = (args_me_arguments_df.select("argument-id").rdd.map(lambda r: r[0])).repartition(400)
    vectors = arguments.map(lambda argument:project_argument(argument))
    ids_with_vectors=vectors.zip(ids)
    ids_with_vectors.saveAsTextFile('/user/befi8957/args-me-esa-topic-vectors-sample-vectors-new1')



project_arguments('debatepedia')
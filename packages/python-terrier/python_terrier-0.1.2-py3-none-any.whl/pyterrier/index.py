from jnius import autoclass, cast, PythonJavaClass, java_method
from utils import *
import pandas as pd
import numpy as np
import os

CollectionDocumentList = autoclass("org.terrier.indexing.CollectionDocumentList")
StringReader = autoclass("java.io.StringReader")
HashMap = autoclass("java.util.HashMap")
TaggedDocument = autoclass("org.terrier.indexing.TaggedDocument")
Tokeniser = autoclass("org.terrier.indexing.tokenisation.Tokeniser")
TRECCollection = autoclass("org.terrier.indexing.TRECCollection")
SimpleFileCollection = autoclass("org.terrier.indexing.SimpleFileCollection")
BasicIndexer = autoclass("org.terrier.structures.indexing.classical.BasicIndexer")
BlockIndexer = autoclass("org.terrier.structures.indexing.classical.BlockIndexer")
Collection = autoclass("org.terrier.indexing.Collection")
Arrays = autoclass("java.util.Arrays")
Array = autoclass('java.lang.reflect.Array')
ApplicationSetup = autoclass('org.terrier.utility.ApplicationSetup')
Properties = autoclass('java.util.Properties')

class Index:
    default_properties={
            "TrecDocTags.doctag":"DOC",
            "TrecDocTags.idtag":"DOCNO",
            "TrecDocTags.skip":"DOCHDR",
            "TrecDocTags.casesensitive":"false",
            "trec.collection.class": "TRECCollection",
    }
    def __init__(self, index_path, blocks=False):
        self.path = os.path.join(index_path, "data.properties")
        self.index_dir = index_path
        self.blocks = blocks
        self.properties = Properties()
        self.setProperties(**self.default_properties)

    def setProperties(self, **kwargs):
        for control,value in kwargs.items():
            self.properties.put(control,value)

class DFIndex(Index):
    def index(self, text, *args, **kwargs):
        all_metadata={}
        for arg in args:
            if isinstance(arg, pd.Series):
                all_metadata[arg.name]=arg
                assert len(arg)==len(text), "Length of metadata arguments needs to be equal to length of text argument"
            elif isinstance(arg, pd.DataFrame):
                for name, column in arg.items():
                    all_metadata[name]=column
                    assert len(column)==len(text), "Length of metadata arguments needs to be equal to length of text argument"
            else:
                raise ValueError("Non-keyword args need to be of type pandas.Series or pandas,DataFrame")
        for key, value in kwargs.items():
            if isinstance(value, (pd.Series, list, tuple)):
                all_metadata[key]=value
                assert len(value)==len(value), "Length of metadata arguments needs to be equal to length of text argument"
            elif isinstance(value, pd.DataFrame):
                for name, column in arg.items():
                    all_metadata[name]=column
                    assert len(column)==len(text), "Length of metadata arguments needs to be equal to length of text argument"
            else:
                raise ValueError("Keyword kwargs need to be of type pandas.Series, list or tuple")

        doc_list=[]
        df=pd.DataFrame(all_metadata)
        for text_row, meta_column in zip(text.values, df.iterrows()):
            meta_row=[]
            hashmap = HashMap()
            for column, value in meta_column[1].iteritems():
                hashmap.put(column,value)
            tagDoc = TaggedDocument(StringReader(text_row), hashmap, Tokeniser.getTokeniser())
            doc_list.append(tagDoc)

        javaDocCollection = CollectionDocumentList(doc_list, "null")
        index = BasicIndexer(self.index_dir, "data")
        index.index([javaDocCollection])

class TRECIndex(Index):
    def index(self, files_path):
        ApplicationSetup.bootstrapInitialisation(self.properties)
        if self.blocks:
            index = BlockIndexer(self.index_dir,"data")
        else:
            index = BasicIndexer(self.index_dir,"data")

        if type(files_path) == type(""):
            asList = Arrays.asList(files_path)
        if type(files_path) == type([]):
            asList = Arrays.asList(*files_path)

        trecCol = TRECCollection(asList,"TrecDocTags","","")
        index.index([trecCol])


class FilesIndex(Index):
    def index(self, files_path):
        ApplicationSetup.bootstrapInitialisation(self.properties)
        if self.blocks:
            index = BlockIndexer(self.index_dir,"data")
        else:
            index = BasicIndexer(self.index_dir,"data")
        if type(files_path) == type(""):
            asList = Arrays.asList(files_path)
        if type(files_path) == type([]):
            asList = Arrays.asList(*files_path)
        simpleColl = SimpleFileCollection(asList,False)
        index.index([simpleColl])

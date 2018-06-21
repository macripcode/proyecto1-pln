from lxml import etree
from pyfreeling import Analyzer
import nltk
from nltk.tokenize import TweetTokenizer
import re


#list
list_emoticons=[':o',':/',":'(",'>:o','(:',':)','>.<','XD','-__-','o.O',';D',':-)','@_@',':P','8D',':','>:()',':D','=|','<3']
list_arrows=['<-','^','->','>','<']

#functions

#verify this emo belong to this list. Return the tag 'E' o False.
def is_weird_emo(emoticon):
    for i in range(len(list_emoticons)):
        if list_emoticons[i] == emoticon:
            return 'E';
    return False;

#verify this arrow belong to this list. Return the tag 'E' o False.
def is_weird_arrow(arrow):
    for i in range(len(list_arrows)):
        if arrow.find(list_arrows[i])>= 0 :
            return 'G';
    return False;

#verify this is a hashtag. Return the tag 'HASHTAG' o False.
def is_hashtag(hashtag):
    if re.match('#(\w+)',hashtag):
        return 'HASHTAG';
    else:
        return 'false';

#verify this is a nickname. Return the tag 'NICKNAME' o False.
def is_nickname(nickname):
    if re.match('^@[(a-zA-Z0-9\_\-\.)]{2,15}$',nickname):
        return 'NICKNAME';
    else:
        return 'false';

#verify this is a url. Return the tag 'url' o False.
def is_url(direccion):
    if re.match('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)',direccion):
        return 'URL';
    else:
        return 'false';

#Return morphological analisis.
def morpho_analisis(word):
    analyzer = Analyzer(config='es.cfg');
    root = analyzer.run(word);
    #print (type(root));
    #print(etree.tostring(root, pretty_print=True));
    analisis="";
    for i in range(len(root[0][0])):
        analisis+=root[0][0][i].attrib['lemma']+'\t';
        analisis+=root[0][0][i].attrib['tag']+'\n';
        #anal+=root[0][0][i].attrib['ctag'];
        #anal+=root[0][0][i].attrib['pos'];
        #anal+=root[0][0][i].attrib['type'];
        #anal+=root[0][0][i].attrib['prob'];

    return analisis;




#init tokenizer
tknzr = TweetTokenizer();
#text = '#SantosNobeldePaz 2014 "valentia" @JuanManSantos  http://ow.ly/qdL0304XXtd #dummysmiley: :-) :-P < > -> <--'
text='Danielito no es bajo #oshitos_123 @puro_amor http://www.google.com :D <3'
list_tkn=tknzr.tokenize(text);
#list_out=list();

print (list_tkn);

def process_text(text):
    for i in range(len(list_tkn)):
        if is_weird_emo(list_tkn[i]) == 'E':
            print(list_tkn[i]+' E'+' ahora i vale: '+str(i));

            continue;
        elif is_weird_arrow(list_tkn[i]) == 'G':
            print(list_tkn[i]+' G'+' ahora i vale: '+str(i));

            continue;
        elif is_hashtag(list_tkn[i]) == 'HASHTAG':
            print(list_tkn[i]+' HASHTAG'+' ahora i vale: '+str(i));

            continue;
        elif is_nickname(list_tkn[i]) == 'NICKNAME':
            print(list_tkn[i]+' NICKNAME'+' ahora i vale: '+str(i));

            continue;
        elif is_url(list_tkn[i]) == 'URL':
            print(list_tkn[i]+' URL'+' ahora i vale: '+str(i));

            continue;
        else:
            print(list_tkn[i]+' WORD'+' ahora i vale: '+str(i));
            print('analisis morfologico:\n');
            print(morpho_analisis(list_tkn[i]));


process_text(text);

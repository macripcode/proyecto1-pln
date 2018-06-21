from lxml import etree
from pyfreeling import Analyzer
import nltk
from nltk.tokenize import TweetTokenizer
import re
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

#list
list_emoticons=[':o',':/',":'(",'>:o','(:',':)','>.<','XD','-__-','o.O',';D',':-)','@_@',':P','8D',':','>:()',':D','=|','<3']
list_arrows=['<-','^','->','>','<']

#ejemplo
#El niño toca el bajo bajo la lluvia #Usemos_sombrilla @Mojado_123 http://www.google.com <--------- :D <3 :) ----------> ^ "valor"
#
#docker run --rm -it  -p 5000:5000 -v $(pwd):/root/app p9  python3 /root/app/hello_flask.py




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
        analisis+="<div class='tokens'>"
        analisis+="<p class='c_lemma'>"+root[0][0][i].attrib['lemma']+"</p>"
        analisis+="<p class='c_tag'>"+root[0][0][i].attrib['tag']+"</p>"
        #anal+=root[0][0][i].attrib['ctag'];
        #anal+=root[0][0][i].attrib['pos'];
        #anal+=root[0][0][i].attrib['type'];
        #anal+=root[0][0][i].attrib['prob'];
        analisis+="</div>"

    return analisis;


def process_text(list_tkn):
    str_salida=""
    for i in range(len(list_tkn)):
        str_salida+="<td><div class='c_grupo'><div><p class='clase_palabra'>"+list_tkn[i]+"</p></div>"
        str_salida+="<div class='analisis_morfo'>"
        if is_weird_emo(list_tkn[i]) == 'E':
            str_salida+="<div class='tokens'><p class='c_emoticon'>EMOTICON</p></div>"
            str_salida+="</div></div></td>"
            continue;
        elif is_weird_arrow(list_tkn[i]) == 'G':
            str_salida+="<div class='tokens'><p class='c_arrow'>ARROW</p></div>"
            str_salida+="</div></div></td>"

            continue;
        elif is_hashtag(list_tkn[i]) == 'HASHTAG':
            str_salida+="<div class='tokens'><p class='c_hashtag'>HASHTAG</p></div>"
            str_salida+="</div></div></td>"
            continue;
        elif is_nickname(list_tkn[i]) == 'NICKNAME':
            str_salida+="<div class='tokens'><p class='c_nickname'>NICKNAME</p></div>"
            str_salida+="</div></div></td>"
            continue;
        elif is_url(list_tkn[i]) == 'URL':
            #print(list_tkn[i]+' URL'+' ahora i vale: '+str(i));
            str_salida+="<div class='tokens'><p class='c_url'>URL</p></div>"
            str_salida+="</div></div></td>"
            continue;
        else:
            str_salida+=morpho_analisis(list_tkn[i])
            str_salida+="</div></div></td>"

    return str_salida;




@app.route('/analize')
def analize():
    return render_template("analize.html")

@app.route('/process', methods=['POST'])
def process():
    texto=request.form['texto']
    #init tokenizer
    tknzr = TweetTokenizer();
    list_tkn=tknzr.tokenize(texto);
    #generando el html para la salida
    salida=""
    salida+="<div class='table-responsive'>"
    salida+="<table id='res' class='table table-hover'><tr>"
    salida+=process_text(list_tkn);
    salida+="</tr></table></div>"
    return jsonify({'salida' : salida })


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug='True')

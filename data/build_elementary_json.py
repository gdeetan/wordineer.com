import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, '..', '..', 'wordineer-deploy', 'data')

def parse_syl(syl):
    if isinstance(syl, int):
        return syl
    s = str(syl).strip()
    if s.isdigit():
        return int(s)
    return len(s.split('·'))  # middle dot U+00B7

def load_grade(filename, grade_label):
    path = os.path.join(DATA, filename)
    with open(path, encoding='utf-8') as f:
        words = json.load(f)
    result = []
    for w in words:
        result.append({
            'w':      w['w'],
            'grade':  grade_label,
            'diff':   w.get('diff', 'easy'),
            'origin': w.get('origin', 'Anglo-Saxon'),
            'syl':    parse_syl(w.get('syl', 1)),
            'pos':    w.get('pos', 'noun'),
            'd':      w.get('d', '')
        })
    return result

# 1st-grade words (no source file — authored here)
first_grade = [
  {"w":"act","grade":"1st","diff":"easy","origin":"Latin","syl":1,"pos":"verb","d":"to do something"},
  {"w":"ask","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to put a question to someone"},
  {"w":"bag","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a soft container for carrying things"},
  {"w":"bat","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a stick used to hit a ball"},
  {"w":"bed","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a piece of furniture for sleeping"},
  {"w":"big","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"adjective","d":"large in size"},
  {"w":"bug","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a small insect"},
  {"w":"cup","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a small container for drinking"},
  {"w":"cut","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to divide with a sharp edge"},
  {"w":"dig","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to move dirt with a tool"},
  {"w":"dip","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to put briefly into a liquid"},
  {"w":"dot","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a small round spot"},
  {"w":"fan","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a device that moves air"},
  {"w":"fit","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"adjective","d":"the right size or shape"},
  {"w":"fix","grade":"1st","diff":"easy","origin":"Latin","syl":1,"pos":"verb","d":"to repair something broken"},
  {"w":"fox","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a wild animal with a bushy tail"},
  {"w":"fun","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"enjoyment and pleasure"},
  {"w":"got","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"received or obtained something"},
  {"w":"hat","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a covering worn on the head"},
  {"w":"hit","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to strike with force"},
  {"w":"hop","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to jump on one foot"},
  {"w":"hot","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"adjective","d":"having a high temperature"},
  {"w":"hug","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to hold someone close with your arms"},
  {"w":"jet","grade":"1st","diff":"easy","origin":"French","syl":1,"pos":"noun","d":"a fast airplane"},
  {"w":"kit","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a set of tools or supplies"},
  {"w":"lid","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a cover for a container"},
  {"w":"log","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a thick piece of wood"},
  {"w":"map","grade":"1st","diff":"easy","origin":"Latin","syl":1,"pos":"noun","d":"a picture showing an area of land"},
  {"w":"mud","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"wet soft earth"},
  {"w":"nap","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a short sleep"},
  {"w":"net","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a mesh used to catch things"},
  {"w":"nut","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a hard-shelled seed that you can eat"},
  {"w":"pan","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a flat cooking container"},
  {"w":"pet","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a tame animal kept at home"},
  {"w":"pin","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a thin pointed piece of metal"},
  {"w":"pot","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a round container for cooking"},
  {"w":"rub","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to move back and forth against something"},
  {"w":"sad","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"adjective","d":"feeling unhappy"},
  {"w":"tag","grade":"1st","diff":"easy","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a label attached to something"},
  {"w":"van","grade":"1st","diff":"easy","origin":"French","syl":1,"pos":"noun","d":"a large vehicle for carrying things"},
  {"w":"bath","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"washing yourself in water"},
  {"w":"best","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"adjective","d":"better than all others"},
  {"w":"bird","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a feathered animal that can fly"},
  {"w":"blow","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to send air out of your mouth"},
  {"w":"blue","grade":"1st","diff":"medium","origin":"French","syl":1,"pos":"adjective","d":"the color of the sky"},
  {"w":"bold","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"adjective","d":"brave and confident"},
  {"w":"bone","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a hard part inside your body"},
  {"w":"cape","grade":"1st","diff":"medium","origin":"Latin","syl":1,"pos":"noun","d":"a sleeveless cloak worn over the shoulders"},
  {"w":"cave","grade":"1st","diff":"medium","origin":"Latin","syl":1,"pos":"noun","d":"a hollow space in a hillside"},
  {"w":"chip","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a small thin piece broken off"},
  {"w":"chop","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to cut with a heavy blow"},
  {"w":"clap","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to strike hands together to make a sound"},
  {"w":"clay","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"soft sticky earth used to make pots"},
  {"w":"clip","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to cut with scissors"},
  {"w":"club","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a group of people with shared interests"},
  {"w":"coin","grade":"1st","diff":"medium","origin":"French","syl":1,"pos":"noun","d":"a small flat piece of metal used as money"},
  {"w":"cold","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"adjective","d":"having a low temperature"},
  {"w":"crab","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a sea creature with claws and a hard shell"},
  {"w":"drip","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to fall in small drops"},
  {"w":"drop","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to let something fall"},
  {"w":"drum","grade":"1st","diff":"medium","origin":"Germanic","syl":1,"pos":"noun","d":"a musical instrument you hit with sticks"},
  {"w":"flag","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a piece of cloth with a pattern or symbol"},
  {"w":"flat","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"adjective","d":"level and smooth with no bumps"},
  {"w":"flip","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to turn over quickly"},
  {"w":"frog","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a small jumping animal that lives near water"},
  {"w":"glad","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"adjective","d":"pleased and happy"},
  {"w":"glow","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to give off a steady light"},
  {"w":"glue","grade":"1st","diff":"medium","origin":"French","syl":1,"pos":"noun","d":"a sticky substance used to join things"},
  {"w":"grab","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to take hold of something suddenly"},
  {"w":"grin","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to smile broadly showing teeth"},
  {"w":"grip","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to hold tightly"},
  {"w":"grow","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to become bigger over time"},
  {"w":"skip","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to jump lightly from one foot to the other"},
  {"w":"slam","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to shut with great force and noise"},
  {"w":"slip","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to slide accidentally"},
  {"w":"slow","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"adjective","d":"not moving quickly"},
  {"w":"snap","grade":"1st","diff":"medium","origin":"Germanic","syl":1,"pos":"verb","d":"to break with a sharp sound"},
  {"w":"spin","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to turn around fast"},
  {"w":"stem","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"the main stalk of a plant"},
  {"w":"step","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"one movement of the foot when walking"},
  {"w":"stop","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to no longer move or continue"},
  {"w":"swim","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to move through water using your body"},
  {"w":"trap","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"noun","d":"a device used to catch animals"},
  {"w":"trim","grade":"1st","diff":"medium","origin":"Anglo-Saxon","syl":1,"pos":"verb","d":"to cut away the edges to make neat"},
  {"w":"trot","grade":"1st","diff":"medium","origin":"French","syl":1,"pos":"verb","d":"to run at a steady moderate pace"},
  {"w":"basket","grade":"1st","diff":"hard","origin":"Anglo-Saxon","syl":2,"pos":"noun","d":"a container made of woven material"},
  {"w":"button","grade":"1st","diff":"hard","origin":"French","syl":2,"pos":"noun","d":"a small disk used to fasten clothing"},
  {"w":"candle","grade":"1st","diff":"hard","origin":"Latin","syl":2,"pos":"noun","d":"a wax stick with a wick that gives light when lit"},
  {"w":"circle","grade":"1st","diff":"hard","origin":"Latin","syl":2,"pos":"noun","d":"a perfectly round flat shape"},
  {"w":"dinner","grade":"1st","diff":"hard","origin":"French","syl":2,"pos":"noun","d":"the main meal of the day"},
  {"w":"garden","grade":"1st","diff":"hard","origin":"French","syl":2,"pos":"noun","d":"a piece of ground where plants are grown"},
  {"w":"gentle","grade":"1st","diff":"hard","origin":"Latin","syl":2,"pos":"adjective","d":"soft and calm, not rough"},
  {"w":"golden","grade":"1st","diff":"hard","origin":"Anglo-Saxon","syl":2,"pos":"adjective","d":"made of gold or bright yellow like gold"},
  {"w":"happen","grade":"1st","diff":"hard","origin":"Anglo-Saxon","syl":2,"pos":"verb","d":"to take place or occur"},
  {"w":"hidden","grade":"1st","diff":"hard","origin":"Anglo-Saxon","syl":2,"pos":"adjective","d":"kept out of sight"},
  {"w":"kitten","grade":"1st","diff":"hard","origin":"French","syl":2,"pos":"noun","d":"a young cat"},
  {"w":"ladder","grade":"1st","diff":"hard","origin":"Anglo-Saxon","syl":2,"pos":"noun","d":"a set of steps used for climbing"},
  {"w":"letter","grade":"1st","diff":"hard","origin":"Latin","syl":2,"pos":"noun","d":"a written message sent to someone"},
  {"w":"little","grade":"1st","diff":"hard","origin":"Anglo-Saxon","syl":2,"pos":"adjective","d":"small in size"},
  {"w":"middle","grade":"1st","diff":"hard","origin":"Anglo-Saxon","syl":2,"pos":"noun","d":"the center or halfway point"},
  {"w":"mitten","grade":"1st","diff":"hard","origin":"French","syl":2,"pos":"noun","d":"a glove with one section for all fingers"},
  {"w":"number","grade":"1st","diff":"hard","origin":"French","syl":2,"pos":"noun","d":"a symbol used in counting"},
  {"w":"pencil","grade":"1st","diff":"hard","origin":"Latin","syl":2,"pos":"noun","d":"a thin writing tool with a graphite tip"},
  {"w":"picnic","grade":"1st","diff":"hard","origin":"French","syl":2,"pos":"noun","d":"a meal eaten outdoors"},
  {"w":"pocket","grade":"1st","diff":"hard","origin":"French","syl":2,"pos":"noun","d":"a small pouch sewn into clothing"},
  {"w":"puppet","grade":"1st","diff":"hard","origin":"French","syl":2,"pos":"noun","d":"a figure moved by the hand to act out stories"},
  {"w":"rabbit","grade":"1st","diff":"hard","origin":"Anglo-Saxon","syl":2,"pos":"noun","d":"a small furry animal with long ears"},
  {"w":"rocket","grade":"1st","diff":"hard","origin":"Italian","syl":2,"pos":"noun","d":"a vehicle that travels through space"},
  {"w":"silver","grade":"1st","diff":"hard","origin":"Anglo-Saxon","syl":2,"pos":"noun","d":"a shiny grey-white metal"},
  {"w":"simple","grade":"1st","diff":"hard","origin":"Latin","syl":2,"pos":"adjective","d":"easy to understand or do"},
  {"w":"sister","grade":"1st","diff":"hard","origin":"Anglo-Saxon","syl":2,"pos":"noun","d":"a girl who has the same parents as you"},
  {"w":"turtle","grade":"1st","diff":"hard","origin":"French","syl":2,"pos":"noun","d":"a reptile with a hard shell on its back"},
  {"w":"winter","grade":"1st","diff":"hard","origin":"Anglo-Saxon","syl":2,"pos":"noun","d":"the coldest season of the year"},
  {"w":"yellow","grade":"1st","diff":"hard","origin":"Anglo-Saxon","syl":2,"pos":"adjective","d":"the color of the sun or a lemon"}
]

all_words = []
all_words += load_grade('spelling-bee-words-kindergarten.json', 'kindergarten')
all_words += first_grade
all_words += load_grade('spelling-bee-2nd-grade.json', '2nd')
all_words += load_grade('spelling-bee-3rd-grade.json', '3rd')
all_words += load_grade('spelling-bee-4th-grade.json', '4th')
all_words += load_grade('spelling-bee-5th-grade.json', '5th')

out_path = os.path.join(DATA, 'spelling-bee-words-elementary.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(all_words, f, ensure_ascii=False)

print(f'Written {len(all_words)} words to {out_path}')
grade_counts = {}
for w in all_words:
    grade_counts[w['grade']] = grade_counts.get(w['grade'], 0) + 1
for g, c in sorted(grade_counts.items()):
    print(f'  {g}: {c}')

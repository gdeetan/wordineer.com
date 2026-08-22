#!/usr/bin/env python3
"""Build the 2026 Word of the Day calendar from seed + SAT + words.json."""
import csv
import json
import os
import re
from collections import defaultdict
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.abspath(__file__))
KEYS = [
    'date', 'word', 'pos', 'pronunciation', 'difficulty', 'definition',
    'explanation', 'example', 'memory', 'quiz', 'answer', 'prompt',
]
POS = {'noun', 'adjective', 'verb', 'adverb'}
# 10-day cycle ≈ 30% easy / 50% medium / 20% hard (7-day E-M-M-H-M-E-M is ~57% medium).
PATTERN = ['easy', 'medium', 'medium', 'hard', 'medium', 'easy', 'medium', 'hard', 'medium', 'easy']
BLOCKLIST = {
    'fopdoodle', 'gardyloo', 'snollygoster', 'mamihlapinatapai',
    'kalsarikanni', 'kalsarikänni', 'ninnyhammer', 'smellfungus',
    'quomodocunquize', 'hornswoggle', 'absquatulate', 'blatteroon',
    'callipygian', 'callipygous', 'limeade', 'elbow',
}
FUNCTION_WORDS = {
    'about', 'above', 'after', 'again', 'ahead', 'almost', 'alone', 'along',
    'already', 'also', 'always', 'among', 'another', 'around', 'because',
    'before', 'behind', 'below', 'between', 'beyond', 'during', 'every',
    'other', 'through', 'under', 'until', 'without', 'would', 'could',
    'should', 'their', 'there', 'these', 'those', 'where', 'which', 'while',
    'whose', 'being', 'having', 'doing', 'using', 'across', 'away', 'back',
    'down', 'from', 'into', 'onto', 'over', 'with', 'this', 'that', 'what',
    'when', 'than', 'then', 'them', 'they', 'just', 'more', 'most', 'much',
    'many', 'such', 'very', 'even', 'still', 'only', 'both', 'each', 'some',
    'any', 'few', 'here', 'near', 'once', 'upon', 'within', 'toward',
    'towards', 'against', 'except', 'inside', 'outside', 'beside', 'besides',
    'though', 'although', 'however', 'therefore', 'instead', 'perhaps',
    'rather', 'quite', 'enough', 'several', 'whatever', 'whenever',
    'wherever', 'whoever', 'indeed', 'unless', 'whereas', 'whether',
    'neither', 'either', 'anyway', 'actually', 'probably', 'really',
    'according', 'become', 'based', 'able', 'anti', 'aboard', 'apart',
    'aside', 'else', 'ever', 'yet', 'thus', 'hence', 'via', 'plus', 'unto',
    'amid', 'atop', 'often', 'never', 'usually', 'sometimes', 'today',
    'together', 'wrong', 'first', 'later',
}
BASIC_SKIP = {
    'apple', 'baby', 'ball', 'bank', 'barn', 'book', 'boy', 'girl', 'house',
    'water', 'food', 'room', 'door', 'table', 'chair', 'school', 'friend',
    'mother', 'father', 'answer', 'question', 'number', 'color', 'colour',
    'animal', 'plant', 'beach', 'album', 'army', 'area', 'article', 'attack',
    'attention', 'average', 'angry', 'afraid', 'alive', 'allow', 'amount',
    'action', 'access', 'account', 'addition', 'accept', 'active', 'basic',
    'begin', 'beginning', 'believe', 'beige', 'write', 'writing', 'written',
    'world', 'window', 'wheel', 'years', 'young', 'western', 'works',
    'working', 'worth', 'wrist', 'white', 'whole', 'woman', 'women', 'child',
    'children', 'people', 'person', 'family', 'sister', 'brother', 'teacher',
    'student', 'class', 'paper', 'phone', 'music', 'movie', 'game', 'city',
    'town', 'street', 'road', 'tree', 'flower', 'river', 'ocean', 'rain',
    'snow', 'wind', 'fire', 'earth', 'moon', 'star', 'night', 'morning',
    'week', 'month', 'year', 'time', 'hour', 'money', 'home', 'love', 'like',
    'want', 'need', 'make', 'take', 'give', 'keep', 'know', 'think', 'feel',
    'look', 'seem', 'show', 'tell', 'call', 'ask', 'try', 'thing', 'place',
    'word', 'name', 'hand', 'head', 'face', 'body', 'heart', 'light', 'dark',
    'air', 'side', 'help', 'kind', 'group', 'list', 'bake', 'base', 'bed',
    'bird', 'boat', 'box', 'bread', 'bus', 'cake', 'car', 'cat', 'dog', 'cup',
    'day', 'egg', 'fish', 'hat', 'job', 'man', 'men', 'kid', 'sun', 'run',
    'sit', 'big', 'good', 'bad', 'new', 'old', 'red', 'blue', 'green',
    'black', 'hot', 'cold', 'warm', 'fast', 'slow', 'hard', 'easy', 'left',
    'right', 'great', 'little', 'small', 'large', 'short', 'long', 'happy',
    'better', 'break', 'breathe', 'build', 'carry', 'catch', 'change',
    'cheap', 'choose', 'clean', 'clear', 'climb', 'close', 'common',
    'complete', 'continue', 'cover', 'create', 'cross', 'dance', 'decide',
    'drink', 'drive', 'fight', 'float', 'follow', 'forget', 'sleep', 'smile',
    'stand', 'share', 'throw', 'touch', 'thank', 'learn', 'leave', 'listen',
    'notice', 'please', 'reach', 'remember', 'return', 'include', 'guide',
    'imagine', 'provide', 'understand', 'useful', 'pretty', 'quiet',
    'quickly', 'brown', 'white', 'green', 'black', 'china', 'hamburger',
    'pretzel', 'kindergarten', 'website', 'percent', 'hours', 'hands',
    'minutes', 'times', 'means', 'services', 'blind', 'broken', 'built',
    'dirty', 'funny', 'empty', 'early', 'finally', 'especially',
    'completely', 'available', 'broad', 'different', 'difficult',
    'describe', 'federal', 'financial', 'foreign', 'fresh', 'certain',
    'certainly', 'central', 'economic', 'abnormal', 'abusive',
    'acceptable', 'accessible', 'accessory', 'accidental', 'absolutely',
    'common', 'heard', 'known', 'higher', 'heavy', 'local', 'major',
    'march', 'further', 'important', 'accordingly', 'accompany',
    'beautiful', 'brave', 'gentle', 'gently', 'giant', 'jolly',
    'joyfully', 'kneel', 'merry', 'needs', 'popular', 'previous',
    'likely', 'grand', 'hastily', 'loudly', 'openly', 'lightly',
    'dearly', 'calmly', 'boldly', 'firmly', 'warmly', 'softly',
    'slowly', 'quickly', 'pretty', 'nice', 'kindly', 'happily',
}
SENSITIVE = {
    'abortion', 'abort', 'abortive', 'aboriginal', 'fucking', 'fuck', 'shit',
    'damn', 'crap', 'ass', 'bitch', 'bastard', 'rape', 'sexy', 'porn', 'nude',
    'naked',
}
WORDNET_BAD = re.compile(
    r'(someone or something|or somebody|class of artifacts|;{2,}|Melville|'
    r'that you can quantify|consorting with|quality of taking advantage|'
    r'nonverbal reaction|manner of beginning a musical|'
    r'fleshy part of the human body|blank pages with pockets|mine or quarry|'
    r'without specification|one of a class of|how much there is or how many|'
    r'living organism that feeds|round fruit|round object used in games|'
    r'very young child|financial institution|farm building|'
    r'termination of pregnancy|on first or second or third base|'
    r'base of operations|slang for|sexual intercourse|'
    r'having a substance added|having been fractured|'
    r'to a complete degree|to a distinctly greater extent|'
    r'N\. Hawthorne|Joe Hing Lowe|Daniel Goleman|Albert Camus|'
    r'^accept to be|^come to have|^in such a manner|'
    r'^put up with|^give or assign|^consent to receive|'
    r'^take measures in|^without advance planning)',
    re.I,
)
LEMMA_SUFFIXES = (
    'ability', 'ibility', 'ation', 'ition', 'tion', 'sion', 'ness', 'ment',
    'ility', 'able', 'ible', 'ious', 'eous', 'ous', 'ative', 'itive',
    'ive', 'ate', 'age', 'ing', 'ity', 'ance', 'ence', 'ant', 'ent',
    'est', 'ful', 'less', 'ical', 'ic', 'ed', 'ly', 'ies', 'es', 'er',
    'or', 'al', 'y', 's',
)
NEAR_REMAINDERS = {
    's', 'es', 'ed', 'ing', 'ly', 'er', 'ers', 'or', 'ors', 'al', 'ial',
    'ness', 'less', 'ful', 'ment', 'ments', 'tion', 'ation', 'sion', 'ion',
    'ions', 'ity', 'ities', 'ility', 'ability', 'able', 'ible', 'ous',
    'eous', 'ious', 'ive', 'ance', 'ence', 'ant', 'ent', 'ary', 'ery',
    'ory', 'ure', 'age', 'hood', 'ship', 'dom', 'ism', 'ist', 'ian',
    'ize', 'ise', 'ic', 'ical', 'y', 'ies', 'ied', 'ier', 'iest', 'e',
}
# Stop topping up a difficulty from words.json once SAT+seed already covers the year.
FILL_CAP = {'easy': 125, 'medium': 200, 'hard': 95}

SEED = [
    {'word': 'lucid', 'pos': 'adjective', 'pronunciation': 'LOO-sid', 'difficulty': 'medium', 'definition': 'clear and easy to understand', 'explanation': 'A lucid idea, sentence, or explanation is clear enough that people can follow it without confusion.', 'example': 'Her lucid summary helped the whole class understand the difficult chapter.', 'memory': 'Think of a clear light switching on: lucid writing lights up the meaning.', 'quiz': 'Which sentence uses lucid correctly?', 'answer': 'Correct use: The teacher gave a lucid explanation of the problem.', 'prompt': 'Give students 60 seconds to rewrite a confusing sentence from today\'s lesson so it is lucid.'},
    {'word': 'resilient', 'pos': 'adjective', 'pronunciation': 'ri-ZIL-yuhnt', 'difficulty': 'medium', 'definition': 'able to recover after difficulty or change', 'explanation': 'A resilient person, plan, or material can handle pressure and keep going.', 'example': 'The resilient team adjusted quickly after the first idea failed.', 'memory': 'Resilient sounds like returning to shape after being bent.', 'quiz': 'If someone stays calm and recovers after a setback, what are they?', 'answer': 'They are resilient.', 'prompt': 'Ask students to describe a time they were resilient in one sentence.'},
    {'word': 'nuance', 'pos': 'noun', 'pronunciation': 'NOO-ahns', 'difficulty': 'hard', 'definition': 'a small but important difference in meaning, feeling, or expression', 'explanation': 'Nuance helps you notice the fine details that make two similar ideas not exactly the same.', 'example': 'The actor captured every nuance of the character\'s nervous smile.', 'memory': 'Nuance is the tiny shade of meaning between almost-matching ideas.', 'quiz': 'What does nuance add to an idea?', 'answer': 'It adds a small, subtle difference in meaning or feeling.', 'prompt': 'Have students compare two similar words and name one nuance that separates them.'},
    {'word': 'pragmatic', 'pos': 'adjective', 'pronunciation': 'prag-MAT-ik', 'difficulty': 'hard', 'definition': 'focused on practical results rather than theory', 'explanation': 'A pragmatic choice may not be perfect, but it works in real life.', 'example': 'They made a pragmatic decision to fix the old laptop instead of buying a new one.', 'memory': 'Pragmatic people ask, "What will actually work?"', 'quiz': 'Is a pragmatic solution more practical or more imaginary?', 'answer': 'More practical.', 'prompt': 'Give students a messy classroom problem and ask for one pragmatic fix in a sentence.'},
    {'word': 'vivid', 'pos': 'adjective', 'pronunciation': 'VIV-id', 'difficulty': 'easy', 'definition': 'bright, clear, or full of life', 'explanation': 'Vivid words, colors, or memories feel strong and easy to picture.', 'example': 'The poem used vivid details that made the street feel alive.', 'memory': 'Vivid writing makes a picture feel visible.', 'quiz': 'What kind of details help readers picture a scene?', 'answer': 'Vivid details.', 'prompt': 'Ask students to add two vivid details to a dull sentence on the board.'},
    {'word': 'meticulous', 'pos': 'adjective', 'pronunciation': 'muh-TIK-yuh-luhs', 'difficulty': 'hard', 'definition': 'very careful and attentive to detail', 'explanation': 'Meticulous work is done with patience, precision, and close attention.', 'example': 'The editor made meticulous notes on every paragraph.', 'memory': 'Meticulous means tiny details matter.', 'quiz': 'Would a meticulous person rush through a task?', 'answer': 'No. A meticulous person works carefully.', 'prompt': 'Have students spend 60 seconds making one sentence more meticulous by adding a precise detail.'},
    {'word': 'cordial', 'pos': 'adjective', 'pronunciation': 'KOR-juhl', 'difficulty': 'medium', 'definition': 'warm, friendly, and polite', 'explanation': 'A cordial greeting is friendly without being overly familiar.', 'example': 'The two neighbors exchanged a cordial hello each morning.', 'memory': 'Cordial sounds connected to the heart: friendly and warm.', 'quiz': 'What is a cordial greeting like?', 'answer': 'It is warm, friendly, and polite.', 'prompt': 'Ask students to write a cordial two-sentence email to a classmate.'},
    {'word': 'tenacious', 'pos': 'adjective', 'pronunciation': 'tuh-NAY-shuhs', 'difficulty': 'hard', 'definition': 'not giving up easily', 'explanation': 'A tenacious person keeps holding on to a goal, even when it is difficult.', 'example': 'Her tenacious research finally uncovered the missing records.', 'memory': 'Tenacious means you hold tight to the task.', 'quiz': 'What word describes someone who keeps trying?', 'answer': 'Tenacious.', 'prompt': 'Students write one sentence about a tenacious person from history or sports.'},
    {'word': 'concise', 'pos': 'adjective', 'pronunciation': 'kuhn-SYSE', 'difficulty': 'medium', 'definition': 'using few words while still being clear', 'explanation': 'Concise writing removes extra words but keeps the meaning.', 'example': 'The instructions were concise, so everyone knew what to do.', 'memory': 'Concise means clear and compact.', 'quiz': 'Is concise writing long-winded or brief?', 'answer': 'Brief.', 'prompt': 'Give students a wordy sentence and 60 seconds to make it concise.'},
    {'word': 'curious', 'pos': 'adjective', 'pronunciation': 'KYUR-ee-uhs', 'difficulty': 'easy', 'definition': 'wanting to know or learn more', 'explanation': 'A curious mind asks questions and looks for patterns.', 'example': 'The curious student stayed after class to ask how the machine worked.', 'memory': 'Curious starts with a question.', 'quiz': 'What does a curious person like to do?', 'answer': 'Ask questions and learn more.', 'prompt': 'Ask each student to write one curious question about today\'s topic.'},
    {'word': 'eloquent', 'pos': 'adjective', 'pronunciation': 'EL-uh-kwuhnt', 'difficulty': 'hard', 'definition': 'expressing ideas clearly and beautifully', 'explanation': 'An eloquent speaker or writer uses language in a graceful, effective way.', 'example': 'Her eloquent speech made the audience feel hopeful.', 'memory': 'Eloquent expression sounds elegant and clear.', 'quiz': 'What does an eloquent speaker do well?', 'answer': 'Express ideas clearly and beautifully.', 'prompt': 'Students rewrite a flat opinion so it sounds more eloquent, without adding fluff.'},
    {'word': 'adapt', 'pos': 'verb', 'pronunciation': 'uh-DAPT', 'difficulty': 'easy', 'definition': 'to change so something works in a new situation', 'explanation': 'When you adapt, you adjust your behavior, plan, or tool to fit new conditions.', 'example': 'We had to adapt the lesson for a younger class.', 'memory': 'Adapt means adjust.', 'quiz': 'If plans change and you adjust, what do you do?', 'answer': 'You adapt.', 'prompt': 'Ask students how they would adapt a playground game for a rainy day.'},
]

# High-utility classroom/writing words to fill easy slots (SAT has too few native easy).
# word, pos, pronunciation, definition, example, memory
EXTRA_EASY_SRC = [
    ('accurate', 'adjective', 'AK-yuh-rit', 'correct in all details; free from error', 'Double-check the graph so every label is accurate before you print the poster.', 'Accurate means the details match the facts.'),
    ('benefit', 'noun', 'BEN-uh-fit', 'a helpful or useful result', 'One benefit of outlining is that your essay stays on topic.', 'Benefit is a plus you get from a choice.'),
    ('challenge', 'noun', 'CHAL-inj', 'a difficult task that tests your skill', 'Revising a weak thesis was the biggest challenge of the week.', 'A challenge is a hard task worth trying.'),
    ('contribute', 'verb', 'kuhn-TRIB-yoot', 'to give something that helps a result', 'Each student will contribute one piece of evidence to the shared outline.', 'Contribute means add your part.'),
    ('debate', 'noun', 'di-BAYT', 'a structured argument with reasons on both sides', 'The class held a debate about whether homework should be optional.', 'Debate is a formal back-and-forth.'),
    ('effective', 'adjective', 'ih-FEK-tiv', 'successful at producing the result you want', 'The effective topic sentence told readers exactly what the paragraph would prove.', 'Effective means it actually works.'),
    ('factor', 'noun', 'FAK-ter', 'one of the things that causes or influences a result', 'Time of day was a factor in how well the group finished the lab.', 'A factor is one piece of the cause.'),
    ('impact', 'noun', 'IM-pakt', 'a strong effect on someone or something', 'The new rule had a clear impact on how quietly the hallway felt.', 'Impact is the effect something leaves.'),
    ('method', 'noun', 'METH-uhd', 'a planned way of doing something', 'Our method was to annotate first, then write a one-sentence summary.', 'Method is the how, not the what.'),
    ('outcome', 'noun', 'OWT-kuhm', 'the result of a process or decision', 'The outcome of the peer review was a clearer thesis.', 'Outcome is what you end up with.'),
    ('process', 'noun', 'PRAH-ses', 'a series of steps taken to reach a result', 'Revision is a process, not a single pass through the draft.', 'Process is the steps, not the finish line.'),
    ('research', 'noun', 'REE-surch', 'careful study to find facts or answers', 'Her research included two interviews and a short article.', 'Research means look it up on purpose.'),
    ('strategy', 'noun', 'STRAT-uh-jee', 'a plan for reaching a goal', 'His strategy was to answer the easy questions first.', 'Strategy is a plan of attack.'),
    ('assume', 'verb', 'uh-SOOM', 'to treat something as true without proving it', 'Do not assume the author agrees with the narrator.', 'Assume is a guess you treat as fact.'),
    ('available', 'adjective', 'uh-VAY-luh-buhl', 'able to be used or obtained', 'The style guide is available on the class site if you need a citation example.', 'Available means you can get it.'),
    ('consist', 'verb', 'kuhn-SIST', 'to be made up of particular parts', 'A strong paragraph should consist of a claim, evidence, and explanation.', 'Consist of means is made of.'),
    ('define', 'verb', 'di-FINE', 'to state the exact meaning of a word or idea', 'Before we argue, we need to define what "fair" means in this policy.', 'Define means pin the meaning down.'),
    ('demonstrate', 'verb', 'DEM-uhn-strayt', 'to show clearly with examples or evidence', 'Use a quotation to demonstrate that the character feels trapped.', 'Demonstrate means show, not just say.'),
    ('emerge', 'verb', 'ih-MURJ', 'to become known or come into view', 'A pattern began to emerge after we sorted the survey answers.', 'Emerge means show up or come out.'),
    ('focus', 'verb', 'FOH-kuhs', 'to give close attention to one thing', 'Focus on the verb in each sentence before you check the commas.', 'Focus means aim your attention.'),
    ('indicate', 'verb', 'IN-di-kayt', 'to point out or show something', 'The heading should indicate what the section will explain.', 'Indicate means point to it.'),
    ('involve', 'verb', 'in-VAHLV', 'to include as a necessary part', 'The project will involve a short presentation and a written reflection.', 'Involve means it is part of the work.'),
    ('obtain', 'verb', 'uhb-TAYN', 'to get something through effort', 'Students must obtain parent permission before the field interview.', 'Obtain means get, usually by trying.'),
    ('occur', 'verb', 'uh-KUR', 'to happen, especially at a particular time', 'Most of the plot twists occur in the final chapter.', 'Occur means it happens.'),
    ('policy', 'noun', 'PAH-luh-see', 'an official rule or plan for how to act', 'The late-work policy is posted at the top of the syllabus.', 'A policy is a rule with a reason.'),
    ('principle', 'noun', 'PRIN-suh-puhl', 'a basic rule or belief that guides action', 'Fair citation is a principle we use in every research paper.', 'A principle is a rule you stand on.'),
    ('range', 'noun', 'RAYNJ', 'the set of things included between limits', 'The essay covers a range of causes, from funding to training.', 'Range is how wide the set is.'),
    ('role', 'noun', 'ROHL', 'the function or part someone or something has', 'Evidence plays a central role in a convincing argument.', 'Role is the job something does.'),
    ('significant', 'adjective', 'sig-NIF-uh-kuhnt', 'important enough to be worth noticing', 'The most significant change was a clearer topic sentence.', 'Significant means it matters.'),
    ('similar', 'adjective', 'SIM-uh-ler', 'almost the same, but not identical', 'The two poems are similar in tone but different in setting.', 'Similar means close, not a copy.'),
    ('specific', 'adjective', 'spuh-SIF-ik', 'exact and clearly identified', 'Replace "stuff" with a specific noun the reader can picture.', 'Specific means name the exact thing.'),
    ('structure', 'noun', 'STRUHK-cher', 'the way parts are organized into a whole', 'A compare-and-contrast structure kept the essay easy to follow.', 'Structure is the skeleton of the writing.'),
    ('analyze', 'verb', 'AN-uh-lize', 'to examine the parts of something to understand it', 'Analyze the image by naming what you see before you guess the message.', 'Analyze means take it apart to understand it.'),
    ('compare', 'verb', 'kuhm-PAIR', 'to note how two things are alike', 'Compare the two headlines and list three shared words.', 'Compare looks for likeness.'),
    ('contrast', 'verb', 'kuhn-TRAST', 'to note how two things are different', 'Contrast the first ending with the revised ending.', 'Contrast looks for difference.'),
    ('describe', 'verb', 'di-SKRIBE', 'to say what something is like in words', 'Describe the setting in three precise details from the page.', 'Describe means show it in words.'),
    ('explain', 'verb', 'ik-SPLAYN', 'to make an idea clear by giving reasons', 'After the quote, explain how it supports your claim.', 'Explain means answer why or how.'),
    ('summarize', 'verb', 'SUHM-uh-rize', 'to retell only the main points', 'Summarize the article in four sentences without copying a line.', 'Summarize is the short version.'),
    ('evaluate', 'verb', 'ih-VAL-yoo-ayt', 'to judge the quality or value of something', 'Evaluate the website by checking the author, date, and evidence.', 'Evaluate means judge with reasons.'),
    ('identify', 'verb', 'eye-DEN-tuh-fye', 'to recognize and name something', 'Identify the claim in the first paragraph before you argue with it.', 'Identify means find it and name it.'),
    ('interpret', 'verb', 'in-TUR-prit', 'to explain the meaning of something', 'Interpret the cartoon by saying what each symbol stands for.', 'Interpret means say what it means.'),
    ('evidence', 'noun', 'EV-i-duhns', 'facts or details that support a claim', 'A date, a quote, and a statistic can all count as evidence.', 'Evidence is proof you can point to.'),
    ('claim', 'noun', 'KLAYM', 'a statement that something is true, needing support', 'Your claim should be a sentence a reader could disagree with.', 'A claim is the point you will prove.'),
    ('context', 'noun', 'KON-tekst', 'the situation or words around something that help explain it', 'Give the context of the quote so readers know who is speaking.', 'Context is the surrounding picture.'),
    ('purpose', 'noun', 'PUR-puhs', 'the reason something is done or written', 'Ask what the author\'s purpose is before you judge the tone.', 'Purpose is the why.'),
    ('audience', 'noun', 'AW-dee-uhns', 'the people a writer or speaker is trying to reach', 'Change the examples if your audience is fifth graders, not seniors.', 'Audience is who it is for.'),
    ('revise', 'verb', 'ri-VIZE', 'to change a draft in order to improve it', 'Revise the introduction so the thesis appears by the end of paragraph one.', 'Revise means make it better, not just neater.'),
    ('outline', 'verb', 'OWT-line', 'to list the main points in order before writing', 'Outline the body paragraphs before you write the first sentence.', 'An outline is the map of the essay.'),
]


def load_json(name):
    with open(os.path.join(ROOT, name), encoding='utf-8') as f:
        return json.load(f)


def ok_word(word, min_len=4):
    w = (word or '').strip()
    if not re.fullmatch(rf'[A-Za-z]{{{min_len},12}}', w):
        return False
    low = w.lower()
    if low in BLOCKLIST or low in FUNCTION_WORDS or low in BASIC_SKIP or low in SENSITIVE:
        return False
    return True


def strip_ly(word):
    low = word.strip().lower()
    if low.endswith('ily') and len(low) > 6:
        return low[:-3] + 'y'
    if low.endswith('ly') and len(low) > 5:
        base = low[:-2]
        if len(base) >= 4 and base.endswith('l') and not base.endswith('ll'):
            return base + 'e'
        return base
    return low


def strip_neg_prefix(word):
    low = word.strip().lower()
    for p in ('dis', 'non', 'un', 'in', 'im', 'ir', 'il'):
        if low.startswith(p) and len(low) - len(p) >= 6:
            return low[len(p):]
    return low


def lemma_key(word):
    low = strip_neg_prefix(strip_ly(word))
    for suf in LEMMA_SUFFIXES:
        if len(low) > len(suf) + 2 and low.endswith(suf):
            stem = low[:-len(suf)]
            if len(stem) >= 3:
                return stem
    return low


def family_stems(word):
    low = word.strip().lower()
    stems = {low, strip_ly(low), strip_neg_prefix(low), lemma_key(low)}
    lk = lemma_key(low)
    if len(lk) >= 6:
        stems.add(lk[:6])
    return {s for s in stems if len(s) >= 3}


def near_lemma(a, b):
    a, b = a.strip().lower(), b.strip().lower()
    if a == b:
        return True
    if a + 'ly' == b or b + 'ly' == a:
        return True
    if strip_ly(a) == strip_ly(b):
        return True
    if lemma_key(a) == lemma_key(b):
        return True
    sa, sb = lemma_key(a), lemma_key(b)
    if len(sa) >= 6 and len(sb) >= 6 and (sa.startswith(sb[:6]) or sb.startswith(sa[:6])):
        return True
    short, long_ = (a, b) if len(a) <= len(b) else (b, a)
    if len(short) >= 5 and long_.startswith(short):
        return True
    if len(short) >= 4 and long_.startswith(short):
        rest = long_[len(short):]
        if rest in NEAR_REMAINDERS or 0 < len(rest) <= 3:
            return True
    if len(short) >= 4 and short.endswith('e') and long_.startswith(short[:-1]):
        if long_[len(short) - 1:] in NEAR_REMAINDERS:
            return True
    return False


def useful_definition(definition, strict=False):
    d = (definition or '').strip()
    if len(d) < (24 if strict else 12):
        return False
    if '<' in d or '>' in d:
        return False
    if d.count(';') >= 2:
        return False
    if WORDNET_BAD.search(d):
        return False
    if re.search(r'slang for|sexual intercourse|termination of pregnancy', d, re.I):
        return False
    if strict and not re.search(
        r'\b(to |a |an |the |having |being |not |of |with |from )\b',
        ' ' + d,
        re.I,
    ):
        return False
    return True


def pron_from_syl(syl, word):
    if not syl:
        return word.upper()
    parts = [p for p in re.split(r'[·.\-]+', syl) if p]
    if not parts:
        return word.upper()
    parts = [p.lower() for p in parts]
    parts[-1] = parts[-1].upper()
    return '-'.join(parts)


def make_example(word, pos, definition):
    w = word.strip()
    if pos == 'adjective':
        return f'The {w} paragraph in her essay made a hard idea easier to follow.'
    if pos == 'adverb':
        return f'She answered {w}, and the class understood the point right away.'
    if pos == 'verb':
        return f'The teacher asked us to {w} the claim with evidence from the article.'
    return f'In writing workshop we used "{w}" when we meant {definition}.'


def make_memory(word, definition):
    return f'Picture a classroom moment that shows "{word}": {definition}.'


def fill_fields(word, pos, pronunciation, difficulty, definition, example, memory):
    word = word.strip()
    pos = pos.strip().lower()
    definition = definition.strip().rstrip('.')
    if definition[0].isupper() and not definition.startswith(word.capitalize()):
        definition = definition[0].lower() + definition[1:]
    if len(definition) > 100:
        definition = definition[:97].rsplit(' ', 1)[0] + '…'
    article = 'an' if pos in ('adjective', 'adverb') else 'a'
    explanation = (
        f'{word.capitalize()} is {article} {pos} meaning {definition}. '
        f'Use it when that meaning is exactly what you need in writing or speech.'
    )
    if not example:
        example = make_example(word, pos, definition)
    if not memory:
        memory = make_memory(word, definition)
    quiz = f'What does "{word}" mean?'
    answer = definition[0].upper() + definition[1:] + '.'
    prompt = (
        f'Give students 60 seconds to use "{word}" in an original sentence '
        f'that shows it means "{definition}".'
    )
    return {
        'word': word.lower() if word.islower() or word.istitle() else word,
        'pos': pos,
        'pronunciation': pronunciation,
        'difficulty': difficulty,
        'definition': definition,
        'explanation': explanation,
        'example': example,
        'memory': memory,
        'quiz': quiz,
        'answer': answer,
        'prompt': prompt,
    }


def display_word(word):
    return word[:1].upper() + word[1:] if word else word


def collect_candidates():
    used_words = set()
    used_lemmas = set()
    used_stems = set()
    buckets = defaultdict(list)

    def take(entry):
        w = entry['word']
        key = w.strip().lower()
        lemma = lemma_key(w)
        stems = family_stems(w)
        if key in used_words or lemma in used_lemmas or (stems & used_stems):
            return False
        if key + 'ly' in used_words or (key.endswith('ly') and strip_ly(key) in used_words):
            return False
        if any(near_lemma(key, u) for u in used_words):
            return False
        used_words.add(key)
        used_lemmas.add(lemma)
        used_stems.update(s for s in stems if len(s) >= 6)
        used_stems.add(lemma)
        entry = dict(entry)
        entry['word'] = display_word(w)
        buckets[entry['difficulty']].append(entry)
        return True

    for row in SEED:
        take(dict(row))

    for word, pos, pron, definition, example, memory in EXTRA_EASY_SRC:
        take(fill_fields(word, pos, pron, 'easy', definition, example, memory))

    sat = load_json('sat-vocab-data.json')

    def sat_sort_key(r):
        w = (r.get('w') or '').lower()
        diff = {'easy': 0, 'medium': 1, 'hard': 2}.get(r.get('diff'), 9)
        prefixed = 1 if strip_neg_prefix(w) != w else 0
        return (prefixed, diff, w)

    sat_sorted = sorted(sat, key=sat_sort_key)
    for r in sat_sorted:
        w = r.get('w') or ''
        pos = (r.get('pos') or '').lower()
        diff = r.get('diff') or 'medium'
        definition = r.get('d') or ''
        if not ok_word(w) or pos not in POS or diff not in {'easy', 'medium', 'hard'}:
            continue
        if not useful_definition(definition, strict=False):
            continue
        take(fill_fields(
            w, pos, pron_from_syl(r.get('syl'), w), diff,
            definition, r.get('ex') or '', r.get('root_note') or '',
        ))

    words = load_json('words.json')
    for row in words:
        w, pos, definition, diff = row[0], row[1], row[2], row[3]
        if diff not in {'easy', 'medium', 'hard'}:
            continue
        if len(buckets[diff]) >= FILL_CAP[diff]:
            continue
        if not ok_word(w, min_len=5) or pos not in POS:
            continue
        if pos in ('noun', 'adverb'):
            continue
        if w.lower().endswith(('ing', 'ed', 'ly')):
            continue
        if not useful_definition(definition, strict=True):
            continue
        take(fill_fields(w, pos, w.upper(), diff, definition, '', ''))

    return buckets


def assign_dates(buckets):
    dates = []
    d = date(2026, 1, 1)
    while d.year == 2026:
        dates.append(d.isoformat())
        d += timedelta(days=1)

    pointers = {k: 0 for k in ('easy', 'medium', 'hard')}
    out = []
    for i, dt in enumerate(dates):
        want = PATTERN[i % len(PATTERN)]
        chosen = None
        for candidate in (want, 'medium', 'easy', 'hard'):
            idx = pointers[candidate]
            if idx < len(buckets[candidate]):
                chosen = dict(buckets[candidate][idx])
                pointers[candidate] = idx + 1
                break
        if chosen is None:
            raise SystemExit('Not enough candidate words to fill 365 days')
        chosen['date'] = dt
        out.append({k: chosen[k] for k in KEYS})
    return out


def write_csv(rows, path):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=KEYS, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)


def assert_one_lemma(rows):
    lows = [r['word'].strip().lower() for r in rows]
    seen = set(lows)
    for w in lows:
        if w + 'ly' in seen:
            raise SystemExit(f'lemma pair {w} / {w}ly')
        if w.endswith('ly') and strip_ly(w) in seen:
            raise SystemExit(f'lemma pair {strip_ly(w)} / {w}')
        if w.endswith('ly') and w[:-2] in seen:
            raise SystemExit(f'lemma pair {w[:-2]} / {w}')


def main():
    buckets = collect_candidates()
    rows = assign_dates(buckets)
    assert_one_lemma(rows)
    json_path = os.path.join(ROOT, 'wotd-2026.json')
    csv_path = os.path.join(ROOT, 'wotd-2026.csv')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
        f.write('\n')
    write_csv(rows, csv_path)
    print(f'wrote {len(rows)} rows -> {json_path} and {csv_path}')


if __name__ == '__main__':
    main()

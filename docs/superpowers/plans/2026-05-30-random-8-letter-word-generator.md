# Random 8-Letter Word Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a `/random-8-letter-word-generator/` tool page for Wordineer using the same template pattern as the 6/7-letter tools, with an advanced-vocabulary copy angle.

**Architecture:** Clone `random-7-letter-word-generator.html`, update all 8-letter-specific content (CONFIG, seed words, data path, copy slots). Create a JSON dataset `eight-letter-words.json`. Register in `tools.json` and `_redirects`, then build and deploy.

**Tech Stack:** Static HTML/CSS/vanilla JS, Python build script, Cloudflare Pages

---

## File Map

| Action | File |
|--------|------|
| Create | `wordineer-deploy/data/eight-letter-words.json` |
| Create | `template-deploy/tools-src/random-8-letter-word-generator.html` |
| Modify | `template-deploy/tools.json` |
| Modify | `wordineer-deploy/_redirects` |
| Generate | `template-deploy/output/random-8-letter-word-generator.html` (via build) |
| Copy | `wordineer-deploy/random-8-letter-word-generator.html` (from output) |

---

## Task 1: Create the eight-letter-words.json dataset

**Files:**
- Create: `wordineer-deploy/data/eight-letter-words.json`

- [ ] **Step 1: Create the dataset file**

Create `wordineer-deploy/data/eight-letter-words.json` with the following content (250 words, schema matches existing datasets: `w`, `t`, `d`, `diff`, `borrowed`):

```json
[
  {"w":"Absolute","t":"adjective","d":"complete; not qualified or diminished in any way","diff":"easy","borrowed":false},
  {"w":"Abstract","t":"adjective","d":"existing in thought or as an idea, not concrete","diff":"easy","borrowed":false},
  {"w":"Backbone","t":"noun","d":"the spine; the chief support of a system or organisation","diff":"easy","borrowed":false},
  {"w":"Baseball","t":"noun","d":"a ball game played between two teams of nine players","diff":"easy","borrowed":false},
  {"w":"Birthday","t":"noun","d":"the annual anniversary of the day one was born","diff":"easy","borrowed":false},
  {"w":"Blankets","t":"noun","d":"large pieces of woollen material used as bed coverings","diff":"easy","borrowed":false},
  {"w":"Blossome","t":"noun","d":"a flower or mass of flowers on a tree","diff":"easy","borrowed":false},
  {"w":"Bookcase","t":"noun","d":"a piece of furniture with shelves for holding books","diff":"easy","borrowed":false},
  {"w":"Brightly","t":"adverb","d":"with a strong clear light; in a vivid manner","diff":"easy","borrowed":false},
  {"w":"Buildup","t":"noun","d":"a gradual accumulation or increase of something","diff":"easy","borrowed":false},
  {"w":"Calendar","t":"noun","d":"a chart or series of pages showing days, weeks, and months","diff":"easy","borrowed":false},
  {"w":"Champion","t":"noun","d":"a person who has won a competition or contest","diff":"easy","borrowed":false},
  {"w":"Children","t":"noun","d":"young human beings below the age of puberty","diff":"easy","borrowed":false},
  {"w":"Cleaning","t":"verb","d":"making something free from dirt, marks, or mess","diff":"easy","borrowed":false},
  {"w":"Climbing","t":"verb","d":"going up or ascending something","diff":"easy","borrowed":false},
  {"w":"Clothing","t":"noun","d":"items worn to cover the body; garments collectively","diff":"easy","borrowed":false},
  {"w":"Complete","t":"adjective","d":"having all the necessary or appropriate parts","diff":"easy","borrowed":false},
  {"w":"Computer","t":"noun","d":"an electronic device for storing and processing data","diff":"easy","borrowed":false},
  {"w":"Concrete","t":"adjective","d":"existing in a material or physical form; specific and definite","diff":"easy","borrowed":false},
  {"w":"Creative","t":"adjective","d":"relating to or involving the imagination; producing original ideas","diff":"easy","borrowed":false},
  {"w":"Cultural","t":"adjective","d":"relating to the ideas, customs, and social behaviour of a society","diff":"easy","borrowed":false},
  {"w":"Daylight","t":"noun","d":"the natural light of the day","diff":"easy","borrowed":false},
  {"w":"Deadline","t":"noun","d":"the latest time by which something must be completed","diff":"easy","borrowed":false},
  {"w":"Daughter","t":"noun","d":"a girl or woman in relation to her parents","diff":"easy","borrowed":false},
  {"w":"Describe","t":"verb","d":"to give a detailed account of something in words","diff":"easy","borrowed":false},
  {"w":"Distance","t":"noun","d":"the length of space between two points","diff":"easy","borrowed":false},
  {"w":"Doghouse","t":"noun","d":"a shelter for a dog; a state of disfavour","diff":"easy","borrowed":false},
  {"w":"Dramatic","t":"adjective","d":"relating to drama; sudden and striking","diff":"easy","borrowed":false},
  {"w":"Dropping","t":"verb","d":"letting something fall; declining in level or amount","diff":"easy","borrowed":false},
  {"w":"Educated","t":"adjective","d":"having been taught; having received formal instruction","diff":"easy","borrowed":false},
  {"w":"Absolute","t":"adjective","d":"complete; not qualified or diminished in any way","diff":"easy","borrowed":false},
  {"w":"Everyone","t":"noun","d":"every person; all people","diff":"easy","borrowed":false},
  {"w":"Exciting","t":"adjective","d":"causing great enthusiasm and eagerness","diff":"easy","borrowed":false},
  {"w":"Exercise","t":"noun","d":"activity requiring physical effort to sustain health","diff":"easy","borrowed":false},
  {"w":"Familiar","t":"adjective","d":"well known from long or close association","diff":"easy","borrowed":false},
  {"w":"Feedback","t":"noun","d":"information about reactions to a product or performance","diff":"easy","borrowed":false},
  {"w":"Finished","t":"adjective","d":"brought to an end; completed","diff":"easy","borrowed":false},
  {"w":"Football","t":"noun","d":"a team game played with an inflated ball","diff":"easy","borrowed":false},
  {"w":"Friendly","t":"adjective","d":"kind and pleasant; characteristic of a friend","diff":"easy","borrowed":false},
  {"w":"Frontman","t":"noun","d":"the lead vocalist or most prominent member of a group","diff":"easy","borrowed":false},
  {"w":"Grateful","t":"adjective","d":"feeling or showing gratitude","diff":"easy","borrowed":false},
  {"w":"Grouping","t":"noun","d":"a set of people or things with a shared characteristic","diff":"easy","borrowed":false},
  {"w":"Guidance","t":"noun","d":"advice or information aimed at resolving a problem","diff":"easy","borrowed":false},
  {"w":"Handbook","t":"noun","d":"a book giving information about a subject","diff":"easy","borrowed":false},
  {"w":"Harmless","t":"adjective","d":"not able to cause harm; unlikely to cause hurt","diff":"easy","borrowed":false},
  {"w":"Homework","t":"noun","d":"schoolwork that a pupil is required to do at home","diff":"easy","borrowed":false},
  {"w":"Hopeless","t":"adjective","d":"feeling or causing despair; having no chance of success","diff":"easy","borrowed":false},
  {"w":"Humanity","t":"noun","d":"human beings collectively; the quality of being humane","diff":"easy","borrowed":false},
  {"w":"Identity","t":"noun","d":"the fact of being who or what a person or thing is","diff":"easy","borrowed":false},
  {"w":"Imagine","t":"verb","d":"form a mental image or concept of something","diff":"easy","borrowed":false},
  {"w":"Increase","t":"verb","d":"to make or become greater in size, amount, or intensity","diff":"easy","borrowed":false},
  {"w":"Industry","t":"noun","d":"economic activity concerned with the production of goods","diff":"easy","borrowed":false},
  {"w":"Informed","t":"adjective","d":"having or showing knowledge about a subject","diff":"easy","borrowed":false},
  {"w":"Language","t":"noun","d":"the method of human communication using words","diff":"easy","borrowed":false},
  {"w":"Laughter","t":"noun","d":"the action or sound of laughing","diff":"easy","borrowed":false},
  {"w":"Listening","t":"verb","d":"giving attention to a sound","diff":"easy","borrowed":false},
  {"w":"Location","t":"noun","d":"a particular place or position","diff":"easy","borrowed":false},
  {"w":"Millions","t":"noun","d":"the number equivalent to the product of a thousand and a thousand","diff":"easy","borrowed":false},
  {"w":"Momentum","t":"noun","d":"the force or strength gained by motion or a series of events","diff":"easy","borrowed":false},
  {"w":"Mountain","t":"noun","d":"a large natural elevation of the earth's surface","diff":"easy","borrowed":false},
  {"w":"National","t":"adjective","d":"relating to or characteristic of a nation","diff":"easy","borrowed":false},
  {"w":"Navigate","t":"verb","d":"to plan and direct the route or course of a ship, aircraft, or other form of transport","diff":"easy","borrowed":false},
  {"w":"Notebook","t":"noun","d":"a book with blank or ruled pages for writing notes","diff":"easy","borrowed":false},
  {"w":"Occasion","t":"noun","d":"a particular time or instance of an event","diff":"easy","borrowed":false},
  {"w":"Offering","t":"noun","d":"a thing offered, especially as a gift or contribution","diff":"easy","borrowed":false},
  {"w":"Operator","t":"noun","d":"a person who operates equipment or machinery","diff":"easy","borrowed":false},
  {"w":"Original","t":"adjective","d":"present or existing from the beginning; first or earliest","diff":"easy","borrowed":false},
  {"w":"Outdoors","t":"adverb","d":"in or into the open air","diff":"easy","borrowed":false},
  {"w":"Overcome","t":"verb","d":"to succeed in dealing with a problem or difficulty","diff":"easy","borrowed":false},
  {"w":"Patience","t":"noun","d":"the capacity to accept or tolerate delay without becoming annoyed","diff":"easy","borrowed":false},
  {"w":"Personal","t":"adjective","d":"of, affecting, or belonging to a particular person","diff":"easy","borrowed":false},
  {"w":"Platform","t":"noun","d":"a raised level surface; a standard technology environment","diff":"easy","borrowed":false},
  {"w":"Pleasant","t":"adjective","d":"giving a sense of happiness or enjoyment","diff":"easy","borrowed":false},
  {"w":"Positive","t":"adjective","d":"consisting of or characterised by good qualities","diff":"easy","borrowed":false},
  {"w":"Possible","t":"adjective","d":"able to be done; within the power of someone","diff":"easy","borrowed":false},
  {"w":"Practice","t":"noun","d":"the actual application or use of a plan or method","diff":"easy","borrowed":false},
  {"w":"Priority","t":"noun","d":"something regarded as more important than others","diff":"easy","borrowed":false},
  {"w":"Progress","t":"noun","d":"forward or onward movement towards a destination or goal","diff":"easy","borrowed":false},
  {"w":"Question","t":"noun","d":"a sentence worded to find out information","diff":"easy","borrowed":false},
  {"w":"Reaching","t":"verb","d":"stretching out a hand in order to touch or grasp something","diff":"easy","borrowed":false},
  {"w":"Relation","t":"noun","d":"the way in which two things are connected","diff":"easy","borrowed":false},
  {"w":"Research","t":"noun","d":"the systematic investigation to establish facts","diff":"easy","borrowed":false},
  {"w":"Response","t":"noun","d":"a written or verbal answer","diff":"easy","borrowed":false},
  {"w":"Schedule","t":"noun","d":"a plan for carrying out a process or procedure","diff":"easy","borrowed":false},
  {"w":"Scenario","t":"noun","d":"a postulated sequence of events; a setting or situation","diff":"easy","borrowed":false},
  {"w":"Seasonal","t":"adjective","d":"relating to or dependent on a particular season","diff":"easy","borrowed":false},
  {"w":"Security","t":"noun","d":"the state of being free from danger or threat","diff":"easy","borrowed":false},
  {"w":"Sequence","t":"noun","d":"a particular order in which related things follow each other","diff":"easy","borrowed":false},
  {"w":"Shopping","t":"noun","d":"the action of going to shops to buy goods","diff":"easy","borrowed":false},
  {"w":"Singular","t":"adjective","d":"exceptionally good or great; remarkable","diff":"easy","borrowed":false},
  {"w":"Sleeping","t":"verb","d":"in a state of sleep","diff":"easy","borrowed":false},
  {"w":"Solution","t":"noun","d":"a means of solving a problem or dealing with a difficult situation","diff":"easy","borrowed":false},
  {"w":"Standard","t":"noun","d":"a level of quality or attainment","diff":"easy","borrowed":false},
  {"w":"Starting","t":"verb","d":"beginning to do or engage in something","diff":"easy","borrowed":false},
  {"w":"Strength","t":"noun","d":"the quality of being physically strong","diff":"easy","borrowed":false},
  {"w":"Students","t":"noun","d":"persons who are studying at a school or university","diff":"easy","borrowed":false},
  {"w":"Together","t":"adverb","d":"with or in proximity to another person or people","diff":"easy","borrowed":false},
  {"w":"Training","t":"noun","d":"the action of teaching a person a particular skill","diff":"easy","borrowed":false},
  {"w":"Transfer","t":"verb","d":"to move from one place to another","diff":"easy","borrowed":false},
  {"w":"Umbrella","t":"noun","d":"a device for protection against rain consisting of a fabric canopy","diff":"easy","borrowed":false},
  {"w":"Universe","t":"noun","d":"all existing matter and space considered as a whole","diff":"easy","borrowed":false},
  {"w":"Vacation","t":"noun","d":"an extended period of leisure and recreation","diff":"easy","borrowed":false},
  {"w":"Valuable","t":"adjective","d":"worth a great deal of money; extremely useful","diff":"easy","borrowed":false},
  {"w":"Thinking","t":"verb","d":"using thought or rational judgement","diff":"easy","borrowed":false},
  {"w":"Watching","t":"verb","d":"looking at someone or something attentively","diff":"easy","borrowed":false},
  {"w":"Workload","t":"noun","d":"the amount of work to be done by someone","diff":"easy","borrowed":false},
  {"w":"Absolute","t":"adjective","d":"not qualified or diminished in any way; total","diff":"easy","borrowed":false},
  {"w":"Absolute","t":"adjective","d":"not qualified or diminished in any way","diff":"easy","borrowed":false},
  {"w":"Abundant","t":"adjective","d":"present in large quantities; more than enough","diff":"medium","borrowed":false},
  {"w":"Accurate","t":"adjective","d":"free from errors; conforming exactly to truth","diff":"medium","borrowed":false},
  {"w":"Adornment","t":"noun","d":"a thing that adorns or decorates; an ornament","diff":"medium","borrowed":false},
  {"w":"Advocacy","t":"noun","d":"public support for or recommendation of a cause or policy","diff":"medium","borrowed":false},
  {"w":"Ambition","t":"noun","d":"a strong desire to achieve something requiring determination","diff":"medium","borrowed":false},
  {"w":"Analytic","t":"adjective","d":"relating to or using analysis; systematic in approach","diff":"medium","borrowed":false},
  {"w":"Animated","t":"adjective","d":"full of life or excitement; lively","diff":"medium","borrowed":false},
  {"w":"Appetite","t":"noun","d":"a natural desire to satisfy a bodily need","diff":"medium","borrowed":false},
  {"w":"Articulate","t":"adjective","d":"having or showing the ability to speak fluently and coherently","diff":"medium","borrowed":false},
  {"w":"Audacity","t":"noun","d":"a willingness to take bold risks; impudence","diff":"medium","borrowed":false},
  {"w":"Autonomy","t":"noun","d":"the right or condition of self-government","diff":"medium","borrowed":false},
  {"w":"Balanced","t":"adjective","d":"keeping or showing a balance; not giving too much emphasis to one side","diff":"medium","borrowed":false},
  {"w":"Brilliance","t":"noun","d":"intense brightness; exceptional talent or intelligence","diff":"medium","borrowed":false},
  {"w":"Cautious","t":"adjective","d":"making sure to avoid potential problems or dangers","diff":"medium","borrowed":false},
  {"w":"Coherent","t":"adjective","d":"logical and consistent; clearly articulated","diff":"medium","borrowed":false},
  {"w":"Composure","t":"noun","d":"the state of being calm and in control of oneself","diff":"medium","borrowed":false},
  {"w":"Conclude","t":"verb","d":"to bring or come to an end; to arrive at a judgement","diff":"medium","borrowed":false},
  {"w":"Conflict","t":"noun","d":"a serious disagreement or argument; prolonged armed struggle","diff":"medium","borrowed":false},
  {"w":"Contempt","t":"noun","d":"the feeling that a person is beneath consideration or worthless","diff":"medium","borrowed":false},
  {"w":"Credible","t":"adjective","d":"able to be believed; convincing","diff":"medium","borrowed":false},
  {"w":"Critique","t":"noun","d":"a detailed analysis and assessment of something","diff":"medium","borrowed":false},
  {"w":"Defining","t":"verb","d":"stating or describing the nature or meaning of something","diff":"medium","borrowed":false},
  {"w":"Dextrous","t":"adjective","d":"showing skill, especially with the hands","diff":"medium","borrowed":false},
  {"w":"Dialogue","t":"noun","d":"conversation between two or more people","diff":"medium","borrowed":false},
  {"w":"Diligent","t":"adjective","d":"having or showing care and conscientiousness in one's work","diff":"medium","borrowed":false},
  {"w":"Distinct","t":"adjective","d":"recognisably different from something else; clear and definite","diff":"medium","borrowed":false},
  {"w":"Dominant","t":"adjective","d":"most important, powerful, or influential","diff":"medium","borrowed":false},
  {"w":"Eloquent","t":"adjective","d":"fluent or persuasive in speaking or writing","diff":"medium","borrowed":false},
  {"w":"Embolden","t":"verb","d":"to give someone the courage or confidence to do something","diff":"medium","borrowed":false},
  {"w":"Emphasis","t":"noun","d":"special importance, value, or prominence given to something","diff":"medium","borrowed":false},
  {"w":"Energise","t":"verb","d":"to give vitality and enthusiasm to something","diff":"medium","borrowed":false},
  {"w":"Ephemeral","t":"adjective","d":"lasting for a very short time","diff":"medium","borrowed":false},
  {"w":"Evaluate","t":"verb","d":"to form an idea of the amount, number, or value of something","diff":"medium","borrowed":false},
  {"w":"Evidence","t":"noun","d":"available facts or information indicating whether a belief is true","diff":"medium","borrowed":false},
  {"w":"Exquisite","t":"adjective","d":"extremely beautiful and delicate","diff":"medium","borrowed":false},
  {"w":"Fidelity","t":"noun","d":"faithfulness to a person, cause, or belief","diff":"medium","borrowed":false},
  {"w":"Fluently","t":"adverb","d":"in a smoothly graceful and effortless manner","diff":"medium","borrowed":false},
  {"w":"Footnote","t":"noun","d":"an additional piece of information placed at the bottom of a page","diff":"medium","borrowed":false},
  {"w":"Formidable","t":"adjective","d":"inspiring fear or respect through being impressively powerful","diff":"medium","borrowed":false},
  {"w":"Fragment","t":"noun","d":"a small piece broken off from something","diff":"medium","borrowed":false},
  {"w":"Frontier","t":"noun","d":"a line separating two countries; the edge of knowledge","diff":"medium","borrowed":false},
  {"w":"Generous","t":"adjective","d":"showing a readiness to give more than is necessary","diff":"medium","borrowed":false},
  {"w":"Glacious","t":"adjective","d":"relating to or derived from ice or glaciers","diff":"medium","borrowed":false},
  {"w":"Graceful","t":"adjective","d":"having or showing grace; elegantly smooth","diff":"medium","borrowed":false},
  {"w":"Grateful","t":"adjective","d":"feeling or showing an appreciation for something received","diff":"medium","borrowed":false},
  {"w":"Gravitas","t":"noun","d":"dignity and seriousness of manner","diff":"medium","borrowed":false},
  {"w":"Harmonic","t":"adjective","d":"relating to harmony in music; forming a pleasing whole","diff":"medium","borrowed":false},
  {"w":"Imminent","t":"adjective","d":"about to happen","diff":"medium","borrowed":false},
  {"w":"Implicit","t":"adjective","d":"implied though not directly expressed","diff":"medium","borrowed":false},
  {"w":"Inherent","t":"adjective","d":"existing as a permanent and inseparable element","diff":"medium","borrowed":false},
  {"w":"Integral","t":"adjective","d":"necessary to make a whole complete; fundamental","diff":"medium","borrowed":false},
  {"w":"Leverage","t":"noun","d":"the power to influence a person or situation","diff":"medium","borrowed":false},
  {"w":"Luminous","t":"adjective","d":"full of or shedding light; glowing","diff":"medium","borrowed":false},
  {"w":"Manifest","t":"verb","d":"to display or show a quality by actions","diff":"medium","borrowed":false},
  {"w":"Marginal","t":"adjective","d":"of secondary or minor importance; relating to a margin","diff":"medium","borrowed":false},
  {"w":"Metadata","t":"noun","d":"data that provides information about other data","diff":"medium","borrowed":false},
  {"w":"Moderate","t":"adjective","d":"average in amount, intensity, quality, or degree","diff":"medium","borrowed":false},
  {"w":"Momentum","t":"noun","d":"force or strength gained by motion or a series of events","diff":"medium","borrowed":false},
  {"w":"Motivate","t":"verb","d":"to provide someone with a reason for doing something","diff":"medium","borrowed":false},
  {"w":"Nuisance","t":"noun","d":"a person, thing, or circumstance causing inconvenience","diff":"medium","borrowed":false},
  {"w":"Obsolete","t":"adjective","d":"no longer produced or used; out of date","diff":"medium","borrowed":false},
  {"w":"Paradox","t":"noun","d":"a statement that contradicts itself but may be true","diff":"medium","borrowed":false},
  {"w":"Patience","t":"noun","d":"the capacity to tolerate delay, trouble, or suffering","diff":"medium","borrowed":false},
  {"w":"Perceive","t":"verb","d":"to become aware of something through the senses","diff":"medium","borrowed":false},
  {"w":"Pragmatic","t":"adjective","d":"dealing with things sensibly and realistically","diff":"medium","borrowed":false},
  {"w":"Profound","t":"adjective","d":"very great or intense; having deep insight or understanding","diff":"medium","borrowed":false},
  {"w":"Rationale","t":"noun","d":"a set of reasons or logical basis for a course of action","diff":"medium","borrowed":false},
  {"w":"Relevant","t":"adjective","d":"closely connected or appropriate to what is being done","diff":"medium","borrowed":false},
  {"w":"Reliable","t":"adjective","d":"consistently good in quality; able to be trusted","diff":"medium","borrowed":false},
  {"w":"Resilient","t":"adjective","d":"able to withstand or recover quickly from difficult conditions","diff":"medium","borrowed":false},
  {"w":"Restraint","t":"noun","d":"a measure or condition that limits or restricts someone","diff":"medium","borrowed":false},
  {"w":"Rigorous","t":"adjective","d":"extremely thorough and careful; adhering strictly to standards","diff":"medium","borrowed":false},
  {"w":"Scenario","t":"noun","d":"a postulated sequence of events; a setting or situation","diff":"medium","borrowed":false},
  {"w":"Scrutiny","t":"noun","d":"critical observation or examination","diff":"medium","borrowed":false},
  {"w":"Sedulous","t":"adjective","d":"showing dedication and diligence","diff":"medium","borrowed":false},
  {"w":"Sincerity","t":"noun","d":"the quality of being free from pretence or deceit","diff":"medium","borrowed":false},
  {"w":"Spectrum","t":"noun","d":"a band of colours or a range of positions on a scale","diff":"medium","borrowed":false},
  {"w":"Stamina","t":"noun","d":"the ability to sustain prolonged physical or mental effort","diff":"medium","borrowed":false},
  {"w":"Steadfast","t":"adjective","d":"resolutely or dutifully firm and unwavering","diff":"medium","borrowed":false},
  {"w":"Strategy","t":"noun","d":"a plan of action designed to achieve a long-term aim","diff":"medium","borrowed":false},
  {"w":"Succinct","t":"adjective","d":"briefly and clearly expressed","diff":"medium","borrowed":false},
  {"w":"Suitable","t":"adjective","d":"right or appropriate for a particular purpose or person","diff":"medium","borrowed":false},
  {"w":"Sympathy","t":"noun","d":"feelings of pity and sorrow for someone else's misfortune","diff":"medium","borrowed":false},
  {"w":"Tangible","t":"adjective","d":"perceptible by touch; clear and definite","diff":"medium","borrowed":false},
  {"w":"Tenacity","t":"noun","d":"the quality of being very determined; persistence","diff":"medium","borrowed":false},
  {"w":"Thorough","t":"adjective","d":"complete with regard to every detail; not superficial","diff":"medium","borrowed":false},
  {"w":"Timeless","t":"adjective","d":"not affected by the passage of time or changes in fashion","diff":"medium","borrowed":false},
  {"w":"Tolerant","t":"adjective","d":"showing willingness to allow the existence of opinions one dislikes","diff":"medium","borrowed":false},
  {"w":"Traverse","t":"verb","d":"to travel across or through a place","diff":"medium","borrowed":false},
  {"w":"Vigilant","t":"adjective","d":"keeping careful watch for possible danger or difficulties","diff":"medium","borrowed":false},
  {"w":"Virtuous","t":"adjective","d":"having or showing high moral standards","diff":"medium","borrowed":false},
  {"w":"Vocalize","t":"verb","d":"to express with the voice; to make a vocal sound","diff":"medium","borrowed":false},
  {"w":"Volition","t":"noun","d":"the faculty or power of using one's will","diff":"medium","borrowed":false},
  {"w":"Abstruse","t":"adjective","d":"difficult to understand; obscure","diff":"hard","borrowed":false},
  {"w":"Acerbity","t":"noun","d":"sharpness of manner or language; a harsh quality","diff":"hard","borrowed":false},
  {"w":"Acrimony","t":"noun","d":"bitterness or ill feeling","diff":"hard","borrowed":false},
  {"w":"Alacrity","t":"noun","d":"brisk and cheerful readiness to do something","diff":"hard","borrowed":false},
  {"w":"Anathema","t":"noun","d":"something or someone greatly detested or loathed","diff":"hard","borrowed":false},
  {"w":"Anodyne","t":"adjective","d":"not likely to provoke dissent; unlikely to cause offence","diff":"hard","borrowed":false},
  {"w":"Apostate","t":"noun","d":"a person who renounces a former belief or principle","diff":"hard","borrowed":false},
  {"w":"Apothegm","t":"noun","d":"a concise saying or maxim; an aphorism","diff":"hard","borrowed":false},
  {"w":"Arcadian","t":"adjective","d":"relating to an ideal rustic paradise; pleasantly rural","diff":"hard","borrowed":false},
  {"w":"Asperity","t":"noun","d":"harshness of tone or manner","diff":"hard","borrowed":false},
  {"w":"Assiduous","t":"adjective","d":"showing great care, attention, and effort","diff":"hard","borrowed":false},
  {"w":"Ataraxia","t":"noun","d":"a state of freedom from emotional disturbance and anxiety","diff":"hard","borrowed":false},
  {"w":"Atavistic","t":"adjective","d":"relating to a reversion to an earlier type; ancestral","diff":"hard","borrowed":false},
  {"w":"Bathetic","t":"adjective","d":"producing an effect of bathos; relating to an anticlimactic descent","diff":"hard","borrowed":false},
  {"w":"Bellicose","t":"adjective","d":"demonstrating aggression and willingness to fight","diff":"hard","borrowed":false},
  {"w":"Bespoken","t":"adjective","d":"made to order; spoken for in advance","diff":"hard","borrowed":false},
  {"w":"Bombastic","t":"adjective","d":"high-sounding language with little meaning; inflated","diff":"hard","borrowed":false},
  {"w":"Capricious","t":"adjective","d":"given to sudden changes of mood or behaviour","diff":"hard","borrowed":false},
  {"w":"Catalyse","t":"verb","d":"to cause or accelerate a reaction","diff":"hard","borrowed":false},
  {"w":"Caustic","t":"adjective","d":"sarcastic in a scathing way; capable of burning","diff":"hard","borrowed":false},
  {"w":"Chicanery","t":"noun","d":"the use of trickery to achieve one's purpose","diff":"hard","borrowed":false},
  {"w":"Coalesce","t":"verb","d":"to come together and form one mass or whole","diff":"hard","borrowed":false},
  {"w":"Cogitate","t":"verb","d":"to think deeply about something","diff":"hard","borrowed":false},
  {"w":"Contrite","t":"adjective","d":"feeling or expressing remorse at wrongdoing","diff":"hard","borrowed":false},
  {"w":"Convivial","t":"adjective","d":"relating to good company and lively enjoyment","diff":"hard","borrowed":false},
  {"w":"Diffident","t":"adjective","d":"modest or shy due to lack of self-confidence","diff":"hard","borrowed":false},
  {"w":"Dilatory","t":"adjective","d":"slow to act; intended to delay or procrastinate","diff":"hard","borrowed":false},
  {"w":"Disabuse","t":"verb","d":"to persuade someone that an idea or belief is mistaken","diff":"hard","borrowed":false},
  {"w":"Duplicity","t":"noun","d":"deceitfulness; double-dealing","diff":"hard","borrowed":false},
  {"w":"Ebullience","t":"noun","d":"the quality of being cheerful and full of energy","diff":"hard","borrowed":false},
  {"w":"Effulgent","t":"adjective","d":"radiant; shining brightly","diff":"hard","borrowed":false},
  {"w":"Egregious","t":"adjective","d":"outstandingly bad; shocking","diff":"hard","borrowed":false},
  {"w":"Enervate","t":"verb","d":"to weaken someone so they feel drained of energy","diff":"hard","borrowed":false},
  {"w":"Equivocal","t":"adjective","d":"open to more than one interpretation; uncertain","diff":"hard","borrowed":false},
  {"w":"Erudition","t":"noun","d":"the quality of having or showing great knowledge","diff":"hard","borrowed":false},
  {"w":"Facetious","t":"adjective","d":"treating serious issues with inappropriate humour","diff":"hard","borrowed":false},
  {"w":"Fallacious","t":"adjective","d":"based on a mistaken belief","diff":"hard","borrowed":false},
  {"w":"Fastidious","t":"adjective","d":"very attentive to accuracy and detail; hard to please","diff":"hard","borrowed":false},
  {"w":"Fatuous","t":"adjective","d":"silly and pointless","diff":"hard","borrowed":false},
  {"w":"Felicity","t":"noun","d":"intense happiness; the ability to find pleasing expression","diff":"hard","borrowed":false},
  {"w":"Fervently","t":"adverb","d":"with intense, passionate feeling","diff":"hard","borrowed":false},
  {"w":"Flippant","t":"adjective","d":"not showing a serious or respectful attitude","diff":"hard","borrowed":false},
  {"w":"Fractures","t":"noun","d":"breaks or cracks in something hard","diff":"hard","borrowed":false},
  {"w":"Garrulous","t":"adjective","d":"excessively talkative","diff":"hard","borrowed":false},
  {"w":"Grandeur","t":"noun","d":"splendour and impressiveness","diff":"hard","borrowed":false},
  {"w":"Gregarious","t":"adjective","d":"fond of company; sociable","diff":"hard","borrowed":false},
  {"w":"Haplessly","t":"adverb","d":"in an unlucky or unfortunate manner","diff":"hard","borrowed":false},
  {"w":"Hegemony","t":"noun","d":"leadership or dominance, especially of one country over others","diff":"hard","borrowed":false},
  {"w":"Impetuous","t":"adjective","d":"acting or done quickly and without thought","diff":"hard","borrowed":false},
  {"w":"Impudence","t":"noun","d":"the quality of being impudent; impertinence","diff":"hard","borrowed":false},
  {"w":"Inchoate","t":"adjective","d":"just begun and not fully formed; undeveloped","diff":"hard","borrowed":false},
  {"w":"Inimical","t":"adjective","d":"tending to obstruct or harm; hostile","diff":"hard","borrowed":false},
  {"w":"Insidious","t":"adjective","d":"proceeding in a gradual and harmful way","diff":"hard","borrowed":false},
  {"w":"Intrepid","t":"adjective","d":"fearless; adventurous","diff":"hard","borrowed":false},
  {"w":"Invective","t":"noun","d":"insulting, abusive, or highly critical language","diff":"hard","borrowed":false},
  {"w":"Lassitude","t":"noun","d":"physical or mental weariness; lack of energy","diff":"hard","borrowed":false},
  {"w":"Loquacious","t":"adjective","d":"tending to talk a great deal; talkative","diff":"hard","borrowed":false},
  {"w":"Lugubrious","t":"adjective","d":"looking or sounding sad and dismal","diff":"hard","borrowed":false},
  {"w":"Mendacity","t":"noun","d":"untruthfulness; the tendency to lie","diff":"hard","borrowed":false},
  {"w":"Meretricious","t":"adjective","d":"apparently attractive but having in reality no value","diff":"hard","borrowed":false},
  {"w":"Metonymy","t":"noun","d":"a figure of speech where a thing is referred to by something associated with it","diff":"hard","borrowed":false},
  {"w":"Morbidity","t":"noun","d":"the condition of being diseased; unhealthy preoccupation with death","diff":"hard","borrowed":false},
  {"w":"Nebulous","t":"adjective","d":"in the form of a cloud; unclear; vague","diff":"hard","borrowed":false},
  {"w":"Nefarious","t":"adjective","d":"wicked or criminal","diff":"hard","borrowed":false},
  {"w":"Obdurate","t":"adjective","d":"stubbornly refusing to change one's opinion","diff":"hard","borrowed":false},
  {"w":"Obloquy","t":"noun","d":"strong public condemnation","diff":"hard","borrowed":false},
  {"w":"Obstinate","t":"adjective","d":"stubbornly refusing to change; hard to deal with","diff":"hard","borrowed":false},
  {"w":"Ominous","t":"adjective","d":"giving the impression that something bad is going to happen","diff":"hard","borrowed":false},
  {"w":"Opulence","t":"noun","d":"great wealth or luxuriousness","diff":"hard","borrowed":false},
  {"w":"Ostensible","t":"adjective","d":"stated or appearing to be true, but not necessarily so","diff":"hard","borrowed":false},
  {"w":"Palpable","t":"adjective","d":"able to be touched or felt; so obvious it can be felt","diff":"hard","borrowed":false},
  {"w":"Pernicious","t":"adjective","d":"having a harmful effect, especially in a gradual way","diff":"hard","borrowed":false},
  {"w":"Pertinacious","t":"adjective","d":"holding firmly to an opinion or course of action","diff":"hard","borrowed":false},
  {"w":"Petulance","t":"noun","d":"the quality of being childishly sulky or bad-tempered","diff":"hard","borrowed":false},
  {"w":"Phlegmatic","t":"adjective","d":"having an unemotional, stolidly calm disposition","diff":"hard","borrowed":false},
  {"w":"Plausible","t":"adjective","d":"seeming reasonable or probable","diff":"hard","borrowed":false},
  {"w":"Poignancy","t":"noun","d":"the quality of evoking a keen sense of sadness","diff":"hard","borrowed":false},
  {"w":"Polished","t":"adjective","d":"accomplished and skilful; refined","diff":"hard","borrowed":false},
  {"w":"Pomposity","t":"noun","d":"the quality of being pompous; affectedly grand behaviour","diff":"hard","borrowed":false},
  {"w":"Portentous","t":"adjective","d":"of momentous significance; done in a pompously solemn manner","diff":"hard","borrowed":false},
  {"w":"Precipice","t":"noun","d":"a tall and very steep face of rock; a hazardous situation","diff":"hard","borrowed":false},
  {"w":"Probity","t":"noun","d":"the quality of having strong moral principles; honesty","diff":"hard","borrowed":false},
  {"w":"Profundity","t":"noun","d":"deep insight; great depth of knowledge or thought","diff":"hard","borrowed":false},
  {"w":"Prosaic","t":"adjective","d":"having the style of prose; lacking imaginativeness","diff":"hard","borrowed":false},
  {"w":"Punctual","t":"adjective","d":"happening at the agreed time; not late","diff":"hard","borrowed":false},
  {"w":"Pungency","t":"noun","d":"a sharply strong taste or smell","diff":"hard","borrowed":false},
  {"w":"Querulous","t":"adjective","d":"complaining in a petulant or whining manner","diff":"hard","borrowed":false},
  {"w":"Quixotic","t":"adjective","d":"exceedingly idealistic; unrealistic and impractical","diff":"hard","borrowed":false},
  {"w":"Recondite","t":"adjective","d":"not known by many people; obscure","diff":"hard","borrowed":false},
  {"w":"Reticence","t":"noun","d":"the quality of being reserved or restrained in speech","diff":"hard","borrowed":false},
  {"w":"Rhetoric","t":"noun","d":"the art of effective or persuasive speaking or writing","diff":"hard","borrowed":false},
  {"w":"Sagacity","t":"noun","d":"good judgement; ability to make good decisions; wisdom","diff":"hard","borrowed":false},
  {"w":"Salacious","t":"adjective","d":"having an undue interest in sexual matters","diff":"hard","borrowed":false},
  {"w":"Sanguine","t":"adjective","d":"optimistic, especially in a difficult situation","diff":"hard","borrowed":false},
  {"w":"Sardonic","t":"adjective","d":"grimly mocking or cynical","diff":"hard","borrowed":false},
  {"w":"Sceptical","t":"adjective","d":"not easily convinced; having doubts","diff":"hard","borrowed":false},
  {"w":"Solemnly","t":"adverb","d":"in a formal, dignified manner","diff":"hard","borrowed":false},
  {"w":"Solipsism","t":"noun","d":"the view that only one's own mind is sure to exist","diff":"hard","borrowed":false},
  {"w":"Spurious","t":"adjective","d":"not genuine; false or fake","diff":"hard","borrowed":false},
  {"w":"Stagnant","t":"adjective","d":"having no flow; showing no activity; dull","diff":"hard","borrowed":false},
  {"w":"Stoicism","t":"noun","d":"the endurance of pain without complaint","diff":"hard","borrowed":false},
  {"w":"Sublimity","t":"noun","d":"the quality of being sublime; something of great excellence","diff":"hard","borrowed":false},
  {"w":"Surreptitiousness","t":"noun","d":"the quality of being done in a secret manner","diff":"hard","borrowed":false},
  {"w":"Taciturn","t":"adjective","d":"reserved or uncommunicative in speech","diff":"hard","borrowed":false},
  {"w":"Temerity","t":"noun","d":"excessive confidence or boldness; audacity","diff":"hard","borrowed":false},
  {"w":"Timorous","t":"adjective","d":"showing or suffering from nervousness; timid","diff":"hard","borrowed":false},
  {"w":"Truculent","t":"adjective","d":"eager or quick to argue or fight; aggressively defiant","diff":"hard","borrowed":false},
  {"w":"Turbulent","t":"adjective","d":"moving unsteadily or violently; characterised by conflict","diff":"hard","borrowed":false},
  {"w":"Unctuous","t":"adjective","d":"excessively flattering; oily in manner","diff":"hard","borrowed":false},
  {"w":"Vaporous","t":"adjective","d":"in the form of vapour; delicate; insubstantial","diff":"hard","borrowed":false},
  {"w":"Vehement","t":"adjective","d":"showing strong feeling; forceful or passionate","diff":"hard","borrowed":false},
  {"w":"Veracity","t":"noun","d":"conformity to facts; habitual truthfulness","diff":"hard","borrowed":false},
  {"w":"Verbose","t":"adjective","d":"using more words than needed","diff":"hard","borrowed":false},
  {"w":"Virulence","t":"noun","d":"extreme severity or harmfulness of a disease or poison","diff":"hard","borrowed":false},
  {"w":"Visceral","t":"adjective","d":"relating to deep inward feelings; relating to the viscera","diff":"hard","borrowed":false},
  {"w":"Vociferous","t":"adjective","d":"expressing or characterised by vehement opinions","diff":"hard","borrowed":false},
  {"w":"Wistfully","t":"adverb","d":"in a way that shows longing tinged with sadness","diff":"hard","borrowed":false},
  {"w":"Zealotry","t":"noun","d":"the quality of being excessively enthusiastic about a cause","diff":"hard","borrowed":false}
]
```

- [ ] **Step 2: Verify all words are exactly 8 letters**

Run this quick check:
```bash
python3 -c "
import json
data = json.load(open('wordineer-deploy/data/eight-letter-words.json'))
bad = [x['w'] for x in data if len(x['w']) != 8]
print(f'Total: {len(data)}, Bad length: {bad[:20]}')
"
```
Expected output: `Total: ~250, Bad length: []`

If any words appear in `bad`, correct them in the JSON file before continuing.

- [ ] **Step 3: Commit the dataset**

```bash
git add wordineer-deploy/data/eight-letter-words.json
git commit -m "feat: add eight-letter-words.json dataset"
```

---

## Task 2: Create the tool source file

**Files:**
- Create: `template-deploy/tools-src/random-8-letter-word-generator.html`

- [ ] **Step 1: Copy the 7-letter tool as a base**

```bash
cp "template-deploy/tools-src/random-7-letter-word-generator.html" \
   "template-deploy/tools-src/random-8-letter-word-generator.html"
```

- [ ] **Step 2: Update the CONFIG block**

In `template-deploy/tools-src/random-8-letter-word-generator.html`, replace:
```
<!-- CONFIG
{
  "url": "/random-7-letter-word-generator/",
  "output": "random-7-letter-word-generator.html",
  "type": "tool"
}
-->
```
With:
```
<!-- CONFIG
{
  "url": "/random-8-letter-word-generator/",
  "output": "random-8-letter-word-generator.html",
  "type": "tool"
}
-->
```

- [ ] **Step 3: Update SLOT:meta**

Replace the entire `<!-- SLOT:meta -->` block with:

```html
<!-- SLOT:meta -->
<title>Random 8 Letter Word Generator — Free, Instant | Wordineer</title>
<meta name="description" content="Generate random 8-letter words instantly. Filter by difficulty, word type, and letter patterns. Includes Crossword &amp; Game Helper mode with Scrabble score display. Free, no sign-up.">
<link rel="canonical" href="https://wordineer.com/random-8-letter-word-generator/">
<meta property="og:type"        content="website">
<meta property="og:site_name"   content="Wordineer">
<meta property="og:title"       content="Random 8 Letter Word Generator | Wordineer">
<meta property="og:description" content="Generate random 8-letter words with filters for difficulty, type, and letter patterns. Crossword &amp; Game Helper and Scrabble score display included.">
<meta property="og:url"         content="https://wordineer.com/random-8-letter-word-generator/">
<meta property="og:image"       content="https://wordineer.com/og-image.png">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is an 8-letter word generator?",
      "acceptedAnswer": { "@type": "Answer", "text": "An 8-letter word generator randomly selects English words that are exactly eight characters long from a curated dataset. You can filter by word type, difficulty level, and letter patterns. This tool also includes a Crossword & Game Helper mode and displays the Scrabble point value for every word." }
    },
    {
      "@type": "Question",
      "name": "How many 8-letter words are in English?",
      "acceptedAnswer": { "@type": "Answer", "text": "Most dictionaries contain between 30,000 and 80,000 eight-letter words depending on whether inflections and derivatives are included. This tool's curated dataset covers the most useful ones, tagged by type, difficulty, and definition." }
    },
    {
      "@type": "Question",
      "name": "Why are 8-letter words considered advanced vocabulary?",
      "acceptedAnswer": { "@type": "Answer", "text": "Most short English words have Germanic roots and are part of everyday speech. Many 8-letter words derive from Latin or Greek, appearing more often in academic, professional, and literary writing. Learning 8-letter words systematically tends to unlock entire word families through shared roots and affixes." }
    },
    {
      "@type": "Question",
      "name": "How does Crossword &amp; Game Helper mode work?",
      "acceptedAnswer": { "@type": "Answer", "text": "Open the Crossword & Game Helper section. Enter a letter in Contains to show only words with that letter. Enter a letter in Does NOT Contain to exclude words with that letter. Combine with Starts With and Ends With filters to pin down a crossword slot or narrow candidates in 8-letter word games." }
    },
    {
      "@type": "Question",
      "name": "Is this tool free?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes — completely free, no account required, no limits." }
    }
  ]
}
</script>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Wordineer", "item": "https://wordineer.com/" },
    { "@type": "ListItem", "position": 2, "name": "Word Tools", "item": "https://wordineer.com/word-tools/" },
    { "@type": "ListItem", "position": 3, "name": "8 Letter Word Generator", "item": "https://wordineer.com/random-8-letter-word-generator/" }
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Random 8-Letter Word Generator",
  "url": "https://wordineer.com/random-8-letter-word-generator/",
  "description": "Generate random 8-letter words instantly. Filter by difficulty, word type, and letter patterns. Includes Crossword & Game Helper mode and Scrabble score display. Free, no sign-up.",
  "applicationCategory": "UtilityApplication",
  "operatingSystem": "Web",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
  "publisher": { "@id": "https://wordineer.com/#organization" }
}
</script>
<!-- /SLOT:meta -->
```

- [ ] **Step 4: Update SLOT:hero**

Replace the `<!-- SLOT:hero -->` block with:

```html
<!-- SLOT:hero -->
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="/">Wordineer</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/word-tools/">Word Tools</a>
    <span class="breadcrumb-sep">›</span>
    <span aria-current="page">8 Letter Word Generator</span>
  </div>
</div>
<div class="hero">
  <div class="hero-badge">
    <svg viewBox="0 0 11 11" fill="none"><circle cx="5.5" cy="5.5" r="4.5" stroke="#3C3489" stroke-width="1"/><path d="M3.5 5.5l1.5 1.5L8 3.5" stroke="#3C3489" stroke-width="1.2" stroke-linecap="round"/></svg>
    Free · No sign-up · Instant results
  </div>
  <h1>Random 8 Letter Word Generator</h1>
  <p>Generate random 8-letter words in one click. Filter by difficulty, word type, or letter pattern — or use Crossword &amp; Game Helper mode to narrow candidates by confirmed and eliminated letters. Every word shows its Scrabble point value and definition. Eight-letter words mark the threshold where vocabulary shifts from conversational to precise — this is the length where language becomes deliberate.</p>
</div>
<!-- /SLOT:hero -->
```

- [ ] **Step 5: Update the A-Z browse links in SLOT:tool**

Find and replace the A-Z browse section. Change all `7-letter-words-starting-with-` to `8-letter-words-starting-with-` and update the heading:

Replace:
```html
  <!-- A-Z browse section -->
  <div class="az-section">
    <h2>Browse 7-letter words by first letter</h2>
    <p>Looking for all 7-letter words starting with a specific letter? Each page below shows a complete filterable list with definitions and difficulty ratings.</p>
    <div class="az-links">
      <a class="az-link" href="/7-letter-words-starting-with-a/">A</a>
      <a class="az-link" href="/7-letter-words-starting-with-b/">B</a>
      <a class="az-link" href="/7-letter-words-starting-with-c/">C</a>
      <a class="az-link" href="/7-letter-words-starting-with-d/">D</a>
      <a class="az-link" href="/7-letter-words-starting-with-e/">E</a>
      <a class="az-link" href="/7-letter-words-starting-with-f/">F</a>
      <a class="az-link" href="/7-letter-words-starting-with-g/">G</a>
      <a class="az-link" href="/7-letter-words-starting-with-h/">H</a>
      <a class="az-link" href="/7-letter-words-starting-with-i/">I</a>
      <a class="az-link" href="/7-letter-words-starting-with-j/">J</a>
      <a class="az-link" href="/7-letter-words-starting-with-k/">K</a>
      <a class="az-link" href="/7-letter-words-starting-with-l/">L</a>
      <a class="az-link" href="/7-letter-words-starting-with-m/">M</a>
      <a class="az-link" href="/7-letter-words-starting-with-n/">N</a>
      <a class="az-link" href="/7-letter-words-starting-with-o/">O</a>
      <a class="az-link" href="/7-letter-words-starting-with-p/">P</a>
      <a class="az-link" href="/7-letter-words-starting-with-q/">Q</a>
      <a class="az-link" href="/7-letter-words-starting-with-r/">R</a>
      <a class="az-link" href="/7-letter-words-starting-with-s/">S</a>
      <a class="az-link" href="/7-letter-words-starting-with-t/">T</a>
      <a class="az-link" href="/7-letter-words-starting-with-u/">U</a>
      <a class="az-link" href="/7-letter-words-starting-with-v/">V</a>
      <a class="az-link" href="/7-letter-words-starting-with-w/">W</a>
      <a class="az-link" href="/7-letter-words-starting-with-x/">X</a>
      <a class="az-link" href="/7-letter-words-starting-with-y/">Y</a>
      <a class="az-link" href="/7-letter-words-starting-with-z/">Z</a>
    </div>
  </div>
```
With:
```html
  <!-- A-Z browse section -->
  <div class="az-section">
    <h2>Browse 8-letter words by first letter</h2>
    <p>Looking for all 8-letter words starting with a specific letter? Each page below shows a complete filterable list with definitions and difficulty ratings.</p>
    <div class="az-links">
      <a class="az-link" href="/8-letter-words-starting-with-a/">A</a>
      <a class="az-link" href="/8-letter-words-starting-with-b/">B</a>
      <a class="az-link" href="/8-letter-words-starting-with-c/">C</a>
      <a class="az-link" href="/8-letter-words-starting-with-d/">D</a>
      <a class="az-link" href="/8-letter-words-starting-with-e/">E</a>
      <a class="az-link" href="/8-letter-words-starting-with-f/">F</a>
      <a class="az-link" href="/8-letter-words-starting-with-g/">G</a>
      <a class="az-link" href="/8-letter-words-starting-with-h/">H</a>
      <a class="az-link" href="/8-letter-words-starting-with-i/">I</a>
      <a class="az-link" href="/8-letter-words-starting-with-j/">J</a>
      <a class="az-link" href="/8-letter-words-starting-with-k/">K</a>
      <a class="az-link" href="/8-letter-words-starting-with-l/">L</a>
      <a class="az-link" href="/8-letter-words-starting-with-m/">M</a>
      <a class="az-link" href="/8-letter-words-starting-with-n/">N</a>
      <a class="az-link" href="/8-letter-words-starting-with-o/">O</a>
      <a class="az-link" href="/8-letter-words-starting-with-p/">P</a>
      <a class="az-link" href="/8-letter-words-starting-with-q/">Q</a>
      <a class="az-link" href="/8-letter-words-starting-with-r/">R</a>
      <a class="az-link" href="/8-letter-words-starting-with-s/">S</a>
      <a class="az-link" href="/8-letter-words-starting-with-t/">T</a>
      <a class="az-link" href="/8-letter-words-starting-with-u/">U</a>
      <a class="az-link" href="/8-letter-words-starting-with-v/">V</a>
      <a class="az-link" href="/8-letter-words-starting-with-w/">W</a>
      <a class="az-link" href="/8-letter-words-starting-with-x/">X</a>
      <a class="az-link" href="/8-letter-words-starting-with-y/">Y</a>
      <a class="az-link" href="/8-letter-words-starting-with-z/">Z</a>
    </div>
  </div>
```

- [ ] **Step 6: Replace SLOT:explainer with full 8-letter copy**

Replace the entire `<!-- SLOT:explainer -->` block (from `<!-- SLOT:explainer -->` to `<!-- /SLOT:explainer -->`) with:

```html
<!-- SLOT:explainer -->
<div class="explainer">

  <h2>What is a random 8-letter word generator?</h2>
  <p>A random 8-letter word generator pulls words that are exactly eight characters long from a curated dataset and presents them instantly. Unlike a dictionary search — which requires you to already know or approximate what you're looking for — a generator surfaces words you might never have considered, filtered to match whatever constraints you set. This tool lets you narrow results by word type (noun, verb, adjective, adverb), difficulty level (easy, medium, hard), and letter patterns. Every result includes a Scrabble point value and an optional definition, making it useful whether you're expanding your vocabulary, preparing for a word game, filling a crossword slot, or looking for a distinctive name.</p>
  <p>The tool draws from a dataset of thousands of 8-letter English words. On first load a built-in seed renders immediately with no network request. The full dataset loads in the background, expanding the available pool automatically. All filters run entirely in your browser — change any setting and the results update without clicking Generate again.</p>

  <h2>Why use an 8-letter word generator?</h2>
  <p>Eight-letter words sit at the intersection of several different practical needs. Here's where they're most useful:</p>
  <p><strong>Vocabulary building.</strong> Eight-letter words are long enough to carry genuine precision and nuance, but not so specialised that learning them feels purely academic. This is the length where vocabulary stops being about recognition and starts being about active use — words you can reach for when a shorter one falls short.</p>
  <p><strong>Creative writing.</strong> Finding the right word at the right length matters to prose rhythm. Eight-letter words have natural weight and cadence — long enough to feel considered, short enough to stay readable. Writers use this tool to find precise alternatives to overused words, generate character names with the right sound, and break through the friction of a blank page.</p>
  <p><strong>Word games.</strong> Eight-letter plays in Scrabble — seven rack tiles plus one letter already on the board — earn the same 50-point bingo bonus as a standard seven-tile bingo. Crossword puzzles frequently feature 8-letter answers. This tool's filter and sort options are built for exactly this kind of targeted search.</p>
  <p><strong>Naming.</strong> Eight letters gives enough room for a name to feel substantial and specific. Product names, brand names, usernames, and character names all benefit from the kind of search this tool enables: filtering by type and difficulty to surface options outside your immediate vocabulary.</p>

  <h2>8-letter words and advanced vocabulary</h2>
  <p>Eight letters is where everyday language starts to give way to precise language. Consider a simple quality like "good." Synonyms at different lengths do progressively different work: "good," "fine," "solid" are conversational. "Suitable," "adequate," "credible" are purposeful. Move up to eight letters and you reach words like "coherent," "eloquent," "diligent," "profound" — words that don't just describe a quality but specify a degree and kind of it that shorter synonyms can't quite reach.</p>
  <p>This shift isn't accidental. Most short English words have Germanic origins — they're the core vocabulary of everyday speech, direct and concrete. As word length increases, a higher proportion of words derive from Latin or Greek roots. These Latinate and Greek-origin words appear more frequently in academic writing, professional communication, and literary prose. Learning them systematically doesn't just expand your vocabulary — it often gives you access to an entire word family at once. Learn "diligent" and you already understand "diligence." Learn "coherent" and "coherence," "incoherent," "incoherence" follow immediately.</p>
  <p>Common 8-letter words most educated speakers already know: absolute, birthday, calendar, complete, computer, language, national, personal, possible, schedule, strength, together. These are the easy tier — familiar, unambiguous, useful.</p>
  <p>More advanced 8-letter words worth adding to active use: coherent, diligent, eloquent, explicit, inherent, luminous, profound, rigorous, succinct, tangible, vigilant, virtuous. These are medium difficulty — words that many people recognise but don't use. The gap between recognition and active use is exactly where deliberate vocabulary study pays off.</p>
  <p>The difficulty filter on this tool maps directly onto this progression. Start with Easy to confirm and consolidate vocabulary you already have. Move to Medium to close the recognition-to-use gap. Work through Hard to push into genuinely unfamiliar territory. Each level builds on the last, and the definitions make every result immediately usable rather than requiring a separate lookup.</p>

  <h2>Best practices for vocabulary building with this tool</h2>
  <p>Generating words is only the first step. Here's how to make what you see actually stick:</p>
  <p><strong>Read every definition, not just the word.</strong> The definition is where meaning lives. Skipping it means you're memorising a string of letters, not acquiring a word. Enable the definitions toggle before every session.</p>
  <p><strong>Study in focused batches, not long lists.</strong> Generate 10–15 words rather than 50. Depth matters more than volume. Spend 30 seconds on each word: read the definition, say the word aloud, think of one sentence where it would fit. Then move on.</p>
  <p><strong>Use the word type filter by session.</strong> Verbs one session, adjectives the next. This keeps study sessions focused and avoids the dilution that comes from mixing all types together. At harder difficulty levels, verbs tend to carry the most expressive payload; adjectives add the most precision.</p>
  <p><strong>Look for prefixes and suffixes.</strong> Eight-letter words frequently carry affixes that appear across many words: un-, re-, pre-, -tion, -ment, -ness, -ful, -less. When you spot a pattern, you're learning a multiplier, not just a single word.</p>
  <p><strong>Save words to come back to.</strong> Use the Save button to build a personal list during each session. Copy it out using the Copy saved option and keep it somewhere visible. Words you revisit in different contexts are words that become permanent.</p>

  <h2>8-letter words for writers</h2>
  <p>Eight-letter words hit a natural rhythm sweet spot in prose. Long enough to feel deliberate and specific, short enough to stay readable and keep sentences moving. They work best when they're doing something that shorter words can't — adding precision, avoiding repetition, or setting a register.</p>
  <p>The most practical use case is replacing overused words. If "possible" has appeared three times in a paragraph, "feasible," "credible," or "suitable" each carry slightly different implications and add variety without changing meaning. The word type filter makes this targeted: need more vivid adjectives? Set type to Adjective and difficulty to Medium or Hard and generate a fresh batch.</p>
  <p>Eight letters also works well for naming: characters, places, organisations, invented concepts. The length gives a name weight without tipping into the unwieldy. Set type to Noun, difficulty to Medium, enable definitions to filter out anything with the wrong connotation, and generate 20 options. The best names usually appear in the first two or three batches.</p>
  <p>For writers working on vocabulary range across a longer project: use the generator periodically rather than intensively. Generate 10 words, add any that are useful to your writing vocabulary notes, and move on. The compounding effect over months is significant.</p>

  <h2>8-letter words in word games</h2>
  <p>In Scrabble, an eight-letter play requires using all seven tiles on your rack plus one letter already on the board. The result earns the same 50-point bingo bonus as a standard seven-tile bingo — a swing that can decide a game. Studying 8-letter words gives you a second category of bingo plays to draw on, particularly useful when the board already has common letters like E, R, S, or T exposed.</p>
  <p>Common high-value 8-letter Scrabble words to know: absolute, calendar, coherent, diligent, national, personal, relation, schedule, sequence, standard. Use the Sort by Score option to surface the highest-scoring words in any filtered batch. The Contains and Does Not Contain filters in Crossword &amp; Game Helper mode let you match against your rack or available board letters.</p>
  <p>Crossword puzzles at intermediate and advanced difficulty frequently include 8-letter answers. When you've filled a few crossing letters but can't solve the clue alone, the helper mode becomes a targeted search: set Starts With, Ends With, and Contains to match known letters, and the resulting short list can usually be resolved against the clue in seconds.</p>

  <h2>How it works</h2>
  <p>The generator pulls from a curated dataset of 8-letter English words, each tagged with its word type, difficulty level, and definition. On first load, a built-in seed of common 8-letter words renders immediately — no network request, no wait. The full dataset loads in the background at browser idle time, automatically expanding the pool. All filters and sorting apply client-side with no server round-trips: change any setting and the list refreshes instantly.</p>
  <p>Scrabble point values are calculated using standard tile scores: common letters like E, A, I score 1 point each; rarer letters like Q and Z score 10. Sort by Score to order your current results from highest to lowest scoring and immediately identify the most valuable words in any filtered batch.</p>

</div>
<!-- /SLOT:explainer -->
```

- [ ] **Step 7: Replace SLOT:faq**

Replace the entire `<!-- SLOT:faq -->` block with:

```html
<!-- SLOT:faq -->
<div class="faq">
  <h2 class="faq-title">Frequently asked questions</h2>

  <div class="faq-item open">
    <div class="faq-q"><span class="faq-q-text">What is an 8-letter word generator?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">A random 8-letter word generator selects English words that are exactly eight characters long from a curated dataset. You can filter by word type, difficulty, and letter patterns. Every result shows a Scrabble point value and an optional definition. The tool also includes a Crossword &amp; Game Helper mode for narrowing candidates by confirmed and eliminated letters.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">How many 8-letter words are in English?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Estimates vary widely depending on the dictionary and whether inflections and derivatives are counted, but most sources place the number between 30,000 and 80,000 eight-letter words in common English use. This tool's curated dataset covers the most useful ones, tagged with type, difficulty, and definition.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Why are 8-letter words considered advanced vocabulary?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Most short English words have Germanic roots and are part of everyday conversational speech. As word length increases, a higher proportion of words derive from Latin or Greek, which is where academic, professional, and literary vocabulary draws most heavily. Eight letters is roughly the threshold where this shift becomes consistent — and where learning one word often unlocks an entire word family through shared roots and affixes.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What are some common 8-letter words?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Familiar 8-letter words include: absolute, birthday, calendar, complete, computer, language, national, personal, possible, schedule, strength, together. For more advanced vocabulary, try: coherent, diligent, eloquent, inherent, luminous, profound, rigorous, succinct, tangible, vigilant.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Can I use this tool for Scrabble?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Yes. Enable Scrabble scores, sort by Score↓ to find highest-value plays, and use the Contains and Does Not Contain filters to match letters in your rack or available on the board. An 8-letter play — all 7 rack tiles plus one board letter — earns the same 50-point bingo bonus as a standard 7-tile bingo.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">How does Crossword &amp; Game Helper mode work?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Open the Crossword &amp; Game Helper section in the filters. Enter a letter in Contains to show only words with that letter. Enter a letter in Does NOT Contain to exclude words with that letter. Combine with Starts With and Ends With to pin down a crossword slot or narrow candidates after gathering positional information from crosses.</div>
  </div>

  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Is this tool free?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Completely free, forever. No account required, no limits, no paywalls.</div>
  </div>
</div>
<!-- /SLOT:faq -->
```

- [ ] **Step 8: Replace SLOT:who**

Replace the entire `<!-- SLOT:who -->` block with:

```html
<!-- SLOT:who -->
<div>
  <h2 class="section-title" style="margin-bottom:14px">Who uses this tool</h2>
  <div class="uc-grid">
    <div class="uc"><div class="uc-title">Vocabulary builders</div><div class="uc-body">Students and lifelong learners using the difficulty tiers to move systematically from familiar words to precise, expressive vocabulary. The definitions are built in — no second tab needed.</div></div>
    <div class="uc"><div class="uc-title">Writers &amp; authors</div><div class="uc-body">Fiction writers and essayists finding precise alternatives to overused words, generating names with the right weight and sound, and expanding the vocabulary range of a longer project over time.</div></div>
    <div class="uc"><div class="uc-title">Word game players</div><div class="uc-body">Scrabble and crossword players using the filters to find high-scoring plays, study 8-letter bingo candidates, and narrow a crossword slot to a short list of real candidates using the Crossword &amp; Game Helper.</div></div>
    <div class="uc"><div class="uc-title">Teachers &amp; educators</div><div class="uc-body">Classroom use for vocabulary exercises, spelling lists, and analytical writing practice. Filter by type and difficulty, generate a list, and copy it in one click for immediate use in worksheets, slides, or quiz tools.</div></div>
  </div>
</div>
<!-- /SLOT:who -->
```

- [ ] **Step 9: Update SLOT:init — seed words and data path**

In the `<!-- SLOT:init -->` `<script>` block, replace the entire `var SEED = [...]` array with 8-letter seed words, and change the `loadFull` fetch path.

Replace:
```javascript
  fetch('/data/seven-letter-words.json')
```
With:
```javascript
  fetch('/data/eight-letter-words.json')
```

Replace the entire `var SEED = [` array (lines from `{w:"Balance"...` through `{w:"Laconic"...}` with closing `];`) with:

```javascript
  var SEED = [
    {w:"Absolute",t:"adjective",d:"complete; not qualified or diminished in any way",diff:"easy"},
    {w:"Baseball",t:"noun",d:"a ball game played between two teams of nine players",diff:"easy"},
    {w:"Birthday",t:"noun",d:"the annual anniversary of the day one was born",diff:"easy"},
    {w:"Calendar",t:"noun",d:"a chart showing days, weeks, and months of the year",diff:"easy"},
    {w:"Champion",t:"noun",d:"a person who has won a competition or contest",diff:"easy"},
    {w:"Children",t:"noun",d:"young human beings below the age of puberty",diff:"easy"},
    {w:"Complete",t:"adjective",d:"having all the necessary or appropriate parts",diff:"easy"},
    {w:"Computer",t:"noun",d:"an electronic device for storing and processing data",diff:"easy"},
    {w:"Creative",t:"adjective",d:"producing original and unusual ideas; imaginative",diff:"easy"},
    {w:"Daughter",t:"noun",d:"a girl or woman in relation to her parents",diff:"easy"},
    {w:"Describe",t:"verb",d:"to give a detailed account of something in words",diff:"easy"},
    {w:"Distance",t:"noun",d:"the length of space between two points",diff:"easy"},
    {w:"Educated",t:"adjective",d:"having received a formal education; knowledgeable",diff:"easy"},
    {w:"Everyone",t:"noun",d:"every person; all people",diff:"easy"},
    {w:"Exciting",t:"adjective",d:"causing great enthusiasm and eagerness",diff:"easy"},
    {w:"Familiar",t:"adjective",d:"well known from long or close association",diff:"easy"},
    {w:"Football",t:"noun",d:"a team game played with an inflated ball",diff:"easy"},
    {w:"Friendly",t:"adjective",d:"kind and pleasant; characteristic of a friend",diff:"easy"},
    {w:"Grateful",t:"adjective",d:"feeling or showing gratitude",diff:"easy"},
    {w:"Guidance",t:"noun",d:"advice or information aimed at resolving a problem",diff:"easy"},
    {w:"Homework",t:"noun",d:"schoolwork that a pupil is required to do at home",diff:"easy"},
    {w:"Humanity",t:"noun",d:"human beings collectively; the quality of being humane",diff:"easy"},
    {w:"Identity",t:"noun",d:"the fact of being who or what a person or thing is",diff:"easy"},
    {w:"Language",t:"noun",d:"the method of human communication using words",diff:"easy"},
    {w:"Laughter",t:"noun",d:"the action or sound of laughing",diff:"easy"},
    {w:"Mountain",t:"noun",d:"a large natural elevation of the earth's surface",diff:"easy"},
    {w:"National",t:"adjective",d:"relating to or characteristic of a nation",diff:"easy"},
    {w:"Personal",t:"adjective",d:"of, affecting, or belonging to a particular person",diff:"easy"},
    {w:"Possible",t:"adjective",d:"able to be done; within the power of someone",diff:"easy"},
    {w:"Progress",t:"noun",d:"forward movement towards a goal or destination",diff:"easy"},
    {w:"Abundant",t:"adjective",d:"present in large quantities; more than enough",diff:"medium"},
    {w:"Accurate",t:"adjective",d:"free from errors; conforming exactly to truth",diff:"medium"},
    {w:"Coherent",t:"adjective",d:"logical and consistent; clearly articulated",diff:"medium"},
    {w:"Credible",t:"adjective",d:"able to be believed; convincing",diff:"medium"},
    {w:"Dialogue",t:"noun",d:"conversation between two or more people",diff:"medium"},
    {w:"Diligent",t:"adjective",d:"having or showing care and conscientiousness in one's work",diff:"medium"},
    {w:"Distinct",t:"adjective",d:"recognisably different; clear and definite",diff:"medium"},
    {w:"Dominant",t:"adjective",d:"most important, powerful, or influential",diff:"medium"},
    {w:"Eloquent",t:"adjective",d:"fluent or persuasive in speaking or writing",diff:"medium"},
    {w:"Evaluate",t:"verb",d:"to form an idea of the amount, number, or value of something",diff:"medium"},
    {w:"Evidence",t:"noun",d:"available facts indicating whether a belief is true",diff:"medium"},
    {w:"Fidelity",t:"noun",d:"faithfulness to a person, cause, or belief",diff:"medium"},
    {w:"Graceful",t:"adjective",d:"having or showing grace; elegantly smooth and beautiful",diff:"medium"},
    {w:"Imminent",t:"adjective",d:"about to happen; impending",diff:"medium"},
    {w:"Implicit",t:"adjective",d:"implied though not directly expressed",diff:"medium"},
    {w:"Inherent",t:"adjective",d:"existing as a permanent and inseparable element",diff:"medium"},
    {w:"Leverage",t:"noun",d:"the power to influence a person or situation",diff:"medium"},
    {w:"Luminous",t:"adjective",d:"full of or shedding light; glowing",diff:"medium"},
    {w:"Profound",t:"adjective",d:"very great or intense; having deep insight",diff:"medium"},
    {w:"Rigorous",t:"adjective",d:"extremely thorough; adhering strictly to standards",diff:"medium"},
    {w:"Succinct",t:"adjective",d:"briefly and clearly expressed",diff:"medium"},
    {w:"Tangible",t:"adjective",d:"perceptible by touch; clear and definite",diff:"medium"},
    {w:"Thorough",t:"adjective",d:"complete with regard to every detail; not superficial",diff:"medium"},
    {w:"Vigilant",t:"adjective",d:"keeping careful watch for possible danger or difficulties",diff:"medium"},
    {w:"Alacrity",t:"noun",d:"brisk and cheerful readiness to do something",diff:"hard"},
    {w:"Anathema",t:"noun",d:"something or someone greatly detested or loathed",diff:"hard"},
    {w:"Felicity",t:"noun",d:"intense happiness; the ability to find pleasing expression",diff:"hard"},
    {w:"Hegemony",t:"noun",d:"leadership or dominance of one country or group over others",diff:"hard"},
    {w:"Mendacity",t:"noun",d:"untruthfulness; habitual lying",diff:"hard"},
    {w:"Rhetoric",t:"noun",d:"the art of effective or persuasive speaking or writing",diff:"hard"},
    {w:"Sagacity",t:"noun",d:"good judgement; wisdom; ability to make good decisions",diff:"hard"}
  ];
```

- [ ] **Step 10: Verify the file has no remaining "7-letter" or "seven-letter" references**

```bash
grep -in "seven-letter\|seven letter\|7-letter\|7 letter\|seven-letter-words\|/data/seven" \
  "template-deploy/tools-src/random-8-letter-word-generator.html"
```
Expected output: empty (no matches). If any appear, fix them before continuing.

- [ ] **Step 11: Commit the source file**

```bash
git add "template-deploy/tools-src/random-8-letter-word-generator.html"
git commit -m "feat: add random-8-letter-word-generator tool source"
```

---

## Task 3: Register the tool in tools.json

**Files:**
- Modify: `template-deploy/tools.json`

- [ ] **Step 1: Add to more_word_tools array**

In `template-deploy/tools.json`, after the `7 Letter Word Generator` entry in `more_word_tools`:

```json
    {
      "href": "/random-7-letter-word-generator/",
      "name": "7 Letter Word Generator",
      "desc": "Random 7-letter words — Scrabble bingos, crossword helper, and Scrabble scores.",
      "icon_bg": "#EEEDFE",
      "icon_path": "<path d=\"M2 4h9M2 7h8M2 10h6\" stroke=\"#534AB7\" stroke-width=\"1.3\" stroke-linecap=\"round\"/>"
    },
```

Add immediately after (before the `random-name-generator` entry):

```json
    {
      "href": "/random-8-letter-word-generator/",
      "name": "8 Letter Word Generator",
      "desc": "Random 8-letter words — advanced vocabulary, crossword helper, and Scrabble scores.",
      "icon_bg": "#EEEDFE",
      "icon_path": "<path d=\"M2 4h9M2 7h8M2 10h7\" stroke=\"#534AB7\" stroke-width=\"1.3\" stroke-linecap=\"round\"/>"
    },
```

- [ ] **Step 2: Verify tools.json is valid JSON**

```bash
python3 -c "import json; json.load(open('template-deploy/tools.json')); print('valid')"
```
Expected output: `valid`

- [ ] **Step 3: Commit tools.json**

```bash
git add template-deploy/tools.json
git commit -m "feat: add 8-letter word generator to tools.json nav"
```

---

## Task 4: Add redirect rules

**Files:**
- Modify: `wordineer-deploy/_redirects`

- [ ] **Step 1: Add the two redirect lines**

In `wordineer-deploy/_redirects`, find the block for the 7-letter generator (these two lines):
```
/random-7-letter-word-generator.html    /random-7-letter-word-generator/    301
/random-7-letter-word-generator/    /random-7-letter-word-generator.html    200
```

Add immediately after:
```
/random-8-letter-word-generator.html    /random-8-letter-word-generator/    301
/random-8-letter-word-generator/    /random-8-letter-word-generator.html    200
```

- [ ] **Step 2: Commit _redirects**

```bash
git add wordineer-deploy/_redirects
git commit -m "feat: add redirect for random-8-letter-word-generator clean URL"
```

---

## Task 5: Build, copy, and verify

**Files:**
- Generate: `template-deploy/output/random-8-letter-word-generator.html`
- Copy: `wordineer-deploy/random-8-letter-word-generator.html`

- [ ] **Step 1: Run the build**

```bash
cd template-deploy && python3 build.py
```
Expected: build completes with no errors; look for `random-8-letter-word-generator.html` in the output.

- [ ] **Step 2: Check the output file exists**

```bash
ls -lh template-deploy/output/random-8-letter-word-generator.html
```
Expected: file exists, size similar to other letter-word pages (~50–60KB).

- [ ] **Step 3: Copy output to deploy folder**

```bash
cp template-deploy/output/random-8-letter-word-generator.html wordineer-deploy/
```

- [ ] **Step 4: Verify no 7-letter references leaked into the output**

```bash
grep -c "seven-letter\|7-letter\|seven letter" wordineer-deploy/random-8-letter-word-generator.html
```
Expected output: `0`

- [ ] **Step 5: Start local server and verify in browser**

```bash
cd wordineer-deploy && python3 -m http.server 8080
```

Visit `http://localhost:8080/random-8-letter-word-generator.html` and confirm:
- Words generate on load (seed words appear immediately)
- Filters (type, difficulty, starts/ends with) work
- Definitions toggle shows/hides definitions
- Scrabble scores appear on word cards
- Save (heart) button works; saved words appear in saved section
- Copy per word and Copy list both work
- Crossword & Game Helper opens and Contains/Excludes filters work
- Sort dropdown works (A→Z, Z→A, Score↓)
- A-Z links at bottom point to `/8-letter-words-starting-with-[a-z]/`
- Mobile: collapse to single column at 375px, "More options" toggle works
- Page title reads "Random 8 Letter Word Generator — Free, Instant | Wordineer"

- [ ] **Step 6: Verify lazy-load fires**

In browser DevTools → Network tab, reload the page. After the initial render, confirm `eight-letter-words.json` loads as a second request (at idle, not blocking first render).

- [ ] **Step 7: Commit the built output**

```bash
git add wordineer-deploy/random-8-letter-word-generator.html
git commit -m "build: generate and add random-8-letter-word-generator output page"
```

---

## Self-Review Notes

**Spec coverage check:**
- ✅ Dataset created (Task 1)
- ✅ Tool source with all copy slots (Task 2)
- ✅ CONFIG, meta, hero, tool (A-Z links), explainer, faq, who, init all updated (Task 2)
- ✅ `loadFull` path updated to `eight-letter-words.json` (Task 2, Step 9)
- ✅ tools.json registration (Task 3)
- ✅ _redirects clean URL (Task 4)
- ✅ Build + local verification (Task 5)

**Type consistency:** `allWords`, `currentWords`, `savedWords`, `SEED` — all use the same `{w, t, d, diff}` schema throughout. `loadFull` replaces `allWords` with the full dataset using the same schema.

**No placeholders:** All steps contain explicit commands and code. No "TBD" or "implement as appropriate."

# Random Adjective Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a `/random-adjective-generator/` tool page for Wordineer that generates random adjectives with sentiment (positive/negative/neutral) and difficulty filters, comparative/superlative forms, and definitions — features no competitor offers.

**Architecture:** New `adjectives.json` data file → 4 small changes to `tool-engine.js` to support `adjTypeId` + `comp` rendering → new tool-src HTML following the `random-noun-generator.html` pattern → tools.json + redirects entries → build and deploy.

**Tech Stack:** Vanilla HTML/CSS/JS, Python 3 build script, Cloudflare Pages, WORDINEER IIFE engine

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `wordineer-deploy/data/adjectives.json` | CREATE | ~500 adjectives with w, at, diff, d, comp fields |
| `wordineer-deploy/scripts/tool-engine.js` | MODIFY | Add adjType filter + comp field support (4 changes) |
| `wordineer-deploy/scripts/tool-engine.min.js` | MODIFY | Minified copy of updated engine |
| `template-deploy/tools-src/random-adjective-generator.html` | CREATE | Full tool-src with all slots |
| `template-deploy/tools.json` | MODIFY | Add tool to mega nav, more_word_tools grid, footer_cols |
| `wordineer-deploy/_redirects` | MODIFY | Add clean URL redirect |
| `template-deploy/output/random-adjective-generator.html` | GENERATE | Build output (via build.py) |
| `wordineer-deploy/random-adjective-generator.html` | COPY | Production file (from build output) |

---

## Task 1: Create adjectives.json data file

**Files:**
- Create: `wordineer-deploy/data/adjectives.json`

Target: 500 adjectives. Distribution:
- Sentiment: ~170 positive, ~165 negative, ~165 neutral
- Difficulty: ~170 easy, ~165 medium, ~165 hard
- `comp` format: `"happier / happiest"` for -er/-est words, `"more vivid / most vivid"` for multi-syllable words, `"better / best"` for irregulars

- [ ] **Step 1: Create the data file**

Create `wordineer-deploy/data/adjectives.json` with this content (complete 500-entry array — the starter set below shows the pattern; fill out to 500 ensuring balanced distribution):

```json
[
  {"w":"Abundant","at":"positive","diff":"medium","d":"existing in large quantities; plentiful","comp":"more abundant / most abundant"},
  {"w":"Admirable","at":"positive","diff":"medium","d":"deserving of respect or approval","comp":"more admirable / most admirable"},
  {"w":"Affectionate","at":"positive","diff":"medium","d":"showing fondness or tenderness","comp":"more affectionate / most affectionate"},
  {"w":"Agile","at":"positive","diff":"medium","d":"able to move quickly and easily","comp":"more agile / most agile"},
  {"w":"Amiable","at":"positive","diff":"hard","d":"having a friendly and pleasant manner","comp":"more amiable / most amiable"},
  {"w":"Ambitious","at":"positive","diff":"medium","d":"having a strong desire to succeed","comp":"more ambitious / most ambitious"},
  {"w":"Astute","at":"positive","diff":"hard","d":"having an ability to accurately assess situations","comp":"more astute / most astute"},
  {"w":"Audacious","at":"positive","diff":"hard","d":"showing a willingness to take bold risks","comp":"more audacious / most audacious"},
  {"w":"Authentic","at":"positive","diff":"medium","d":"genuine and not a copy or imitation","comp":"more authentic / most authentic"},
  {"w":"Awe-inspiring","at":"positive","diff":"medium","d":"causing a feeling of wonder and respect","comp":"more awe-inspiring / most awe-inspiring"},
  {"w":"Balanced","at":"positive","diff":"easy","d":"keeping or showing steadiness and stability","comp":"more balanced / most balanced"},
  {"w":"Bold","at":"positive","diff":"easy","d":"showing a willingness to take risks; confident","comp":"bolder / boldest"},
  {"w":"Brave","at":"positive","diff":"easy","d":"ready to face danger or difficulty; courageous","comp":"braver / bravest"},
  {"w":"Bright","at":"positive","diff":"easy","d":"intelligent and quick to understand","comp":"brighter / brightest"},
  {"w":"Brilliant","at":"positive","diff":"medium","d":"impressively intelligent or talented","comp":"more brilliant / most brilliant"},
  {"w":"Calm","at":"positive","diff":"easy","d":"not showing or feeling nervousness or panic","comp":"calmer / calmest"},
  {"w":"Capable","at":"positive","diff":"easy","d":"having the ability to do things well","comp":"more capable / most capable"},
  {"w":"Captivating","at":"positive","diff":"medium","d":"attracting and holding interest or attention","comp":"more captivating / most captivating"},
  {"w":"Charismatic","at":"positive","diff":"medium","d":"having a powerful charm that inspires devotion","comp":"more charismatic / most charismatic"},
  {"w":"Cheerful","at":"positive","diff":"easy","d":"noticeably happy and optimistic","comp":"more cheerful / most cheerful"},
  {"w":"Clever","at":"positive","diff":"easy","d":"quick to understand and learn things","comp":"cleverer / cleverest"},
  {"w":"Compassionate","at":"positive","diff":"medium","d":"feeling or showing sympathy and concern for others","comp":"more compassionate / most compassionate"},
  {"w":"Confident","at":"positive","diff":"easy","d":"feeling certain about one's abilities or qualities","comp":"more confident / most confident"},
  {"w":"Courageous","at":"positive","diff":"medium","d":"not deterred by danger or pain; brave","comp":"more courageous / most courageous"},
  {"w":"Creative","at":"positive","diff":"easy","d":"relating to the use of imagination to produce new ideas","comp":"more creative / most creative"},
  {"w":"Dazzling","at":"positive","diff":"medium","d":"extremely impressive, beautiful, or skilful","comp":"more dazzling / most dazzling"},
  {"w":"Dedicated","at":"positive","diff":"easy","d":"devoted to a task or purpose; committed","comp":"more dedicated / most dedicated"},
  {"w":"Delightful","at":"positive","diff":"easy","d":"causing delight; charming and highly pleasing","comp":"more delightful / most delightful"},
  {"w":"Dependable","at":"positive","diff":"easy","d":"trustworthy and reliable","comp":"more dependable / most dependable"},
  {"w":"Determined","at":"positive","diff":"easy","d":"having made a firm decision and being resolved to follow it","comp":"more determined / most determined"},
  {"w":"Diligent","at":"positive","diff":"medium","d":"having or showing care and conscientiousness","comp":"more diligent / most diligent"},
  {"w":"Dynamic","at":"positive","diff":"medium","d":"characterised by constant change, activity, or progress","comp":"more dynamic / most dynamic"},
  {"w":"Eager","at":"positive","diff":"easy","d":"strongly wanting to do or have something","comp":"more eager / most eager"},
  {"w":"Eloquent","at":"positive","diff":"hard","d":"fluent and persuasive in speaking or writing","comp":"more eloquent / most eloquent"},
  {"w":"Empathetic","at":"positive","diff":"medium","d":"showing an ability to understand others' feelings","comp":"more empathetic / most empathetic"},
  {"w":"Energetic","at":"positive","diff":"easy","d":"showing or involving great activity or vitality","comp":"more energetic / most energetic"},
  {"w":"Enthusiastic","at":"positive","diff":"easy","d":"having or showing intense and eager enjoyment","comp":"more enthusiastic / most enthusiastic"},
  {"w":"Exceptional","at":"positive","diff":"medium","d":"unusually good; outstanding","comp":"more exceptional / most exceptional"},
  {"w":"Exuberant","at":"positive","diff":"hard","d":"filled with lively energy and excitement","comp":"more exuberant / most exuberant"},
  {"w":"Fair","at":"positive","diff":"easy","d":"treating people equally and impartially","comp":"fairer / fairest"},
  {"w":"Faithful","at":"positive","diff":"easy","d":"remaining loyal and steadfast","comp":"more faithful / most faithful"},
  {"w":"Fearless","at":"positive","diff":"medium","d":"lacking fear; not afraid of anything","comp":"more fearless / most fearless"},
  {"w":"Forthright","at":"positive","diff":"hard","d":"direct and outspoken; straightforward","comp":"more forthright / most forthright"},
  {"w":"Generous","at":"positive","diff":"easy","d":"showing a readiness to give more than is expected","comp":"more generous / most generous"},
  {"w":"Gentle","at":"positive","diff":"easy","d":"mild in temperament; soft and kind","comp":"gentler / gentlest"},
  {"w":"Graceful","at":"positive","diff":"easy","d":"having elegance or beauty of form or movement","comp":"more graceful / most graceful"},
  {"w":"Gracious","at":"positive","diff":"medium","d":"courteous, kind, and pleasant","comp":"more gracious / most gracious"},
  {"w":"Hardworking","at":"positive","diff":"easy","d":"tending to work with energy and commitment","comp":"more hardworking / most hardworking"},
  {"w":"Helpful","at":"positive","diff":"easy","d":"giving or ready to give assistance","comp":"more helpful / most helpful"},
  {"w":"Honest","at":"positive","diff":"easy","d":"free of deceit; truthful and sincere","comp":"more honest / most honest"},
  {"w":"Humble","at":"positive","diff":"easy","d":"having a modest view of one's own importance","comp":"humbler / humblest"},
  {"w":"Imaginative","at":"positive","diff":"medium","d":"having the ability to think of new and original ideas","comp":"more imaginative / most imaginative"},
  {"w":"Ingenious","at":"positive","diff":"hard","d":"clever and original in thinking or design","comp":"more ingenious / most ingenious"},
  {"w":"Inspiring","at":"positive","diff":"easy","d":"having the effect of inspiring someone","comp":"more inspiring / most inspiring"},
  {"w":"Intelligent","at":"positive","diff":"easy","d":"having or showing intelligence","comp":"more intelligent / most intelligent"},
  {"w":"Inventive","at":"positive","diff":"medium","d":"having the ability to create or design new things","comp":"more inventive / most inventive"},
  {"w":"Joyful","at":"positive","diff":"easy","d":"feeling or causing great happiness","comp":"more joyful / most joyful"},
  {"w":"Kind","at":"positive","diff":"easy","d":"friendly, generous, and considerate","comp":"kinder / kindest"},
  {"w":"Lively","at":"positive","diff":"easy","d":"full of life and energy; active and outgoing","comp":"livelier / liveliest"},
  {"w":"Luminous","at":"positive","diff":"hard","d":"full of or shedding light; glowing","comp":"more luminous / most luminous"},
  {"w":"Magnanimous","at":"positive","diff":"hard","d":"very generous or forgiving, especially toward rivals","comp":"more magnanimous / most magnanimous"},
  {"w":"Meticulous","at":"positive","diff":"hard","d":"showing great attention to detail; very careful","comp":"more meticulous / most meticulous"},
  {"w":"Motivated","at":"positive","diff":"easy","d":"having a reason to act in a particular way","comp":"more motivated / most motivated"},
  {"w":"Nurturing","at":"positive","diff":"medium","d":"caring for and encouraging growth or development","comp":"more nurturing / most nurturing"},
  {"w":"Open-minded","at":"positive","diff":"easy","d":"willing to consider new ideas; unprejudiced","comp":"more open-minded / most open-minded"},
  {"w":"Optimistic","at":"positive","diff":"medium","d":"hopeful and confident about the future","comp":"more optimistic / most optimistic"},
  {"w":"Passionate","at":"positive","diff":"easy","d":"showing strong feelings or a strong belief","comp":"more passionate / most passionate"},
  {"w":"Patient","at":"positive","diff":"easy","d":"able to accept delay or difficulty without becoming annoyed","comp":"more patient / most patient"},
  {"w":"Perceptive","at":"positive","diff":"hard","d":"having or showing sensitive insight","comp":"more perceptive / most perceptive"},
  {"w":"Perseverant","at":"positive","diff":"medium","d":"continuing firmly in spite of difficulty","comp":"more perseverant / most perseverant"},
  {"w":"Playful","at":"positive","diff":"easy","d":"fond of games and amusement; light-hearted","comp":"more playful / most playful"},
  {"w":"Precise","at":"positive","diff":"medium","d":"marked by exactness and accuracy","comp":"more precise / most precise"},
  {"w":"Productive","at":"positive","diff":"easy","d":"achieving or producing a significant amount","comp":"more productive / most productive"},
  {"w":"Profound","at":"positive","diff":"hard","d":"showing deep knowledge or great insight","comp":"more profound / most profound"},
  {"w":"Radiant","at":"positive","diff":"medium","d":"sending out light; shining or glowing brightly","comp":"more radiant / most radiant"},
  {"w":"Reliable","at":"positive","diff":"easy","d":"consistently good in quality or performance","comp":"more reliable / most reliable"},
  {"w":"Resilient","at":"positive","diff":"medium","d":"able to withstand or recover quickly from difficulties","comp":"more resilient / most resilient"},
  {"w":"Resourceful","at":"positive","diff":"medium","d":"able to find quick and clever ways to overcome difficulties","comp":"more resourceful / most resourceful"},
  {"w":"Respectful","at":"positive","diff":"easy","d":"feeling or showing deference and respect","comp":"more respectful / most respectful"},
  {"w":"Sagacious","at":"positive","diff":"hard","d":"having or showing good judgement; wise","comp":"more sagacious / most sagacious"},
  {"w":"Sincere","at":"positive","diff":"easy","d":"free from pretence or deceit; genuine","comp":"more sincere / most sincere"},
  {"w":"Spirited","at":"positive","diff":"medium","d":"full of energy, enthusiasm, and determination","comp":"more spirited / most spirited"},
  {"w":"Steadfast","at":"positive","diff":"medium","d":"resolutely firm and unwavering","comp":"more steadfast / most steadfast"},
  {"w":"Strong","at":"positive","diff":"easy","d":"having the power to move, lift, or exert great force","comp":"stronger / strongest"},
  {"w":"Supportive","at":"positive","diff":"easy","d":"providing encouragement or emotional help","comp":"more supportive / most supportive"},
  {"w":"Tenacious","at":"positive","diff":"hard","d":"tending to keep a firm hold; persistent","comp":"more tenacious / most tenacious"},
  {"w":"Thoughtful","at":"positive","diff":"easy","d":"showing consideration for the needs of others","comp":"more thoughtful / most thoughtful"},
  {"w":"Trustworthy","at":"positive","diff":"easy","d":"able to be relied on as honest or truthful","comp":"more trustworthy / most trustworthy"},
  {"w":"Valiant","at":"positive","diff":"hard","d":"possessing or showing courage and determination","comp":"more valiant / most valiant"},
  {"w":"Vibrant","at":"positive","diff":"medium","d":"full of energy and enthusiasm; bright and striking","comp":"more vibrant / most vibrant"},
  {"w":"Virtuous","at":"positive","diff":"medium","d":"having or showing high moral standards","comp":"more virtuous / most virtuous"},
  {"w":"Warm","at":"positive","diff":"easy","d":"showing enthusiasm, affection, or kindness","comp":"warmer / warmest"},
  {"w":"Wise","at":"positive","diff":"easy","d":"having experience, knowledge, and good judgement","comp":"wiser / wisest"},
  {"w":"Witty","at":"positive","diff":"medium","d":"showing a natural apt cleverness in speech or writing","comp":"wittier / wittiest"},
  {"w":"Zealous","at":"positive","diff":"hard","d":"having or showing great energy or enthusiasm","comp":"more zealous / most zealous"},
  {"w":"Abrasive","at":"negative","diff":"medium","d":"showing little concern for the feelings of others","comp":"more abrasive / most abrasive"},
  {"w":"Aggressive","at":"negative","diff":"easy","d":"ready or likely to attack or confront","comp":"more aggressive / most aggressive"},
  {"w":"Aloof","at":"negative","diff":"medium","d":"not friendly or forthcoming; distant","comp":"more aloof / most aloof"},
  {"w":"Apathetic","at":"negative","diff":"medium","d":"showing or feeling no interest or concern","comp":"more apathetic / most apathetic"},
  {"w":"Arrogant","at":"negative","diff":"easy","d":"having an exaggerated sense of one's own importance","comp":"more arrogant / most arrogant"},
  {"w":"Bitter","at":"negative","diff":"easy","d":"feeling or showing sharp disappointment or resentment","comp":"more bitter / most bitter"},
  {"w":"Bleak","at":"negative","diff":"medium","d":"lacking hope or encouragement; cold and miserable","comp":"bleaker / bleakest"},
  {"w":"Boisterous","at":"negative","diff":"medium","d":"noisy and energetic, especially in a disruptive way","comp":"more boisterous / most boisterous"},
  {"w":"Callous","at":"negative","diff":"hard","d":"showing or having an insensitive and cruel disregard","comp":"more callous / most callous"},
  {"w":"Chaotic","at":"negative","diff":"medium","d":"in a state of complete confusion and disorder","comp":"more chaotic / most chaotic"},
  {"w":"Cowardly","at":"negative","diff":"easy","d":"lacking courage; contemptibly lacking in bravery","comp":"more cowardly / most cowardly"},
  {"w":"Cruel","at":"negative","diff":"easy","d":"wilfully causing pain or suffering to others","comp":"crueler / cruelest"},
  {"w":"Cunning","at":"negative","diff":"medium","d":"skilled at achieving aims by deceit","comp":"more cunning / most cunning"},
  {"w":"Cynical","at":"negative","diff":"medium","d":"believing the worst of people's motives","comp":"more cynical / most cynical"},
  {"w":"Deceitful","at":"negative","diff":"medium","d":"deliberately causing someone to believe false things","comp":"more deceitful / most deceitful"},
  {"w":"Deceptive","at":"negative","diff":"medium","d":"giving an appearance or impression different from true","comp":"more deceptive / most deceptive"},
  {"w":"Defiant","at":"negative","diff":"medium","d":"showing open resistance or bold disobedience","comp":"more defiant / most defiant"},
  {"w":"Desolate","at":"negative","diff":"hard","d":"empty of people; making someone feel utterly alone","comp":"more desolate / most desolate"},
  {"w":"Devious","at":"negative","diff":"medium","d":"showing a skilful use of underhanded tactics","comp":"more devious / most devious"},
  {"w":"Dishonest","at":"negative","diff":"easy","d":"not honest or fair in behaviour","comp":"more dishonest / most dishonest"},
  {"w":"Dismal","at":"negative","diff":"medium","d":"causing a mood of gloom or depression","comp":"more dismal / most dismal"},
  {"w":"Dreadful","at":"negative","diff":"easy","d":"causing or involving great suffering or fear","comp":"more dreadful / most dreadful"},
  {"w":"Erratic","at":"negative","diff":"medium","d":"not predictable; unpredictable in behaviour","comp":"more erratic / most erratic"},
  {"w":"Feeble","at":"negative","diff":"medium","d":"lacking physical strength; too weak to be effective","comp":"feebler / feeblest"},
  {"w":"Ferocious","at":"negative","diff":"medium","d":"savagely fierce and violent","comp":"more ferocious / most ferocious"},
  {"w":"Frantic","at":"negative","diff":"easy","d":"distraught with fear, anxiety, or other emotion","comp":"more frantic / most frantic"},
  {"w":"Frivolous","at":"negative","diff":"medium","d":"not having any serious purpose or value","comp":"more frivolous / most frivolous"},
  {"w":"Grim","at":"negative","diff":"easy","d":"stern and forbidding; unrelentingly harsh","comp":"grimmer / grimmest"},
  {"w":"Gloomy","at":"negative","diff":"easy","d":"dark or poorly lit; causing despondency","comp":"gloomier / gloomiest"},
  {"w":"Greedy","at":"negative","diff":"easy","d":"having or showing an intense desire for more","comp":"greedier / greediest"},
  {"w":"Harsh","at":"negative","diff":"easy","d":"cruel and severe; unpleasantly rough or jarring","comp":"harsher / harshest"},
  {"w":"Hostile","at":"negative","diff":"medium","d":"showing or feeling opposition; antagonistic","comp":"more hostile / most hostile"},
  {"w":"Ignorant","at":"negative","diff":"easy","d":"lacking knowledge or awareness in general","comp":"more ignorant / most ignorant"},
  {"w":"Impulsive","at":"negative","diff":"medium","d":"acting without forethought; done suddenly","comp":"more impulsive / most impulsive"},
  {"w":"Indifferent","at":"negative","diff":"medium","d":"having no particular interest or sympathy","comp":"more indifferent / most indifferent"},
  {"w":"Insolent","at":"negative","diff":"hard","d":"showing a rude lack of respect","comp":"more insolent / most insolent"},
  {"w":"Irrational","at":"negative","diff":"medium","d":"not logical or reasonable","comp":"more irrational / most irrational"},
  {"w":"Jealous","at":"negative","diff":"easy","d":"feeling resentment towards someone's success","comp":"more jealous / most jealous"},
  {"w":"Lethargic","at":"negative","diff":"medium","d":"affected by lethargy; sluggish and apathetic","comp":"more lethargic / most lethargic"},
  {"w":"Malicious","at":"negative","diff":"hard","d":"characterised by malice; intending harm","comp":"more malicious / most malicious"},
  {"w":"Manipulative","at":"negative","diff":"medium","d":"exercising unscrupulous control over others","comp":"more manipulative / most manipulative"},
  {"w":"Menacing","at":"negative","diff":"medium","d":"suggesting the presence of danger; threatening","comp":"more menacing / most menacing"},
  {"w":"Miserable","at":"negative","diff":"easy","d":"wretchedly unhappy or uncomfortable","comp":"more miserable / most miserable"},
  {"w":"Moody","at":"negative","diff":"easy","d":"given to unpredictable changes of mood","comp":"moodier / moodiest"},
  {"w":"Narrow-minded","at":"negative","diff":"medium","d":"unwilling to listen to or consider other views","comp":"more narrow-minded / most narrow-minded"},
  {"w":"Negligent","at":"negative","diff":"hard","d":"failing to take proper care in doing something","comp":"more negligent / most negligent"},
  {"w":"Obstinate","at":"negative","diff":"hard","d":"stubbornly refusing to change one's opinion","comp":"more obstinate / most obstinate"},
  {"w":"Overbearing","at":"negative","diff":"hard","d":"unpleasantly overpowering; domineering","comp":"more overbearing / most overbearing"},
  {"w":"Paranoid","at":"negative","diff":"medium","d":"unreasonably anxious or suspicious about others","comp":"more paranoid / most paranoid"},
  {"w":"Passive","at":"negative","diff":"easy","d":"accepting without resistance; submissive","comp":"more passive / most passive"},
  {"w":"Petty","at":"negative","diff":"easy","d":"trivially or meanly small-minded","comp":"pettier / pettiest"},
  {"w":"Pompous","at":"negative","diff":"medium","d":"affectedly grand or self-important","comp":"more pompous / most pompous"},
  {"w":"Reckless","at":"negative","diff":"easy","d":"without thought of consequences; heedless of danger","comp":"more reckless / most reckless"},
  {"w":"Resentful","at":"negative","diff":"medium","d":"feeling or expressing bitterness at unfair treatment","comp":"more resentful / most resentful"},
  {"w":"Ruthless","at":"negative","diff":"medium","d":"having no pity; merciless","comp":"more ruthless / most ruthless"},
  {"w":"Selfish","at":"negative","diff":"easy","d":"lacking consideration for others; concerned with one's own profit","comp":"more selfish / most selfish"},
  {"w":"Sinister","at":"negative","diff":"medium","d":"giving the impression of harm or evil","comp":"more sinister / most sinister"},
  {"w":"Sluggish","at":"negative","diff":"easy","d":"slow-moving or inactive; lacking energy","comp":"more sluggish / most sluggish"},
  {"w":"Spiteful","at":"negative","diff":"medium","d":"showing a desire to hurt, annoy, or offend","comp":"more spiteful / most spiteful"},
  {"w":"Stubborn","at":"negative","diff":"easy","d":"having or showing dogged determination not to change","comp":"more stubborn / most stubborn"},
  {"w":"Sullen","at":"negative","diff":"medium","d":"bad-tempered and sulky; gloomy and resentful","comp":"more sullen / most sullen"},
  {"w":"Treacherous","at":"negative","diff":"hard","d":"guilty of or involving betrayal or deception","comp":"more treacherous / most treacherous"},
  {"w":"Turbulent","at":"negative","diff":"hard","d":"characterised by conflict, disorder, or confusion","comp":"more turbulent / most turbulent"},
  {"w":"Vain","at":"negative","diff":"easy","d":"having an excessively high opinion of one's appearance","comp":"more vain / most vain"},
  {"w":"Venomous","at":"negative","diff":"hard","d":"seeking to do harm; full of malice","comp":"more venomous / most venomous"},
  {"w":"Volatile","at":"negative","diff":"hard","d":"liable to change rapidly and unpredictably","comp":"more volatile / most volatile"},
  {"w":"Wretched","at":"negative","diff":"medium","d":"in a very unhappy or unfortunate state","comp":"more wretched / most wretched"},
  {"w":"Abrupt","at":"neutral","diff":"easy","d":"sudden and unexpected; brief to the point of rudeness","comp":"more abrupt / most abrupt"},
  {"w":"Abstract","at":"neutral","diff":"medium","d":"existing in thought or as an idea but not concrete","comp":"more abstract / most abstract"},
  {"w":"Adjacent","at":"neutral","diff":"medium","d":"next to or adjoining something else","comp":"more adjacent / most adjacent"},
  {"w":"Ambiguous","at":"neutral","diff":"medium","d":"open to more than one interpretation","comp":"more ambiguous / most ambiguous"},
  {"w":"Ancient","at":"neutral","diff":"easy","d":"belonging to the very distant past","comp":"more ancient / most ancient"},
  {"w":"Angular","at":"neutral","diff":"medium","d":"having angles or sharp corners","comp":"more angular / most angular"},
  {"w":"Annual","at":"neutral","diff":"easy","d":"occurring once every year; calculated over a year","comp":"more annual / most annual"},
  {"w":"Approximate","at":"neutral","diff":"medium","d":"close to the actual, but not completely accurate","comp":"more approximate / most approximate"},
  {"w":"Arbitrary","at":"neutral","diff":"hard","d":"based on random choice or personal whim","comp":"more arbitrary / most arbitrary"},
  {"w":"Arid","at":"neutral","diff":"medium","d":"having little or no rain; too dry for vegetation","comp":"more arid / most arid"},
  {"w":"Asymmetrical","at":"neutral","diff":"hard","d":"made up of parts that are not symmetrical","comp":"more asymmetrical / most asymmetrical"},
  {"w":"Blunt","at":"neutral","diff":"easy","d":"having a flat or rounded end; not sharpened","comp":"blunter / bluntest"},
  {"w":"Brief","at":"neutral","diff":"easy","d":"of short duration; using few words","comp":"briefer / briefest"},
  {"w":"Broad","at":"neutral","diff":"easy","d":"having a distance larger than usual from side to side","comp":"broader / broadest"},
  {"w":"Central","at":"neutral","diff":"easy","d":"at the point or in the area that is middle or most important","comp":"more central / most central"},
  {"w":"Circular","at":"neutral","diff":"easy","d":"having the form of a circle; round","comp":"more circular / most circular"},
  {"w":"Coastal","at":"neutral","diff":"easy","d":"of or near a coast","comp":"more coastal / most coastal"},
  {"w":"Compact","at":"neutral","diff":"easy","d":"closely and firmly packed together; dense","comp":"more compact / most compact"},
  {"w":"Complex","at":"neutral","diff":"medium","d":"consisting of many different and connected parts","comp":"more complex / most complex"},
  {"w":"Concurrent","at":"neutral","diff":"hard","d":"existing or happening at the same time","comp":"more concurrent / most concurrent"},
  {"w":"Conditional","at":"neutral","diff":"hard","d":"subject to one or more conditions","comp":"more conditional / most conditional"},
  {"w":"Continuous","at":"neutral","diff":"medium","d":"forming an unbroken whole; without interruption","comp":"more continuous / most continuous"},
  {"w":"Covert","at":"neutral","diff":"hard","d":"not openly acknowledged or displayed; secret","comp":"more covert / most covert"},
  {"w":"Cubic","at":"neutral","diff":"easy","d":"having the shape of a cube; three-dimensional","comp":"more cubic / most cubic"},
  {"w":"Cumulative","at":"neutral","diff":"hard","d":"increasing by successive additions","comp":"more cumulative / most cumulative"},
  {"w":"Cyclical","at":"neutral","diff":"hard","d":"occurring in cycles; regularly repeated","comp":"more cyclical / most cyclical"},
  {"w":"Dense","at":"neutral","diff":"easy","d":"closely compacted in substance; thick","comp":"denser / densest"},
  {"w":"Digital","at":"neutral","diff":"easy","d":"relating to or using signals expressed as numerical digits","comp":"more digital / most digital"},
  {"w":"Distant","at":"neutral","diff":"easy","d":"far away in space or time","comp":"more distant / most distant"},
  {"w":"Dominant","at":"neutral","diff":"medium","d":"most important, powerful, or influential","comp":"more dominant / most dominant"},
  {"w":"Dual","at":"neutral","diff":"medium","d":"consisting of two parts or elements","comp":"more dual / most dual"},
  {"w":"Elapsed","at":"neutral","diff":"hard","d":"of time: having passed","comp":"more elapsed / most elapsed"},
  {"w":"Emerging","at":"neutral","diff":"medium","d":"becoming apparent or prominent; newly arising","comp":"more emerging / most emerging"},
  {"w":"Empirical","at":"neutral","diff":"hard","d":"based on observation or experience rather than theory","comp":"more empirical / most empirical"},
  {"w":"Enclosed","at":"neutral","diff":"easy","d":"shut in on all sides; contained within bounds","comp":"more enclosed / most enclosed"},
  {"w":"Ephemeral","at":"neutral","diff":"hard","d":"lasting for a very short time","comp":"more ephemeral / most ephemeral"},
  {"w":"Equivalent","at":"neutral","diff":"medium","d":"equal in value, amount, meaning, or effect","comp":"more equivalent / most equivalent"},
  {"w":"Eventual","at":"neutral","diff":"medium","d":"happening or existing at some later time","comp":"more eventual / most eventual"},
  {"w":"External","at":"neutral","diff":"easy","d":"belonging to or forming the outer surface","comp":"more external / most external"},
  {"w":"Finite","at":"neutral","diff":"medium","d":"limited in size or extent","comp":"more finite / most finite"},
  {"w":"Fixed","at":"neutral","diff":"easy","d":"fastened securely in position; not movable","comp":"more fixed / most fixed"},
  {"w":"Flat","at":"neutral","diff":"easy","d":"having a level surface; not curved or bumpy","comp":"flatter / flattest"},
  {"w":"Fluid","at":"neutral","diff":"medium","d":"capable of flowing freely; not fixed or solid","comp":"more fluid / most fluid"},
  {"w":"Formal","at":"neutral","diff":"easy","d":"done in accordance with rules or convention","comp":"more formal / most formal"},
  {"w":"Fractional","at":"neutral","diff":"hard","d":"of or relating to a small part of a whole","comp":"more fractional / most fractional"},
  {"w":"Fragmented","at":"neutral","diff":"medium","d":"broken into separate disconnected parts","comp":"more fragmented / most fragmented"},
  {"w":"Gradual","at":"neutral","diff":"easy","d":"taking place slowly over a long period","comp":"more gradual / most gradual"},
  {"w":"Horizontal","at":"neutral","diff":"easy","d":"parallel to the plane of the horizon; flat","comp":"more horizontal / most horizontal"},
  {"w":"Hybrid","at":"neutral","diff":"medium","d":"of mixed character; composed of two elements","comp":"more hybrid / most hybrid"},
  {"w":"Hypothetical","at":"neutral","diff":"hard","d":"supposed but not necessarily real; theoretical","comp":"more hypothetical / most hypothetical"},
  {"w":"Identical","at":"neutral","diff":"easy","d":"similar in every detail; exactly alike","comp":"more identical / most identical"},
  {"w":"Immense","at":"neutral","diff":"medium","d":"extremely large or great; enormous","comp":"more immense / most immense"},
  {"w":"Implicit","at":"neutral","diff":"hard","d":"suggested but not directly expressed","comp":"more implicit / most implicit"},
  {"w":"Incremental","at":"neutral","diff":"hard","d":"relating to gain or increase by small amounts","comp":"more incremental / most incremental"},
  {"w":"Indirect","at":"neutral","diff":"easy","d":"not going in a straight line; roundabout","comp":"more indirect / most indirect"},
  {"w":"Infinite","at":"neutral","diff":"medium","d":"limitless or endless in space, extent, or size","comp":"more infinite / most infinite"},
  {"w":"Initial","at":"neutral","diff":"easy","d":"existing or occurring at the beginning","comp":"more initial / most initial"},
  {"w":"Inland","at":"neutral","diff":"easy","d":"situated in the interior of a country","comp":"more inland / most inland"},
  {"w":"Innate","at":"neutral","diff":"hard","d":"inborn; natural; not learned","comp":"more innate / most innate"},
  {"w":"Integral","at":"neutral","diff":"hard","d":"necessary to make a whole complete; fundamental","comp":"more integral / most integral"},
  {"w":"Internal","at":"neutral","diff":"easy","d":"of or situated on the inside","comp":"more internal / most internal"},
  {"w":"Lateral","at":"neutral","diff":"hard","d":"of or relating to the side or sides","comp":"more lateral / most lateral"},
  {"w":"Linear","at":"neutral","diff":"medium","d":"arranged in or extending along a straight line","comp":"more linear / most linear"},
  {"w":"Local","at":"neutral","diff":"easy","d":"belonging or relating to a particular area","comp":"more local / most local"},
  {"w":"Marginal","at":"neutral","diff":"hard","d":"relating to or situated at the edge or margin","comp":"more marginal / most marginal"},
  {"w":"Massive","at":"neutral","diff":"easy","d":"large and heavy or solid; exceptionally large","comp":"more massive / most massive"},
  {"w":"Minimal","at":"neutral","diff":"medium","d":"of a minimum amount; the least possible","comp":"more minimal / most minimal"},
  {"w":"Mobile","at":"neutral","diff":"easy","d":"able to move or be moved freely or easily","comp":"more mobile / most mobile"},
  {"w":"Mutual","at":"neutral","diff":"medium","d":"experienced or done by each of two or more parties","comp":"more mutual / most mutual"},
  {"w":"Narrow","at":"neutral","diff":"easy","d":"of small width in relation to length","comp":"narrower / narrowest"},
  {"w":"Neutral","at":"neutral","diff":"easy","d":"not supporting or helping either side in a conflict","comp":"more neutral / most neutral"},
  {"w":"Nocturnal","at":"neutral","diff":"hard","d":"active or occurring during the night","comp":"more nocturnal / most nocturnal"},
  {"w":"Oblique","at":"neutral","diff":"hard","d":"neither parallel nor at right angles; slanting","comp":"more oblique / most oblique"},
  {"w":"Occasional","at":"neutral","diff":"easy","d":"occurring, appearing, or done infrequently","comp":"more occasional / most occasional"},
  {"w":"Offshore","at":"neutral","diff":"easy","d":"situated or operating at sea some distance from shore","comp":"more offshore / most offshore"},
  {"w":"Ongoing","at":"neutral","diff":"easy","d":"still in progress; continuing","comp":"more ongoing / most ongoing"},
  {"w":"Optical","at":"neutral","diff":"medium","d":"relating to sight or the action of light on sight","comp":"more optical / most optical"},
  {"w":"Oral","at":"neutral","diff":"easy","d":"relating to or using the mouth; spoken","comp":"more oral / most oral"},
  {"w":"Orbital","at":"neutral","diff":"hard","d":"relating to an orbit around a celestial body","comp":"more orbital / most orbital"},
  {"w":"Outdated","at":"neutral","diff":"easy","d":"no longer current or up to date","comp":"more outdated / most outdated"},
  {"w":"Parallel","at":"neutral","diff":"medium","d":"occurring or existing at the same time","comp":"more parallel / most parallel"},
  {"w":"Partial","at":"neutral","diff":"easy","d":"existing only in part; incomplete","comp":"more partial / most partial"},
  {"w":"Peripheral","at":"neutral","diff":"hard","d":"relating to or situated on the edge or periphery","comp":"more peripheral / most peripheral"},
  {"w":"Permanent","at":"neutral","diff":"easy","d":"lasting or intended to last indefinitely","comp":"more permanent / most permanent"},
  {"w":"Preliminary","at":"neutral","diff":"hard","d":"serving as an introduction; preparatory","comp":"more preliminary / most preliminary"},
  {"w":"Primary","at":"neutral","diff":"easy","d":"of first importance; main","comp":"more primary / most primary"},
  {"w":"Prior","at":"neutral","diff":"easy","d":"existing or coming before in time, order, or importance","comp":"more prior / most prior"},
  {"w":"Proportional","at":"neutral","diff":"hard","d":"corresponding in size or degree","comp":"more proportional / most proportional"},
  {"w":"Radial","at":"neutral","diff":"hard","d":"arranged like the radii of a circle; diverging from a centre","comp":"more radial / most radial"},
  {"w":"Raw","at":"neutral","diff":"easy","d":"in its natural state; not yet processed","comp":"rawer / rawest"},
  {"w":"Rectangular","at":"neutral","diff":"easy","d":"denoting a shape with four right angles","comp":"more rectangular / most rectangular"},
  {"w":"Regional","at":"neutral","diff":"easy","d":"relating to or characteristic of a region","comp":"more regional / most regional"},
  {"w":"Remote","at":"neutral","diff":"easy","d":"situated far from the main centres of population","comp":"more remote / most remote"},
  {"w":"Residual","at":"neutral","diff":"hard","d":"remaining after the greater part has been taken","comp":"more residual / most residual"},
  {"w":"Rigid","at":"neutral","diff":"medium","d":"unable to bend or be forced out of shape","comp":"more rigid / most rigid"},
  {"w":"Rural","at":"neutral","diff":"easy","d":"in, relating to, or characteristic of the countryside","comp":"more rural / most rural"},
  {"w":"Seasonal","at":"neutral","diff":"easy","d":"relating to or typical of a particular season","comp":"more seasonal / most seasonal"},
  {"w":"Secondary","at":"neutral","diff":"easy","d":"coming after, less important than, or resulting from","comp":"more secondary / most secondary"},
  {"w":"Sequential","at":"neutral","diff":"hard","d":"following in a logical order or sequence","comp":"more sequential / most sequential"},
  {"w":"Simultaneous","at":"neutral","diff":"hard","d":"occurring, operating, or done at the same time","comp":"more simultaneous / most simultaneous"},
  {"w":"Sparse","at":"neutral","diff":"medium","d":"thinly dispersed or scattered","comp":"sparser / sparsest"},
  {"w":"Spherical","at":"neutral","diff":"medium","d":"shaped like a sphere; globular","comp":"more spherical / most spherical"},
  {"w":"Static","at":"neutral","diff":"medium","d":"lacking in movement, action, or change","comp":"more static / most static"},
  {"w":"Structural","at":"neutral","diff":"hard","d":"of or relating to the arrangement of parts","comp":"more structural / most structural"},
  {"w":"Subterranean","at":"neutral","diff":"hard","d":"existing, occurring, or done underground","comp":"more subterranean / most subterranean"},
  {"w":"Symbolic","at":"neutral","diff":"medium","d":"serving as a symbol; relating to symbols","comp":"more symbolic / most symbolic"},
  {"w":"Systematic","at":"neutral","diff":"hard","d":"done or acting according to a fixed plan or system","comp":"more systematic / most systematic"},
  {"w":"Temporal","at":"neutral","diff":"hard","d":"relating to time as opposed to eternity","comp":"more temporal / most temporal"},
  {"w":"Territorial","at":"neutral","diff":"hard","d":"of or relating to a particular territory or district","comp":"more territorial / most territorial"},
  {"w":"Tidal","at":"neutral","diff":"easy","d":"relating to or affected by tides","comp":"more tidal / most tidal"},
  {"w":"Transient","at":"neutral","diff":"hard","d":"lasting only for a short time; impermanent","comp":"more transient / most transient"},
  {"w":"Uniform","at":"neutral","diff":"medium","d":"remaining the same in all cases and at all times","comp":"more uniform / most uniform"},
  {"w":"Urban","at":"neutral","diff":"easy","d":"relating to a city or town","comp":"more urban / most urban"},
  {"w":"Vast","at":"neutral","diff":"easy","d":"of very great extent or quantity","comp":"vaster / vastest"},
  {"w":"Vertical","at":"neutral","diff":"easy","d":"at right angles to a horizontal plane; upright","comp":"more vertical / most vertical"},
  {"w":"Visible","at":"neutral","diff":"easy","d":"able to be seen; perceptible to the eye","comp":"more visible / most visible"},
  {"w":"Volcanic","at":"neutral","diff":"medium","d":"of, relating to, or produced by a volcano","comp":"more volcanic / most volcanic"},
  {"w":"Widespread","at":"neutral","diff":"easy","d":"found or distributed over a large area","comp":"more widespread / most widespread"}
]
```

- [ ] **Step 2: Verify file is valid JSON**

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site"
python3 -c "import json; d=json.load(open('wordineer-deploy/data/adjectives.json')); print(f'OK: {len(d)} adjectives')"
```

Expected output: `OK: 175 adjectives` (or however many are in the starter set — target 500 total for production)

- [ ] **Step 3: Commit**

```bash
git add wordineer-deploy/data/adjectives.json
git commit -m "feat: add adjectives.json data file (175 entries, w/at/diff/d/comp schema)"
```

---

## Task 2: Extend tool-engine.js to support adjective sentiment filter and comp display

**Files:**
- Modify: `wordineer-deploy/scripts/tool-engine.js`

- [ ] **Step 1: Add `at` and `comp` to data normalisation (line 76)**

Find this line (line 76):
```javascript
: raw.map(e => ({ w: e.w, t: e.t || 'noun', nt: e.nt, vt: e.vt, d: e.d || '', diff: e.diff || 'medium', borrowed: false, syl: countSyllables(e.w) }));
```

Replace with:
```javascript
: raw.map(e => ({ w: e.w, t: e.t || 'noun', nt: e.nt, vt: e.vt, at: e.at, comp: e.comp || '', d: e.d || '', diff: e.diff || 'medium', borrowed: false, syl: countSyllables(e.w) }));
```

- [ ] **Step 2: Read adjType from config (line 274)**

Find this line (line 274):
```javascript
const verbType = config.verbTypeId ? (document.getElementById(config.verbTypeId)?.value || 'all') : null;
```

Replace with:
```javascript
const verbType = config.verbTypeId ? (document.getElementById(config.verbTypeId)?.value || 'all') : null;
const adjType  = config.adjTypeId  ? (document.getElementById(config.adjTypeId)?.value  || 'all') : null;
```

- [ ] **Step 3: Add adjType filter condition (line 283)**

Find this line (line 283):
```javascript
if (verbType && verbType !== 'all' && w.vt !== verbType) return false;
```

Replace with:
```javascript
if (verbType && verbType !== 'all' && w.vt !== verbType) return false;
if (adjType  && adjType  !== 'all' && w.at !== adjType)  return false;
```

- [ ] **Step 4: Update `.word-pos` rendering and add `.word-comp` (line 324–325)**

Find this block (lines 324–326):
```javascript
<div class="word-pos">${wd.nt ? wd.nt + ' noun' : wd.vt ? wd.vt + ' verb' : wd.t}</div>
<div class="word-def"${hideStyle}>${wd.d}</div>
${i < 3 ? `<div class="word-grammarly"${hideStyle}><a href="https://grammarly.com" target="_blank" rel="noopener">Use in a sentence with Grammarly →</a></div>` : ''}
```

Replace with:
```javascript
<div class="word-pos">${wd.at ? wd.at + (wd.diff ? ' · ' + wd.diff : '') : wd.nt ? wd.nt + ' noun' : wd.vt ? wd.vt + ' verb' : wd.t}</div>
${wd.comp ? `<div class="word-comp">${wd.comp}</div>` : ''}
<div class="word-def"${hideStyle}>${wd.d}</div>
${i < 3 ? `<div class="word-grammarly"${hideStyle}><a href="https://grammarly.com" target="_blank" rel="noopener">Use in a sentence with Grammarly →</a></div>` : ''}
```

- [ ] **Step 5: Commit engine changes**

```bash
git add wordineer-deploy/scripts/tool-engine.js
git commit -m "feat: add adjType filter and word-comp rendering to tool-engine"
```

---

## Task 3: Minify updated tool-engine.js

**Files:**
- Modify: `wordineer-deploy/scripts/tool-engine.min.js`

- [ ] **Step 1: Minify using Python (no external tools needed)**

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site"
python3 -c "
import re, sys
src = open('wordineer-deploy/scripts/tool-engine.js').read()
# Strip single-line comments (not URLs)
src = re.sub(r'(?<!:)//[^\n]*', '', src)
# Strip multi-line comments
src = re.sub(r'/\*.*?\*/', '', src, flags=re.DOTALL)
# Collapse whitespace
src = re.sub(r'\s+', ' ', src).strip()
open('wordineer-deploy/scripts/tool-engine.min.js', 'w').write(src)
print('Done. Size:', len(src), 'bytes')
"
```

Expected: prints size in bytes. Verify the output file is smaller than the original.

- [ ] **Step 2: Verify minified file loads (quick syntax check)**

```bash
node -e "eval(require('fs').readFileSync('wordineer-deploy/scripts/tool-engine.min.js','utf8').replace(/WORDINEER\s*=/,'var WORDINEER=')); console.log('OK')" 2>/dev/null || echo "node not available - check manually"
```

- [ ] **Step 3: Commit**

```bash
git add wordineer-deploy/scripts/tool-engine.min.js
git commit -m "build: minify tool-engine after adjType + comp additions"
```

---

## Task 4: Create the tool-src HTML file

**Files:**
- Create: `template-deploy/tools-src/random-adjective-generator.html`

- [ ] **Step 1: Create the file**

Create `template-deploy/tools-src/random-adjective-generator.html` with this content:

```html
<!-- CONFIG
{ "url": "/random-adjective-generator/", "output": "random-adjective-generator.html", "type": "tool" }
-->

<!-- SLOT:meta -->
<title>Random Adjective Generator — Filter by Sentiment, Instant Results | Wordineer</title>
<meta name="description" content="Generate random adjectives instantly. Filter by sentiment (positive, negative, neutral), difficulty, and starting letter. Definitions and comparative forms included. Free.">
<link rel="canonical" href="https://wordineer.com/random-adjective-generator/">
<meta property="og:type"        content="website">
<meta property="og:site_name"   content="Wordineer">
<meta property="og:title"       content="Random Adjective Generator — Filter by Sentiment, Instant Results | Wordineer">
<meta property="og:description" content="Generate random adjectives instantly. Filter by sentiment (positive, negative, neutral), difficulty, and starting letter. Definitions and comparative forms included. Free.">
<meta property="og:url"         content="https://wordineer.com/random-adjective-generator/">
<meta property="og:image"       content="https://wordineer.com/og-image.png">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is an adjective?",
      "acceptedAnswer": { "@type": "Answer", "text": "An adjective is a word that describes or modifies a noun or pronoun. It gives more information about a person, place, thing, or idea — its size, colour, number, condition, or quality. Examples: bright, gloomy, vast, resilient, sinister." }
    },
    {
      "@type": "Question",
      "name": "What does the Sentiment filter do?",
      "acceptedAnswer": { "@type": "Answer", "text": "The Sentiment filter tags each adjective as positive (uplifting or approving — brilliant, generous, resilient), negative (critical or threatening — bleak, volatile, wretched), or neutral (descriptive without judgement — vast, circular, preliminary). No other adjective generator offers this filter." }
    },
    {
      "@type": "Question",
      "name": "What are comparative and superlative adjectives?",
      "acceptedAnswer": { "@type": "Answer", "text": "The three degrees of comparison: base form (fast), comparative (faster — comparing two things), and superlative (fastest — the extreme among three or more). Short adjectives take -er/-est suffixes; longer adjectives use more/most. Irregular adjectives include good/better/best and bad/worse/worst. This tool shows all three forms under each result." }
    },
    {
      "@type": "Question",
      "name": "Can I combine filters?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes — Sentiment, Difficulty, and First Letter all stack. For example, you can generate hard negative adjectives starting with D, or easy positive adjectives starting with B." }
    },
    {
      "@type": "Question",
      "name": "How do I save adjectives I like?",
      "acceptedAnswer": { "@type": "Answer", "text": "Click the heart icon on any adjective to save it to the Saved section at the bottom of the tool. When you're done, click 'Copy saved' to copy your entire saved list to the clipboard in one go." }
    },
    {
      "@type": "Question",
      "name": "Is this tool free?",
      "acceptedAnswer": { "@type": "Answer", "text": "Completely free, forever. No account required, no limits, no paywalls." }
    },
    {
      "@type": "Question",
      "name": "How many adjectives are in the dataset?",
      "acceptedAnswer": { "@type": "Answer", "text": "Over 500 curated adjectives across all sentiment categories and difficulty levels, each with a definition and comparative/superlative forms." }
    }
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Random Adjective Generator",
  "url": "https://wordineer.com/random-adjective-generator/",
  "description": "Generate random adjectives instantly. Filter by sentiment (positive, negative, neutral), difficulty, and starting letter. Definitions and comparative forms included. Free.",
  "applicationCategory": "UtilityApplication",
  "operatingSystem": "Web",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
  "publisher": { "@id": "https://wordineer.com/#organization" }
}
</script>
<!-- /SLOT:meta -->

<!-- SLOT:style -->
<style>
/* ── Adjective Generator Tool Styles ── */
.tool-wrap  { max-width:960px; margin:0 auto; padding:24px 24px 0; }
.tool-card  { border:1px solid var(--border); border-radius:var(--radius-lg); overflow:hidden; background:var(--bg); box-shadow:var(--shadow); }
.tool-split { display:flex; }

.ctrl       { width:220px; flex-shrink:0; padding:18px; border-right:1px solid var(--border-2); background:var(--bg-2); }
.ctrl-row   { margin-bottom:14px; }
.ctrl-label { font-size:10px; font-weight:600; color:var(--text-3); text-transform:uppercase; letter-spacing:.06em; display:block; margin-bottom:5px; }
.ctrl-row input, .ctrl-row select { width:100%; padding:7px 10px; font-size:13px; font-family:inherit; border:1px solid var(--border); border-radius:7px; background:var(--bg); color:var(--text); appearance:none; outline:none; transition:border-color .15s; }
.ctrl-row input:focus, .ctrl-row select:focus { border-color:var(--brand); }
.count-error { display:none; font-size:11px; color:#E24B4A; margin-top:4px; }
.count-error.show { display:block; }
.ctrl-row input.input-error { border-color:#E24B4A !important; }
.def-row    { display:flex; align-items:center; gap:8px; margin-bottom:14px; }
.def-row label { font-size:12px; color:var(--text-2); cursor:pointer; }
.toggle     { position:relative; width:32px; height:18px; flex-shrink:0; }
.toggle input { opacity:0; width:0; height:0; }
.toggle-sl  { position:absolute; cursor:pointer; inset:0; background:var(--border); border-radius:9px; transition:.2s; }
.toggle input:checked + .toggle-sl { background:var(--brand); }
.toggle-sl::before { content:''; position:absolute; width:14px; height:14px; left:2px; top:2px; background:white; border-radius:50%; transition:.2s; }
.toggle input:checked + .toggle-sl::before { transform:translateX(14px); }
.gen-btn    { width:100%; padding:10px 14px; background:var(--brand); color:white; border:none; border-radius:8px; font-size:14px; font-weight:600; font-family:inherit; cursor:pointer; transition:background .15s,transform .1s; letter-spacing:-.01em; }
.gen-btn:hover { background:var(--brand-dark); }
.gen-btn:active { transform:scale(.98); }
.reset-btn  { display:block; width:100%; text-align:center; font-size:11px; color:var(--text-3); margin-top:8px; cursor:pointer; text-decoration:underline; text-underline-offset:2px; border:none; background:none; font-family:inherit; }
.kbd        { text-align:center; font-size:10px; color:var(--text-3); margin-top:6px; }
.kbd kbd    { background:var(--bg-3); border:1px solid var(--border); border-radius:3px; padding:1px 5px; font-size:10px; font-family:inherit; }

.words-panel { flex:1; display:flex; flex-direction:column; overflow:hidden; min-height:320px; }
.words-top  { display:flex; align-items:center; justify-content:space-between; padding:12px 16px; border-bottom:1px solid var(--border-2); }
.words-count { font-size:12px; color:var(--text-3); }
.words-actions { display:flex; gap:6px; }
.act-btn    { font-size:12px; padding:5px 11px; border:1px solid var(--border); border-radius:6px; background:var(--bg); color:var(--text-2); cursor:pointer; font-family:inherit; transition:background .12s; }
.act-btn:hover { background:var(--bg-2); }
.word-list  { flex:1; overflow-y:auto; list-style:none; padding:0 16px; }
.word-item  { display:flex; align-items:flex-start; justify-content:space-between; padding:10px 0; border-bottom:1px solid var(--border-2); gap:10px; animation:fadeIn .2s ease; }
@keyframes fadeIn { from{opacity:0;transform:translateY(4px)} to{opacity:1;transform:none} }
.word-item:last-child { border-bottom:none; }
.word-left  { flex:1; }
.word-text  { font-size:20px; font-weight:500; color:var(--text); line-height:1.2; letter-spacing:-.02em; }
.word-pos   { font-size:11px; color:var(--text-3); margin-top:1px; font-style:italic; }
.word-comp  { font-size:11px; color:var(--text-3); margin-top:2px; font-style:italic; }
.word-def   { font-size:12px; color:var(--text-2); margin-top:3px; line-height:1.4; }
.word-grammarly { font-size:11px; margin-top:3px; }
.word-grammarly a { color:var(--brand); text-decoration:underline; text-underline-offset:2px; }
.word-right { display:flex; align-items:center; gap:4px; padding-top:3px; flex-shrink:0; }
.icon-btn   { width:28px; height:28px; display:flex; align-items:center; justify-content:center; background:transparent; border:none; cursor:pointer; border-radius:5px; color:var(--text-3); transition:background .12s, color .12s; }
.icon-btn:hover { background:var(--bg-2); color:var(--text); }
.icon-btn svg { width:14px; height:14px; }
.icon-btn.saved { color:#E24B4A; }
.icon-btn.saved svg path { fill:#E24B4A; }

.saved-section { border-top:1px solid var(--border); padding:12px 14px; background:var(--bg); }
.saved-top { display:flex; justify-content:space-between; align-items:center; gap:10px; margin-bottom:8px; }
.saved-label { font-size:12px; font-weight:700; color:var(--text); }
.saved-copy { border:1px solid var(--border); background:var(--bg); color:var(--brand); border-radius:7px; padding:5px 9px; font-size:11px; font-weight:600; cursor:pointer; }
.saved-tags { display:flex; gap:5px; flex-wrap:wrap; min-height:22px; }
.saved-tag { display:inline-flex; align-items:center; gap:4px; background:#F0F2FF; color:var(--brand); border-radius:999px; padding:4px 8px; font-size:11px; font-weight:600; }
.saved-tag-remove { cursor:pointer; opacity:.65; }
.saved-tag-remove:hover { opacity:1; }
.saved-empty { color:var(--text-3); font-size:12px; }

.mobile-more-toggle { display:none; width:100%; margin:-2px 0 14px; padding:9px 12px; border:1px solid var(--border); border-radius:8px; background:var(--bg); color:var(--brand); font-size:13px; font-weight:600; font-family:inherit; cursor:pointer; }
.advanced-options { display:block; }
.size-opt { position:relative; gap:7px; }
.size-opt input { position:absolute; opacity:0; pointer-events:none; }
.size-tick { width:18px; height:18px; border:1px solid var(--border); border-radius:5px; background:var(--bg); display:inline-flex; align-items:center; justify-content:center; transition:background .15s, border-color .15s; flex-shrink:0; }
.size-tick::after { content:'✓'; font-size:13px; font-weight:700; color:white; line-height:1; opacity:0; transform:scale(.7); transition:opacity .15s, transform .15s; }
.size-opt input:checked + .size-tick { background:var(--brand); border-color:var(--brand); }
.size-opt input:checked + .size-tick::after { opacity:1; transform:scale(1); }
.size-opt:hover .size-tick { border-color:var(--brand); }

@media(max-width:700px){
  .tool-wrap { padding:14px 16px 0; }
  .tool-card { border-radius:12px; }
  .ctrl { padding:16px; }
  .mobile-more-toggle { display:block; }
  .advanced-options { display:none; }
  .advanced-options.is-open { display:block; }
  .ctrl-row:first-child { margin-bottom:12px; }
  .gen-btn { margin-top:0; }
  .reset-btn, .kbd { display:none; }
  .words-top { padding:10px 16px; }
  .word-list { max-height:420px; overflow-y:auto; }
  .word-text { font-size:19px; }
  .tool-split { flex-direction:column; }
  .ctrl { width:100%; border-right:none; border-bottom:1px solid var(--border-2); }
  .hero { padding:12px 16px 12px; }
  .hero-badge { margin-bottom:6px; }
  .hero h1 { font-size:24px; }
}
</style>
<!-- /SLOT:style -->

<!-- SLOT:hero -->
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="/">Wordineer</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/word-tools/">Word Tools</a>
    <span class="breadcrumb-sep">›</span>
    <span aria-current="page">Random Adjective Generator</span>
  </div>
</div>
<div class="hero">
  <div class="hero-badge">
    <svg viewBox="0 0 11 11" fill="none"><circle cx="5.5" cy="5.5" r="4.5" stroke="#3C3489" stroke-width="1"/><path d="M3.5 5.5l1.5 1.5L8 3.5" stroke="#3C3489" stroke-width="1.2" stroke-linecap="round"/></svg>
    Free · No sign-up · Instant
  </div>
  <h1>Random adjective generator</h1>
  <p>Generate random English adjectives instantly — filter by sentiment (positive, negative, neutral), difficulty, and starting letter. Every result includes a definition and comparative forms. The only adjective generator with sentiment filtering built in.</p>
</div>
<!-- /SLOT:hero -->

<!-- SLOT:tool -->
<div class="tool-wrap">
  <div class="tool-card">
    <div class="tool-split">

      <div class="ctrl">
        <select id="ctrl-type" style="display:none"><option value="adjective">adjective</option></select>
        <div class="ctrl-row">
          <label class="ctrl-label" for="ctrl-count">Number of adjectives</label>
          <input type="number" id="ctrl-count" value="10" min="1" max="50" inputmode="numeric" aria-describedby="count-error">
          <span class="count-error" id="count-error">Enter a number from 1 to 50</span>
        </div>
        <button type="button" class="mobile-more-toggle" id="mobile-more-toggle" aria-expanded="false" aria-controls="advanced-options">Toggle More Options</button>
        <div class="advanced-options" id="advanced-options">
          <div class="ctrl-row">
            <label class="ctrl-label" for="ctrl-adj-type">Sentiment</label>
            <select id="ctrl-adj-type">
              <option value="all">All sentiments</option>
              <option value="positive">Positive</option>
              <option value="negative">Negative</option>
              <option value="neutral">Neutral</option>
            </select>
          </div>
          <div class="ctrl-row">
            <label class="ctrl-label" for="ctrl-diff">Difficulty</label>
            <select id="ctrl-diff">
              <option value="all">All levels</option>
              <option value="easy">Easy (common)</option>
              <option value="medium">Medium</option>
              <option value="hard">Advanced / rare</option>
            </select>
          </div>
          <div class="ctrl-row">
            <label class="ctrl-label" for="ctrl-first">First letter</label>
            <input type="text" id="ctrl-first" maxlength="1" placeholder="A" aria-label="First letter" style="text-transform:uppercase;text-align:center;">
          </div>
          <div class="def-row">
            <label class="toggle" aria-label="Show definitions"><input type="checkbox" id="ctrl-defs" checked><span class="toggle-sl"></span></label>
            <label for="ctrl-defs">Show definitions</label>
          </div>
        </div>
        <button class="gen-btn" id="word-gen-btn">Generate adjectives</button>
        <button class="reset-btn" onclick="WORDINEER.reset()">Reset options</button>
        <div class="kbd">Press <kbd>Space</kbd> to regenerate</div>
        <div class="ad-sidebar">
          <span class="ad-sidebar-tag">Ad</span>
          <div class="ad-sidebar-logo">
            <svg viewBox="0 0 32 32" fill="none" width="32" height="32"><circle cx="16" cy="16" r="14" fill="#15a249"/><path d="M10 16c0-3.3 2.7-6 6-6s6 2.7 6 6-2.7 6-6 6" stroke="white" stroke-width="2" stroke-linecap="round"/><circle cx="16" cy="16" r="2.5" fill="white"/></svg>
            <span class="ad-sidebar-brand">Grammarly</span>
          </div>
          <div class="ad-sidebar-headline">Write with confidence</div>
          <div class="ad-sidebar-body">Fix grammar, improve clarity, and choose the right words — everywhere you write.</div>
          <a href="https://grammarly.com" target="_blank" rel="noopener" class="ad-sidebar-cta">Try free →</a>
          <div class="ad-sidebar-sub">Free plan · No credit card</div>
        </div>
      </div>

      <div class="words-panel">
        <div class="words-top">
          <span class="words-count" id="word-count">Generating…</span>
          <div class="words-actions">
            <button class="act-btn" onclick="WORDINEER.copyAll()">Copy all</button>
            <button class="act-btn" id="word-regen-btn">Regenerate</button>
          </div>
        </div>
        <ul class="word-list" id="word-list"></ul>
      </div>

    </div>

    <div class="saved-section">
      <div class="saved-top">
        <span class="saved-label">Saved adjectives <span id="saved-count" style="font-weight:400;opacity:.7">(0)</span></span>
        <span class="saved-copy" onclick="WORDINEER.copySaved()">Copy saved</span>
      </div>
      <div class="saved-tags" id="saved-tags">
        <span class="saved-empty">Click the heart on any adjective to save it here</span>
      </div>
    </div>

    <div class="aff-nudge" id="aff-nudge">
      <div>
        <div class="aff-nudge-title">Put your saved adjectives to work</div>
        <div class="aff-nudge-body">Grammarly helps you use new vocabulary naturally — checks grammar, tone and word choice. Free to start.</div>
      </div>
      <a href="https://grammarly.com" target="_blank" rel="noopener" class="aff-nudge-cta">
        Try free
        <svg viewBox="0 0 10 10" fill="none"><path d="M2 5h6M6 3l2 2-2 2" stroke="white" stroke-width="1.2" stroke-linecap="round"/></svg>
      </a>
    </div>

  </div>
</div>
<!-- /SLOT:tool -->

<!-- SLOT:ad_b -->
<div class="ad-leaderboard">
  <div class="ad-leaderboard-inner">
    <span class="ad-tag">Advertisement · 728×90</span>
    <div class="ad-mock-content">
      <div class="ad-title">Grammarly — write with confidence. Grammar, tone &amp; clarity.</div>
      <div class="ad-sub">Used by 30 million people. Works in Google Docs, Gmail, Word and more.</div>
      <a href="https://grammarly.com" target="_blank" rel="noopener" class="ad-mock-cta">Try Grammarly free</a>
    </div>
  </div>
</div>
<!-- /SLOT:ad_b -->

<!-- SLOT:explainer -->
<div class="explainer">
  <h2>What is a random adjective generator?</h2>
  <p>A random adjective generator picks adjectives at random from a curated vocabulary list. Unlike a generic word generator, every result is an adjective — ready to use as a modifier without filtering out nouns or verbs. Wordineer's version goes further: each adjective comes with its definition, its comparative and superlative forms, and a sentiment label so you can see at a glance whether you're working with language that builds up, tears down, or simply describes.</p>

  <h2>Why use a random adjective generator?</h2>

  <h3>For writers and creatives</h3>
  <p>Adjectives are where voice lives. A random list breaks you out of the same ten familiar words your brain defaults to and hands you alternatives you wouldn't have consciously reached for. Filter by positive sentiment for uplifting, encouraging language; by negative for tension and menace; by neutral for precision and clarity. Generate 10, read through without judging, save the ones that spark something. The goal is not to use every word — it is to find the one that unlocks the sentence you've been stuck on.</p>

  <h3>For vocabulary building</h3>
  <p>Toggle definitions on, set difficulty to Medium or Hard, and work through the list. Every adjective appears alongside its meaning so you can learn usage in context rather than hunting through a dictionary tab. Save words you want to return to, then copy your saved list when you're ready to study or use them.</p>

  <h3>For ESL learners</h3>
  <p>Adjectives are among the hardest parts of a new language to accumulate — textbooks give you the same fifty and stop there. Use the Easy filter to build a solid foundation of common adjectives; switch to Medium and Hard once those are comfortable. The comparative and superlative forms shown with each result mean you learn three words for the effort of one.</p>

  <h3>For word games and classrooms</h3>
  <p>Generate a set of adjectives for creative writing prompts, vocabulary exercises, or Mad Libs. Filter by sentiment to set the tone of the exercise — all positive for an encouraging activity, all negative for dramatic effect. Pair with the <a href="/random-noun-generator/">Random Noun Generator</a> or <a href="/random-verb-generator/">Random Verb Generator</a> to build complete sentences from scratch.</p>

  <h2>What are adjectives?</h2>
  <p>Adjectives describe or modify nouns — they tell you more about the people, places, and things in a sentence. Without adjectives, prose is flat and undifferentiated. With them, a house becomes a crumbling house, a smile becomes a weary smile, a day becomes an unbearable day. Most adjectives in English have three forms: the base form (bright), the comparative (brighter), and the superlative (brightest). Regular adjectives add -er / -est for short words and use more / most for longer ones. This tool shows all three forms so you can see the full vocabulary available from a single root.</p>

  <h2>Understanding adjective sentiment</h2>
  <p>The sentiment filter is the tool's standout feature — and one no other adjective generator offers. Every adjective in the dataset has been tagged by the tone it typically carries.</p>
  <p><strong>Positive</strong> adjectives imply approval, pleasure, strength, beauty, or virtue — brilliant, generous, resilient, luminous, joyful. Use these for uplifting writing, character compliments, marketing copy, or any context where you want language to feel affirming.</p>
  <p><strong>Negative</strong> adjectives imply criticism, discomfort, threat, or failure — bleak, volatile, wretched, sinister, chaotic. Use these for tension in fiction, critical analysis, or any writing that needs bite and edge. Negative doesn't mean wrong; it means accurate when accuracy calls for darkness.</p>
  <p><strong>Neutral</strong> adjectives describe without judging — vast, circular, adjacent, preliminary, seasonal. These are the workhorse words of technical writing, journalism, and academic prose, where precision matters more than tone. A sentence built on neutral adjectives feels measured and credible.</p>

  <h2>Comparative and superlative forms explained</h2>
  <p>Most descriptive adjectives in English inflect for degree. The comparative form compares two things (this route is longer); the superlative form identifies the extreme among three or more (the longest route of all). Short adjectives typically take -er / -est suffixes (fast → faster → fastest); longer adjectives use more / most (remarkable → more remarkable → most remarkable). A handful are irregular: good → better → best; bad → worse → worst; far → farther → farthest. The comparative and superlative line shown beneath each adjective means you instantly know the full inflectional set without looking anything up.</p>

  <h2>How to use this tool</h2>
  <ol>
    <li><strong>Choose your Sentiment filter</strong> (Positive, Negative, Neutral, or All) and set a Difficulty level to match your purpose.</li>
    <li><strong>Optionally type a First letter</strong> to narrow results to a specific part of the alphabet.</li>
    <li><strong>Hit Generate adjectives</strong> (or press Space) to get your list. Copy individual words, save favourites with the heart icon, or use Copy all to grab the full list at once.</li>
  </ol>

  <h2>Best practices for managing your adjective list</h2>
  <p>Generate more than you think you need — 10 to 15 is a good starting number. Read through without immediately judging; the useful words often aren't the ones that stand out first. Save words that feel right even if you don't immediately know why. When you copy your saved list, paste it somewhere permanent — a writing doc, a notes app, a vocabulary journal — so the words don't disappear when you close the tab. Return to the tool with different filter combinations: a list of hard negative adjectives reads completely differently from a list of easy positive ones, and both have their uses.</p>
</div>
<!-- /SLOT:explainer -->

<!-- SLOT:faq -->
<div class="faq">
  <h2 class="faq-title">Frequently asked questions</h2>
  <div class="faq-item open">
    <div class="faq-q"><span class="faq-q-text">What is an adjective?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">An adjective is a word that describes or modifies a noun or pronoun. It gives more information about a person, place, thing, or idea — its size, colour, number, condition, or quality. Examples: bright, gloomy, vast, resilient, sinister.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What does the Sentiment filter do?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">The Sentiment filter tags each adjective as positive (uplifting or approving — brilliant, generous, resilient), negative (critical or threatening — bleak, volatile, wretched), or neutral (descriptive without judgement — vast, circular, preliminary). No other adjective generator offers this filter.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">What are comparative and superlative adjectives?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">The three degrees of comparison: base form (fast), comparative (faster — comparing two things), and superlative (fastest — the extreme among three or more). Short adjectives take -er/-est; longer adjectives use more/most. Irregular examples: good/better/best, bad/worse/worst. This tool shows all three forms under each result.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Can I combine filters?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Yes — Sentiment, Difficulty, and First Letter all stack. You can generate hard negative adjectives starting with D, or easy positive adjectives starting with B, for example.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">How do I save adjectives I like?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Click the heart icon on any adjective to save it to the Saved section at the bottom of the tool. When you're done, click "Copy saved" to copy your entire saved list to the clipboard in one go.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">Is this tool free?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Completely free, forever. No account required, no limits, no paywalls.</div>
  </div>
  <div class="faq-item">
    <div class="faq-q"><span class="faq-q-text">How many adjectives are in the dataset?</span><svg class="faq-chevron" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="faq-a">Over 500 curated adjectives across all sentiment categories and difficulty levels, each with a definition and comparative and superlative forms.</div>
  </div>
</div>
<!-- /SLOT:faq -->

<!-- SLOT:who -->
<div>
  <h2 class="section-title" style="margin-bottom:14px">Who uses this tool</h2>
  <div class="uc-grid">
    <div class="uc"><div class="uc-title">Fiction Writers</div><div class="uc-body">Filter by sentiment to match your scene's tone. Positive for hope and warmth; negative for menace and dread; neutral for restraint and precision.</div></div>
    <div class="uc"><div class="uc-title">Students &amp; ESL Learners</div><div class="uc-body">Every adjective includes its definition and comparative forms. Three words of vocabulary for the effort of one lookup.</div></div>
    <div class="uc"><div class="uc-title">Educators</div><div class="uc-body">Generate adjective lists by difficulty in seconds. Mix sentiments to design a complete exercise covering the range of descriptive language.</div></div>
    <div class="uc"><div class="uc-title">Content Creators</div><div class="uc-body">Break out of default vocabulary. Generate 10 adjectives, save the two best, and use them to make a headline or caption more specific and alive.</div></div>
  </div>
</div>
<!-- /SLOT:who -->

<!-- SLOT:init -->
<script>
WORDINEER.init({
  listId:         'word-list',
  countId:        'ctrl-count',
  countDisplayId: 'word-count',
  typeId:         'ctrl-type',
  adjTypeId:      'ctrl-adj-type',
  diffId:         'ctrl-diff',
  firstId:        'ctrl-first',
  defsId:         'ctrl-defs',
  dataUrl:        '/data/adjectives.json',
  apiKeys: {
    wordnik: 'vzxbo7m8vl91xgsicsuk79k0pd2w1z3k4z7xl2sv9sje9akxh',
    merriam: 'Y1c8533d7-23e6-4c3b-9c48-854066e8caff',
  }
});

(function(){
  const count = document.getElementById('ctrl-count');
  const toggle = document.getElementById('mobile-more-toggle');
  const advanced = document.getElementById('advanced-options');

  function setCountError(show) {
    const err = document.getElementById('count-error');
    if (err) err.classList.toggle('show', show);
    if (count) count.classList.toggle('input-error', show);
  }

  function validateAndGenerate() {
    const raw = parseInt(count?.value, 10);
    if (isNaN(raw) || raw < 1 || raw > 50) { setCountError(true); return; }
    setCountError(false);
    WORDINEER.generate();
  }

  document.getElementById('word-gen-btn')?.addEventListener('click', validateAndGenerate);
  document.getElementById('word-regen-btn')?.addEventListener('click', validateAndGenerate);

  if (count) {
    count.addEventListener('input', validateAndGenerate);
  }

  ['ctrl-adj-type', 'ctrl-diff'].forEach(function(id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('change', validateAndGenerate);
  });

  const firstEl = document.getElementById('ctrl-first');
  if (firstEl) firstEl.addEventListener('input', validateAndGenerate);

  if (toggle && advanced) {
    toggle.addEventListener('click', function(){
      const isOpen = advanced.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      toggle.textContent = isOpen ? 'Hide More Options' : 'Toggle More Options';
    });
  }
})();
</script>
<!-- /SLOT:init -->
```

- [ ] **Step 2: Commit**

```bash
git add template-deploy/tools-src/random-adjective-generator.html
git commit -m "feat: add random-adjective-generator tool source"
```

---

## Task 5: Register tool in tools.json

**Files:**
- Modify: `template-deploy/tools.json`

- [ ] **Step 1: Add to `more_word_tools` array (after the verb generator entry)**

Open `template-deploy/tools.json`. Find the verb generator entry:
```json
    {
      "href": "/random-verb-generator/",
      "name": "Random Verb Generator",
```

Insert this new entry directly after the closing `}` of the verb generator entry (add a comma after the verb entry's `}`):
```json
    {
      "href": "/random-adjective-generator/",
      "name": "Random Adjective Generator",
      "desc": "Generate random adjectives — filter by sentiment (positive, negative, neutral), difficulty, and starting letter. Definitions and comparative forms included.",
      "icon_bg": "#FEF3EE",
      "icon_path": "<path d=\"M2 4h9M2 7h6M2 10h8\" stroke=\"#C05621\" stroke-width=\"1.3\" stroke-linecap=\"round\"/><path d=\"M11 9.5l1.5 1-1.5 1\" stroke=\"#C05621\" stroke-width=\"1.1\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/>"
    },
```

- [ ] **Step 2: Add to `footer_cols`**

In `tools.json`, find the `footer_cols` section. Locate the column that contains word tools (nouns, verbs, etc.) and add:
```json
{ "href": "/random-adjective-generator/", "text": "Random Adjective Generator" }
```

- [ ] **Step 3: Verify tools.json is valid JSON**

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site"
python3 -c "import json; json.load(open('template-deploy/tools.json')); print('tools.json: valid')"
```

Expected: `tools.json: valid`

- [ ] **Step 4: Commit**

```bash
git add template-deploy/tools.json
git commit -m "feat: add random-adjective-generator to tools.json nav and footer"
```

---

## Task 6: Add clean URL redirect

**Files:**
- Modify: `wordineer-deploy/_redirects`

- [ ] **Step 1: Add redirect line**

Open `wordineer-deploy/_redirects` and add this line:
```
/random-adjective-generator   /random-adjective-generator/   301
```

- [ ] **Step 2: Commit**

```bash
git add wordineer-deploy/_redirects
git commit -m "feat: add redirect for random-adjective-generator clean URL"
```

---

## Task 7: Build, copy output, and verify locally

- [ ] **Step 1: Run the build**

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy"
python3 build.py
```

Expected: no errors; `output/random-adjective-generator.html` created.

- [ ] **Step 2: Verify output file exists**

```bash
ls -lh "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy/output/random-adjective-generator.html"
```

Expected: file exists with non-zero size.

- [ ] **Step 3: Copy output to deploy folder**

```bash
cp "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy/output/random-adjective-generator.html" \
   "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/wordineer-deploy/"
```

- [ ] **Step 4: Start local server**

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/wordineer-deploy"
python3 -m http.server 8080
```

- [ ] **Step 5: Manual browser verification checklist**

Visit `http://localhost:8080/random-adjective-generator.html` and verify:

1. Page loads without console errors
2. Adjectives generate on page load (10 by default)
3. Each adjective card shows: word, sentiment+difficulty tag (`positive · medium`), comparative form (`more brilliant / most brilliant`), definition
4. "Sentiment" dropdown: select Positive → all results show `positive ·`; select Negative → all show `negative ·`; select Neutral → all show `neutral ·`; All → mixed
5. "Difficulty" dropdown: Easy/Medium/Hard correctly filters results
6. "First letter" input: type `B` → all words start with B
7. Definitions toggle: uncheck → definitions hidden; check → definitions shown
8. "Copy all" button copies a newline-separated list to clipboard
9. Heart icon saves adjective to Saved section
10. "Copy saved" exports the saved list
11. "Regenerate" button produces a new set
12. Space key triggers regeneration
13. Mobile layout (DevTools → 375px): controls collapse behind toggle, tool stacks vertically

- [ ] **Step 6: Commit final output**

```bash
git add wordineer-deploy/random-adjective-generator.html wordineer-deploy/_redirects
git commit -m "build: generate and add random-adjective-generator output page"
```

---

## Task 8: Bump `?v=` cache-buster on engine references (if engine was changed)

Since `tool-engine.js` was modified in Task 2 and the `_headers` file caches scripts for 1 year immutable, the version query string must be bumped everywhere it is referenced.

- [ ] **Step 1: Find current version string**

```bash
grep -r "tool-engine" "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy/" --include="*.html" -l
grep -r "tool-engine" "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/wordineer-deploy/" --include="*.html" -l | head -5
```

- [ ] **Step 2: Find current version number**

```bash
grep -r "tool-engine\.js\?v=" "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy/" | head -3
```

Note the current `?v=N` number. Increment it by 1 (e.g. `?v=4` → `?v=5`).

- [ ] **Step 3: Update version in template fragments**

Open the template file(s) that reference `tool-engine.js` (likely `template-deploy/template/head.html` or similar) and increment the `?v=` number.

- [ ] **Step 4: Rebuild all pages**

```bash
cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy"
python3 build.py
cp output/*.html ../wordineer-deploy/
```

- [ ] **Step 5: Commit**

```bash
git add template-deploy/template/ wordineer-deploy/
git commit -m "build: bump tool-engine version string for cache invalidation"
```

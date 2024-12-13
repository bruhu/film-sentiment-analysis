# content_tagging.py

import pandas as pd

def assign_content_tags(df):
    """
    Adds a 'content_tags' column to the DataFrame based on matching values in the 'events' column.
    
    """
    # Define the mapping of categories to their events
    categories = {
        'Sexual Violence / Abuse': [
            'stalking', 'abused forgives abuser', 'abused becomes abuser', 'gaslighting abuse with belt',
            'women brutalized for spectacle', 'domestic violence', 'rape mentions', 'sexual assault',
            'sexual assault on men is a joke', 'onscreen rape', 'women slapped', 'sexualized minor',
            'kidnapping', 'cheating', 'incarceration', 'BDSM', 'being watched', 'large age gap',
            'lose virginity', 'sexual objectification', 'incest', 'sexual content', 'bestiality'
        ],
        'Horror / Supernatural': [
            'non-human death', 'ghosts', 'jump scares', 'demonic possession', 'shaky cam',
            'sudden loud noises', 'screaming', 'demons or Hell', 'blood or gore', 'being watched',
            'self-sacrifice'
        ],
        'Physical Violence': [
            'abuse with belt', 'women brutalized for spectacle', 'domestic violence', 'held under water',
            'beaten up by bully', 'restraints', 'sexual assault', 'mouth covering', 'onscreen rape',
            'women slapped', 'hand damage', 'dislocations', 'throat mutilation', 'choking', 'decapitation',
            'cannibalism', 'crushed to death', 'chokings', 'people being burned alive', 'buried alive',
            'amputation', 'heads getting squashed', 'bones breaking', 'torture', 'falling down stairs',
            'falling deaths', 'eye mutilation', 'stabbings', 'excessive gore', 'hangings', 'kidnapping',
            'audio gore', 'needles or syringes are used', 'self harming', 'people getting hit by cars',
            'drownings', 'blood or gore'
        ],
        'Animal Abuse': [
            'dogs dying', 'animals harmed during making', 'animals (besides dog/cat/horse) dying',
            'animal abuse', 'dog fighting', 'dead animals', 'sad animals', 'harmed rabbits',
            'cats dying', 'pets die', 'dragons dying', 'horses dying', 'abandoned animals',
            'non-human death', 'bestiality'
        ],
        'Medical / Health': [
            'restraints amputation', 'Achilles tendon injury', 'asphyxiation', 'genital trauma/mutilation',
            'unconscious', 'bones breaking', 'seizures', 'overdose', 'vomiting', 'needles or syringes are used',
            'electro-therapy', 'hospital scenes', 'menstruation', 'cancer', 'mental institutions',
            'self harming', 'violent mentally ill person', 'dissociation / depersonalization / derealization',
            'D.I.D. misrepresentation', 'autism abuse', 'suicide attempts', 'mental illness', 'anxiety attacks',
            'ABA therapy', 'suicide threats', 'body dysphoria', 'body dysmorphia', 'eating disorders',
            'people dying by suicide', 'PTSD', 'meltdowns', 'stillbirths', 'miscarriages', 'babies/unborn',
            'childbirth', 'abortions', 'pregnant people deaths', 'strokes', 'chronic illnesses',
            "dementia/Alzheimer's", 'terminal illness'
        ],
        'Child Abuse': [
            'child abuse', 'abusive parents', 'pedophilia', 'infant abduction', 'sexualized minor',
            'kids dying', 'parents dying', 'dear toy destruction', 'crying babies', 'large age gap'
        ],
        'Death / Trauma / Grief': [
            'abusive parents', 'kids dying', 'self-sacrifice', 'non-human death', 'someone dies',
            'major character dies', 'parents dying', 'family dies', 'cancer', 'suicide attempts',
            'people dying by suicide', 'strokes', 'chronic illnesses', 'terminal illness', 'ghosts', '9/11'
        ],
        'LGBTQ+ Phobia': [
            'sexual assault', 'sexual assault on men is a joke', 'trans person depicted predatorily',
            'deadnaming / birthnaming', 'LGBT+ person outed', 'transphobic slurs', 'bisexual cheating',
            'homophobic slurs', 'man in a dress jokes', 'misgendering', 'LGBT people dying', 'male crying ridicule'
        ],
        'Systemic Issues / Social Injustice': [
            'beaten up by bully', 'disabled played by able-bodied', 'R-slur', 'copaganda', 'incarceration',
            'trans person depicted predatorily', 'homelessness', 'anti-abortion', 'religion discussed',
            'antisemitism', 'n-word usage', 'black guy dies first', 'hate speech', 'minority misrepresentation',
            'blackface'
        ],
        'Fear / Anxiety': [
            'snakes', 'spiders', 'bugs', 'stalking', 'held under water', 'shaving or cutting', 'bedbugs',
            'family dies', 'bodies of water', 'clowns', 'trypophobia', 'razors', 'mannequins', 'vomiting',
            'needles or syringes are used', 'being watched', 'aphobia', 'alligators/crocodiles', 'sharks',
            'people being burned alive', 'buried alive', 'claustrophobic scenes'
        ],
        'Racism': [
            'copaganda', 'n-word usage', 'black guy dies first', 'hate speech', 'minority misrepresentation', 'blackface'
        ],
        'Sensory Sensitivity': [
            'bones breaking', 'jump scares', 'audio gore', 'underwater scenes', 'sudden loud noises',
            'shaky cam', 'crying babies', 'screaming', 'flashing lights or images', 'car honk / tire screech',
            'obscene language/gestures', 'being watched', 'stalking', 'claustrophobic scenes'
        ],
        'Gore / Body Horror': [
            'hand damage', 'dislocations', 'throat mutilation', 'choking', 'decapitation', 'cannibalism',
            'crushed to death', 'people being burned alive', 'buried alive', 'body horror', 'amputation',
            'heads getting squashed', 'shaving or cutting', 'genital trauma/mutilation', 'bones breaking',
            'torture', 'falling down stairs', 'falling deaths', 'eye mutilation', 'stabbings', 'excessive gore',
            'hangings', 'someone is eaten', 'audio gore', 'needles or syringes are used', 'self harming',
            'blood or gore', 'drownings', 'people getting hit by cars', 'gun violence'
        ],
        'Sexism': [
            'women brutalized for spectacle', 'domestic violence', 'sexual assault', 'onscreen rape',
            'women slapped', 'anti-abortion', 'stalked', 'being watched', 'large age gap'
        ],
        'Mental Health / Ableism': [
            'seizures', 'disabled played by able-bodied', 'R-slur', 'electro-therapy', 'mental institutions',
            'self harming', 'autism misrepresented', 'violent mentally ill person', 'dissociation / depersonalization / derealization',
            'D.I.D. misrepresentation', 'autism abuse', 'suicide attempts', 'reality unhinged', 'mental illness',
            'misophonia', 'anxiety attacks', 'ABA therapy', 'suicide threats', 'body dysphoria', 'body dysmorphia',
            'claustrophobic scenes', 'eating disorders', 'people dying by suicide', 'PTSD', 'meltdowns', 'ableism',
            "dementia/Alzheimer's"
        ],
        'Addiction / Substance Abuse': [
            'alcohol abuse', 'addiction', 'drug use', 'druggings', 'overdose', 'needles or syringes are used'
        ],
        'Catastrophes / Accidents': [
            'car crashes', 'planes crashing', 'people getting hit by cars', 'drownings', 'nuclear explosions',
            'gun violence', '9/11', 'copaganda', 'incarceration', 'falling down stairs', 'falling deaths'
        ],
        'Body Shaming / Fatphobia': [
            'fat jokes', 'eating disorders', 'fat suits', 'vomiting', 'mental institutions', 'self harming',
            'body dysphoria', 'body dysmorphia'
        ],
        'Plot Warnings / Spoilers': [
            'major character dies', 'leave without goodbye', 'jump scares', 'fourth wall', 'Santa (et al) spoilers',
            'end credit scenes', 'sad endings'
        ]
    }


    # # usage
    # df['content_tags'] = df['events'].apply(
    #     lambda events: [
    #         category for category, tags in categories.items() if any(event.strip() in tags for event in events.split(","))
    #     ]
    # )
    # return df

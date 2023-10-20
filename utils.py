import os
import re
import json
import time
import torch
import openai
import random
import numpy as np
import pandas as pd

from tqdm import tqdm, trange
from collections import Counter, defaultdict

from transformers import AutoTokenizer, AutoModelForCausalLM

pad_ids = {
    'gpt2': 50256,
    'EleutherAI/gpt-neo-1.3B': 50256,
    'EleutherAI/gpt-neo-2.7B': 50256,
    'EleutherAI/gpt-j-6b': 50256,
    'togethercomputer/GPT-JT-6B-v1': 50256,
    'chavinlo/alpaca-native': 0,
    'chavinlo/alpaca-13b': 0
}

max_lengths = {
    'gpt2': 1023,
    'EleutherAI/gpt-neo-1.3B': 2047,
    'EleutherAI/gpt-neo-2.7B': 2047,
    'EleutherAI/gpt-j-6b': 2047,
    'togethercomputer/GPT-JT-6B-v1': 2047,
    'chavinlo/alpaca-native': 2047,
    'chavinlo/alpaca-13b': 2047
}

def prepare_data(df, name, prompt_type, number_of_shots, prompt_set):
    prompts = {'g': 'ANSWER:'}
    
    if name == 'cola':
        prompts['g_prime'] = 'CONTEXT: {context}\nQUESTION: Is this (0) unacceptable, or (1) acceptable?\nANSWER:'
        index_to_label = {0: 'unacceptable', 1: 'acceptable'}
    
    elif name in ['multinli', 'snli']:
        prompts['g_prime'] = 'SENTENCE1: {sentence1}\nSENTENCE2: {sentence2}\nQUESTION: Is this (0) contradiction, (1) entailment, or (2) neutral?\nANSWER:'
        label_to_index = {'contradiction': 0, 'entailment': 1, 'neutral': 2, '-': 3}

    elif name == 'boolq':
        prompts['g_prime'] = 'SENTENCE1: {sentence1}\nSENTENCE2: {sentence2}\nQUESTION: Is this (0) True, or (1) False?\nANSWER:'
        label_to_index = {True: 0, False: 1}
    
    elif name == 'rte':
        prompts['g_prime'] = 'SENTENCE1: {sentence1}\nSENTENCE2: {sentence2}\nQUESTION: Is this (0) entailment, or (1) not_entailment?\nANSWER:'
        label_to_index = {'entailment': 0, 'not_entailment': 1}
    
    elif name == 'advice':
        prompts['g_prime'] = 'CONTEXT: {context}\nQUESTION: Is this (0) no advice, (1) weak advice, or (2) strong advice?\nANSWER:'
    
    elif name == 'pubmed':
        prompts['g_prime'] = 'CONTEXT: {context}\nQUESTION: Is this (0) no claim, (1) correlational, (2) conditional causal, or (3) direct causal?\nANSWER:'
    
    prefix = ''
    if number_of_shots != 0:
        with open(f'prompts/{prompt_set}/{name}/{prompt_type}-{number_of_shots}.txt') as file:
            prefix = file.read()        
    
    inputs_targets = []
    for i in range(len(df)):
        if name in ['cola', 'advice', 'pubmed']:
            target = str(df.label.tolist()[i])
        if name in ['multinli', 'snli']:
            target = str(label_to_index[df.gold_label.tolist()[i]])
        if name in ['boolq', 'rte']:
            target = str(label_to_index[df.label.tolist()[i]])
        if prompt_type in ['g']:
            input = prompts[prompt_type]
        if prompt_type in ['g_prime']:
            if name in ['cola', 'advice', 'pubmed']:
                input = prompts[prompt_type].format(context=df.sentence.tolist()[i])
            if name in ['multinli', 'snli']:
                input = prompts[prompt_type].format(sentence1=df.sentence1.tolist()[i], sentence2=df.sentence2.tolist()[i])
            if name in ['boolq']:
                input = prompts[prompt_type].format(sentence1=df.question.tolist()[i], sentence2=df.passage.tolist()[i])
            if name in ['rte']:
                input = prompts[prompt_type].format(sentence1=df.premise.tolist()[i], sentence2=df.hypothesis.tolist()[i])
        inputs_targets.append((prefix + input, target))
    return inputs_targets

def predict(input, model, tokenizer, max_length, max_new_tokens, pad_token_id, eos_token_id, top_k=20, temperature=0.9, do_sample=True, device='cuda'):
    input = tokenizer(input, max_length=max_length, truncation=True, return_tensors='pt').to(device)
    with torch.no_grad():
        output = model.generate(
            **input,
            max_new_tokens=max_new_tokens,
            top_k=top_k,
            pad_token_id=pad_token_id,
            eos_token_id=eos_token_id,
            do_sample=do_sample,
            temperature=temperature,
            return_dict_in_generate=True,
            output_scores=True
        )
    return  tokenizer.batch_decode(output.sequences)[0], output.scores

def append_correctness(df):
    correctness= []
    for i in range(len(df)):
        answer = df.prediction_g_prime.tolist()[i].replace('</s>', '').lstrip(' ').rstrip(' ').rstrip('\n')
        if answer == df.target.tolist()[i]:
            correctness.append('T')
        else:
            correctness.append('F')
    return pd.concat([df, pd.DataFrame(correctness, columns=['true_or_false'])], axis=1)

def average_pvi(df, label):
    count, total = 0, 0
    for i in range(len(df)):
        if df.true_or_false.tolist()[i] == label:
            count += 1
            total += df.pvi.tolist()[i]
    if count == 0:
        return 0
    return total / count

def accuracy_quantile(df, q, r):
    quantile = np.quantile(df.pvi.tolist(), q)
    correct, total = 0, 0
    for i in range(len(df)):
        if r == '<':
            if df.pvi.tolist()[i] < quantile:
                if df.true_or_false.tolist()[i] == 'T':
                    correct += 1
                total += 1
        if r == '>':
            if df.pvi.tolist()[i] > quantile:
                if df.true_or_false.tolist()[i] == 'T':
                    correct += 1
                total += 1
    return correct / total

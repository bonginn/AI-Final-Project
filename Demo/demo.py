from flask import Flask, request, jsonify
from flask_cors import CORS
import webbrowser
import threading
import os
import torch
import torch.nn as nn
from transformers import BertTokenizer, BertModel
import numpy as np

"""
    CREATING MODEL
"""
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
class BERTClass(torch.nn.Module):
    def __init__(self):
        super(BERTClass, self).__init__()
        self.bert_model = BertModel.from_pretrained('bert-base-uncased', return_dict=True)
        self.dropout = torch.nn.Dropout(0.3)
        self.linear = torch.nn.Linear(768, 41)
    
    def forward(self, input_ids, attn_mask, token_type_ids):
        output = self.bert_model(
            input_ids, 
            attention_mask=attn_mask, 
            token_type_ids=token_type_ids
        )
        output_dropout = self.dropout(output.pooler_output)
        output = self.linear(output_dropout)
        return output
    
model = BERTClass()
model.load_state_dict(torch.load('../Model/trained_model_state.pt', map_location=torch.device('cpu')))
model.to(device)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
MAX_LEN = 512
"""
    REDICTION
"""
categoryList = ['ARTS', 'ARTS & CULTURE', 'BLACK VOICES', 'BUSINESS', 'COLLEGE', 'COMEDY',
 'CRIME' ,'CULTURE & ARTS' ,'DIVORCE' ,'EDUCATION' ,'ENTERTAINMENT',
 'ENVIRONMENT', 'FIFTY', 'FOOD & DRINK' ,'GOOD NEWS' ,'GREEN', 'HEALTHY LIVING',
 'HOME & LIVING', 'IMPACT', 'LATINO VOICES', 'MEDIA' ,'MONEY', 'PARENTING',
 'PARENTS' ,'POLITICS', 'QUEER VOICES', 'RELIGION', 'SCIENCE' ,'SPORTS', 'STYLE',
 'STYLE & BEAUTY', 'TASTE', 'TECH', 'TRAVEL', 'U.S. NEWS', 'WEDDINGS',
 'WEIRD NEWS', 'WELLNESS', 'WOMEN' ,'WORLD NEWS' ,'WORLDPOST']
model.eval()
app = Flask(__name__)
CORS(app)  

@app.route('/process', methods=['POST'])
def process_text():
    data = request.get_json()
    input_text = data.get('text')
    encodings = tokenizer.encode_plus(
        input_text,
        None,
        add_special_tokens=True,
        max_length=MAX_LEN,
        padding='max_length',
        return_token_type_ids=True,
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt'
    )
    with torch.no_grad():
        input_ids = encodings['input_ids'].to(device, dtype=torch.long)
        attention_mask = encodings['attention_mask'].to(device, dtype=torch.long)
        token_type_ids = encodings['token_type_ids'].to(device, dtype=torch.long)
        output = model(input_ids, attention_mask, token_type_ids)
        final_output = torch.sigmoid(output).cpu().detach().numpy().tolist()
    
        threshold = 0.5
        scores = final_output[0]
        sorted_indices = np.argsort(scores)[::-1] 
        pred = [categoryList[i] for i in sorted_indices if scores[i] > threshold][:5]  # 获取前五个大于阈值的类别
        if len(pred) == 0:
            pred = [categoryList[np.argmax(final_output, axis=1)[0]]]

    output_text = f"Prdicted Category : {pred}"

    return jsonify({'output': output_text})

def open_browser():
    file_path = os.path.abspath('index.html')  
    webbrowser.open(f'file://{file_path}')

if __name__ == '__main__':
    threading.Timer(1.25, open_browser).start()
    app.run(debug=True, port=5001)  

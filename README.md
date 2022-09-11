# N-gramm
Let's quickly go over the principle of operation
# Step 1
First of all you need train your model, to generate future text
To train model use command below ( redact directory way for yourself )
Example: $ python train.py train_data_folder model.txt
> $ python train.py D:\tinkoff_project\data\train_data D:\tinkoff_project\data\model.txt
You always need to specify the full path, as necessary
# Step 2 
After creating model we can generate text via command below
Example: $ python generate.py model text num
> $ python generate.py D:\tinkoff_project\data\model.txt Я должен стать сильнее 777
Model - Your trained model of text
text - Your text that you want to extend
num - number of words that will be generated after your text
After executing generate.py you will get a string with your extended text
On that moment documentation is end. Now you can train your own model and generate your unique text

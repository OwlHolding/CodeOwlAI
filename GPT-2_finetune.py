import gpt_2_simple as gpt2

sess = gpt2.start_tf_sess()

gpt2.finetune(sess,
              dataset='full path to GPT2_train.txt',             
              model_dir='full path to run1',
              steps=100,
              restore_from='latest',
              run_name='run1',
              print_every=100,
              sample_every=-1,
              save_every=100,
              overwrite=True,
              
              )
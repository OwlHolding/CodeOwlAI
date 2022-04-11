import gpt_2_simple as gpt2

sess = gpt2.start_tf_sess()
MODEL_NAME = "355M"
MODEL_DIR = ''
gpt2.finetune(sess,
              dataset='full path to GPT2_train.txt',             
              model_dir=MODEL_DIR,
              steps=100,
              restore_from='latest',
              run_name='run1',
              print_every=100,
              sample_every=-1,
              save_every=100,
              overwrite=True,
              model_name=MODEL_NAME
              )
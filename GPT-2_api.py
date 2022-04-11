import gpt_2_simple as gpt2

MODEL_DIR = ''
MODEL_NAME = "355M"
def neuron_net(traceback):
    try:
        sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(sess, model_dir=MODEL_DIR, model_name=MODEL_NAME)
        answer = gpt2.generate(sess, length=600, prefix='Error: ' + traceback + ' Answer:', nsamples=1,
                  return_as_list=True, include_prefix=True,
                 model_dir=MODEL_DIR, model_name=MODEL_NAME)[0]
        gpt2.reset_session(sess)
        while "Answer:" in answer:
            answer = answer[answer.find("Answer:") + 7:]
        return answer
    except:
        return ""
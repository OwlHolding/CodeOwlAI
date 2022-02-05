import gpt_2_simple as gpt2



def neuron_net(traceback):
    try:
        sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(sess,
                   run_name="full path to checkpoint\\run1",
                   checkpoint_dir="full path to checkpoint")
        answer = gpt2.generate(sess, length=600, prefix='Error: ' + traceback + ' Answer:', nsamples=1,
                  return_as_list=True, include_prefix=True,
                  run_name="full path to checkpoint\\run1",
                  checkpoint_dir="full path  to aurora\\checkpoint")[0]
        gpt2.reset_session(sess)
        while "Answer:" in answer:
            answer = answer[answer.find("Answer:") + 7:]
        return answer
    except:
        return ""